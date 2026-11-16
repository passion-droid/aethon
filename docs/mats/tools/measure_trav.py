import io, json, warnings, colorsys
warnings.filterwarnings('ignore')
from PIL import Image, ImageCms, ImageDraw
PATH = '/root/.claude/uploads/11291d80-3cfa-55af-b5f0-c668ea659755/9529e02d-image.jpg'
cols = [(530,760),(835,1065),(1140,1380)]
rows = [(445,590),(660,810),(880,1025),(1095,1245),(1320,1475)]
names = [['CIEL 5','LIGHT BLUE 10','DARK BLUE 15'],['LIGHT GREY 4','LIGHT GREEN 9','DARK GREEN 14'],['GOLD 3','YELLOW 8','DARK GREY 13'],['BEIGE 2','ORANGE 7','BROWN 12'],['WHITE 1','RED 6','BORDEAUX 11']]
B = {names[r][c]:(cols[c][0],rows[r][0],cols[c][1],rows[r][1]) for r in range(5) for c in range(3)}
B['BLACK 16'] = (1435,520,1495,1380)
B['_paper'] = (745,1575,1015,1870)
B['_trav A (links unten)'] = (60,1000,270,1450)
B['_trav B (mitte)'] = (350,950,460,1450)
B['_trav C (rechts unten)'] = (1120,1575,1450,1810)
B['_trav D (oben)'] = (430,80,950,320)
B['_trav E (links oben)'] = (60,100,280,600)
im = Image.open(PATH); icc = im.info.get('icc_profile')
src = ImageCms.ImageCmsProfile(io.BytesIO(icc)); print('ICC', ImageCms.getProfileDescription(src).strip(), im.size)
im = ImageCms.profileToProfile(im.convert('RGB'), src, ImageCms.createProfile('sRGB'), outputMode='RGB'); s = im.size[0]/1500
LIN = [(c/255/12.92 if c/255<=0.04045 else ((c/255+0.055)/1.055)**2.4) for c in range(256)]
def enc(l):
    l=max(0.0,min(1.0,l)); v=l*12.92 if l<=0.0031308 else 1.055*l**(1/2.4)-0.055; return int(round(v*255))
def stats(box):
    x0,y0,x1,y1=[int(v*s) for v in box]; px=list(im.crop((x0,y0,x1,y1)).getdata()); px=px[::max(1,len(px)//40000)]
    n=len(px); clip=sum(1 for p in px if max(p)>=252)/n
    lin=[(LIN[r],LIN[g],LIN[b]) for r,g,b in px]
    mean=tuple(sum(t[i] for t in lin)/n for i in range(3)); med=tuple(sorted(t[i] for t in lin)[n//2] for i in range(3))
    return mean, med, clip
hexof=lambda t:'#%02x%02x%02x'%tuple(enc(v) for v in t)
Y=lambda t:0.2126*t[0]+0.7152*t[1]+0.0722*t[2]
def hsl(t):
    r,g,b=[enc(v)/255 for v in t]; h,l,sat=colorsys.rgb_to_hls(r,g,b); return round(h*360),round(sat*100),round(l*100)
pm,pmed,pclip = stats(B['_paper'])
print('paper raw mean', hexof(pm), 'median', hexof(pmed), 'clipped share', round(pclip,3))
gain=tuple(0.88/p for p in pmed); print('gains', [round(g,2) for g in gain])
out={}
for n,b in B.items():
    mean,med,clip=stats(b); m=tuple(mean[i]*gain[i] for i in range(3))
    out[n]=dict(mean=hexof(m),Y=round(Y(m),3),hsl=hsl(m),raw=hexof(mean))
    print(f'{n:24s} raw {hexof(mean)}  WB {hexof(m)}  Y={Y(m):.3f}  hsl{hsl(m)}  clip {clip:.2f}')
json.dump(out,open('measured-trav.json','w'),indent=1)
ov=im.copy(); d=ImageDraw.Draw(ov)
for n,(x0,y0,x1,y1) in B.items(): d.rectangle([x0*s,y0*s,x1*s,y1*s],outline=(255,0,255),width=5)
ov.resize((900,1200)).save('overview-trav.png')
