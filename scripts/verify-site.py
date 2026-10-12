#!/usr/bin/env python3
"""
verify-site.py — AETHON House · functional regression matrix (Playwright, Python).

Self-serves the repository root over HTTP (default --port 8402; an already-running server on
that port is reused), drives headless Chromium through the site's interactive layer and
prints ONE line per check:

    PASS  <check> — <detail>
    FAIL  <check> — <detail>
    SKIP  <check> — <detail>      only for things this sandbox cannot decide (e.g. an external
                                  host the egress proxy blocks, a browser feature that is absent)

Exit status is 1 when any check FAILs. Nothing in the repository is modified.

Usage
    python3 scripts/verify-site.py                    # the whole matrix
    python3 scripts/verify-site.py --only menu        # checks whose name contains "menu"
    python3 scripts/verify-site.py --no-external      # skip the external-link HEAD requests
    python3 scripts/verify-site.py --artifacts DIR    # where screenshots + the JSON summary go
    python3 scripts/verify-site.py --port 8402

Site gotchas the script handles for you (see CLAUDE.md): the WIP <dialog> opens once per
session (pre-set via sessionStorage 'aethon-wip'), the theme lives in localStorage
'aethon-theme' and a first visit after Paphos sunset auto-opens in Afterglow (R4) — so every
check pins its theme explicitly, except the R4 checks, which fake Date instead. The page
scrolls smoothly (use behavior:'instant'), lazy images only load near the viewport, theme
transitions take ~700ms, the dusk sweep 1600ms, the menu fade 450ms.

Chromium is launched from /opt/pw-browsers/chromium (never `playwright install`).
"""

import argparse
import calendar
import functools
import http.server
import json
import os
import re
import socket
import ssl
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
CHROMIUM = '/opt/pw-browsers/chromium'
PAGES = {'/': 'index.html', '/gallery/': 'gallery/index.html', '/legal/': 'legal/index.html', '/404.html': '404.html'}
DAY_META, NIGHT_META = '#E9E7E0', '#1A1410'
SUN, MOON = '☀', '☾'


# ----------------------------------------------------------------------------------------------
# reporting
# ----------------------------------------------------------------------------------------------
class Report:
    def __init__(self):
        self.rows = []

    def _emit(self, status, name, detail):
        self.rows.append({'status': status, 'name': name, 'detail': detail})
        print(f'{status:4} {name} — {detail}' if detail else f'{status:4} {name}', flush=True)

    def check(self, name, cond, detail=''):
        self._emit('PASS' if cond else 'FAIL', name, detail)
        return bool(cond)

    def skip(self, name, detail=''):
        self._emit('SKIP', name, detail)

    def fail(self, name, detail=''):
        self._emit('FAIL', name, detail)

    @property
    def failed(self):
        return [r for r in self.rows if r['status'] == 'FAIL']


R = Report()


# ----------------------------------------------------------------------------------------------
# local server — serves the repo root like GitHub Pages (+ answers the /e beacon route with 204,
# which is the Cloudflare worker's job in production, so the console stays honest about the SITE)
# ----------------------------------------------------------------------------------------------
class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.avif': 'image/avif', '.webp': 'image/webp', '.woff2': 'font/woff2',
                      '.webmanifest': 'application/manifest+json', '.svg': 'image/svg+xml',
                      '.ico': 'image/x-icon', '.json': 'application/json'}

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _beacon(self):
        return self.path == '/e' or self.path.startswith('/e?')

    def do_POST(self):
        if self._beacon():
            self.send_response(204); self.end_headers(); return
        self.send_error(405)

    def do_GET(self):
        if self._beacon():
            self.send_response(204); self.end_headers(); return
        path = self.translate_path(self.path)
        if not os.path.exists(path):                       # GitHub Pages serves 404.html for unknown paths
            body = open(os.path.join(ROOT, '404.html'), 'rb').read()
            self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body); return
        super().do_GET()


def serve(port):
    """Start the local server, or reuse one already answering on the port. Returns base URL."""
    base = f'http://127.0.0.1:{port}'
    try:
        srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(Handler, directory=ROOT))
    except OSError:
        try:
            with urllib.request.urlopen(base + '/', timeout=5) as r:
                if r.status == 200:
                    print(f'# reusing the server already on {base}', flush=True)
                    return base, None
        except Exception:
            pass
        raise SystemExit(f'port {port} is busy and not serving the site')
    t = threading.Thread(target=srv.serve_forever, daemon=True); t.start()
    return base, srv


# ----------------------------------------------------------------------------------------------
# browser sessions
# ----------------------------------------------------------------------------------------------
def fake_date_script(iso):
    ms = calendar.timegm(time.strptime(iso, '%Y-%m-%dT%H:%M:%SZ')) * 1000
    # Date() with no arguments / Date.now() return the fixed instant; everything else is untouched
    return ("(function(){const F=%d,D=Date;class FD extends D{constructor(...a){super(...(a.length?a:[F]));}"
            "static now(){return F;}}window.Date=FD;})();") % ms


class Session:
    """One browser context + page with console/page-error and network bookkeeping."""

    def __init__(self, site, *, theme='day', wip=True, hint=True, viewport=None, device=None, has_touch=None,
                 is_mobile=None, reduced_motion=None, js=True, dnt=False, gpc=False, fake_time=None,
                 no_view_transitions=False):
        self.site = site
        kw = {}
        if device:
            d = site.pw.devices[device]
            kw.update({k: d[k] for k in ('user_agent', 'viewport', 'device_scale_factor', 'is_mobile', 'has_touch') if k in d})
        if viewport: kw['viewport'] = {'width': viewport[0], 'height': viewport[1]}
        if has_touch is not None: kw['has_touch'] = has_touch
        if is_mobile is not None: kw['is_mobile'] = is_mobile
        if reduced_motion: kw['reduced_motion'] = reduced_motion
        if not js: kw['java_script_enabled'] = False
        self.ctx = site.browser.new_context(**kw)
        self.page = self.ctx.new_page()
        self.errors, self.failed, self.bad = [], [], []
        self.page.on('console', lambda m: self.errors.append('console: ' + m.text) if m.type == 'error' else None)
        self.page.on('pageerror', lambda e: self.errors.append('pageerror: ' + str(e)))
        self.page.on('requestfailed', lambda rq: self.failed.append(f'{rq.url} ({rq.failure})'))
        self.page.on('response', lambda rs: self.bad.append(f'{rs.status} {rs.url}') if rs.status >= 400 else None)
        # storage presets, applied ONCE per context (later navigations keep what the page stores)
        pre = []
        if theme is not None: pre.append(f"localStorage.setItem('aethon-theme','{theme}')")
        if wip: pre.append("sessionStorage.setItem('aethon-wip','1')")
        if hint: pre.append("localStorage.setItem('aethon-hint','1')")
        self.page.add_init_script("(function(){try{if(sessionStorage.getItem('__vs'))return;sessionStorage.setItem('__vs','1');"
                                  + ';'.join(pre) + "}catch(e){}})();")
        if dnt: self.page.add_init_script("Object.defineProperty(Navigator.prototype,'doNotTrack',{get:function(){return '1'},configurable:true});")
        if gpc: self.page.add_init_script("window.globalPrivacyControl=true;")
        if fake_time: self.page.add_init_script(fake_date_script(fake_time))
        if no_view_transitions: self.page.add_init_script("Object.defineProperty(Document.prototype,'startViewTransition',{value:undefined,configurable:true});")

    def goto(self, path, wait='load'):
        resp = self.page.goto(self.site.base + path, wait_until=wait)
        return resp

    def ev(self, js):
        return self.page.evaluate(js)

    def scroll_to(self, y):
        self.page.evaluate(f"window.scrollTo({{top:{int(y)}, left:0, behavior:'instant'}})")

    def scroll_through(self, step=480, pause=110):
        y, h = 0, self.ev('document.documentElement.scrollHeight')
        while y < h:
            self.scroll_to(y); self.page.wait_for_timeout(pause)
            y += step; h = self.ev('document.documentElement.scrollHeight')
        self.scroll_to(h); self.page.wait_for_timeout(pause)

    def shot(self, name, **kw):
        if self.site.artifacts:
            self.page.screenshot(path=os.path.join(self.site.artifacts, name), **kw)

    def finish(self, label, network=True, ignore=()):
        """Close the context and report its console / page-error (and network) hygiene."""
        errs = [e for e in self.errors if not any(i in e for i in ignore)]
        if network:
            errs += ['requestfailed: ' + f for f in self.failed] + ['http: ' + b for b in self.bad]
        try:
            self.ctx.close()
        except Exception:
            pass
        R.check(f'{label}: zero console errors / page errors' + (' / failed requests' if network else ''),
                not errs, '; '.join(errs[:4]) if errs else 'clean')
        return not errs


class Site:
    def __init__(self, pw, browser, base, artifacts):
        self.pw, self.browser, self.base, self.artifacts = pw, browser, base, artifacts

    def session(self, **kw):
        return Session(self, **kw)


def capture_beacons(page):
    hits = []

    def h(route, req):
        m = re.search(r'[?&]n=([^&]+)', req.url)
        hits.append(m.group(1) if m else req.url)
        route.fulfill(status=204, body='')
    page.route(re.compile(r'/e\?n='), h)
    return hits


def mock_brevo(page, mode):
    posts = []

    def h(route, req):
        posts.append({'method': req.method, 'url': req.url, 'body': req.post_data or ''})
        if mode == 'ok':
            route.fulfill(status=200, content_type='text/html', body='<!doctype html><title>ok</title>')
        else:
            route.abort('failed')
    page.route(re.compile(r'sibforms\.com'), h)   # subdomain host: a glob with "**/sibforms.com/**" never matches
    return posts


# ----------------------------------------------------------------------------------------------
# checks
# ----------------------------------------------------------------------------------------------
THEME_STATE = """() => ({
  night: document.body.classList.contains('night'),
  ls: (function(){ try { return localStorage.getItem('aethon-theme'); } catch(e){ return 'ERR'; } })(),
  meta: document.querySelector('meta[name=theme-color]').getAttribute('content'),
  pressed: document.getElementById('theme-toggle').getAttribute('aria-pressed'),
  icon: document.querySelector('#theme-toggle .toggle-icon').textContent,
  chip: (function(){ var c = document.querySelector('.hero-media'); return c ? c.getAttribute('aria-pressed') : null; })(),
  vt: document.documentElement.classList.contains('vt-live'),
  sweep: document.documentElement.getAttribute('data-sweep')
})"""


def check_theme_toggle(site):
    s = site.session(theme='day', reduced_motion='reduce')
    s.goto('/')
    st = s.ev(THEME_STATE)
    R.check('theme: saved day opens in Daylight', not st['night'] and st['meta'] == DAY_META and st['pressed'] == 'false' and st['icon'] == MOON, json.dumps(st))
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(150)
    st = s.ev(THEME_STATE)
    R.check('theme: toggle day→night (body.night, localStorage, theme-color, aria-pressed, icon)',
            st['night'] and st['ls'] == 'night' and st['meta'] == NIGHT_META and st['pressed'] == 'true' and st['icon'] == SUN and st['chip'] == 'true', json.dumps(st))
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(150)
    st = s.ev(THEME_STATE)
    R.check('theme: toggle night→day restores everything',
            not st['night'] and st['ls'] == 'day' and st['meta'] == DAY_META and st['pressed'] == 'false' and st['icon'] == MOON and st['chip'] == 'false', json.dumps(st))
    s.page.click('.hero-media'); s.page.wait_for_timeout(150)
    st = s.ev(THEME_STATE)
    R.check('theme: hero chip is a second toggle (both buttons sync)', st['night'] and st['pressed'] == 'true' and st['chip'] == 'true' and st['ls'] == 'night', json.dumps(st))
    # the choice carries across pages (same localStorage key)
    s.goto('/gallery/'); g = s.ev(THEME_STATE)
    s.goto('/legal/'); l = s.ev(THEME_STATE)
    R.check('theme: choice persists to /gallery/ and /legal/', g['night'] and g['meta'] == NIGHT_META and l['night'] and l['meta'] == NIGHT_META, f'gallery={g["night"]} legal={l["night"]}')
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(150)
    s.goto('/'); i = s.ev(THEME_STATE)
    R.check('theme: a switch on /legal/ carries back to /', not i['night'] and i['ls'] == 'day', json.dumps(i))
    s.finish('theme')

    # the evening-line text buttons set Afterglow by day and are a no-op at night
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/')
    s.ev("document.querySelector('#interior .evening-line').scrollIntoView({block:'center'})")
    s.page.click('#interior .evening-line'); s.page.wait_for_timeout(150)
    a = s.ev(THEME_STATE)
    s.page.click('#gallery .evening-line', force=True); s.page.wait_for_timeout(150)
    b = s.ev(THEME_STATE)
    R.check('theme: .evening-line sets Afterglow by day; no-op at night (stays night)', a['night'] and b['night'] and b['ls'] == 'night', f'after interior={a["night"]} after views={b["night"]}')
    s.finish('theme evening-line')

    # one-time hint on the first switch to evening (gate = localStorage 'aethon-hint'; survives a reload)
    HINT = "(function(){var e=document.querySelector('.toggle-hint');return {show:e.classList.contains('show'),text:e.textContent,ls:localStorage.getItem('aethon-hint')}})()"
    s = site.session(theme='day', hint=False, reduced_motion='reduce'); s.goto('/')
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(200)
    h1 = s.ev(HINT)
    s.page.reload(wait_until='load')                       # arrives in the saved night
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(150)   # → day
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(200)   # → night again: no second hint
    h2 = s.ev(HINT)
    R.check('theme: Afterglow hint shows on the first switch only (role=status text, aethon-hint=1; silent after a reload)',
            h1['show'] and 'Afterglow' in h1['text'] and h1['ls'] == '1' and not h2['show'] and h2['text'] == '', json.dumps(h1) + f' second={json.dumps(h2)}')
    s.finish('theme hint')


R4_CASES = [
    # (label, fixed UTC instant, expected night) — Cyprus is UTC+3 under EU DST (last Sun Mar → last Sun Oct), else UTC+2
    ('summer evening 21:30 local', '2026-07-15T18:30:00Z', True),
    ('summer noon 12:00 local', '2026-07-15T09:00:00Z', False),
    ('winter dusk 17:30 local (sunset table 17.2)', '2026-01-15T15:30:00Z', True),
    ('winter afternoon 16:00 local', '2026-01-15T14:00:00Z', False),
    ('summer pre-dawn 05:00 local (sunrise 5.6)', '2026-06-15T02:00:00Z', True),
    ('DST still on: 24 Oct 16:00Z = 19:00 local', '2026-10-24T16:00:00Z', True),
    ('DST ended: 26 Oct 16:00Z = 18:00 local (< 18.3)', '2026-10-26T16:00:00Z', False),
]


def check_r4_clock(site):
    for label, iso, night in R4_CASES:
        s = site.session(theme=None, fake_time=iso)
        s.goto('/')
        st = s.ev(THEME_STATE)
        ok = st['night'] == night and st['ls'] is None and st['meta'] == (NIGHT_META if night else DAY_META) and st['pressed'] == ('true' if night else 'false')
        R.check(f'r4 clock: {label} → {"Afterglow" if night else "Daylight"}, not persisted, toggle seeded from body', ok, json.dumps(st))
        s.finish(f'r4 clock ({label})')
    # saved preference wins over the clock, both ways
    s = site.session(theme='day', fake_time='2026-07-15T18:30:00Z'); s.goto('/')
    a = s.ev(THEME_STATE)
    R.check('r4 clock: saved Daylight beats an evening arrival', not a['night'] and a['ls'] == 'day', json.dumps(a)); s.finish('r4 saved day')
    s = site.session(theme='night', fake_time='2026-07-15T09:00:00Z'); s.goto('/')
    a = s.ev(THEME_STATE)
    R.check('r4 clock: saved Afterglow beats a noon arrival', a['night'] and a['ls'] == 'night', json.dumps(a)); s.finish('r4 saved night')
    # the init is hand-synced across the three pages
    for path in ('/gallery/', '/legal/'):
        s = site.session(theme=None, fake_time='2026-07-15T18:30:00Z'); s.goto(path)
        a = s.ev(THEME_STATE)
        R.check(f'r4 clock: {path} evening arrival opens in Afterglow (hand-synced init)', a['night'] and a['ls'] is None and a['meta'] == NIGHT_META, json.dumps(a))
        s.finish(f'r4 {path}')


def _dark_from_left(site, s, tag):
    """Burst helper: how many of 64 viewport columns, counted from the LEFT edge, are night-dark
    (mean luminance < 120). Needs Pillow; returns None without it."""
    try:
        from PIL import Image
    except Exception:
        return None
    path = os.path.join(site.artifacts or tempfile.gettempdir(), f'sweep-{tag}.png')
    s.page.screenshot(path=path)
    im = Image.open(path).convert('L').resize((64, 8))
    cols = [sum(im.getpixel((x, y)) for y in range(8)) / 8 for x in range(64)]
    n = 0
    for c in cols:
        if c < 120: n += 1
        else: break
    return n


def _burst(site, s, tag, frames=5, gap=210):
    prof = []
    for i in range(frames):
        d = _dark_from_left(site, s, f'{tag}-{i}')
        if d is None: return None
        prof.append(d); s.page.wait_for_timeout(gap)
    return prof


def _direction(prof, night):
    """A night sweep grows the dark-from-left count; a day return shrinks it. A single still cannot
    tell a reversed wipe — the burst must progress monotonically AND show an intermediate frame."""
    if prof is None: return None, 'needs Pillow'
    inter = [p for p in prof if 0 < p < 64]
    if not inter: return None, f'no intermediate frame captured {prof}'
    mono = all((b >= a) if night else (b <= a) for a, b in zip(prof, prof[1:]))
    moved = prof[-1] != prof[0]
    return mono and moved, f'dark-from-left per frame: {prof}'


VT_ANIM = """() => document.getAnimations().filter(a => a.effect && a.effect.pseudoElement && a.effect.pseudoElement.indexOf('view-transition-new') >= 0)
  .map(a => ({ name: a.animationName, state: a.playState, progress: +(a.effect.getComputedTiming().progress || 0).toFixed(2) }))"""


def _sweep_round(site, s, to_night, tag):
    """Click the toggle, sample the pseudo-element animation (screenshot-free), burst-capture the
    wipe, then wait for the transition to finish. Returns (anim samples, burst profile)."""
    s.page.click('#theme-toggle')
    st = s.ev(THEME_STATE)
    R.check(f'sweep: toggle starts a view transition (html.vt-live + data-sweep={"night" if to_night else "day"})', st['vt'] and st['sweep'] == ('night' if to_night else 'day'), json.dumps(st))
    s.page.wait_for_timeout(250); a1 = s.ev(VT_ANIM)
    prof = _burst(site, s, tag)
    s.page.wait_for_function("!document.documentElement.classList.contains('vt-live')", timeout=6000); s.page.wait_for_timeout(150)
    return a1, prof


def check_dusk_sweep(site):
    s = site.session(theme='day'); s.goto('/')
    if s.ev("typeof document.startViewTransition") != 'function':
        R.skip('sweep: View Transitions API absent in this Chromium — fallback path only'); s.finish('sweep'); return
    s.ev("document.getElementById('architecture').scrollIntoView({block:'start', behavior:'instant'})"); s.page.wait_for_timeout(400)   # plain ground, no hero imagery
    a1, prof = _sweep_round(site, s, True, 'night')
    R.check('sweep: the night wipe runs on ::view-transition-new(root) with the dusk-sweep keyframes (progress sampled at ~250ms)',
            len(a1) == 1 and a1[0]['name'] == 'dusk-sweep' and a1[0]['state'] == 'running' and 0 < a1[0]['progress'] < 0.6, json.dumps(a1))
    st = s.ev(THEME_STATE)
    R.check('sweep: night sweep ends clean (vt-live/data-sweep removed, body.night, localStorage, theme-color)',
            not st['vt'] and st['sweep'] is None and st['night'] and st['ls'] == 'night' and st['meta'] == NIGHT_META, json.dumps(st))
    ok, why = _direction(prof, True)
    if ok is None and prof is not None:                      # a capture burst can miss the wipe once — retry in a fresh session before judging
        s.finish('sweep (first pass)')
        s = site.session(theme='day'); s.goto('/'); s.ev("document.getElementById('architecture').scrollIntoView({block:'start', behavior:'instant'})"); s.page.wait_for_timeout(400)
        s.page.click('#theme-toggle'); prof = _burst(site, s, 'night-retry')
        s.page.wait_for_function("!document.documentElement.classList.contains('vt-live')", timeout=6000); s.page.wait_for_timeout(150)
        ok, why = _direction(prof, True); why += ' (retry)'
    if ok is None: R.skip('sweep: direction day→night (burst)', why)
    else: R.check('sweep: direction day→night — the dark region grows in from the LEFT across the burst', ok, why)
    a1, prof = _sweep_round(site, s, False, 'day')
    R.check('sweep: the day return runs its OWN reversed keyframes (dusk-sweep-back), not the night set played backwards',
            len(a1) == 1 and a1[0]['name'] == 'dusk-sweep-back' and a1[0]['state'] == 'running', json.dumps(a1))
    st = s.ev(THEME_STATE)
    R.check('sweep: day sweep ends clean (Daylight restored, attributes removed)',
            not st['vt'] and st['sweep'] is None and not st['night'] and st['ls'] == 'day' and st['meta'] == DAY_META, json.dumps(st))
    ok, why = _direction(prof, False)
    if ok is None: R.skip('sweep: direction night→day (burst)', why)
    else: R.check('sweep: direction night→day — the light region returns from the RIGHT across the burst', ok, why)
    s.finish('sweep')

    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/')
    s.page.click('#theme-toggle')
    st = s.ev(THEME_STATE)
    R.check('sweep: reduced-motion falls back to the instant token switch (no vt-live, night applied synchronously)',
            not st['vt'] and st['sweep'] is None and st['night'] and st['meta'] == NIGHT_META, json.dumps(st))
    s.finish('sweep reduced-motion')

    s = site.session(theme='day', no_view_transitions=True); s.goto('/')
    s.page.click('#theme-toggle')
    st = s.ev(THEME_STATE)
    R.check('sweep: without startViewTransition the toggle still applies instantly, no errors', not st['vt'] and st['night'], json.dumps(st))
    s.finish('sweep no-support')

    for path in ('/gallery/', '/legal/'):
        s = site.session(theme='day'); s.goto(path)
        s.page.click('#theme-toggle')
        a = s.ev(THEME_STATE); s.page.wait_for_timeout(2300); b = s.ev(THEME_STATE)
        R.check(f'sweep: {path} runs the sweep and ends in Afterglow (hand-synced)', a['vt'] and a['sweep'] == 'night' and not b['vt'] and b['night'], f'start={a["sweep"]} end night={b["night"]}')
        s.finish(f'sweep {path}')


HOLD_STATE = """(i) => { var el = document.querySelectorAll('.pause-media[data-hold]')[i];
  var d = el.querySelector('.shot-day'), n = el.querySelector('.shot-night');
  return { held: el.classList.contains('held'), day: getComputedStyle(d).opacity, night: getComputedStyle(n).opacity,
           label: el.getAttribute('aria-label'), cursor: getComputedStyle(el).cursor.slice(0, 30) }; }"""


def check_hold(site):
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/')
    n = s.ev("document.querySelectorAll('.pause-media[data-hold]').length")
    R.check('hold: two pause plates carry data-hold', n == 2, f'found {n}')
    for i in range(n):
        el = s.page.locator('.pause-media[data-hold]').nth(i)
        el.scroll_into_view_if_needed(); s.page.wait_for_timeout(150)
        box = el.bounding_box(); cx, cy = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
        base = s.page.evaluate(HOLD_STATE, i)
        s.page.mouse.move(cx, cy); s.page.mouse.down(); s.page.wait_for_timeout(350)
        held = s.page.evaluate(HOLD_STATE, i)
        s.page.mouse.up(); s.page.wait_for_timeout(120)
        rel = s.page.evaluate(HOLD_STATE, i)
        R.check(f'hold: plate {i+1} mouse-hold (≥200ms) shows the evening layer, release restores',
                base['day'] == '1' and base['night'] == '0' and held['held'] and held['night'] == '1' and held['day'] == '0'
                and not rel['held'] and rel['day'] == '1' and rel['night'] == '0', f'base={base["day"]}/{base["night"]} held={held["held"]} {held["day"]}/{held["night"]} released={rel["day"]}/{rel["night"]}')
        # quick tap never engages
        s.page.mouse.move(cx, cy); s.page.mouse.down(); s.page.wait_for_timeout(60); s.page.mouse.up(); s.page.wait_for_timeout(300)
        q = s.page.evaluate(HOLD_STATE, i)
        # movement beyond 10px before the delay cancels (a scroll, not a hold)
        s.page.mouse.move(cx, cy); s.page.mouse.down(); s.page.wait_for_timeout(60); s.page.mouse.move(cx + 40, cy + 40); s.page.wait_for_timeout(350)
        m = s.page.evaluate(HOLD_STATE, i); s.page.mouse.up(); s.page.wait_for_timeout(100)
        R.check(f'hold: plate {i+1} quick tap and >10px drag do not engage', not q['held'] and not m['held'], f'tap={q["held"]} drag={m["held"]}')
        # keyboard: Space and Enter
        el.focus()
        for key in ('Space', 'Enter'):
            s.page.keyboard.down(key); s.page.wait_for_timeout(80)
            k = s.page.evaluate(HOLD_STATE, i)
            s.page.keyboard.up(key); s.page.wait_for_timeout(80)
            k2 = s.page.evaluate(HOLD_STATE, i)
            R.check(f'hold: plate {i+1} keyboard {key} engages while held, releases on keyup', k['held'] and k['night'] == '1' and not k2['held'] and k2['day'] == '1', f'down={k["held"]} up={k2["held"]}')
        R.check(f'hold: plate {i+1} aria-label names the evening by day; fine-pointer cursor is the moon glyph',
                base['label'] == 'Hold to preview the evening view' and base['cursor'].startswith('url("data:image/svg+xml'), f'label={base["label"]!r} cursor={base["cursor"]!r}')
    # at night the hold shows the DAY layer and the label flips
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(200)
    el = s.page.locator('.pause-media[data-hold]').nth(0); el.scroll_into_view_if_needed(); s.page.wait_for_timeout(100)
    box = el.bounding_box(); cx, cy = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
    base = s.page.evaluate(HOLD_STATE, 0)
    s.page.mouse.move(cx, cy); s.page.mouse.down(); s.page.wait_for_timeout(350)
    held = s.page.evaluate(HOLD_STATE, 0); s.page.mouse.up(); s.page.wait_for_timeout(100)
    R.check('hold: at night the hold previews DAYLIGHT (day layer on top) and the label says so',
            base['night'] == '1' and base['day'] == '0' and held['held'] and held['day'] == '1' and held['night'] == '0' and base['label'] == 'Hold to preview the daylight view',
            f'base={base["day"]}/{base["night"]} held={held["day"]}/{held["night"]} label={base["label"]!r}')
    s.finish('hold')


MENU_STATE = """() => { var b = document.getElementById('menu-btn'), m = document.getElementById('menu');
  var ae = document.activeElement;
  return { open: document.body.classList.contains('menu-open'), expanded: b.getAttribute('aria-expanded'), text: b.textContent.trim(),
    hidden: m.getAttribute('aria-hidden'), vis: getComputedStyle(m).visibility, btnDisplay: getComputedStyle(b).display,
    linksDisplay: getComputedStyle(document.querySelector('nav.links')).display,
    mainInert: document.getElementById('top').inert, footInert: document.querySelector('footer').inert, markInert: document.querySelector('.bar .mark').inert,
    bodyPos: document.body.style.position, bodyTop: document.body.style.top, scrollY: window.scrollY,
    focus: ae ? (ae.id || ae.className || ae.tagName) + ':' + (ae.getAttribute && ae.getAttribute('href') || '') + ':' + (m.contains(ae)) : null,
    overflowY: getComputedStyle(m).overflowY, alignItems: getComputedStyle(m).alignItems }; }"""


def check_menu_phone(site):
    s = site.session(theme='day', viewport=(390, 844), reduced_motion='reduce'); s.goto('/')
    st = s.ev(MENU_STATE)
    R.check('menu: ≤700px shows the Menu button and hides the inline nav', st['btnDisplay'] != 'none' and st['linksDisplay'] == 'none' and st['vis'] == 'hidden', json.dumps({k: st[k] for k in ('btnDisplay', 'linksDisplay', 'vis')}))
    s.scroll_to(600); s.page.wait_for_timeout(100)
    s.page.click('#menu-btn'); s.page.wait_for_timeout(520)
    st = s.ev(MENU_STATE); s.shot('menu-phone-open.png')
    R.check('menu: open → body.menu-open, aria-expanded, "Close", menu visible, focus on first menu link',
            st['open'] and st['expanded'] == 'true' and st['text'] == 'Close' and st['hidden'] == 'false' and st['vis'] == 'visible' and st['focus'].endswith(':#place:true'), json.dumps({k: st[k] for k in ('open', 'expanded', 'text', 'hidden', 'vis', 'focus')}))
    R.check('menu: background inert (main, footer, wordmark) + iOS-safe scroll-lock at the opening offset',
            st['mainInert'] and st['footInert'] and st['markInert'] and st['bodyPos'] == 'fixed' and st['bodyTop'] == '-600px', json.dumps({k: st[k] for k in ('mainInert', 'footInert', 'markInert', 'bodyPos', 'bodyTop')}))
    # focus trap: Tab from the last link wraps to the toggle, Shift+Tab from the toggle wraps to the last link
    s.ev("document.querySelector('#menu a[href=\"#interest\"]').focus()")
    s.page.keyboard.press('Tab'); f1 = s.ev("document.activeElement.id")
    s.page.keyboard.press('Shift+Tab'); f2 = s.ev("document.activeElement.getAttribute('href')")
    R.check('menu: focus trap wraps (last link → toggle → last link)', f1 == 'theme-toggle' and f2 == '#interest', f'tab={f1} shift+tab={f2}')
    # URL-bar resize must not close it; leaving the phone range does
    s.page.set_viewport_size({'width': 390, 'height': 760}); s.page.wait_for_timeout(150)
    a = s.ev(MENU_STATE)['open']
    s.page.keyboard.press('Escape'); s.page.wait_for_timeout(520)
    st = s.ev(MENU_STATE)
    R.check('menu: a mobile URL-bar resize keeps it open; Esc closes, focus returns to the button, lock + scroll restored',
            a and not st['open'] and st['expanded'] == 'false' and st['text'] == 'Menu' and st['vis'] == 'hidden' and st['focus'].startswith('menu-btn') and not st['mainInert'] and st['bodyPos'] == '' and abs(st['scrollY'] - 600) < 3,
            json.dumps({'openAfterResize': a, **{k: st[k] for k in ('open', 'focus', 'mainInert', 'bodyPos', 'scrollY')}}))
    s.page.click('#menu-btn'); s.page.wait_for_timeout(520)
    s.page.click('#menu a[href="#architecture"]'); s.page.wait_for_timeout(520)
    st = s.ev(MENU_STATE); h = s.ev('location.hash'); top = s.ev("Math.round(document.getElementById('architecture').getBoundingClientRect().top)")
    R.check('menu: a link tap closes the menu and lands on the section (scroll-margin clears the bar)', not st['open'] and h == '#architecture' and not st['mainInert'] and 0 <= top <= 90, f'open={st["open"]} hash={h} section top={top}px')
    s.page.click('#menu-btn'); s.page.wait_for_timeout(520)
    s.page.set_viewport_size({'width': 1200, 'height': 800}); s.page.wait_for_timeout(200)
    st = s.ev(MENU_STATE)
    R.check('menu: growing to desktop width closes an open overlay (resize guard, other branch)', not st['open'] and st['btnDisplay'] == 'none' and st['linksDisplay'] != 'none', json.dumps({k: st[k] for k in ('open', 'btnDisplay', 'linksDisplay')}))
    s.finish('menu phone')


def check_menu_landscape(site):
    s = site.session(theme='day', viewport=(844, 390), has_touch=True, reduced_motion='reduce'); s.goto('/')
    st = s.ev(MENU_STATE)
    R.check('menu: landscape phone 844×390 (coarse + short) gets the overlay button, not the wrapped nav', st['btnDisplay'] != 'none' and st['linksDisplay'] == 'none', json.dumps({k: st[k] for k in ('btnDisplay', 'linksDisplay')}))
    s.page.click('#menu-btn'); s.page.wait_for_timeout(520)
    st = s.ev(MENU_STATE); s.shot('menu-landscape-open.png')
    reach = s.ev("""() => Array.from(document.querySelectorAll('#menu a')).map(a => { a.scrollIntoView({block:'nearest'}); var r = a.getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight && r.height > 0; })""")
    R.check('menu: landscape overlay is top-aligned + scrollable and every item can be brought into view',
            st['open'] and st['overflowY'] == 'auto' and st['alignItems'] == 'flex-start' and len(reach) == 6 and all(reach), f'overflowY={st["overflowY"]} align={st["alignItems"]} reachable={reach}')
    s.page.set_viewport_size({'width': 844, 'height': 340}); s.page.wait_for_timeout(150)
    R.check('menu: landscape URL-bar resize keeps the menu open', s.ev(MENU_STATE)['open'])
    s.finish('menu landscape')
    s = site.session(theme='day', viewport=(1024, 768), has_touch=True, reduced_motion='reduce'); s.goto('/')
    st = s.ev(MENU_STATE)
    R.check('menu: tablet 1024×768 (coarse but tall) keeps the desktop nav', st['btnDisplay'] == 'none' and st['linksDisplay'] != 'none', json.dumps({k: st[k] for k in ('btnDisplay', 'linksDisplay')}))
    s.finish('menu tablet')


LB_STATE = """() => { var d = document.getElementById('lightbox'); var im = d.querySelector('.lb-img');
  return { open: d.open, src: (im.getAttribute('src') || '').split('/').pop(), imgShown: im.style.display !== 'none', ph: d.querySelector('.lb-ph').style.display,
    cap: d.querySelector('.lb-cap').textContent, bodyPos: document.body.style.position,
    focus: document.activeElement ? (document.activeElement.className + '|' + (document.activeElement.getAttribute('aria-label') || '')) : null }; }"""


def check_lightbox(site):
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/gallery/')
    n = s.ev("document.querySelectorAll('main .plate').length")
    kb = s.ev("Array.from(document.querySelectorAll('main .plate')).every(f => f.getAttribute('tabindex') === '0' && f.getAttribute('role') === 'button' && f.getAttribute('aria-label'))")
    R.check('lightbox: all plates are keyboard-operable buttons with labels', n == 23 and kb, f'{n} plates, all labelled={kb}')
    first = s.page.locator('main .plate').first
    first.scroll_into_view_if_needed(); s.page.wait_for_timeout(200)
    first.click(); s.page.wait_for_timeout(250)
    st = s.ev(LB_STATE); s.shot('lightbox-open.png')
    R.check('lightbox: click opens the <dialog> with the plate\'s DAY image and its caption, page scroll-locked',
            st['open'] and 'gallery-approach-day' in st['src'] and st['imgShown'] and st['ph'] == 'none' and st['cap'] == 'Approach · the western coast' and st['bodyPos'] == 'fixed', json.dumps(st))
    s.page.keyboard.press('ArrowRight'); s.page.wait_for_timeout(100); a = s.ev(LB_STATE)
    s.page.keyboard.press('ArrowLeft'); s.page.wait_for_timeout(100); b = s.ev(LB_STATE)
    s.page.keyboard.press('ArrowLeft'); s.page.wait_for_timeout(100); c = s.ev(LB_STATE)
    R.check('lightbox: → and ← move through the plates (and wrap at the ends)',
            'gallery-threshold' in a['src'] and a['cap'] == 'The threshold' and 'gallery-approach-day' in b['src'] and 'gallery-coast-still' in c['src'], f'right={a["cap"]!r} left={b["cap"]!r} wrap={c["cap"]!r}')
    s.page.keyboard.press('Escape'); s.page.wait_for_timeout(150)
    st = s.ev(LB_STATE)
    R.check('lightbox: Esc closes, restores focus to the plate and releases the scroll-lock', not st['open'] and st['bodyPos'] == '' and st['focus'].startswith('plate feature'), json.dumps({k: st[k] for k in ('open', 'bodyPos', 'focus')}))
    # keyboard open + ✕
    first.focus(); s.page.keyboard.press('Enter'); s.page.wait_for_timeout(200); a = s.ev(LB_STATE)
    s.page.click('#lightbox .lb-close'); s.page.wait_for_timeout(150); b = s.ev(LB_STATE)
    R.check('lightbox: Enter on a focused plate opens; ✕ closes', a['open'] and not b['open'], f'enter={a["open"]} after ✕={b["open"]}')
    # backdrop click
    s.page.locator('main .plate').nth(4).scroll_into_view_if_needed(); s.page.wait_for_timeout(100)   # 4 = "Dining, at the long table" (single hour)
    s.page.locator('main .plate').nth(4).click(); s.page.wait_for_timeout(200); a = s.ev(LB_STATE)
    s.page.mouse.click(12, 160); s.page.wait_for_timeout(150); b = s.ev(LB_STATE)
    R.check('lightbox: a single-hour plate opens its one image; clicking the backdrop closes', a['open'] and 'gallery-dining' in a['src'] and a['imgShown'] and not b['open'], f'src={a["src"]} closed={not b["open"]}')
    s.finish('lightbox day')

    # at night the CURRENT hour's layer is chosen (feature pairs → the eve image; singles → their only image)
    s = site.session(theme='night', reduced_motion='reduce'); s.goto('/gallery/')
    first = s.page.locator('main .plate').first; first.scroll_into_view_if_needed(); s.page.wait_for_timeout(200)
    first.click(); s.page.wait_for_timeout(250); a = s.ev(LB_STATE)
    s.page.keyboard.press('ArrowRight'); s.page.wait_for_timeout(100); b = s.ev(LB_STATE)
    s.page.keyboard.press('Escape'); s.page.wait_for_timeout(100)
    R.check('lightbox: under Afterglow a paired plate opens its EVENING image; a single-hour plate its only one',
            a['open'] and 'gallery-approach-eve' in a['src'] and 'gallery-threshold' in b['src'], f'pair={a["src"]} single={b["src"]}')
    s.finish('lightbox night')

    # phone + night: the guardrail hides the evening layer, so the lightbox must fall back to the day image
    s = site.session(theme='night', device='iPhone 13', reduced_motion='reduce'); s.goto('/gallery/')
    first = s.page.locator('main .plate').first; first.scroll_into_view_if_needed(); s.page.wait_for_timeout(200)
    first.tap(); s.page.wait_for_timeout(250); a = s.ev(LB_STATE)
    disp = s.ev("getComputedStyle(document.querySelector('main .plate .shot-night')).display")
    s.page.keyboard.press('Escape')
    R.check('lightbox: on a phone at night (evening layer display:none) a pair opens its DAY image', a['open'] and 'gallery-approach-day' in a['src'] and disp == 'none', f'src={a["src"]} shot-night display={disp}')
    s.finish('lightbox phone night')


WIP_STATE = """() => { var d = document.getElementById('wip'); var ae = document.activeElement;
  return { present: !!d, open: d ? d.open : null, bodyPos: document.body.style.position,
    focus: ae ? ae.className : null, ss: (function(){ try { return sessionStorage.getItem('aethon-wip'); } catch(e){ return 'ERR'; } })() }; }"""


def check_wip(site):
    for path in ('/', '/gallery/', '/legal/'):
        for method in ('✕', 'Look around', 'Esc', 'click-outside'):
            s = site.session(theme='day', wip=False, reduced_motion='reduce'); s.goto(path)
            st = s.ev(WIP_STATE)
            opened = st['present'] and st['open'] and st['bodyPos'] == 'fixed' and st['focus'] == 'wip-dismiss' and st['ss'] == '1'
            if method == '✕': s.page.click('#wip .wip-close')
            elif method == 'Look around': s.page.click('#wip .wip-dismiss')
            elif method == 'Esc': s.page.keyboard.press('Escape')
            else: s.page.mouse.click(4, 4)
            s.page.wait_for_timeout(150)
            st2 = s.ev(WIP_STATE)
            s.page.reload(wait_until='load'); st3 = s.ev(WIP_STATE)
            R.check(f'wip: {path} opens (autofocus "Look around", scroll-locked, session flag set); {method} closes; reload stays closed',
                    opened and not st2['open'] and st2['bodyPos'] == '' and not st3['open'], f'opened={opened} closed={not st2["open"]} lock={st2["bodyPos"]!r} gated={not st3["open"]}')
            s.finish(f'wip {path} {method}')
    s = site.session(theme='day', wip=False, reduced_motion='reduce'); s.goto('/')
    seq = []
    for _ in range(5):   # a modal <dialog> may hand focus to the browser chrome (= body) between its last and first control, never to page content
        s.page.keyboard.press('Tab')
        seq.append(s.ev("(function(){var e=document.activeElement;return e===document.body?'body':(document.getElementById('wip').contains(e)?'wip:'+e.className:'PAGE:'+(e.className||e.tagName))})()"))
    R.check('wip: while the notice is open, Tab never reaches page content (✕ and "Look around" cycle, nothing behind)',
            all(x == 'body' or x.startswith('wip:') for x in seq) and 'wip:wip-close' in seq and 'wip:wip-dismiss' in seq, ' → '.join(seq))
    s.finish('wip focus trap')
    s = site.session(theme='day', wip=True); s.goto('/')
    R.check('wip: a pre-set session flag keeps the notice closed', s.ev(WIP_STATE)['open'] is False); s.finish('wip gated')
    # a deep link has to survive the notice: the browser's fragment scroll runs while the body is position:fixed
    for path, frag in (('/', '#interest'), ('/gallery/', '#ch-evening')):
        s = site.session(theme='day', wip=False, reduced_motion='reduce'); s.goto(path + frag); s.page.wait_for_timeout(400)
        s.page.keyboard.press('Escape'); s.page.wait_for_timeout(700)
        top = s.ev(f"Math.round(document.querySelector('{frag}').getBoundingClientRect().top)"); sy = s.ev('window.scrollY')
        R.check(f'wip: a fresh-session arrival at {path}{frag} lands on that section once the notice is closed', 0 <= top <= 120,
                f'section top={top}px, scrollY={sy} after closing (the notice locks the body before the fragment scroll; unlock restores the pre-lock scrollY)')
        s.finish(f'wip deep link {path}{frag}')
    s = site.session(theme='day', wip=True, reduced_motion='reduce'); s.goto('/#interest'); s.page.wait_for_timeout(400)
    top = s.ev("Math.round(document.getElementById('interest').getBoundingClientRect().top)")
    R.check('wip: control — with the notice already dismissed this session, /#interest lands on the form', 0 <= top <= 120, f'section top={top}px'); s.finish('wip deep link control')
    s = site.session(theme='day'); s.goto('/404.html')
    R.check('wip: the 404 page carries no notice', not s.ev(WIP_STATE)['present']); s.finish('wip 404', network=False)


FORM_STATE = """() => { var f = document.getElementById('register-form'), b = f.querySelector('button[type=submit]');
  return { formHidden: f.hidden, noteHidden: document.getElementById('register-note').hidden, errHidden: document.getElementById('register-error').hidden,
    thanksHidden: document.getElementById('register-thanks').hidden, btnText: b.textContent, btnDisabled: b.disabled,
    focus: document.activeElement ? (document.activeElement.id || document.activeElement.className) : null }; }"""


def check_form(site):
    s = site.session(theme='day', reduced_motion='reduce'); posts = mock_brevo(s.page, 'ok'); s.goto('/')
    s.page.fill('#name', 'Verify Script'); s.page.fill('#email', 'verify@example.com'); s.page.fill('#message', 'regression run')
    s.page.click('button.submit'); s.page.wait_for_timeout(600)
    st = s.ev(FORM_STATE)
    R.check('form: AJAX success hides form + note, shows and focuses the thank-you block',
            st['formHidden'] and st['noteHidden'] and not st['thanksHidden'] and st['errHidden'] and st['focus'] == 'register-thanks', json.dumps(st))
    body = urllib.parse.parse_qs(posts[0]['body'], keep_blank_values=True) if posts else {}
    R.check('form: one POST to the Brevo serve URL carrying FIRSTNAME/EMAIL/MESSAGE/SOURCE, honeypot empty',
            len(posts) == 1 and posts[0]['method'] == 'POST' and '06e3f483.sibforms.com/serve/' in posts[0]['url']
            and body.get('FIRSTNAME') == ['Verify Script'] and body.get('EMAIL') == ['verify@example.com'] and body.get('MESSAGE') == ['regression run']
            and body.get('SOURCE') == ['aethon.house'] and body.get('locale') == ['en'] and body.get('email_address_check', ['']) == [''],
            f'{len(posts)} post(s); keys={sorted(body.keys())}')
    s.finish('form success')

    s = site.session(theme='day', reduced_motion='reduce'); posts = mock_brevo(s.page, 'fail'); s.goto('/')
    s.page.fill('#name', 'Verify Script'); s.page.fill('#email', 'verify@example.com')
    s.page.click('button.submit'); s.page.wait_for_timeout(600)
    st = s.ev(FORM_STATE)
    R.check('form: network failure shows the quiet error line, keeps the form, re-enables + refocuses the button',
            not st['formHidden'] and not st['errHidden'] and st['thanksHidden'] and not st['btnDisabled'] and st['btnText'] == 'Register interest' and st['focus'] == 'submit' and len(posts) == 1, json.dumps(st))
    s.finish('form failure', network=False, ignore=('net::ERR_FAILED',))   # the aborted request IS the mock

    s = site.session(theme='day', reduced_motion='reduce'); posts = mock_brevo(s.page, 'ok'); s.goto('/')
    s.page.fill('#name', 'Bot'); s.page.fill('#email', 'bot@example.com'); s.ev("document.getElementById('company').value = 'spam'")
    s.page.click('button.submit'); s.page.wait_for_timeout(500)
    st = s.ev(FORM_STATE)
    R.check('form: a filled honeypot is silently ignored (no request, form untouched)', len(posts) == 0 and not st['formHidden'] and st['thanksHidden'], f'posts={len(posts)}')
    s.ev("document.getElementById('company').value = ''"); s.page.fill('#email', 'not-an-email')
    s.page.click('button.submit'); s.page.wait_for_timeout(400)
    v = s.ev("document.getElementById('email').validity.valid")
    R.check('form: native validation blocks an invalid email before any request', len(posts) == 0 and not v, f'posts={len(posts)} email valid={v}')
    s.finish('form honeypot/validation')

    s = site.session(theme='day', js=False); s.goto('/')
    act = s.ev("(function(){var f=document.getElementById('register-form');return [f.getAttribute('method'), f.action.indexOf('sibforms.com/serve/')>0, getComputedStyle(f).display]})()")
    R.check('form: without JavaScript the native POST to Brevo remains (method, action, visible)', act[0].upper() == 'POST' and act[1] and act[2] != 'none', json.dumps(act))
    s.finish('form no-js', network=False)


def check_beacons(site):
    chapters = ['ch-place', 'ch-architecture', 'ch-plan', 'ch-garden', 'ch-interior', 'ch-materials', 'ch-views', 'reach-register']
    s = site.session(theme='day', reduced_motion='reduce'); hits = capture_beacons(s.page); mock_brevo(s.page, 'ok')
    s.goto('/?via=gate'); s.page.wait_for_timeout(300)
    search = s.ev('location.search')
    R.check('beacons: ?via=gate is counted once and stripped from the address bar', hits.count('via-gate') == 1 and search == '', f'hits={hits} search={search!r}')
    R.check('beacons: a Daylight arrival sends no afterglow-auto', 'afterglow-auto' not in hits, f'hits={hits}')
    s.scroll_through(step=400, pause=120)
    got = [c for c in chapters if c in hits]
    R.check('beacons: all seven chapter-reach events + reach-register fire on a full scroll', got == chapters, f'got={got}')
    el = s.page.locator('.pause-media[data-hold]').first; el.scroll_into_view_if_needed(); s.page.wait_for_timeout(100)
    b = el.bounding_box(); s.page.mouse.move(b['x'] + b['width'] / 2, b['y'] + b['height'] / 2); s.page.mouse.down(); s.page.wait_for_timeout(350); s.page.mouse.up()
    R.check('beacons: hold fires', 'hold' in hits, f'hits={hits}')
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(200)
    R.check('beacons: a chosen switch into Afterglow fires afterglow (not afterglow-auto)', hits.count('afterglow') == 1 and 'afterglow-auto' not in hits, f'hits={hits}')
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(200); s.page.click('#theme-toggle'); s.page.wait_for_timeout(200)
    s.page.focus('#name'); s.page.wait_for_timeout(100)
    R.check('beacons: focusing the form fires form-start', 'form-start' in hits, f'hits={hits}')
    s.page.fill('#name', 'V'); s.page.fill('#email', 'v@example.com'); s.page.click('button.submit'); s.page.wait_for_timeout(500)
    R.check('beacons: submitting fires form-submit (beside the AJAX post)', 'form-submit' in hits, f'hits={hits}')
    s.scroll_to(0); s.scroll_through(step=600, pause=60)
    dup = [h for h in set(hits) if hits.count(h) > 1]
    R.check('beacons: every event counts at most once per pageview (re-scroll, re-toggle)', not dup, f'duplicates={dup} total={len(hits)}')
    s.finish('beacons flow')

    s = site.session(theme=None, fake_time='2026-07-15T18:30:00Z'); hits = capture_beacons(s.page); s.goto('/'); s.page.wait_for_timeout(300)
    R.check('beacons: an evening arrival with no saved theme fires afterglow-auto, not afterglow', hits.count('afterglow-auto') == 1 and 'afterglow' not in hits, f'hits={hits}')
    s.finish('beacons afterglow-auto')

    for flag, kw in (('DNT', {'dnt': True}), ('Global Privacy Control', {'gpc': True})):
        s = site.session(theme=None, fake_time='2026-07-15T18:30:00Z', reduced_motion='reduce', **kw); hits = capture_beacons(s.page); mock_brevo(s.page, 'ok')
        s.goto('/?via=sea'); s.scroll_through(step=500, pause=60)
        el = s.page.locator('.pause-media[data-hold]').first; el.scroll_into_view_if_needed(); b = el.bounding_box()
        s.page.mouse.move(b['x'] + 10, b['y'] + 10); s.page.mouse.down(); s.page.wait_for_timeout(300); s.page.mouse.up()
        s.page.click('#theme-toggle'); s.page.wait_for_timeout(150); s.page.click('#theme-toggle'); s.page.wait_for_timeout(150)
        s.page.fill('#name', 'V'); s.page.fill('#email', 'v@example.com'); s.page.click('button.submit'); s.page.wait_for_timeout(400)
        R.check(f'beacons: with {flag} the whole flow sends ZERO beacons (via, auto-evening, scroll, hold, toggle, form)', len(hits) == 0, f'hits={hits}')
        s.finish(f'beacons {flag}')

    for path in ('/gallery/', '/legal/'):
        s = site.session(theme='day', reduced_motion='reduce'); hits = capture_beacons(s.page); s.goto(path); s.scroll_through(step=800, pause=50)
        R.check(f'beacons: {path} sends none (Cloudflare counts its views)', len(hits) == 0, f'hits={hits}')
        s.finish(f'beacons {path}')

    # a honeypot-caught submission never reaches Brevo — it should not be counted as a completed ask either
    s = site.session(theme='day', reduced_motion='reduce'); hits = capture_beacons(s.page); posts = mock_brevo(s.page, 'ok'); s.goto('/')
    s.page.fill('#name', 'Bot'); s.page.fill('#email', 'bot@example.com'); s.ev("document.getElementById('company').value = 'spam'")
    s.page.click('button.submit'); s.page.wait_for_timeout(400)
    R.check('beacons: a honeypot-caught submission is not counted as form-submit', 'form-submit' not in hits and len(posts) == 0,
            f'hits={hits} brevo-posts={len(posts)} (the submit beacon listener runs before the AJAX handler\'s honeypot check)')
    s.finish('beacons honeypot')


def _image_requests(s):
    urls = []
    s.page.on('request', lambda rq: urls.append(rq.url) if rq.resource_type == 'image' else None)
    return urls


def check_cellular(site):
    s = site.session(theme='day', device='iPhone 13', reduced_motion='reduce'); urls = _image_requests(s); s.goto('/')
    s.scroll_through(step=300, pause=140); s.page.wait_for_timeout(1200)
    eve = sorted({u.split('/')[-1] for u in urls if '-eve-' in u})
    stray = [u for u in eve if not (u.startswith('hero-eve-') or u.startswith('pause-'))]
    day_views = [u for u in urls if '/images/views/' in u and '-day-' in u]
    R.check('cellular: iPhone 13 full scroll fetches NO evening layer except the hero pair and the two hold plates',
            not stray and any(u.startswith('hero-eve-') for u in eve) and len(day_views) >= 3, f'eve={eve} stray={stray} view-day-requests={len(day_views)}')
    guard = s.ev("""() => ({ night: getComputedStyle(document.querySelector('#gallery .frame.shot-pair .shot-night')).display,
        plate: getComputedStyle(document.querySelector('#architecture .frame.shot-pair .shot-night')).display,
        pause: getComputedStyle(document.querySelector('.pause-media .shot-night')).display })""")
    R.check('cellular: Views + woven plate evening layers are display:none on the phone, pause plates keep theirs', guard['night'] == 'none' and guard['plate'] == 'none' and guard['pause'] != 'none', json.dumps(guard))
    s.page.click('#theme-toggle'); s.page.wait_for_timeout(250)
    op = s.ev("""() => ({ day: getComputedStyle(document.querySelector('#gallery .frame.shot-pair .shot-day')).opacity,
                          plate: getComputedStyle(document.querySelector('#architecture .frame.shot-pair .shot-day')).opacity })""")
    R.check('cellular: at night on the phone the day layer stays visible (opacity revert — frames never go blank)', op['day'] == '1' and op['plate'] == '1', json.dumps(op))
    s.shot('cellular-iphone-night-views.png')
    s.finish('cellular index')

    s = site.session(theme='night', device='iPhone 13', reduced_motion='reduce'); urls = _image_requests(s); s.goto('/gallery/')
    s.scroll_through(step=300, pause=140); s.page.wait_for_timeout(1200)
    eve = sorted({u.split('/')[-1] for u in urls if '-eve-' in u}); days = [u for u in urls if '/images/gallery/' in u]
    R.check('cellular: /gallery/ on iPhone 13 (even at night) fetches no evening layer at all', not eve and len(days) >= 15, f'eve={eve} gallery-requests={len(days)}')
    s.finish('cellular gallery')

    # positive control — on a desktop the evening layers DO load (so the phone assertion is not vacuous)
    s = site.session(theme='day', reduced_motion='reduce'); urls = _image_requests(s); s.goto('/')
    s.scroll_through(step=500, pause=100); s.page.wait_for_timeout(1000)
    eve = sorted({u.split('/')[-1] for u in urls if '-eve-' in u})
    R.check('cellular: desktop control — Views/plate evening layers are fetched (lazy-load reaches them)', any(u.startswith('views-') for u in eve) and any(u.startswith('plate-living-eve') for u in eve), f'eve={eve}')
    s.finish('cellular desktop control')


def check_404(site):
    s = site.session(theme='day'); r = s.goto('/404.html')
    st = s.ev("(function(){var m=document.querySelector('main');return {main:!!m, h1:m&&m.querySelector('h1')&&m.querySelector('h1').textContent.trim(), p:m&&m.querySelector('p')&&m.querySelector('p').textContent.trim(), home:!!document.querySelector('main a[href=\"/\"]'), logo:getComputedStyle(document.querySelector('h1')).backgroundImage.indexOf('logo-dark.svg')>0}})()")
    R.check('404: /404.html renders <main> with the mark, the line and a way home', r.status == 200 and st['main'] and st['h1'] == 'AETHON' and st['p'] == 'This page has slipped from view.' and st['home'] and st['logo'], json.dumps(st))
    s.finish('404 page')
    s = site.session(theme='day'); r = s.goto('/no-such-page/')
    R.check('404: an unknown path serves 404.html with status 404 (local server mirrors GitHub Pages)', r.status == 404 and s.ev("!!document.querySelector('main a[href=\"/\"]')"), f'status={r.status}')
    s.ctx.close()


def check_console_clean(site):
    for path in PAGES:
        for theme in ('day', 'night'):
            s = site.session(theme=theme); s.goto(path)
            if path != '/404.html':
                s.page.keyboard.press('Escape')
            s.scroll_through(step=700, pause=80); s.page.wait_for_timeout(600)
            s.finish(f'console: {path} in {theme} (full scroll, every asset fetched)')


def check_keyboard(site):
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/')
    seq = []
    for _ in range(90):
        s.page.keyboard.press('Tab')
        d = s.ev("(function(){var e=document.activeElement;if(!e||e===document.body)return 'body';return (e.tagName+'#'+(e.id||'')+'.'+(e.className||'').toString().split(' ')[0]+'@'+(e.getAttribute('href')||'')).toLowerCase()})()")
        seq.append(d)
        if d.startswith('button#.submit'): break

    def idx(pred):
        for i, d in enumerate(seq):
            if pred(d): return i
        return -1
    skip = idx(lambda d: d.startswith('a#.skip-link'))
    mark = idx(lambda d: d.startswith('a#.mark'))
    nav = [idx(lambda d, h=h: d.endswith('@' + h) and d.startswith('a#.') and not d.startswith('a#.menu')) for h in ('#place', '#architecture', '#garden', '#interior', '/gallery/', '#interest')]
    tog = idx(lambda d: d.startswith('button#theme-toggle'))
    chip = idx(lambda d: d.startswith('button#.hero-media'))
    holds = [i for i, d in enumerate(seq) if d.startswith('div#.pause-media')]
    name, email, msg, sub = idx(lambda d: d.startswith('input#name')), idx(lambda d: d.startswith('input#email')), idx(lambda d: d.startswith('textarea#message')), idx(lambda d: d.startswith('button#.submit'))
    hp = idx(lambda d: d.startswith('input#company'))
    menu = idx(lambda d: d.startswith('button#menu-btn'))
    ok = (skip == 0 and mark == 1 and nav == list(range(2, 8)) and tog == 8 and chip == 9 and len(holds) == 2
          and 0 < name < email < msg < sub and hp == -1 and menu == -1)
    R.check('keyboard: Tab order — skip link, mark, nav ×6, toggle, hero chip … hold plates … form (honeypot + hidden menu button skipped)', ok,
            f'skip={skip} mark={mark} nav={nav} toggle={tog} chip={chip} holds={holds} form={name},{email},{msg},{sub} honeypot={hp} menubtn={menu}')
    s.ev("document.querySelector('.skip-link').focus()")
    clip = s.ev("getComputedStyle(document.querySelector('.skip-link')).clipPath")
    s.page.keyboard.press('Enter'); s.page.wait_for_timeout(100)
    R.check('keyboard: the skip link becomes visible on focus and Enter jumps to #top', clip == 'none' and s.ev('location.hash') == '#top', f'clip-path={clip} hash={s.ev("location.hash")}')
    s.finish('keyboard')
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/gallery/')
    seq = []
    for _ in range(12):
        s.page.keyboard.press('Tab'); seq.append(s.ev("(function(){var e=document.activeElement;return (e.className||e.tagName).toString().split(' ')[0]+'@'+(e.getAttribute('href')||'')})()"))
    R.check('keyboard: /gallery/ Tab order — skip link, mark, tracker I–VI, back link, toggle, first plate',
            seq[0].startswith('skip-link') and seq[1].startswith('mark') and [x.split('@')[1] for x in seq[2:8]] == ['#ch-arrival', '#ch-ground', '#ch-garden', '#ch-evening', '#ch-withdraw', '#ch-materials']
            and seq[8].endswith('@/') and seq[9].startswith('toggle') and seq[10].startswith('plate'), ' → '.join(seq))
    s.finish('keyboard gallery')


# ----------------------------------------------------------------------------------------------
# static checks — links, anchors, assets on disk, external hosts
# ----------------------------------------------------------------------------------------------
class Collector(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids, self.refs, self.styles, self._style = set(), [], [], False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); line = self.getpos()[0]
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'style': self._style = True
        for k in ('href', 'src', 'action', 'poster'):
            if a.get(k): self.refs.append((tag, k, a[k], line))
        if a.get('srcset'):
            for part in a['srcset'].split(','):
                u = part.strip().split()[0] if part.strip() else ''
                if u: self.refs.append((tag, 'srcset', u, line))
        for k in ('aria-labelledby', 'aria-describedby', 'aria-controls', 'for'):
            if a.get(k):
                for i in a[k].split(): self.refs.append((tag, k, '#' + i, line))

    def handle_endtag(self, tag):
        if tag == 'style': self._style = False

    def handle_data(self, data):
        if self._style:
            for m in re.finditer(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', data):
                self.styles.append((m.group(1), self.getpos()[0]))


def _resolve(page_rel, ref):
    """Map a href/src to (disk path or None, fragment, kind)."""
    u = urllib.parse.urlsplit(ref)
    if u.scheme in ('http', 'https'): return None, '', 'external'
    if u.scheme in ('mailto', 'tel', 'data', 'javascript'): return None, '', u.scheme
    path = u.path
    if not path:
        return os.path.join(ROOT, page_rel), u.fragment, 'self'
    if path.startswith('/'):
        disk = os.path.join(ROOT, path.lstrip('/'))
    else:
        disk = os.path.normpath(os.path.join(ROOT, os.path.dirname(page_rel), path))
    if os.path.isdir(disk): disk = os.path.join(disk, 'index.html')
    return disk, u.fragment, 'local'


def check_static():
    docs, externals, n_assets, n_anchors, problems = {}, {}, 0, 0, []
    for rel in PAGES.values():
        c = Collector(); c.feed(open(os.path.join(ROOT, rel), encoding='utf-8').read()); docs[rel] = c
    for rel, c in docs.items():
        for tag, attr, ref, line in c.refs:
            disk, frag, kind = _resolve(rel, ref)
            if kind == 'external':
                if tag in ('a', 'form'): externals.setdefault(ref, []).append(f'{rel}:{line}')   # visitor-facing links only (not canonical/og self-references)
                continue
            if kind != 'local' and kind != 'self': continue
            if not os.path.isfile(disk):
                problems.append(f'{rel}:{line} <{tag} {attr}="{ref}"> → missing {os.path.relpath(disk, ROOT)}'); continue
            if attr in ('src', 'srcset', 'poster') or (tag == 'link' and attr == 'href'): n_assets += 1
            if frag:
                n_anchors += 1
                target_rel = os.path.relpath(disk, ROOT)
                ids = docs[target_rel].ids if target_rel in docs else Collector().ids
                if frag not in ids and frag:
                    problems.append(f'{rel}:{line} <{tag} {attr}="{ref}"> → no id="{frag}" in {target_rel}')
        for ref, line in c.styles:
            if ref.startswith('data:'): continue
            disk, _, kind = _resolve(rel, ref)
            if kind == 'local' and not os.path.isfile(disk): problems.append(f'{rel}:{line} css url({ref}) → missing')
            elif kind == 'local': n_assets += 1
    R.check('static: every internal href / anchor / <picture> source / img src / CSS url() resolves on disk',
            not problems, f'{n_assets} asset refs + {n_anchors} fragment anchors checked across 4 pages' if not problems else '; '.join(problems[:6]))
    # the files the site promises elsewhere
    extra = []
    for u in re.findall(r'<loc>([^<]+)</loc>', open(os.path.join(ROOT, 'sitemap.xml')).read()):
        p = urllib.parse.urlsplit(u).path
        if not os.path.isfile(_resolve('index.html', p)[0]): extra.append(f'sitemap {u}')
    for ic in json.load(open(os.path.join(ROOT, 'site.webmanifest')))['icons']:
        if not os.path.isfile(_resolve('index.html', ic['src'])[0]): extra.append(f'manifest {ic["src"]}')
    for u in re.findall(r'content="(https://aethon\.house/[^"]+\.(?:jpg|png|svg))"', open(os.path.join(ROOT, 'index.html')).read()):
        if not os.path.isfile(_resolve('index.html', urllib.parse.urlsplit(u).path)[0]): extra.append(f'og {u}')
    R.check('static: sitemap URLs, manifest icons and the og/twitter image exist on disk', not extra, '; '.join(extra) or 'all present')
    return externals


def _head(url, ctx):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36 aethon-verify'})
    try:
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r: return r.status, r.geturl(), None
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 429, 501):          # some hosts refuse HEAD; try a GET before judging
            try:
                req = urllib.request.Request(url, headers=req.headers)
                with urllib.request.urlopen(req, timeout=25, context=ctx) as r: return r.status, r.geturl(), None
            except urllib.error.HTTPError as e2: return e2.code, url, None
            except Exception as e2: return None, url, str(e2)
        return e.code, url, None
    except Exception as e:
        return None, url, str(e)


def check_external(externals, enabled):
    if not enabled:
        for u in externals: R.skip(f'external: {u}', 'not requested (--no-external)')
        return
    ca = next((p for p in (os.environ.get('SSL_CERT_FILE'), os.environ.get('REQUESTS_CA_BUNDLE'), '/root/.ccr/ca-bundle.crt') if p and os.path.isfile(p)), None)
    ctx = ssl.create_default_context(cafile=ca) if ca else ssl.create_default_context()
    for url, where in sorted(externals.items()):
        host = urllib.parse.urlsplit(url).netloc
        code, final, err = _head(url, ctx)
        label = f'external: {host} ({", ".join(sorted(set(where))[:2])})'
        if err is not None:
            hint = ' (a TLS verify failure through a non-intercepting network means the HOST\'s own certificate is at fault — check it in a browser)' if 'CERTIFICATE_VERIFY_FAILED' in err else ''
            R.skip(label, f'unreachable from sandbox — {err[:140]}{hint}'); continue
        if 200 <= code < 400:
            R.check(label, True, f'HTTP {code}' + (f' → {final}' if final != url else ''))
        elif code in (404, 410):
            R.check(label, False, f'HTTP {code} — the link is dead')
        else:
            R.skip(label, f'HTTP {code} to an automated request (bot shield / login wall) — verify in a browser')


# ----------------------------------------------------------------------------------------------
# a few cheap sanity checks around the main matrix
# ----------------------------------------------------------------------------------------------
BAR_STATE = """() => { var mk = document.querySelector('.bar .mark').getBoundingClientRect();
  var links = Array.from(document.querySelectorAll('nav.links a')).map(function(a){ return a.getBoundingClientRect(); });
  var tops = {}; links.forEach(function(r){ tops[Math.round(r.top)] = 1; });
  var navLeft = links.length ? Math.min.apply(null, links.map(function(r){ return r.left; })) : 9999;
  var hint = document.querySelector('.toggle-hint'), tg = document.getElementById('theme-toggle');
  return { mark: Math.round(mk.width), gap: Math.round(navLeft - mk.right), rows: Object.keys(tops).length,
    navVis: getComputedStyle(document.querySelector('nav.links')).display !== 'none',
    menuBtn: getComputedStyle(document.getElementById('menu-btn')).display !== 'none',
    hintRight: hint ? Math.round(hint.getBoundingClientRect().right) : null, toggleRight: Math.round(tg.getBoundingClientRect().right),
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth }; }"""


def check_bar_band(site):
    """The 701–940 band tightens the bar (mark 5rem, small links) so six links + mark + toggle share
    one row; ≤700 is the overlay menu; from 941 the full-size bar. Fine and coarse pointers."""
    for touch in (False, True):
        s = site.session(theme='day', viewport=(760, 1000), has_touch=touch, reduced_motion='reduce'); s.goto('/')
        s.ev("document.getElementById('theme-toggle').click()"); s.page.wait_for_timeout(150)   # populates the one-time hint
        bad = []
        for w in (700, 701, 744, 768, 820, 901, 915, 940, 941, 1024):
            s.page.set_viewport_size({'width': w, 'height': 1000}); s.page.wait_for_timeout(120)
            st = s.ev(BAR_STATE)
            if w <= 700:
                ok = (not st['navVis']) and st['menuBtn']
            else:
                ok = st['navVis'] and not st['menuBtn'] and st['rows'] == 1 and st['gap'] >= 12 and not st['overflow'] \
                    and st['mark'] == (80 if w <= 940 else 96) and abs(st['hintRight'] - st['toggleRight']) <= 2
            if not ok: bad.append((w, st))
        R.check(f"bar band ({'coarse' if touch else 'fine'}): ≤700 overlay; 701–940 tight bar, one row, mark 80px, hint aligned to the toggle; 941+ full bar",
                not bad, json.dumps(bad[:2]))
        s.finish('bar band ' + ('coarse' if touch else 'fine'))
    # a landscape phone is inside the band's width range but uses the overlay — it must keep the full bar
    s = site.session(theme='day', viewport=(844, 390), has_touch=True, reduced_motion='reduce'); s.goto('/')
    st = s.ev(BAR_STATE); edge = s.ev("parseFloat(getComputedStyle(document.getElementById('bar')).paddingLeft)")
    R.check('bar band: a landscape phone (844×390, coarse) keeps the 6rem mark and the --edge padding (band not applied; overlay in use)',
            st['mark'] == 96 and st['menuBtn'] and not st['navVis'] and abs(edge - 50.64) < 1, json.dumps({'mark': st['mark'], 'menuBtn': st['menuBtn'], 'navVis': st['navVis'], 'padding': edge}))
    s.finish('bar band landscape phone')


PRINT_STATE = """() => { var cs = function(sel){ var e = document.querySelector(sel); return e ? getComputedStyle(e) : null; };
  var mk = cs('.bar .mark'), wip = cs('.wip'), body = getComputedStyle(document.body);
  var hidden = ['.toggle', '.menu-btn', '.wip', '.tracker', '.lightbox', '.hero-media', '.skip-link'].filter(function(sel){ var c = cs(sel); return c && c.display !== 'none'; });
  var fm = cs('.foot-mark');
  return { markIndent: mk.textIndent, markBg: mk.backgroundImage, bodyColor: body.color, bodyBg: body.backgroundColor,
    barPos: cs('header.bar').position, stillShown: hidden, footMarkBg: fm ? fm.backgroundImage : null,
    reveal: cs('.reveal') ? cs('.reveal').opacity : '1', scheme: getComputedStyle(document.documentElement).colorScheme,
    wipOpen: !!(document.getElementById('wip') && document.getElementById('wip').open), bodyPos: body.position, inlinePos: document.body.style.position }; }"""


def check_print(site):
    """Print media: controls hidden (even with the WIP notice open), bar static, wordmarks as text,
    Daylight ink regardless of the saved theme — on all three pages."""
    for path in ('/', '/gallery/', '/legal/'):
        for theme in ('day', 'night'):
            s = site.session(theme=theme, wip=False, viewport=(794, 1123), reduced_motion='reduce'); s.goto(path)
            s.page.wait_for_timeout(300)
            s.page.emulate_media(media='print'); s.page.wait_for_timeout(1200)   # transitions are off in print, but let the switch settle
            st = s.ev(PRINT_STATE)
            ok = st['markIndent'] == '0px' and st['markBg'] == 'none' and st['footMarkBg'] == 'none' and st['barPos'] == 'static' \
                and not st['stillShown'] and st['bodyColor'] == 'rgb(44, 38, 32)' and st['reveal'] == '1' and st['scheme'] == 'light' \
                and st['wipOpen'] and st['inlinePos'] == 'fixed' and st['bodyPos'] == 'static'
            R.check(f'print {path} ({theme}, WIP open): wordmarks as text, controls hidden, bar static, Daylight ink, reveal visible, inline scroll-lock released', ok, json.dumps(st))
            try:
                import pypdfium2 as pdfium
                pages = len(pdfium.PdfDocument(s.page.pdf(format='A4')))
                R.check(f'print {path} ({theme}, WIP open): the PDF runs to more than one page (the lock gave one viewport-sized sheet)', pages > 1, f'{pages} page(s)')
            except ImportError:
                R.skip(f'print {path} ({theme}): PDF page count — pypdfium2 not installed')
            s.page.emulate_media(media='screen')
            s.finish(f'print {path} {theme}')


def check_misc(site):
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/')
    yr = s.ev("document.getElementById('year').textContent")
    R.check('misc: the footer year is live', yr == str(time.gmtime().tm_year), yr)
    s.ev("document.getElementById('garden').scrollIntoView({block:'start'})"); s.page.wait_for_timeout(250)
    spy = s.ev("(function(){var a=document.querySelector('nav.links a.active');return {href:a&&a.getAttribute('href'),cur:a&&a.getAttribute('aria-current'),bar:document.getElementById('bar').classList.contains('scrolled')}})()")
    R.check('misc: scroll-spy marks the section in view (aria-current) and the bar solidifies after 20% viewport', spy['href'] == '#garden' and spy['cur'] == 'true' and spy['bar'], json.dumps(spy))
    s.scroll_through(step=700, pause=60)
    rv = s.ev("Array.from(document.querySelectorAll('.reveal')).filter(e=>!e.classList.contains('in')).length")
    R.check('misc: every .reveal block has been revealed after a full scroll', rv == 0, f'{rv} still hidden')
    chip = s.ev("getComputedStyle(document.querySelector('.hero-media')).display")
    R.check('misc: desktop shows the hero chip (hidden on touch/small screens)', chip != 'none', chip)
    s.finish('misc desktop')
    s = site.session(theme='day', js=False, viewport=(390, 844)); s.goto('/')
    nojs = s.ev("(function(){return {reveal:getComputedStyle(document.querySelector('.reveal')).opacity, menuBtn:getComputedStyle(document.getElementById('menu-btn')).display, wip:document.getElementById('wip').open, jsClass:document.documentElement.classList.contains('js')}})()")
    R.check('misc: without JavaScript the content is visible (.reveal not hidden), the dead Menu button is hidden, no notice', nojs['reveal'] == '1' and nojs['menuBtn'] == 'none' and not nojs['wip'] and not nojs['jsClass'], json.dumps(nojs))
    s.finish('misc no-js', network=False)
    s = site.session(theme='day', reduced_motion='reduce'); s.goto('/gallery/')
    s.ev("document.getElementById('ch-garden').scrollIntoView({block:'start'})"); s.page.wait_for_timeout(300)
    tr = s.ev("(function(){var a=document.querySelector('.tracker a.active');return a&&a.getAttribute('href')})()")
    R.check('misc: the gallery tracker follows the chapter in view', tr == '#ch-garden', f'active={tr}')
    s.finish('misc gallery tracker')
    s = site.session(theme='day'); s.goto('/images/og.jpg')
    dims = s.ev("(function(){var i=document.querySelector('img');return i?[i.naturalWidth,i.naturalHeight]:null})()")
    R.check('misc: og.jpg is 1200×630', dims == [1200, 630], str(dims)); s.ctx.close()
    hero = re.sub(r'<!--.*?-->', '', open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read(), flags=re.S)   # comments mention <img> too
    m = re.search(r'<img src="images/hero/hero-day-1600\.jpg"[^>]*>', hero)
    R.check('misc: the hero day image is the LCP candidate (fetchpriority=high, not lazy, first image in DOM)',
            m and 'fetchpriority="high"' in m.group(0) and 'loading="lazy"' not in m.group(0) and re.search(r'<img\s', hero).start() == m.start(), m.group(0)[:80] if m else 'hero img not found')


# ----------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', type=int, default=8402)
    ap.add_argument('--only', default='', help='run only checks whose group name contains this substring')
    ap.add_argument('--no-external', action='store_true', help='skip HEAD requests to external hosts')
    ap.add_argument('--artifacts', default=os.path.join(tempfile.gettempdir(), 'aethon-verify'), help='screenshots + summary.json')
    ap.add_argument('--headed', action='store_true')
    args = ap.parse_args()
    os.makedirs(args.artifacts, exist_ok=True)
    base, srv = serve(args.port)
    print(f'# AETHON verify-site · {base} · artifacts → {args.artifacts}', flush=True)

    from playwright.sync_api import sync_playwright
    groups = [('theme', check_theme_toggle), ('r4', check_r4_clock), ('sweep', check_dusk_sweep), ('hold', check_hold),
              ('menu', lambda st: (check_menu_phone(st), check_menu_landscape(st))), ('lightbox', check_lightbox), ('wip', check_wip),
              ('form', check_form), ('beacons', check_beacons), ('cellular', check_cellular), ('404', check_404),
              ('console', check_console_clean), ('keyboard', check_keyboard), ('misc', check_misc),
              ('bar', check_bar_band), ('print', check_print)]
    t0 = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=CHROMIUM, headless=not args.headed)
        site = Site(pw, browser, base, args.artifacts)
        for name, fn in groups:
            if args.only and args.only not in name: continue
            try:
                fn(site)
            except Exception as e:                      # a crashed group is a FAIL, never a silent skip
                R.fail(f'{name}: check group crashed', f'{type(e).__name__}: {str(e)[:160]}')
        browser.close()
    if not args.only or args.only in 'static external':
        externals = check_static()
        check_external(externals, not args.no_external)
    if srv: srv.shutdown()
    n = len(R.rows); f = len(R.failed); sk = len([r for r in R.rows if r['status'] == 'SKIP'])
    with open(os.path.join(args.artifacts, 'summary.json'), 'w') as fh:
        json.dump({'base': base, 'checks': R.rows, 'pass': n - f - sk, 'fail': f, 'skip': sk, 'seconds': round(time.time() - t0, 1)}, fh, indent=1)
    print(f'# {n - f - sk} PASS · {f} FAIL · {sk} SKIP · {time.time() - t0:.0f}s', flush=True)
    sys.exit(1 if f else 0)


if __name__ == '__main__':
    main()
