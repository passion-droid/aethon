#!/usr/bin/env python3
"""Generate AETHON stone-signage fabrication blueprints + a working QR (centre 'A').

Outputs (self-contained SVG, dimensions in mm):
  aethon-qr.svg                     — the working QR (error-H), brand 'A' inset, verified scannable
  aethon-signage-sheet-1-entrance.svg
  aethon-signage-sheet-2-monolith.svg
A PIL twin of the QR is rendered + decoded with OpenCV to PROVE it scans.
Brand assets used verbatim: brand/logo-dark.svg (wordmark), icon-512.png ('A').
NO address anywhere (brand guardrail).
"""
import base64, re, segno, numpy as np, cv2
from PIL import Image, ImageDraw

URL = "https://aethon.house/"
ROOT = "."
OUT  = "docs/signage"

# ---- palette (MONOCHROME print set — owner request 2026-07: B&W for printing) ----
PAPER="#FFFFFF"; TRAV="#F2F2F2"; SAND="#EBEBEB"; INK="#000000"; OLIVE="#3A3A3A"
GOLD="#8C8C8C"; MUTE="#707070"; RULE="#000000"; ENAMEL="#333333"; WATER="#FFFFFF"

# ---- brand 'A' icon as base64 (for the QR centre) — greyscaled for the monochrome set ----
import io as _io
_a = Image.open(f"{ROOT}/icon-512.png").convert("L").convert("RGB")
_buf = _io.BytesIO(); _a.save(_buf, format="PNG")
A_B64 = "data:image/png;base64," + base64.b64encode(_buf.getvalue()).decode()

# ---- wordmark: inline paths with explicit fills (drop the <style> classes) ----
raw = open(f"{ROOT}/brand/logo-dark.svg").read()
inner = re.search(r'<g id="Layer_1-2".*?>(.*)</g>\s*</svg>', raw, re.S).group(1)
inner = inner.replace('class="cls-2"', f'fill="{INK}"').replace('class="cls-1"', f'fill="{GOLD}"')
WORD_W, WORD_H = 366.78, 85.09     # wordmark native viewBox

def wordmark(x, y, w, fill=None, dot=GOLD):
    """Place the AETHON wordmark, target width w, top-left (x,y). Optional mono fill override."""
    s = w / WORD_W
    g = inner
    if fill:  # override the letter fill (e.g. show as 'cut' tone), keep dot
        g = re.sub(r'fill="#222216"', f'fill="{fill}"', g)
        g = re.sub(r'fill="#c1a152"', f'fill="{dot}"', g, flags=re.I)
    return f'<g transform="translate({x},{y}) scale({s:.5f})">{g}</g>', w, WORD_H*s

# ============================ QR ============================
def qr_matrix(url):
    qr = segno.make(url, error='h')
    return [[1 if c else 0 for c in row] for row in qr.matrix]

MAT = qr_matrix(URL); N = len(MAT)
LOGO_FRAC = 0.20   # centre logo side as fraction of code (tune to keep it scannable)

def verify_scan():
    """Render a PIL twin (modules + centre A) and decode with OpenCV -> must equal URL."""
    global LOGO_FRAC
    for frac in (0.20, 0.18, 0.16, 0.14):
        px = 12; quiet = 4
        side = (N + 2*quiet) * px
        img = Image.new("RGB", (side, side), "white")
        d = ImageDraw.Draw(img)
        for r in range(N):
            for c in range(N):
                if MAT[r][c]:
                    x0=(c+quiet)*px; y0=(r+quiet)*px
                    d.rectangle([x0,y0,x0+px-1,y0+px-1], fill="black")
        # centre logo (white gap + the olive 'A' tile)
        lside = int(N*frac)*px
        cx=side//2; gap=int(lside*0.16)
        d.rectangle([cx-lside//2-gap, cx-lside//2-gap, cx+lside//2+gap, cx+lside//2+gap], fill="white")
        a = Image.open(f"{ROOT}/icon-512.png").convert("L").convert("RGB").resize((lside,lside))
        img.paste(a, (cx-lside//2, cx-lside//2))
        arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        data,_,_ = cv2.QRCodeDetector().detectAndDecode(arr)
        if data == URL:
            LOGO_FRAC = frac
            img.save(f"{OUT}/aethon-qr-check.png")
            return True, frac
    return False, None

def qr_svg_modules(x, y, size, dark=INK, light="#FFFFFF", logo=True, quiet=4):
    """Return (svg, totalsize) for a QR at (x,y); 'size' = the CODE side (excl quiet zone)."""
    unit = size / N
    total = size + 2*quiet*unit
    s = [f'<rect x="{x}" y="{y}" width="{total:.2f}" height="{total:.2f}" fill="{light}"/>']
    ox = x + quiet*unit; oy = y + quiet*unit
    # group modules into row-runs for fewer rects
    for r in range(N):
        c = 0
        while c < N:
            if MAT[r][c]:
                c0 = c
                while c < N and MAT[r][c]: c += 1
                s.append(f'<rect x="{ox+c0*unit:.2f}" y="{oy+r*unit:.2f}" width="{(c-c0)*unit:.2f}" height="{unit:.2f}" fill="{dark}"/>')
            else:
                c += 1
    if logo:
        lside = int(N*LOGO_FRAC)*unit; gap = lside*0.16
        cx = x + total/2; cy = y + total/2
        s.append(f'<rect x="{cx-lside/2-gap:.2f}" y="{cy-lside/2-gap:.2f}" width="{lside+2*gap:.2f}" height="{lside+2*gap:.2f}" rx="{gap:.2f}" fill="{light}"/>')
        s.append(f'<image x="{cx-lside/2:.2f}" y="{cy-lside/2:.2f}" width="{lside:.2f}" height="{lside:.2f}" href="{A_B64}"/>')
    return "".join(s), total

# ============================ drawing helpers ============================
def line(x1,y1,x2,y2,stroke=RULE,w=1,dash=None,opacity=1):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{stroke}" stroke-width="{w}"{da} stroke-opacity="{opacity}"/>'
def rect(x,y,w,h,fill="none",stroke=RULE,sw=1,rx=0,opacity=1):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>'
def _esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def txt(x,y,s,size=13,fill=INK,anchor="start",weight="400",ff="Helvetica, Arial, sans-serif",ls="0",style=""):
    return f'<text x="{x:.2f}" y="{y:.2f}" font-family="{ff}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" {style}>{_esc(s)}</text>'
def keynote(x,y,n):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{PAPER}" stroke="{OLIVE}" stroke-width="1.3"/>'+txt(x,y+4,str(n),12,OLIVE,"middle",weight="700")
def keylegend(x,y,items):
    s=txt(x,y,"KEYNOTES",11,OLIVE,weight="700",ls="1.6"); y+=22
    for n,t,d in items:
        s+=f'<circle cx="{x+9:.1f}" cy="{y-4:.1f}" r="9" fill="none" stroke="{OLIVE}" stroke-width="1.2"/>'+txt(x+9,y,str(n),11,OLIVE,"middle",weight="700")
        s+=txt(x+28,y,t,11.5,INK,weight="600",ls="0.2")
        if d: s+=txt(x+28,y+13,d,11,MUTE,ls="0.1"); y+=30
        else: y+=22
    return s
def dim_h(x1,x2,y,label,ext_to=None,side="above"):
    s=""
    if ext_to is not None:
        s+=line(x1,ext_to,x1,y,OLIVE,0.8)+line(x2,ext_to,x2,y,OLIVE,0.8)
    s+=f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{OLIVE}" stroke-width="0.9" marker-start="url(#ar)" marker-end="url(#ar)"/>'
    ty = y-6 if side=="above" else y+15
    s+=txt((x1+x2)/2, ty, label, 12.5, OLIVE, "middle", ls="0.3")
    return s
def dim_v(y1,y2,x,label,ext_to=None,side="left"):
    s=""
    if ext_to is not None:
        s+=line(ext_to,y1,x,y1,OLIVE,0.8)+line(ext_to,y2,x,y2,OLIVE,0.8)
    s+=f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{OLIVE}" stroke-width="0.9" marker-start="url(#ar)" marker-end="url(#ar)"/>'
    tx = x-8 if side=="left" else x+8
    an = "end" if side=="left" else "start"
    s+=f'<text x="{tx:.2f}" y="{(y1+y2)/2:.2f}" font-family="Helvetica, Arial, sans-serif" font-size="12.5" fill="{OLIVE}" text-anchor="{an}" letter-spacing="0.3" transform="rotate(-90 {tx:.2f} {(y1+y2)/2:.2f})">{label}</text>'
    return s
def leader(x,y, tx,ty, label, sub=None, anchor="start"):
    s=line(x,y,tx,ty,OLIVE,0.9)+f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.2" fill="{OLIVE}"/>'
    s+=txt(tx + (4 if anchor=="start" else -4), ty-2, label, 12.5, INK, anchor, weight="600", ls="0.2")
    if sub:
        for i,ln in enumerate(sub):
            s+=txt(tx + (4 if anchor=="start" else -4), ty+12+i*13, ln, 11.5, MUTE, anchor, ls="0.1")
    return s

DEFS=f'''<defs>
  <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,1 L9,5 L0,9 z" fill="{OLIVE}"/></marker>
  <pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="0.7" stroke-opacity="0.55"/></pattern>
  <pattern id="hatchS" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <line x1="0" y1="0" x2="0" y2="6" stroke="{INK}" stroke-width="0.7" stroke-opacity="0.4"/></pattern>
</defs>'''

def titleblock(x,y,w, sheet, title, legend, h=152):
    dx=x+w*0.58
    s=rect(x,y,w,h,"none",RULE,1.2)+line(x,y+28,x+w,y+28,RULE,1)+line(dx,y+28,dx,y+h,RULE,1)
    s+=txt(x+13,y+19,"AETHON · HOUSE OF LIGHT",13,INK,weight="700",ls="1.8")
    s+=txt(x+w-12,y+19,"PAPHOS, CYPRUS",10,MUTE,"end",ls="1.4")
    s+=txt(x+13,y+48,title,13.5,INK,weight="700",ls="0.3")
    s+=txt(x+13,y+65,sheet,10,OLIVE,ls="0.3")
    ly=y+86
    s+=txt(x+13,ly,"MATERIALS / FINISH",9.5,MUTE,weight="700",ls="1.4"); ly+=14
    for col,lab in legend:
        s+=rect(x+13,ly-8,14,10,col,RULE,0.7)+txt(x+33,ly,lab,10,INK,ls="0.1"); ly+=13.5
    rx=dx+13
    s+=txt(rx,y+48,"SCALE — DO NOT SCALE",10,INK,weight="700",ls="0.3")
    s+=txt(rx,y+61,"figured dims (mm) govern",9.5,MUTE)
    s+=txt(rx,y+82,"STATUS — design study",10,INK,weight="700",ls="0.3")
    s+=txt(rx,y+95,"for fabrication · verify on site",9.5,MUTE)
    s+=txt(rx,y+118,"DATE 2026-07",10,INK,weight="600")
    s+=txt(rx,y+131,"REV B · monochrome print set · not for structural use",9.5,MUTE)
    return s

def note_block(x,y,title,lines):
    s=txt(x,y,title,11,OLIVE,weight="700",ls="1.6"); y+=18
    for ln in lines:
        bullet = "—" if ln else ""
        s+=txt(x,y,f"{bullet}  {ln}" if ln else "", 11.5, INK, ls="0.1"); y+=15.5
    return s

def svg_doc(vb_w, vb_h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w} {vb_h}" '
            f'width="{vb_w}" height="{vb_h}" font-family="Helvetica, Arial, sans-serif">'
            f'{DEFS}<rect width="{vb_w}" height="{vb_h}" fill="{PAPER}"/>{body}</svg>')

ok = verify_scan()
print("QR verify:", ok, "modules:", N)

# ======================= STANDALONE QR =======================
def build_qr_standalone():
    M=70; code=560
    qs,total=qr_svg_modules(M, M, code, dark=INK, light="#FFFFFF", logo=True)
    S = total + 2*M
    body  = rect(0,0,S,S+90,"#FFFFFF","none",0)
    body += rect(M-10,M-10,total+20,total+20,"none",MUTE,0.8)
    body += qs
    body += txt(S/2, S+34, "AETHON", 26, INK, "middle", weight="700", ls="6")
    body += txt(S/2, S+62, "aethon.house  ·  scan to view", 15, MUTE, "middle", ls="1.5")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S+90}" width="{S}" height="{S+90}">'
            f'{DEFS}{body}</svg>')

# ======================= SHEET 1 — ENTRANCE =======================
def build_sheet1():
    W,H=1320,980; b=[]
    b.append(rect(22,22,W-44,H-44,"none",RULE,1.4)); b.append(rect(28,28,W-56,H-56,"none",MUTE,0.6))
    b.append(txt(54,66,"ENTRANCE THRESHOLD MARKER",25,INK,weight="700",ls="0.8"))
    b.append(txt(54,90,"Honed marble tile 600 × 400 × 20 · carved wordmark · gilded dot · inset QR",12.5,MUTE,ls="0.3"))
    b.append(line(54,104,W-54,104,RULE,0.8))

    # ---- 1 · FRONT ELEVATION (1:1) ----
    px,py,pw,ph=120,200,600,400
    b.append(txt(px,py-16,"1 — FRONT ELEVATION   (1:1)",12,OLIVE,weight="700",ls="1"))
    b.append(rect(px,py,pw,ph,TRAV,RULE,1.5))
    cs=26
    b.append(f'<rect x="{px+cs}" y="{py+cs}" width="{pw-2*cs}" height="{ph-2*cs}" fill="none" stroke="{OLIVE}" stroke-width="0.7" stroke-dasharray="4 4"/>')
    ww=420; wx=px+(pw-ww)/2; wy=py+50
    g,gw,gh=wordmark(wx,wy,ww); b.append(g)
    uy=wy+gh+44
    b.append(txt(px+pw/2,uy,"aethon.house",24,INK,"middle",weight="500",ff="Georgia,'Times New Roman',serif",ls="1"))
    tile=132; tx=px+(pw-tile)/2; ty=py+ph-32-tile
    b.append(rect(tx,ty,tile,tile,"#FFFFFF",ENAMEL,1.2))
    qs,_=qr_svg_modules(tx,ty,tile*N/(N+8),dark=INK,light="#FFFFFF",logo=True); b.append(qs)
    # dims
    b.append(dim_h(px,px+pw,py+ph+46,"600",ext_to=py+ph))
    b.append(dim_v(py,py+ph,px-46,"400",ext_to=px))
    b.append(dim_h(tx,tx+tile,ty-12,"132",ext_to=ty))
    # keynote bubbles on the drawing (legend lower-right)
    dotx=wx+ww*0.749; doty=wy+gh*0.076
    b.append(line(dotx,doty,dotx,py+12,GOLD,0.9)); b.append(keynote(dotx,py+4,2))
    b.append(keynote(wx-4,wy+gh*0.55,1))
    b.append(keynote(px+pw/2+120,uy-6,3))
    b.append(keynote(tx+tile+16,ty+tile/2,4))
    b.append(keynote(px+18,py+ph-18,5))
    b.append(keynote(px+pw-cs-8,py+cs+12,6))

    # ---- 2 · SECTIONS (2:1) ----
    sx=740; sy=190
    b.append(txt(sx,sy-16,"2 — SECTIONS   (2:1)",12,OLIVE,weight="700",ls="1"))
    ax,ay,aw,ah=sx,sy,250,84
    b.append(rect(ax,ay,aw,ah,TRAV,RULE,1.3)); b.append(f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="url(#hatch)"/>')
    b.append(line(ax,ay,ax+aw,ay,INK,1.6))
    vcx=ax+84; vw=26; vd=24
    b.append(f'<path d="M{vcx-vw/2},{ay} L{vcx},{ay+vd} L{vcx+vw/2},{ay} Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.3"/>')
    dcx=ax+166; dw=30
    b.append(f'<path d="M{dcx-dw/2},{ay} Q{dcx},{ay+24} {dcx+dw/2},{ay} Z" fill="{GOLD}" stroke="{INK}" stroke-width="1.1"/>')
    b.append(dim_v(ay,ay+vd,ax-12,"6",ext_to=vcx-vw/2,side="left"))
    b.append(dim_v(ay,ay+ah,ax+aw+14,"20",ext_to=ax+aw,side="right"))
    b.append(txt(ax,ay+ah+20,"(a) V-cut 60° · 6 deep · bare; gilded dot = cup + leaf",10.6,INK,ls="0.05"))
    bx,byy,bw,bh=sx+292,sy,250,84
    b.append(rect(bx,byy,bw,bh,TRAV,RULE,1.3)); b.append(f'<rect x="{bx}" y="{byy}" width="{bw}" height="{bh}" fill="url(#hatch)"/>')
    pw2=150; pd=20; pcx=bx+bw/2
    b.append(rect(pcx-pw2/2,byy,pw2,pd,PAPER,INK,1.2)); b.append(rect(pcx-pw2/2,byy,pw2,7,ENAMEL,INK,1.0))
    b.append(line(bx,byy,bx+bw,byy,INK,1.6))
    b.append(dim_v(byy,byy+pd,bx-12,"~6",ext_to=pcx-pw2/2,side="left"))
    b.append(txt(bx,byy+bh+20,"(b) QR plate flush in routed pocket · sealed · swappable",10.6,INK,ls="0.05"))

    # ---- 3 · QR SPECIFICATION ----
    qy=382
    b.append(txt(sx,qy-2,"3 — QR SPECIFICATION",12,OLIVE,weight="700",ls="1"))
    qsz=148; b.append(rect(sx,qy+12,qsz,qsz,"#FFFFFF",ENAMEL,1))
    qq,_=qr_svg_modules(sx,qy+12,qsz*N/(N+8),dark=INK,light="#FFFFFF",logo=True); b.append(qq)
    specs=[("Links to","aethon.house · verified scannable"),
           ("Error corr.","Level H (30%) — survives weather / grime"),
           ("Centre","AETHON 'A' · ≤ 20% of area"),
           ("Code / tile","≥ 90 code · 132 tile · quiet zone ≥ 4 modules"),
           ("Finish","matte, dark-on-pale, anti-glare — never gloss"),
           ("Execution","porcelain-enamel OR etched 316 stainless, flush")]
    ly=qy+30
    for k,v in specs:
        b.append(txt(sx+qsz+22,ly,k,11,OLIVE,weight="700",ls="0.3"))
        b.append(txt(sx+qsz+126,ly,v,10.6,INK,ls="0.05")); ly+=22.5

    # ---- keynotes legend (right column, below spec) ----
    b.append(keylegend(sx, qy+qsz+40, [
        (1,"Carved wordmark","LT Museum (brand vector) · V-cut · bare letters"),
        (2,"Gild this dot only","23.5ct gold leaf — the single gold accent"),
        (3,"Engraved URL","'aethon.house' — permanent (a link never ages)"),
        (4,"Inset QR plate","see panel 3 · matte · replaceable"),
        (5,"Honed marble tile","600 × 400 × 20 · matte · sealed · shelter from spray"),
        (6,"Clear space","≥ 2X around the lock-up (1X = gold-dot diameter)")]))

    # ---- general notes (lower-left) ----
    b.append(note_block(120,688,"GENERAL NOTES",[
        "Lettering hand-carved V-incision preferred (CNC acceptable); letters left bare.",
        "Lighting: warm 2700–3000K grazing from one side; a tight glint on the dot. Never cool / blue.",
        "Fixing: full-bed adhesive + concealed 316 pins sized to the 20 thick tile; verify substrate.",
        "Setting-out: wordmark centre-line approx. 1400–1500 AFL; QR centre approx. 1200–1300 AFL.",
        "Sign-off: cut a stone sample (two letters + gilded dot) and scan-test the QR in sun and dusk."]))

    b.append(titleblock(740,H-180,540,"Sheet 1 of 2  ·  ENTRANCE THRESHOLD MARKER",
        "AETHON · ENTRANCE PLATE",
        [(TRAV,"Honed marble — tile 600 × 400 × 20"),(GOLD,"23.5ct gold leaf — dot only"),
         (ENAMEL,"Enamel / etched 316 stainless — QR tile"),(INK,"V-cut incision — bare letters")]))
    return svg_doc(W,H,"".join(b))

# ======================= SHEET 2 — MONOLITH =======================
def build_sheet2():
    W,H=1320,980; b=[]
    b.append(rect(22,22,W-44,H-44,"none",RULE,1.4)); b.append(rect(28,28,W-56,H-56,"none",MUTE,0.6))
    b.append(txt(54,66,"SEASIDE PROMENADE MONOLITH",25,INK,weight="700",ls="0.8"))
    b.append(txt(54,90,"Coastal sandstone standing stone · deep-cut wordmark · bare (no infill) · engraved URL · inset QR",12.5,MUTE,ls="0.3"))
    b.append(line(54,104,W-54,104,RULE,0.8))

    # ---- 1 · FRONT ELEVATION (1:10) ----
    s=0.46                       # units per mm (≈1:10 shown larger)
    gx=300; grdY=760             # ground line x-centre / y
    mw=600*s; mh=1100*s; emb=300*s
    mx=gx-mw/2; my=grdY-mh
    b.append(txt(mx,my-16,"1 — FRONT ELEVATION   (indicative 1:10)",12,OLIVE,weight="700",ls="1"))
    # rough monolith body (slightly irregular)
    b.append(f'<path d="M{mx+6},{my+14} L{mx+mw*0.46},{my} L{mx+mw-4},{my+20} L{mx+mw},{grdY} L{mx},{grdY} Z" fill="{SAND}" stroke="{RULE}" stroke-width="1.5"/>')
    # dressed inscription panel
    panW=mw*0.78; panH=mh*0.42; panx=gx-panW/2; pany=my+mh*0.20
    b.append(rect(panx,pany,panW,panH,"#F7F7F7",RULE,1))
    gw_=panW*0.86; gx0=gx-gw_/2; gy0=pany+panH*0.12
    gmark,gww,ghh=wordmark(gx0,gy0,gw_,fill=INK,dot=INK)   # mono: bare deep-cut, dot bare too on the monolith
    b.append(gmark)
    # engraved URL beneath the wordmark (a link never ages)
    uy2=gy0+ghh+26
    b.append(txt(gx,uy2,"aethon.house",15,INK,"middle",weight="500",ff="Georgia,'Times New Roman',serif",ls="0.8"))
    # inset QR plate (matte enamel / etched 316, flush) — spec as Sheet 1, panel 3
    qtile=132*s; qtx=gx-qtile/2; qty=pany+panH-16-qtile
    b.append(rect(qtx,qty,qtile,qtile,"#FFFFFF",ENAMEL,1.1))
    qmods,_=qr_svg_modules(qtx,qty,qtile*N/(N+8),dark=INK,light="#FFFFFF",logo=True)
    b.append(qmods)
    b.append(dim_h(qtx,qtx+qtile,qty-8,"132",ext_to=qty))
    # ground + foundation
    b.append(line(mx-90,grdY,gx+mw,grdY,INK,1.8))
    for i in range(int((mw+180)//12)):
        xx=mx-90+i*12; b.append(line(xx,grdY,xx-9,grdY+9,INK,0.7,opacity=0.5))
    b.append(rect(mx-18,grdY,mw+36,emb,"#E0E0E0",RULE,1.1))      # footing
    b.append(f'<rect x="{mx-18}" y="{grdY}" width="{mw+36}" height="{emb}" fill="url(#hatchS)"/>')
    b.append(txt(gx,grdY+emb+18,"concrete footing — size/depth by engineer",10.5,MUTE,"middle"))
    # uplight
    lx=mx-46
    b.append(f'<path d="M{lx},{grdY} L{lx-26},{my+mh*0.30} L{lx+34},{my+mh*0.30} Z" fill="{GOLD}" fill-opacity="0.18"/>')
    b.append(rect(lx-9,grdY-6,18,9,INK,INK,1))
    b.append(txt(lx-14,grdY+24,"warm in-ground uplight",10.5,MUTE,"start"))
    # dims
    b.append(dim_v(my,grdY,mx-70,"1100",ext_to=mx))
    b.append(dim_v(grdY,grdY+emb,mx-70,"300",ext_to=mx-18,side="left"))
    b.append(dim_h(mx,mx+mw,grdY+emb+44,"600",ext_to=grdY+emb))
    b.append(dim_v(gy0,gy0+ghh,gx+mw/2+20,"180",ext_to=gx0+gw_,side="right"))
    b.append(leader(gx,gy0+ghh*0.5,gx+mw/2+150,my+120,"AETHON deep-cut",["cap height 180 · depth 15","bare — reads by shadow only"]))
    b.append(leader(panx+panW,pany+panH*0.5,gx+mw/2+150,my+210,"Dressed inscription panel",["honed face within a","split / rock-face surround"]))
    b.append(leader(mx+mw*0.5,my+30,gx+mw/2+150,my+30,"Natural riven top",["sandstone, left rough"]))
    b.append(leader(gx+22,uy2-5,gx+mw/2+150,my+300,"Engraved URL",["'aethon.house' · V-cut ~35 cap","bare — permanent"]))
    b.append(leader(qtx+qtile,qty+qtile*0.5,gx+mw/2+150,my+382,"Inset QR plate 132",["matte enamel / etched 316, flush","spec + centre 'A': Sheet 1, panel 3"]))

    # ---- 2 · SECTION (2:1) ----
    sx=W-540; sy=200
    b.append(txt(sx,sy-14,"2 — LETTER SECTION   (2:1)",12,OLIVE,weight="700",ls="1"))
    ax,ay,aw,ah=sx,sy,300,150
    b.append(rect(ax,ay,aw,ah,SAND,RULE,1.3))
    b.append(f'<rect x="{ax}" y="{ay}" width="{aw}" height="{ah}" fill="url(#hatchS)"/>')
    b.append(line(ax,ay,ax+aw,ay,INK,1.6))
    vcx=ax+150; vw=44; vd=30
    b.append(f'<path d="M{vcx-vw/2},{ay} L{vcx},{ay+vd} L{vcx+vw/2},{ay} Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>')
    b.append(dim_v(ay,ay+vd,ax-14,"15",ext_to=vcx-vw/2,side="left"))
    b.append(txt(ax,ay+ah+24,"Deep V-incision 60° · 15 deep · NO infill.",11.5,INK,ls="0.2"))
    b.append(txt(ax,ay+ah+40,"Soft stone: cut deep; edges round gracefully with the coast.",11,MUTE,ls="0.2"))

    # ---- notes ----
    b.append(note_block(W-540,430,"GENERAL NOTES",[
        "Material: coastal sandstone (the cliff's own stone). For a forever-crisp inscription,",
        "   a sandstone-toned granite reads near-identical and lasts generations — sample both.",
        "Inscription: deep-cut, bare (shadow only). Sandblast or hand-carve. Accept weathering.",
        "Finish: natural riven top + split surround; dressed honed inscription panel only.",
        "Lighting: a single warm 2700–3000K in-ground uplight at the base. Never cool / blue.",
        "QR: never carved into rough stone — an inset matte plate (enamel / etched 316) sits flush",
        "   in the dressed panel; spec + verification as Sheet 1, panel 3. Scan-test in sun and dusk.",
        "Foundation, drainage & embedment by structural engineer; allow for salt-air durability."]))

    b.append(titleblock(780,H-180,500,"Sheet 2 of 2  ·  SEASIDE PROMENADE MONOLITH",
        "AETHON · PROMENADE MONOLITH",
        [(SAND,"Coastal sandstone (or sandstone-toned granite)"),(INK,"Deep V-cut — bare, no infill"),
         (ENAMEL,"Enamel / etched 316 stainless — QR tile"),
         (GOLD,"Warm in-ground uplight — no gilding outdoors here")]))
    return svg_doc(W,H,"".join(b))

for name,svg in [("aethon-qr.svg",build_qr_standalone()),
                 ("aethon-signage-sheet-1-entrance.svg",build_sheet1()),
                 ("aethon-signage-sheet-2-monolith.svg",build_sheet2())]:
    open(f"{OUT}/{name}","w").write(svg)
    print("wrote", name, len(svg), "bytes")
print("done")

