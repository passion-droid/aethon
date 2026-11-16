import sys, io, json, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,'.')
from boxes import *
from PIL import Image, ImageCms, ImageDraw

def to_srgb(path):
    im = Image.open(path)
    icc = im.info.get('icc_profile')
    name = None
    if icc:
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc)); name = ImageCms.getProfileDescription(src).strip()
        im = ImageCms.profileToProfile(im.convert('RGB'), src, ImageCms.createProfile('sRGB'), outputMode='RGB')
    return im.convert('RGB'), name

LIN = [ (c/255/12.92 if c/255<=0.04045 else ((c/255+0.055)/1.055)**2.4) for c in range(256) ]
def enc(l):
    l = max(0.0,min(1.0,l)); s = l*12.92 if l<=0.0031308 else 1.055*l**(1/2.4)-0.055
    return int(round(s*255))
def stats(im, box, s):
    x0,y0,x1,y1 = [int(v*s) for v in box]
    px = list(im.crop((x0,y0,x1,y1)).getdata())
    step = max(1, len(px)//40000); px = px[::step]
    lin = [(LIN[r],LIN[g],LIN[b]) for r,g,b in px]
    Y = lambda t: 0.2126*t[0]+0.7152*t[1]+0.0722*t[2]
    lin.sort(key=Y); n=len(lin)
    mean = tuple(sum(t[i] for t in lin)/n for i in range(3))
    med  = tuple(sorted(t[i] for t in lin)[n//2] for i in range(3))
    hi   = lin[int(n*0.70):int(n*0.90)]; hi = tuple(sum(t[i] for t in hi)/len(hi) for i in range(3))
    return mean, med, hi
def hexof(t): return '#%02x%02x%02x' % tuple(enc(v) for v in t)
def Y(t): return 0.2126*t[0]+0.7152*t[1]+0.0722*t[2]
def cr(a,b):
    hi,lo = max(a,b),min(a,b); return (hi+0.05)/(lo+0.05)
import colorsys
def hsl(t):
    r,g,b = [enc(v)/255 for v in t]; h,l,s = colorsys.rgb_to_hls(r,g,b); return round(h*360), round(s*100), round(l*100)

PAPER_R = 0.88   # assumed reflectance of office paper
out = {}
for tag,path,boxes in (('prado',PRADO,PRADO_BOXES),('vinyl',VINYL,VINYL_BOXES)):
    im, prof = to_srgb(path); s = im.size[0]/1500
    pm, pmed, _ = stats(im, boxes['_paper'], s)
    gain = tuple(PAPER_R/p for p in pmed)
    print(f'\n=== {tag}  (ICC: {prof})  paper median raw {hexof(pmed)}  gains R{gain[0]:.2f} G{gain[1]:.2f} B{gain[2]:.2f}')
    res = {}
    for n,b in boxes.items():
        mean,med,hi = stats(im,b,s)
        wb = lambda t: tuple(t[i]*gain[i] for i in range(3))
        m,md,h = wb(mean), wb(med), wb(hi)
        res[n] = dict(mean=hexof(m), median=hexof(md), hi=hexof(h), Y=round(Y(m),3), hsl=hsl(m), raw=hexof(mean))
        print(f'{n:18s} raw {hexof(mean)}  WB mean {hexof(m)}  median {hexof(md)}  hi {hexof(h)}  Y={Y(m):.3f}  hsl{hsl(m)}')
    out[tag] = res
    # contact sheet of crops for visual verification
    tiles = [(n, im.crop(tuple(int(v*s) for v in b)).resize((220,160))) for n,b in boxes.items()]
    sheet = Image.new('RGB',(4*230+10, ((len(tiles)+3)//4)*190+10),'white'); d = ImageDraw.Draw(sheet)
    for i,(n,t) in enumerate(tiles):
        x,y = 10+(i%4)*230, 10+(i//4)*190; sheet.paste(t,(x,y)); d.text((x+2,y+162), n, fill='black')
    sheet.save(f'crops-{tag}.png')
json.dump(out, open('measured.json','w'), indent=1)
