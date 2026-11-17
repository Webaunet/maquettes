import os,re,shutil,subprocess,zipfile
from PIL import Image,ImageDraw,ImageFont
U='/mnt/user-data/uploads/Maquettes/'
IMG=U+'Images/Paysagiste/'
MOD=U+'Squelettes/Modules/'
D='/home/claude/maquettes/branche-et-nature/'
BASE='https://webaunet.github.io/maquettes/branche-et-nature/'
NOM='Branche et Nature';VILLE='Forges-les-Bains (91)';TEL='06 83 60 84 49';TELH='+33683608449'
PAGES=[('index.html','Accueil'),('prestations.html','Prestations'),('contact.html','Contact')]
PHP='<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
PHONE_SVG=f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PHP}</svg>'

# 1. squelette S19
if os.path.exists(D):shutil.rmtree(D)
os.makedirs(D+'images')
zipfile.ZipFile(U+'Squelettes/S19.zip').extractall(D)
for f in ('_SKELETON.md','realisations.html','services.html','index.html','prestations.html','contact.html'):
    if os.path.exists(D+f):os.remove(D+f)

# 2. CSS : variables de palette 8 (remplacements ciblés, contrôlés)
p=D+'style.css';s=open(p,encoding='utf8').read()
VARS={'ink':'#23261a','palm':'#3b4a1f','lawn':'#53563f','sun':'#c4912a','sun-d':'#a8741a','chalk':'#f6f3e8','sand':'#e8e6cf','stone':'#e1e5c8','text':'#23261a','soft':'#53563f'}
for k,v in VARS.items():
    s,n=re.subn(r'--'+re.escape(k)+r':#[0-9a-fA-F]{3,6}','--'+k+':'+v,s)
    assert n>=1,'variable absente: '+k
open(p,'w',encoding='utf8').write(s)

# 3. images (recadrage centré au ratio voulu, sans agrandissement)
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
SZ['hero-1']=pic('imgi_4_creation-espace-vert.jpg','hero-1.jpg',700/900,700)
SZ['hero-2']=pic('imgi_2_tonte.jpg','hero-2.jpg',700/900,700)
SZ['hero-3']=pic('imgi_6_plantation.jpg','hero-3.jpg',700/900,700)
SZ['c1']=pic('conception chantier.jpg','c1.jpg',16/9,1408,q=70)
SZ['p1']=pic('imgi_1_taille-haies.jpg','p1.jpg',900/700,900)
SZ['p2']=pic('imgi_6_plantation.jpg','p2.jpg',900/700,900)
SZ['p3']=pic('chantier terrasse en bois.jpg','p3.jpg',900/700,900)
SZ['p4']=pic('imgi_5_feuilles.jpg','p4.jpg',900/700,900)
fv=Image.new('RGB',(64,64),'#3b4a1f');d=ImageDraw.Draw(fv)
try:f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',40)
except Exception:f=ImageFont.load_default()
d.text((32,32),'B',fill='#c4912a',font=f,anchor='mm');fv.save(D+'favicon.png')

# 4. pages
GF='<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,600..800,100&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap">'
def head(t,dsc):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{dsc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#3b4a1f">
<link rel="icon" href="favicon.png" type="image/png">
{GF}
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''
def header(cur):
    li=''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h,n in PAGES)
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="{BASE}" aria-label="{NOM}, accueil"><span><b>BRANCHE ET NATURE</b><small>Paysagiste · Forges-les-Bains (91)</small></span></a>
    <nav id="menu" aria-label="Navigation principale"><ul>{li}</ul></nav>
    <a class="call" href="tel:{TELH}" aria-label="Appeler le {TEL}">{PHONE_SVG}<span>{TEL}</span></a>
    <button class="burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </div>
</header>

<main id="contenu">
'''
def footer():
    li=''.join(f'<a href="{h}">{n}</a>' for h,n in PAGES)
    return f'''</main>
<footer class="hf hf5"><div class="hf5-top"><div class="hv-wrap"><strong>{NOM}</strong><a href="contact.html">Demander un devis</a></div></div><div class="hf5-b"><div class="hv-wrap"><nav aria-label="Pied de page">{li}</nav><p class="hf-cop">{NOM} · {VILLE} · <a href="tel:{TELH}">{TEL}</a> · Maquette de démonstration</p></div></div></footer>
<script src="script.js"></script>
</body>
</html>
'''
def W(n,t):open(D+n,'w',encoding='utf8').write(t)
def mod(name,pairs):
    t=open(MOD+name+'.html',encoding='utf8').read()
    for old,new,cnt in pairs:
        assert t.count(old)>=1,name+': cible absente '+old[:40]
        t=t.replace(old,new) if cnt==0 else t.replace(old,new,cnt)
    return t
def im(k,alt,lazy=True):
    w,h=SZ[k];return f'<img src="images/{k}.jpg" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""} alt="{alt}">'

def index():
    s=head(f'{NOM} · Paysagiste à Forges-les-Bains (91)',f'{NOM}, paysagiste à Forges-les-Bains (91) : création, entretien et aménagement de jardins. Appelez le {TEL}.')+header('index.html')
    h8=mod('H8',[
        ('Paysagiste à Commune (00)',f'Paysagiste à Forges-les-Bains (91)',0),
        ('Titre principal du site','Des jardins créés, entretenus et aménagés avec soin.',0),
        ('Deux phrases concrètes sur l’activité et la zone d’intervention.'.replace('’',"'"),"Branche et Nature crée, entretient et aménage vos espaces verts à Forges-les-Bains et dans les environs, avec un seul interlocuteur.",0),
        ('Appeler le 00 00 00 00 00',f'Appeler le {TEL}',0),
        ('tel:+33000000000',f'tel:{TELH}',0),
        ('Texte alternatif exact','Jardin entretenu avec pelouse et massifs fleuris (image d’illustration)',1),
        ('Texte alternatif exact','Pelouse et massifs, jardin soigné (image d’illustration)',1),
        ('Texte alternatif exact','Plantation d’un arbuste dans un massif (image d’illustration)',1),
        ('images/hero-1.jpg',f'images/hero-1.jpg',0),
    ])
    h8=h8.replace('width="700" height="900"',f'width="{SZ["hero-1"][0]}" height="{SZ["hero-1"][1]}"',1)
    h8=h8.replace('width="700" height="900"',f'width="{SZ["hero-2"][0]}" height="{SZ["hero-2"][1]}"',1)
    h8=h8.replace('width="700" height="900"',f'width="{SZ["hero-3"][0]}" height="{SZ["hero-3"][1]}"',1)
    s+=h8+'\n'
    s+=mod('A5',[
        ('Une phrase d\'introduction.','Quelques repères sur l’entreprise de Mickael Lapalut.',0),
        ('Titre de la section','Branche et Nature en bref',0),
        ('Titre 1','Dirigeant',0),('Deux phrases concrètes.','Entreprise dirigée par Mickael Lapalut, à Forges-les-Bains.',1),
        ('Titre 2','Activité',0),('Deux phrases concrètes.','Services d’aménagement paysager : conception, plantation et entretien d’espaces verts.',1),
        ('Titre 3','Localisation',0),('Deux phrases concrètes.','Basée à Forges-les-Bains, en Essonne (91).',1),
    ])+'\n'
    s+=mod('M4',[
        ('Notre méthode','Notre façon de travailler',0),
        ('Titre de la section','Écouter, concevoir, entretenir',0),
        ('Une phrase d\'introduction.','Chaque espace vert demande une approche adaptée.',0),
        ('Étape 1','Échange',0),('Deux phrases concrètes.','Vous décrivez votre terrain et vos besoins.',1),
        ('Étape 2','Conseil',0),('Deux phrases concrètes.','Nous vous conseillons sur les travaux à prévoir.',1),
        ('Étape 3','Réalisation',0),('Deux phrases concrètes.','Les travaux sont réalisés avec soin.',1),
        ('Étape 4','Entretien',0),('Deux phrases concrètes.','Un suivi régulier de votre espace vert.',1),
    ])+'\n'
    s+=mod('C3',[
        ('Un projet de jardin ? Parlons-en.','Un projet de jardin à Forges-les-Bains ?',0),
        ('Une phrase d\'invitation à demander un devis.','Appelez-nous ou demandez un devis en ligne.',0),
        ('Appeler le 00 00 00 00 00',f'Appeler le {TEL}',0),
        ('tel:+33000000000',f'tel:{TELH}',0),
        ('images/c1.jpg',f'images/c1.jpg',0),
        ('width="1600" height="900"',f'width="{SZ["c1"][0]}" height="{SZ["c1"][1]}"',0),
    ])+'\n'
    s+=footer()
    W('index.html',s)

def prest():
    s=head(f'Prestations · {NOM} à Forges-les-Bains (91)',f'Conception, plantation, entretien et terrasses : les prestations de {NOM} à Forges-les-Bains (91).')+header('prestations.html')
    s+=f'''<section class="sv sv-intro" aria-labelledby="h1"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h1 id="h1">Conception, plantation, entretien et terrasses</h1><p class="hv-lead">{NOM} intervient à Forges-les-Bains et dans les environs pour les jardins des particuliers.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="contact.html">Demander un devis</a></div></div></section>
'''
    v3=mod('V3',[
        ('Titre de la section','Quatre domaines pour votre jardin',0),
        ('Une phrase d\'introduction.','Décrivez votre projet, nous vous conseillons.',0),
        ('Prestation 1','Conception de jardin',0),('Prestation 2','Plantations et massifs',0),
        ('Prestation 3','Entretien de jardin',0),('Prestation 4','Terrasses et allées',0),
        ('Une phrase courte.','Un plan d’aménagement adapté à votre terrain.',1),
        ('Une phrase courte.','Création de massifs et plantation d’arbustes et de vivaces.',1),
        ('Une phrase courte.','Tonte, taille de haies et ramassage des feuilles.',1),
        ('Une phrase courte.','Terrasse, allée et abords aménagés.',1),
        ('Deux phrases concrètes.','Un plan d’aménagement construit à partir de votre terrain et de vos usages.',1),
        ('Deux phrases concrètes.','Massifs et plantations choisis selon votre exposition.',1),
        ('Deux phrases concrètes.','Pelouse et haies suivies, ponctuellement ou régulièrement.',1),
        ('Deux phrases concrètes.','Des accès et des espaces de vie extérieurs soignés.',1),
        ('Texte alternatif exact','Jardinier taillant une haie (image d’illustration)',1),
        ('Texte alternatif exact','Plantation dans un massif (image d’illustration)',1),
        ('Texte alternatif exact','Terrasse en bois en cours de pose (image d’illustration)',1),
        ('Texte alternatif exact','Feuilles ramassées dans un jardin (image d’illustration)',1),
        ('images/p1.jpg',f'images/p1.jpg',0),
    ])
    v3=v3.replace('images/p3.jpg','images/p4.jpg',1)
    for n in range(1,5):v3=v3.replace('<figure class="sv3-v sv3-v'+str(n)+'"','<figure id="p'+str(n)+'" class="sv3-v sv3-v'+str(n)+'"',1)
    for k in ['p1','p2','p3','p4']:
        w,h=SZ[k];v3=re.sub(r'(<img src="images/'+k+r'\.jpg") width="\d+" height="\d+"',lambda m:m.group(1)+f' width="{w}" height="{h}"',v3)
    s+=v3+'\n'
    s+=footer()
    W('prestations.html',s)

def contact():
    s=head(f'Contact et devis · {NOM} à Forges-les-Bains (91)',f'Contactez {NOM}, paysagiste à Forges-les-Bains (91) : téléphone ou demande de devis en ligne.')+header('contact.html')
    s+=f'''<section class="sv sv-intro" aria-labelledby="h1"><div class="hv-wrap"><p class="hv-kick">Contact</p><h1 id="h1">Parlons de votre jardin</h1><p class="hv-lead">Décrivez votre besoin : le récapitulatif se prépare en quelques secondes, à envoyer par SMS.</p></div></section>
'''
    k4=mod('K4',[
        ('Nom de l\'entreprise',NOM,0),
        ('data-sms="+33000000000"',f'data-sms="{TELH}"',0),
        ('data-tel="+33000000000"',f'data-tel="{TELH}"',0),
        ('Parlez-nous de votre projet','Demandez votre devis',0),
        ('Une phrase d\'introduction.','Indiquez votre commune et votre besoin : nous vous recontactons.',0),
        ('<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>','<option>Conception de jardin</option><option>Plantations et massifs</option><option>Entretien de jardin</option><option>Terrasse ou allée</option>',0),
    ])
    aside=f'<aside class="sk-side"><h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:{TELH}">{TEL}</a></li><li><span>Commune</span><p>Forges-les-Bains (91)</p></li></ul></aside>'
    k4=re.sub(r'<aside class="sk-side">.*?</aside>',aside,k4,flags=re.S)
    assert 'aside' in k4
    s+=k4+'\n'
    s+=footer().replace('<script src="script.js"></script>','<script src="script.js"></script>\n<script src="js/k.js" defer></script>')
    W('contact.html',s)

# nettoyage des traces du squelette (script.js, commentaire CSS)
sp=D+'script.js';js=open(sp,encoding='utf8').read()
for a,b in [("var TELH = '+33605507947', MAIL = 'andreipintilii96@gmail.com';","var TELH = '"+TELH+"', MAIL = 'contact@exemple.fr';"),("'Bonjour Andrei, je suis '","'Bonjour, je suis '")]:
    assert js.count(a)==1,'trace JS absente';js=js.replace(a,b)
open(sp,'w',encoding='utf8').write(js)
cp=D+'style.css';cs=open(cp,encoding='utf8').read()
cs=re.sub(r'/\* Concept :[^*]*\*/','/* Branche et Nature : feuille commune */',cs,count=1)
open(cp,'w',encoding='utf8').write(cs)
index();prest();contact()

r=subprocess.run(['python3','-I',MOD+'mod.py',D,'H8','V3','A5','M4','C3','F5','K4','--bg','#f6f3e8','--bg2','#e8e6cf','--ink','#23261a','--mu','#53563f','--main','#3b4a1f','--acc','#c4912a','--accink','#23261a','--fh','Fraunces','--fb','Nunito Sans','--fw','700'],capture_output=True,text=True)
print(r.stdout,r.stderr);assert r.returncode==0
open(D+'README.md','w',encoding='utf8').write(f'# {NOM}\n\nMaquette de site vitrine (démonstration) : accueil, prestations, contact.\n')
print('ok')
