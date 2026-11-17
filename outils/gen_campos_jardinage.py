import os,re,shutil,subprocess,zipfile
from PIL import Image,ImageDraw,ImageFont
U='/mnt/user-data/uploads/Maquettes/'
IMG=U+'Images/Paysagiste/'
MOD=U+'Squelettes/Modules/'
D='/home/claude/maquettes/campos-jardinage/'
BASE='https://webaunet.github.io/maquettes/campos-jardinage/'
NOM='Campos Jardinage';VILLE='Versailles (78)'
TEL='06 08 45 69 86';TELH='+33608456986'
PAGES=[('index.html','Accueil'),('prestations.html','Prestations'),('entreprise.html',"L’entreprise"),('contact.html','Contact')]
PHP='<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
PHONE_SVG=f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PHP}</svg>'

# 1. squelette S10
if os.path.exists(D):shutil.rmtree(D)
os.makedirs(D+'images')
zipfile.ZipFile(U+'Squelettes/S10.zip').extractall(D)
for f in ('_SKELETON.md','index.html','prestations.html','contact.html','entreprise.html'):
    if os.path.exists(D+f):os.remove(D+f)

# 2. CSS : palette 2 (terre cuite et sable), polices 2 (Bricolage Grotesque / Source Sans 3)
p=D+'css/style.css';s=open(p,encoding='utf8').read()
VARS={'bg':'#f7efe4','bg2':'#ecdcc6','ink':'#2b211b','muted':'#5f4f44','line':'#d6c7b1','band':'#7a3b22','band-ink':'#fff8ef','band-muted':'#e8d6c4','leaf':'#3f6b4f','leaf-ink':'#ffffff','link':'#7a3b22'}
for k,v in VARS.items():
    s,n=re.subn(r'--'+re.escape(k)+r':#[0-9a-fA-F]{3,6}','--'+k+':'+v,s)
    assert n>=1,'variable absente: '+k
s=s.replace('Figtree','Source Sans 3')
s=re.sub(r'/\*\s*Artivert[^\n]*?\*/','/* Campos Jardinage : feuille commune */',s,count=1)
open(p,'w',encoding='utf8').write(s)

# 3. images (recadrage centré au ratio voulu, jamais agrandies)
def pic(src,dst,ratio,maxw,q=78):
    i=Image.open(IMG+src).convert('RGB');w,h=i.size
    if w/h>ratio:
        nw=round(h*ratio);x=(w-nw)//2;i=i.crop((x,0,x+nw,h))
    else:
        nh=round(w/ratio);y=(h-nh)//2;i=i.crop((0,y,w,y+nh))
    if i.width>maxw:i=i.resize((maxw,round(i.height*maxw/i.width)),Image.LANCZOS)
    i.save(D+'images/'+dst,quality=q,optimize=True,progressive=True)
    return i.size
SZ={}
SZ['hero']=pic('imgi_7_entretien-jardin.jpg','hero.jpg',1400/900,1400,q=60)
SZ['p1']=pic('imgi_4_creation-espace-vert.jpg','p1.jpg',900/600,900)
SZ['p2']=pic('imgi_2_tonte.jpg','p2.jpg',900/600,900)
fv=Image.new('RGB',(64,64),'#7a3b22');d=ImageDraw.Draw(fv)
try:f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',40)
except Exception:f=ImageFont.load_default()
d.text((32,32),'C',fill='#f7efe4',font=f,anchor='mm');fv.save(D+'favicon.png')

# 4. pages
GF='<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Source+Sans+3:wght@400;600;700&display=swap">'
def head(t,dsc):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{dsc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#7a3b22">
<link rel="icon" href="favicon.png" type="image/png">
{GF}
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''
def header(cur):
    li=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a>' for h,n in PAGES)
    return f'''<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="{BASE}" aria-label="{NOM}, accueil"><span>Campos <b>Jardinage</b></span></a>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      {li}
    </nav>
    <a class="btn btn--leaf hdr__call" href="tel:{TELH}" aria-label="Appeler le {TEL}">{PHONE_SVG}<span>{TEL}</span></a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>

<main id="contenu">
'''
F3=open(MOD+'F3.html',encoding='utf8').read()
def footer(k=False):
    f=F3
    for a,b in [("Nom de l'entreprise",NOM),('a-propos.html','entreprise.html'),('À propos',"L’entreprise"),
                (f'<a href="tel:+33000000000">00 00 00 00 00</a><a href="mailto:contact@exemple.fr">contact@exemple.fr</a>',f'<a href="tel:{TELH}">{TEL}</a>')]:
        assert f.count(a)>=1,'F3 cible absente '+a[:30]
        f=f.replace(a,b)
    f=re.sub(r'<a href="mailto:[^"]*">[^<]*</a>','',f)
    sc='<script src="js/main.js"></script>\n'+('<script src="js/k.js" defer></script>\n' if k else '')
    return '</main>\n'+f+'\n'+sc+'</body>\n</html>\n'
def W(n,t):open(D+n,'w',encoding='utf8').write(t)
def mod(name,pairs,regex=()):
    t=open(MOD+name+'.html',encoding='utf8').read()
    for old,new,cnt in pairs:
        assert t.count(old)>=1,name+': cible absente '+old[:40]
        t=t.replace(old,new) if cnt==0 else t.replace(old,new,cnt)
    for pat,new in regex:
        t,n=re.subn(pat,new,t,flags=re.S);assert n>=1,name+': regex absente '+pat[:30]
    return t
def size_fix(t,k):
    w,h=SZ[k]
    return re.sub(r'(<img src="images/'+k+r'\.jpg") width="\d+" height="\d+"',lambda m:m.group(1)+f' width="{w}" height="{h}"',t)

def index():
    s=head(f'{NOM} · Aménagement et entretien d’espaces verts à Versailles (78)',f'{NOM}, aménagement et entretien d’espaces verts à Versailles (78). Appelez le {TEL}.')+header('index.html')
    h9=mod('H9',[
        ('Paysagiste à Commune (00)',"Aménagement et entretien d’espaces verts à Versailles (78)",0),
        ('Titre principal du site','Des espaces verts aménagés et entretenus à Versailles.',0),
        ("Deux phrases concrètes sur l'activité et la zone d'intervention.","Campos Jardinage conçoit, aménage et entretient vos espaces verts à Versailles et dans les Yvelines.",0),
        ('Appeler le 00 00 00 00 00',f'Appeler le {TEL}',0),
        ('tel:+33000000000',f'tel:{TELH}',0),
        ('Texte alternatif exact',"Jardin entretenu avec pelouse et massifs (image d’illustration)",0),
    ],regex=[(r'<ul class="hv9-facts">.*?</ul>','<ul class="hv9-facts"><li><strong>Versailles</strong> (78)</li><li><strong>Jose de Campos Cibrao</strong>, dirigeant</li></ul>')])
    h9=size_fix(h9,'hero')
    s+=h9+'\n'
    s+=mod('V5',[
        ('Titre de la section','Aménagement et entretien',0),
        ("Une phrase d'introduction.",'Un seul interlocuteur pour vos espaces verts.',0),
        ('Prestation 1','Création et aménagement',0),('Prestation 2','Entretien de jardin',0),
        ('Deux phrases concrètes sur cette prestation.','Conception et aménagement de vos espaces verts, selon votre terrain et vos envies.',1),
        ('Deux phrases concrètes sur cette prestation.','Entretien régulier de vos espaces verts, pour un jardin soigné toute l’année.',1),
        ('Texte alternatif exact',"Jardin en cours de création, massifs et pelouse (image d’illustration)",1),
        ('Texte alternatif exact',"Tonte de pelouse dans un jardin (image d’illustration)",1),
    ],regex=[(r'<p class="sv5-more">.*?</p>','')])
    s=size_fix(s,'p1');s=size_fix(s,'p2')
    s+=mod('A2',[
        ('Une phrase forte qui résume l\'engagement de l\'entreprise.',"Une entreprise d’aménagement et d’entretien d’espaces verts à Versailles.",0),
        ("Un paragraphe concret et vérifié sur l'entreprise.","Campos Jardinage intervient en aménagement paysager et en entretien d’espaces verts à Versailles (78), sous la direction de Jose de Campos Cibrao.",0),
        ('Prénom Nom, dirigeant','Jose de Campos Cibrao, dirigeant',0),
    ],regex=[(r'<ul class="sa2-facts">.*?</ul>','<ul class="sa2-facts"><li><strong>Versailles</strong>(78)</li><li><strong>Aménagement</strong>et entretien</li><li><strong>Contact</strong>direct</li></ul>')])+'\n'
    s+=mod('C4',[
        ('Un projet de jardin ? Parlons-en.',"Un projet d’espace vert ? Parlons-en.",0),
        ("Une phrase d'invitation à demander un devis.","Appelez-nous ou écrivez-nous : nous revenons vers vous pour établir un devis.",0),
        ('00 00 00 00 00',TEL,0),('tel:+33000000000',f'tel:{TELH}',0),
    ],regex=[(r'<a href="contact.html">Formulaire de contact</a>','<a href="contact.html">Formulaire de contact</a>')])+'\n'
    s+=footer()
    W('index.html',s)

def prest():
    s=head(f'Prestations · {NOM} à Versailles (78)',f'Création et entretien d’espaces verts : les prestations de {NOM} à Versailles (78).')+header('prestations.html')
    s+=f'''<section class="sv sv-intro" aria-labelledby="h1"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h1 id="h1">Aménagement et entretien d’espaces verts</h1><p class="hv-lead">{NOM} intervient à Versailles (78) pour vos espaces verts. Décrivez votre besoin, nous vous répondons.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="contact.html">Demander un devis</a></div></div></section>
'''
    v5=mod('V5',[
        ('Titre de la section','Aménagement et entretien',0),
        ("Une phrase d'introduction.",'Un seul interlocuteur pour vos espaces verts.',0),
        ('Prestation 1','Création et aménagement',0),('Prestation 2','Entretien de jardin',0),
        ('Deux phrases concrètes sur cette prestation.','Conception et aménagement de vos espaces verts, selon votre terrain et vos envies.',1),
        ('Deux phrases concrètes sur cette prestation.','Entretien régulier de vos espaces verts, pour un jardin soigné toute l’année.',1),
        ('Texte alternatif exact',"Jardin en cours de création, massifs et pelouse (image d’illustration)",1),
        ('Texte alternatif exact',"Tonte de pelouse dans un jardin (image d’illustration)",1),
        ('<article class="sv5-row">','<article id="p1" class="sv5-row">',1),
        ('<article class="sv5-row">','<article id="p2" class="sv5-row">',1),
    ],regex=[(r'<p class="sv5-more">.*?</p>','')])
    v5=size_fix(v5,'p1');v5=size_fix(v5,'p2')
    s+=v5+'\n'
    s+=mod('M5',[
        ('Titre de la section','Une démarche simple, du devis au suivi',0),
        ("Une phrase d'introduction.",'Un interlocuteur unique, de la demande à la réalisation.',0),
        ('1. Étape 1','1. Échange',0),('2. Étape 2','2. Devis',0),('3. Étape 3','3. Réalisation ou entretien',0),
        ('Deux phrases concrètes.','Vous décrivez votre projet ou vos besoins, par téléphone ou par formulaire.',1),
        ('Deux phrases concrètes.','Nous vous répondons pour établir un devis adapté à votre espace vert.',1),
        ('Deux phrases concrètes.','Les travaux sont réalisés, ou l’entretien est planifié selon votre demande.',1),
    ])+'\n'
    s+=mod('C4',[
        ('Un projet de jardin ? Parlons-en.',"Un projet d’espace vert ? Parlons-en.",0),
        ("Une phrase d'invitation à demander un devis.","Appelez-nous ou écrivez-nous : nous revenons vers vous pour établir un devis.",0),
        ('00 00 00 00 00',TEL,0),('tel:+33000000000',f'tel:{TELH}',0),
    ])+'\n'
    s+=footer()
    W('prestations.html',s)

def entreprise():
    s=head(f'L’entreprise · {NOM} à Versailles (78)',f'{NOM}, entreprise d’aménagement et d’entretien d’espaces verts à Versailles (78), dirigée par Jose de Campos Cibrao.')+header('entreprise.html')
    s+=f'''<section class="sv sv-intro" aria-labelledby="h1"><div class="hv-wrap"><p class="hv-kick">L’entreprise</p><h1 id="h1">{NOM}, à Versailles</h1><p class="hv-lead">Une entreprise d’aménagement et d’entretien d’espaces verts dans les Yvelines.</p></div></section>
'''
    s+=mod('A2',[
        ('Une phrase forte qui résume l\'engagement de l\'entreprise.',"Un interlocuteur pour l’aménagement et l’entretien de vos espaces verts.",0),
        ("Un paragraphe concret et vérifié sur l'entreprise.","Campos Jardinage intervient en aménagement paysager et en entretien d’espaces verts à Versailles (78), sous la direction de Jose de Campos Cibrao.",0),
        ('Prénom Nom, dirigeant','Jose de Campos Cibrao, dirigeant',0),
    ],regex=[(r'<ul class="sa2-facts">.*?</ul>','<ul class="sa2-facts"><li><strong>Versailles</strong>(78)</li><li><strong>Aménagement</strong>et entretien</li><li><strong>Contact</strong>direct</li></ul>')])+'\n'
    s+=mod('C4',[
        ('Un projet de jardin ? Parlons-en.',"Un projet d’espace vert ? Parlons-en.",0),
        ("Une phrase d'invitation à demander un devis.","Appelez-nous ou écrivez-nous : nous revenons vers vous pour établir un devis.",0),
        ('00 00 00 00 00',TEL,0),('tel:+33000000000',f'tel:{TELH}',0),
    ])+'\n'
    s+=footer()
    W('entreprise.html',s)

def contact():
    s=head(f'Contact et devis · {NOM} à Versailles (78)',f'Contactez {NOM} à Versailles (78) : téléphone ou demande de devis en ligne.')+header('contact.html')
    s+=f'''<section class="sv sv-intro" aria-labelledby="h1"><div class="hv-wrap"><p class="hv-kick">Contact</p><h1 id="h1">Parlons de votre espace vert</h1><p class="hv-lead">Décrivez votre besoin : le récapitulatif se prépare en quelques secondes, à envoyer par SMS ou par e-mail.</p></div></section>
'''
    k4=mod('K4',[
        ("data-name=\"Nom de l'entreprise\"",f'data-name="{NOM}"',0),
        ('data-sms="+33000000000"',f'data-sms="{TELH}"',0),
        ('data-tel="+33000000000"',f'data-tel="{TELH}"',0),
        ('Parlez-nous de votre projet','Demandez votre devis',0),
        ("Une phrase d'introduction.",'Indiquez votre commune et votre besoin : nous vous recontactons.',0),
        ('<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>','<option>Aménagement d’un jardin</option><option>Entretien de jardin</option><option>Taille et plantation</option>',0),
    ])
    aside=f'<aside class="sk-side"><h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:{TELH}">{TEL}</a></li><li><span>Commune</span><p>Versailles (78)</p></li></ul></aside>'
    k4=re.sub(r'<aside class="sk-side">.*?</aside>',aside,k4,flags=re.S)
    assert 'Versailles (78)</p>' in k4
    s+=k4+'\n'
    s+=footer(True)
    W('contact.html',s)

index();prest();entreprise();contact()

# correction ciblée : apostrophe non échappée dans js/main.js (erreur de syntaxe du squelette)
jp=D+'js/main.js';jsrc=open(jp,encoding='utf8').read()
assert jsrc.count("pour Nom de l'entreprise")==1,'ligne js absente'
jsrc=jsrc.replace("pour Nom de l'entreprise","pour "+NOM)
open(jp,'w',encoding='utf8').write(jsrc)

# modules CSS + js/k.js
r=subprocess.run(['python3','-I',MOD+'mod.py',D,'H9','V5','A2','M5','C4','F3','K4','--bg','#f7efe4','--bg2','#ecdcc6','--ink','#2b211b','--mu','#5f4f44','--main','#7a3b22','--acc','#3f6b4f','--accink','#ffffff','--fh','Bricolage Grotesque','--fb','Source Sans 3','--fw','700'],capture_output=True,text=True)
print(r.stdout,r.stderr);assert r.returncode==0
open(D+'css/style.css','a',encoding='utf8').write("""
/* harmonisation des sections : mêmes espaces sur toutes les pages */
.sv,.hv9{padding-block:clamp(48px,6vw,80px)!important;min-height:0!important}
@media(max-width:620px){.sv.sv.sv.sv,.hv9{padding-top:40px!important;padding-bottom:40px!important}}
""")
open(D+'README.md','w',encoding='utf8').write(f'# {NOM}\n\nMaquette de site vitrine (démonstration) : accueil, prestations, entreprise, contact.\n')
print('ok')
