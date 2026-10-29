import warnings;warnings.filterwarnings("ignore")
# Usage : python3 -I logo.py <fichier logo> <dossier images> 
# Produit logo.png (fond transparent, recadré, 600px max), favicon.png (64px) et affiche en JSON la palette (AA vérifié) + arguments prêts pour mod.py.
import sys,json,colorsys,os
from PIL import Image
src,out=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True)
im=Image.open(src).convert('RGBA');W,H=im.size;px=im.load()
def lum(c):
    c=[v/255 for v in c];c=[v/12.92 if v<=.03928 else((v+.055)/1.055)**2.4 for v in c];return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    x,y=sorted([lum(a),lum(b)],reverse=True);return (x+.05)/(y+.05)
hx=lambda c:'#%02x%02x%02x'%tuple(int(round(v)) for v in c)
# fond : transparence existante, sinon fond uni clair retiré, sinon fond uni retiré par distance
al=im.getchannel('A');transp=sum(1 for v in al.getdata() if v<250)/(W*H)>.02
if not transp:
    cs=[px[0,0],px[W-1,0],px[0,H-1],px[W-1,H-1]];bg=tuple(sum(c[i] for c in cs)//4 for i in range(3))
    new=Image.new('RGBA',(W,H))
    for y in range(H):
        for x in range(W):
            r,g,b,_=px[x,y];d=max(abs(r-bg[0]),abs(g-bg[1]),abs(b-bg[2]))
            a=0 if d<14 else min(255,int((d-14)*255/60))
            new.putpixel((x,y),(r,g,b,a))
    im=new;px=im.load()
bb=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox() or (0,0,W,H)
im=im.crop((max(bb[0]-4,0),max(bb[1]-4,0),min(bb[2]+4,W),min(bb[3]+4,H)))
if im.width>600:im=im.resize((600,round(im.height*600/im.width)),Image.LANCZOS)
im.save(os.path.join(out,'logo.png'),optimize=True)
w,h=im.size
f=im.crop((0,0,min(w,h),h)) if w/h>2 else im
fb=f.getchannel('A').getbbox() or (0,0,f.width,f.height);f=f.crop(fb);s=max(f.size)
cv=Image.new('RGBA',(s,s),(0,0,0,0));cv.paste(f,((s-f.width)//2,(s-f.height)//2));cv.resize((64,64),Image.LANCZOS).save(os.path.join(out,'favicon.png'))
# couleurs dominantes (hors transparent, blancs et gris)
from collections import Counter
C=Counter()
for r,g,b,a in im.getdata():
    if a<200:continue
    hh,ll,ss=colorsys.rgb_to_hls(r/255,g/255,b/255)
    if ss<.18 or ll>.92:continue
    C[(round(hh*24)%24,round(ll*5))]+=1
cols=[]
for (h24,l5),n in C.most_common(12):
    hh=h24/24;
    if any(min(abs(hh-c[0]),1-abs(hh-c[0]))<.07 for c in cols):continue
    cols.append((hh,n))
    if len(cols)==2:break
def fix(hh,target):  # teinte -> couleur sombre/claire avec contraste AA
    for l in [x/100 for x in range(45,5,-1)]:
        c=[v*255 for v in colorsys.hls_to_rgb(hh,l,.7)]
        if cr(c,(255,255,255))>=target:return c
    return (20,50,30)
if not cols:cols=[(0.33,1)]
main=fix(cols[0][0],5.5)
acc=[v*255 for v in colorsys.hls_to_rgb(cols[1][0],.5,.65)] if len(cols)>1 else [v*255 for v in colorsys.hls_to_rgb(cols[0][0],.55,.7)]
accink=(255,255,255) if cr(acc,(255,255,255))>=4.5 else (20,20,20)
if cr(acc,accink)<4.5:acc=[v*255 for v in colorsys.hls_to_rgb(cols[-1][0],.42,.7)];accink=(255,255,255)
hh=cols[0][0]
bgc=[v*255 for v in colorsys.hls_to_rgb(hh,.96,.35)];bg2=[v*255 for v in colorsys.hls_to_rgb(hh,.90,.30)]
ink=[v*255 for v in colorsys.hls_to_rgb(hh,.12,.25)];mu=[v*255 for v in colorsys.hls_to_rgb(hh,.30,.12)]
res={'logo':{'taille':im.size},'bg':hx(bgc),'bg2':hx(bg2),'ink':hx(ink),'mu':hx(mu),'main':hx(main),'acc':hx(acc),'accink':hx(accink),
 'contrastes':{'main/blanc':round(cr(main,(255,255,255)),2),'acc/accink':round(cr(acc,accink),2),'ink/bg':round(cr(ink,bgc),2),'mu/bg2':round(cr(mu,bg2),2)}}
res['mod_py']="--bg '%s' --bg2 '%s' --ink '%s' --mu '%s' --main '%s' --acc '%s' --accink '%s'"%(res['bg'],res['bg2'],res['ink'],res['mu'],res['main'],res['acc'],res['accink'])
print(json.dumps(res,ensure_ascii=False,indent=1))
