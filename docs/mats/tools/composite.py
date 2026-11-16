import io, re, os, json, warnings
warnings.filterwarnings('ignore')
from PIL import Image, ImageCms, ImageOps
import sys; sys.path.insert(0,'.')
import boxes as BX
TRAVP = '/root/.claude/uploads/11291d80-3cfa-55af-b5f0-c668ea659755/9529e02d-image.jpg'
LIN = [(c/255/12.92 if c/255<=0.04045 else ((c/255+0.055)/1.055)**2.4) for c in range(256)]
def enc(l):
    l=max(0.0,min(1.0,l)); v=l*12.92 if l<=0.0031308 else 1.055*l**(1/2.4)-0.055; return int(round(v*255))
def load(path):
    im=Image.open(path); src=ImageCms.ImageCmsProfile(io.BytesIO(im.info['icc_profile']))
    return ImageCms.profileToProfile(im.convert('RGB'), src, ImageCms.createProfile('sRGB'), outputMode='RGB')
def med_lin(im, box, s):
    px=list(im.crop(tuple(int(v*s) for v in box)).getdata()); px=px[::max(1,len(px)//40000)]; n=len(px)
    return tuple(sorted(LIN[p[i]] for p in px)[n//2] for i in range(3))
def mean_lin(im, box, s):
    px=list(im.crop(tuple(int(v*s) for v in box)).getdata()); px=px[::max(1,len(px)//40000)]; n=len(px)
    return tuple(sum(LIN[p[i]] for p in px)/n for i in range(3))
def wb(im, gain):
    luts=[]
    for g in gain: luts += [enc(LIN[c]*g) for c in range(256)]
    return im.point(luts)
def supertile(t):   # 2x2 mirrored -> seamless when repeated
    w,h=t.size; o=Image.new('RGB',(2*w,2*h)); o.paste(t,(0,0)); o.paste(ImageOps.mirror(t),(w,0)); o.paste(ImageOps.flip(t),(0,h)); o.paste(ImageOps.flip(ImageOps.mirror(t)),(w,h)); return o
hexof=lambda t:'#%02x%02x%02x'%tuple(enc(v) for v in t)
Y=lambda t:0.2126*t[0]+0.7152*t[1]+0.0722*t[2]
cr=lambda a,b:(max(Y(a),Y(b))+0.05)/(min(Y(a),Y(b))+0.05)

# --- travertine photo
cols=[(530,760),(835,1065),(1140,1380)]; rows=[(445,590),(660,810),(880,1025),(1095,1245),(1320,1475)]
names=[['CIEL 5','LIGHT BLUE 10','DARK BLUE 15'],['LIGHT GREY 4','LIGHT GREEN 9','DARK GREEN 14'],['GOLD 3','YELLOW 8','DARK GREY 13'],['BEIGE 2','ORANGE 7','BROWN 12'],['WHITE 1','RED 6','BORDEAUX 11']]
TB={names[r][c]:(cols[c][0],rows[r][0],cols[c][1],rows[r][1]) for r in range(5) for c in range(3)}
TB['BLACK 16']=(1435,520,1495,1380)
T=load(TRAVP); s=T.size[0]/1500
gT=tuple(0.88/p for p in med_lin(T,(745,1575,1015,1870),s)); Tw=wb(T,gT)
stoneT_box=(40,930,300,1500)       # clean left slab
supertile(Tw.crop(tuple(int(v*s) for v in stoneT_box))).save('tile-trav.png')
# --- marble photo
Mi=load(BX.PRADO); gM=tuple(0.88/p for p in med_lin(Mi,BX.PRADO_BOXES['_paper'],s)); Mw=wb(Mi,gM)
stoneM_box=(700,1470,1160,1800)
supertile(Mw.crop(tuple(int(v*s) for v in stoneM_box))).save('tile-marble.png')
info={'trav':{}, 'marble':{}}
for tag,im,bx,stone in (('trav',Tw,TB,stoneT_box),('marble',Mw,BX.PRADO_BOXES,stoneM_box)):
    st=mean_lin(im,stone,s); info[tag]['_stone']=dict(hex=hexof(st),lin=st)
    for n in ('LIGHT GREY 4','BEIGE 2','WHITE 1','DARK GREY 13','DARK GREEN 14','BLACK 16','GOLD 3'):
        b=bx[n]; inset=(b[0]+8,b[1]+8,b[2]-8,b[3]-8)
        if n not in ('DARK GREEN 14','BLACK 16'):
            supertile(im.crop(tuple(int(v*s) for v in inset))).save(f'patch-{tag}-{n.replace(" ","_")}.png')
        m=mean_lin(im,b,s); info[tag][n]=dict(hex=hexof(m),lin=m)
    print(tag,'stone',info[tag]['_stone']['hex'], {k:v['hex'] for k,v in info[tag].items() if k!='_stone'})
    for b in ('LIGHT GREY 4','BEIGE 2','WHITE 1','DARK GREY 13','GOLD 3'):
        print(f"  {b:13s} vs stone {cr(info[tag][b]['lin'],st):.2f} | DG14 {cr(info[tag]['DARK GREEN 14']['lin'],info[tag][b]['lin']):.2f}  Black {cr(info[tag]['BLACK 16']['lin'],info[tag][b]['lin']):.2f}")
json.dump({t:{k:v['hex'] for k,v in d.items()} for t,d in info.items()}, open('composite-info.json','w'), indent=1)
json.dump({t:{k:list(v['lin']) for k,v in d.items()} for t,d in info.items()}, open('composite-lin.json','w'))
