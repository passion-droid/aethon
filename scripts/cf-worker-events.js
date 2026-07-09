// AETHON events — anonymous, aggregate, first-party counters.
//
// Counts ONLY a whitelisted event name into a per-day KV bucket. Stores nothing else:
// no IPs, no identifiers, no user agents, no cookies, no per-visitor anything.
// Honours Do-Not-Track and Global Privacy Control at the edge as well as on the page.
// Lost-update races under concurrency can drop the odd count (±1) — irrelevant at this
// site's scale and a fair trade for having no state beyond a plain counter.
//
// Route:   aethon.house/e*        (same-origin — the page calls navigator.sendBeacon('/e?n=…'))
// Binding: EVENTS                 (Workers KV namespace "aethon_events")
// Deploy:  .github/workflows/deploy-events-worker.yml (scripts/deploy-events-worker.sh)
// Read:    scripts/seo-pull.py — "On-page events" section of the fortnightly report.

const ALLOW = new Set([
  // channel attribution — dormant while the stone QRs carry the pure URL (owner 2026-07-09);
  // available for future digital shares (aethon.house/?via=gate|sea)
  'via-gate', 'via-sea',
  // the one idea — chosen (a switch into Afterglow) vs given (arrival in the house's evening)
  'afterglow', 'afterglow-auto',
  // hold-to-preview engaged (first time per visit)
  'hold',
  // pre-registered for when real media lands (wire in the media elements' play handlers)
  'film-play', 'hero-loop',
  // how far the portrait carries — one count per chapter per visit
  'ch-place', 'ch-architecture', 'ch-plan', 'ch-garden', 'ch-interior', 'ch-materials', 'ch-views',
  // the ask — reached, begun, completed
  'reach-register', 'form-start', 'form-submit',
]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/e')) return new Response(null, { status: 404 });
    const name = url.searchParams.get('n') || '';
    const optedOut = request.headers.get('DNT') === '1' || request.headers.get('Sec-GPC') === '1';
    if (ALLOW.has(name) && !optedOut) {
      const day = new Date().toISOString().slice(0, 10); // UTC day buckets
      const key = `${name}:${day}`;
      const current = parseInt((await env.EVENTS.get(key)) || '0', 10);
      // keep ~13 months, then buckets age out on their own
      await env.EVENTS.put(key, String(current + 1), { expirationTtl: 60 * 60 * 24 * 400 });
    }
    // Always 204, even for unknown names or opted-out visitors — the beacon is fire-and-forget
    // and the response must never invite retries or leak which names count.
    return new Response(null, { status: 204, headers: { 'cache-control': 'no-store' } });
  },
};
