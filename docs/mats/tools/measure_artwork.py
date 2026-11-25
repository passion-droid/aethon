#!/usr/bin/env python3
"""Measure a supplier's mat drawing against the order: per mat the outer size, the edging, the
logo width as a share of the mat width, and how far the logo sits off centre.

    python3 measure_artwork.py drawing.png [--base fac8aa d8bd8c] [--ref-cm 200]

Finds every large area filled with one of the base colours (the mat fields), walks outward to the
white page for the edging, and takes everything inside the field that is not base colour as the
logo. --ref-cm gives the real width of the WIDEST mat found, which sets the scale for cm output.
First used 2026-11-25: the drawing showed logos at 72-84 % where 50 % was ordered, and one mat
rotated. Needs Pillow only. The drawings themselves are not stored in the repository.
"""
import argparse, sys
from PIL import Image

def near(c, t, tol): return all(abs(a - b) <= tol for a, b in zip(c, t))

def fields(px, W, H, target, tol=14, minarea=4000):
    seen = [[False] * W for _ in range(H)]; out = []
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if seen[y][x] or not near(px[x, y], target, tol): continue
            stack = [(x, y)]; seen[y][x] = True; x0 = x1 = x; y0 = y1 = y; n = 0
            while stack:
                cx, cy = stack.pop(); n += 1
                x0 = min(x0, cx); x1 = max(x1, cx); y0 = min(y0, cy); y1 = max(y1, cy)
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and near(px[nx, ny], target, tol):
                        seen[ny][nx] = True; stack.append((nx, ny))
            if n >= minarea: out.append((x0, y0, x1, y1))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image'); ap.add_argument('--base', nargs='+', default=['fac8aa', 'd8bd8c'])
    ap.add_argument('--ref-cm', type=float, default=None)
    a = ap.parse_args()
    im = Image.open(a.image).convert('RGB'); W, H = im.size; px = im.load()
    rows = []
    for hexc in a.base:
        t = tuple(int(hexc[i:i + 2], 16) for i in (0, 2, 4))
        for x0, y0, x1, y1 in fields(px, W, H, t):
            lx0, ly0, lx1, ly1 = W, H, 0, 0
            for y in range(y0 + 4, y1 - 3):
                for x in range(x0 + 4, x1 - 3):
                    if not near(px[x, y], t, 40):
                        lx0 = min(lx0, x); lx1 = max(lx1, x); ly0 = min(ly0, y); ly1 = max(ly1, y)
            def walk(x, y, dx, dy):
                k = 0
                while 0 <= x < W and 0 <= y < H and not near(px[x, y], (255, 255, 255), 12):
                    x += dx; y += dy; k += 1
                return k
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
            eL, eR = walk(x0 - 1, cy, -1, 0), walk(x1 + 1, cy, 1, 0)
            eT, eB = walk(cx, y0 - 1, 0, -1), walk(cx, y1 + 1, 0, 1)
            edge = '#%02x%02x%02x' % px[x0 - max(1, eL // 2), cy] if eL else 'none'
            rows.append(dict(base=hexc, at=(x0, y0), ow=(x1 - x0 + 1) + eL + eR, oh=(y1 - y0 + 1) + eT + eB,
                             edge_px=(eL, eR, eT, eB), edge=edge, lw=max(0, lx1 - lx0 + 1),
                             dx=(lx0 + lx1) / 2 - (x0 + x1) / 2, dy=(ly0 + ly1) / 2 - (y0 + y1) / 2))
    if not rows: sys.exit('no mat fields found - pass the drawing\'s base colours with --base')
    scale = (max(r['ow'] for r in rows) / a.ref_cm) if a.ref_cm else None
    for r in sorted(rows, key=lambda r: (r['at'][1] // 150, r['at'][0])):
        cm = lambda v: f"{v / scale:6.1f} cm" if scale else f"{v:4d} px"
        off = (f"{r['dx'] / scale:+.1f} / {r['dy'] / scale:+.1f} cm" if scale else f"{r['dx']:+.1f} / {r['dy']:+.1f} px")
        print(f"#{r['base']} at {r['at']}: mat {cm(r['ow'])} x {cm(r['oh'])} (w/h {r['ow'] / r['oh']:.3f}) | "
              f"edging {r['edge']} {max(r['edge_px'])} px | logo {cm(r['lw'])} = {r['lw'] / r['ow'] * 100:.0f} % of mat width | "
              f"logo off centre x/y {off}")

if __name__ == '__main__': main()
