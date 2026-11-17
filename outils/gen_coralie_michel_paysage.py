import os,re,shutil,zipfile,subprocess,sys
from PIL import Image,ImageDraw,ImageFont
U='/mnt/user-data/uploads/Maquettes'
D='/home/claude/maquettes/coralie-michel-paysage'
IM=U+'/Images/Paysagiste/'
NOM='Coralie Michel Paysage';COM='Bullion (78)';TEL='06 70 79 02 30';TELI='+33670790230'
URL='https://webaunet.github.io/maquettes/coralie-michel-paysage/'
if os.path.exists(D):shutil.rmtree(D)
os.makedirs(D)
zipfile.ZipFile(U+'/Squelettes/S09.zip').extractall(D)
os.remove(D+'/_SKELETON.md')
for f in ('arboriculture.html','paysage.html','entreprise.html','contact.html','index.html'):os.remove(D+'/'+f)
os.makedirs(D+'/images',exist_ok=True)
SZ={}
def pic(src,name,ratio,focus=.5,maxw=None,q=78):
    im=Image.open(IM+src).convert('RGB');w,h=im.size
    if w/h>ratio:
        nw=int(h*ratio);x=int((w-nw)*focus);im=im.crop((x,0,x+nw,h))
    else:
        nh=int(w/ratio);y=int((h-nh)*.5);im=im.crop((0,y,w,y+nh))
    if maxw and im.size[0]>maxw:im=im.resize((maxw,round(maxw/ratio)),Image.LANCZOS)
    while True:
        im.save(D+'/images/'+name,quality=q,optimize=True,progressive=True)
        if os.path.getsize(D+'/images/'+name)<245000 or q<=50:break
        q-=5
    SZ[name]=im.size
pic('imgi_7_entretien-jardin.jpg','hero.jpg',1408/768,.5,q=70)
pic('imgi_6_plantation.jpg','p1.jpg',1.5,.42)
pic('imgi_2_tonte.jpg','a1.jpg',1000/700,.45)
pic('imgi_4_desherbage.jpg','a2.jpg',700/900,.55)
pic('conception chantier.jpg','f1.jpg',4/4.6,.72,maxw=600)
pic('imgi_3_entretien-general.jpg','f2.jpg',4/4.6,.4,maxw=600)
pic('imgi_5_feuilles.jpg','f3.jpg',4/4.6,.8,maxw=600)
pic('imgi_1_taille-haies.jpg','r1.jpg',16/11,.5,maxw=800)
pic('chantier terrasse en bois.jpg','r2.jpg',16/11,.55,maxw=800)
pic('imgi_7_dechets-verts.jpg','g1.jpg',16/10,.5,maxw=800)
pic('imgi_10_nettoyage.jpg','g2.jpg',16/10,.5,maxw=800)
pic('imgi_7_entretien-jardin.jpg','g3.jpg',16/10,.5,maxw=800)
pic('imgi_4_creation-espace-vert.jpg','r3.jpg',16/11,.6,maxw=800)
# favicon
fv=Image.new('RGB',(128,128),'#4a2340');d=ImageDraw.Draw(fv)
try:ft=ImageFont.truetype('DejaVuSerif-Bold.ttf',84)
except Exception:ft=ImageFont.load_default()
d.text((64,66),'C',font=ft,fill='#b9d9a0',anchor='mm');fv.resize((64,64)).save(D+'/favicon.png')
def wh(n):return 'width="%d" height="%d"'%SZ[n]
# CSS skeleton
p=D+'/css/style.css';s=open(p,encoding='utf8').read()
V={'forest':'#4a2340','forest-2':'#3a1a32','leaf':'#6b3a5e','moss':'#b9d9a0','sage':'#eadde4','cream':'#faf5f3','sand':'#f0e6ea','bark':'#5a4755','rope':'#4f7d34','rope-d':'#3f6a28','ink':'#2a1a26'}
for k,v in V.items():
    s,n=re.subn(r'(--%s:)#[0-9a-fA-F]{3,8}'%re.escape(k),lambda m:m.group(1)+v,s,count=1);assert n==1,k
assert s.count("'Figtree'")>=1;s=s.replace("'Figtree'","'Nunito Sans'")
for a,b in [('#e3ebd5','#eadde4'),('#d3dfc2','#eadde4'),('#2d4034','#4a3946'),('#f4f8ec','#ffffff'),('rgba(18,48,31,','rgba(42,26,38,'),('rgba(169,196,135,','rgba(185,217,160,')]:s=s.replace(a,b)
s=re.sub(r'/\*[^*]*(Cœur|Arbre|Étampes)[^*]*\*/','/* Maquette */',s)
open(p,'w',encoding='utf8').write(s)
r=subprocess.run(['python3','-I',U+'/Squelettes/Modules/mod.py',D,'H11','V6','A8','C2','F5','K8','--bg','#faf5f3','--bg2','#eadde4','--ink','#2a1a26','--mu','#5a4755','--main','#4a2340','--acc','#4f7d34','--accink','#ffffff','--fh','Fraunces','--fb','Nunito Sans','--fw','700'],capture_output=True,text=True);print(r.stdout,r.stderr);assert r.returncode==0
open(p,'a',encoding='utf8').write('''
/* maquette */
.btn-rope{color:#fff}.btn-rope:hover{background:#3f6a28;color:#fff}.c-rope{color:#fff}
.story{grid-template-columns:1fr!important;max-width:860px}
.sv,.hv11{min-height:0!important}.sv{padding-block:clamp(48px,6vw,80px)!important}
@media(max-width:620px){.sv.sv.sv.sv{padding-top:40px!important;padding-bottom:40px!important}.sv6-big img{aspect-ratio:16/10;object-fit:cover;width:100%}.cards3 .card{display:grid;grid-template-columns:auto 1fr;column-gap:1rem;align-items:center;padding:.9rem 1rem}.cards3{gap:.8rem!important}.cards3 .card svg{grid-row:span 2}.cards3 .card h3,.cards3 .card p{margin:0}.gal3 img:nth-child(3){display:none}.gal3 img{aspect-ratio:16/8!important;object-fit:cover}.sv6-t{padding:1rem 1.2rem!important;min-height:0!important}.sv6-t p{display:none!important}.sv6-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important}.sv6-t h3{font-size:1.1rem!important;overflow-wrap:anywhere}.sv6-big{min-height:210px!important}.sv6-grid{margin-top:20px!important}.sv6-big>div{padding:1rem 1.2rem!important}}
''')
# JS fix
jp=D+'/js/main.js';j=open(jp,encoding='utf8').read()
assert j.count("maquette Nom de l'entreprise)")==1;j=j.replace("maquette Nom de l'entreprise)","maquette "+NOM+")")
j=j.replace("var TEL='+33000000000'","var TEL='"+TELI+"'");open(jp,'w',encoding='utf8').write(j)
# pieces
NAV=[('index.html','Accueil'),('prestations.html','Prestations'),('entreprise.html','L’entreprise'),('contact.html','Contact')]
def head(t,d,k=False):
    return '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=Nunito+Sans:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''%(t,d)
def hdr(cur):
    nav=''.join('<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if h==cur else '',l) for h,l in NAV)
    return '''<header class="hdr">
  <div class="wrap">
    <a class="brand" href="%s" aria-label="%s, accueil"><span><b>%s</b><small>Paysagiste · %s</small></span></a>
    <nav class="nav" id="nav" aria-label="Navigation principale">%s</nav>
    <a class="call" href="tel:%s" aria-label="Appeler le %s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg><span>%s</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span></span></button>
  </div>
</header>
<main>
'''%(URL,NOM,NOM,COM,nav,TELI,TEL,TEL)
FOOT='''</main>
<div class="hf hf5" role="contentinfo"><div class="hf5-top"><div class="hv-wrap"><strong>Un projet de jardin ? Demandez votre devis.</strong><a href="contact.html">Nous contacter</a></div></div><div class="hf5-b"><div class="hv-wrap"><nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a><a href="entreprise.html">L’entreprise</a><a href="contact.html">Contact</a></nav><p class="hf-cop">© %s · %s · <a href="tel:%s">%s</a> · Maquette de démonstration</p></div></div></div>
'''%(NOM,COM,TELI,TEL)
def tail(k=False):return FOOT+'<script src="js/main.js" defer></script>\n'+('<script src="js/k.js" defer></script>\n' if k else '')+'</body>\n</html>\n'
def ic(path):return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="%s"/></svg>'%path
I_LEAF='M5 19C5 10 11 5 20 5c0 9-5 15-14 15M5 19l8-8'
I_SPADE='M12 3v9M9 12h6l-1 9h-4zM10 6h4'
I_SUN='M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM12 2v3M12 19v3M2 12h3M19 12h3'
I_HEDGE='M3 20h18M5 20V9h14v11M9 9V5M15 9V5'
I_HOME='M3 11l9-8 9 8M5 10v10h14V10'
I_PIN='M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11zM12 7v6'
I_PHONE='M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z'
I_USER='M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM4 21a8 8 0 0 1 16 0'
C2='<section class="sv sc2" aria-labelledby="sv-c"><div class="hv-wrap"><div><p class="hv-kick">Contact</p><h2 id="sv-c">Un projet de jardin&nbsp;? Parlons-en.</h2><p class="hv-lead">Appelez %s ou demandez un devis en quelques lignes : votre message est prêt à envoyer par SMS.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:%s">Appeler le %s</a><a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div></div><div class="sc2-card"><div><span>Téléphone</span><a href="tel:%s">%s</a></div><div><span>Commune</span><p>%s</p></div></div></div></section>'%('Coralie Michel',TELI,TEL,TELI,TEL,COM)
# INDEX
h=head('%s · Paysagiste à %s'%(NOM,COM),'%s, paysagiste à %s : création, plantation et entretien de jardins et d’espaces verts. Appelez le %s.'%(NOM,COM,TEL))+hdr('index.html')
h+='''<section class="hv hv11 hv-dark" aria-labelledby="hv-t"><div class="hv11-bg"><img src="images/hero.jpg" %s alt="Jardin entretenu avec allée, pelouse et massifs fleuris devant une maison (image d’illustration)"></div><div class="hv-wrap hv11-in"><div class="hv11-top"><p class="hv-kick">%s · %s</p></div><h1 id="hv-t">Un jardin conçu et entretenu <em>avec soin.</em></h1><div class="hv11-bot"><div class="hv11-l"><p class="hv-lead">%s crée, plante et entretient vos espaces verts à Bullion et dans les environs.</p></div><div class="hv11-r"><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:%s">Appeler le %s</a><a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div><p class="hv11-note">Demande de devis en ligne · Bullion (78)</p></div></div></div></section>

<section class="sv sv6" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Créer et entretenir votre jardin</h2><p class="hv-lead">Des services d’aménagement paysager pour les particuliers de Bullion et des environs.</p><div class="sv6-grid"><div class="sv6-big"><img src="images/p1.jpg" %s alt="Jardinier plantant un végétal dans un massif (image d’illustration)" loading="lazy"><div><h3>Création de jardin</h3><p>Conception et aménagement de votre espace vert, selon votre terrain et vos envies.</p><a href="prestations.html#p1">En savoir plus →</a></div></div><div class="sv6-t sv6-t1"><h3>Plantation</h3><p>Arbustes, massifs et végétaux installés avec soin.</p><a href="prestations.html#p2">En savoir plus →</a></div><div class="sv6-t sv6-t2"><h3>Entretien d’espaces verts</h3><p>Un suivi régulier pour garder un jardin net et agréable.</p><a href="prestations.html#p3">En savoir plus →</a></div><div class="sv6-t sv6-t3"><h3>Tonte et taille</h3><p>Pelouses et haies entretenues au fil des saisons.</p><a href="prestations.html#p4">En savoir plus →</a></div><div class="sv6-t sv6-t4"><h3>Aménagement extérieur</h3><p>Mise en valeur de vos abords et de vos espaces extérieurs.</p><a href="prestations.html#p5">En savoir plus →</a></div></div></div></section>

<section class="sv sa8" aria-labelledby="sv-a"><div class="hv-wrap"><div class="sa8-tx"><p class="hv-kick">À propos</p><h2 id="sv-a">Une entreprise de paysage à Bullion</h2><p>%s est dirigée par Coralie Michel. L’entreprise propose des services d’aménagement paysager à Bullion, dans les Yvelines (78).</p><p>Pour parler de votre jardin, un seul numéro : le %s.</p><p class="sa8-sign">Coralie Michel, dirigeante</p></div><div class="sa8-ph"><figure class="sa8-1"><img src="images/a1.jpg" %s alt="Tonte d’une pelouse devant une maison (image d’illustration)" loading="lazy"></figure><figure class="sa8-2"><img src="images/a2.jpg" %s alt="Jardinier entretenant un massif (image d’illustration)" loading="lazy"></figure></div></div></section>

%s
'''%(wh('hero.jpg'),NOM,COM,NOM,TELI,TEL,wh('p1.jpg'),NOM,TEL,wh('a1.jpg'),wh('a2.jpg'),C2)+tail()
open(D+'/index.html','w',encoding='utf8').write(h)
# PRESTATIONS
def card(i,ico,t,x):return '<article class="card c-white" id="p%d">%s<h3>%s</h3><p>%s</p></article>'%(i,ic(ico),t,x)
h=head('Prestations · %s à %s'%(NOM,COM),'Prestations de %s à %s : création de jardin, plantation, entretien d’espaces verts, tonte et taille, aménagement extérieur.'%(NOM,COM))+hdr('prestations.html')
h+='''<section class="sec phead light" aria-labelledby="h1">
  <div class="wrap">
    <div>
      <span class="eyebrow">Prestations · %s</span>
      <h1 id="h1">Des espaces verts conçus et entretenus</h1>
      <p class="lead">Création de jardin, plantation, entretien, tonte et taille, aménagement extérieur : %s accompagne votre projet à Bullion et dans les environs.</p>
      <div class="actions"><a class="btn btn-green" href="contact.html">Demander un devis</a><a class="btn btn-rope" href="tel:%s">Appeler le %s</a></div>
    </div>
    <div class="fan">
      <img src="images/f1.jpg" %s alt="Projet d’aménagement de jardin étudié sur tablette (image d’illustration)">
      <img src="images/f2.jpg" %s alt="Jardinier tondant une pelouse devant une maison (image d’illustration)">
      <img src="images/f3.jpg" %s alt="Entretien d’un massif et ramassage des feuilles (image d’illustration)">
    </div>
  </div>
</section>

<section class="sec s-cream" aria-labelledby="h-serv">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Les prestations</span><h2 id="h-serv">Trois façons de faire vivre votre jardin</h2></div>
    <div class="cards3">
      %s
      %s
      %s
    </div>
  </div>
</section>

<section class="sec s-sand" aria-labelledby="h-p4">
  <div class="wrap">
    <div class="row" id="p4">
      <img src="images/r1.jpg" %s alt="Jardinier taillant une haie (image d’illustration)" loading="lazy">
      <div><span class="eyebrow">Tonte et taille</span><h2 id="h-p4">Pelouses et haies au fil des saisons</h2><p>La tonte et la taille gardent votre jardin net, saison après saison. Décrivez votre terrain, vous obtenez un devis adapté.</p></div>
    </div>
  </div>
</section>

<section class="sec s-sage" aria-labelledby="h-ext">
  <div class="wrap">
    <div class="row rev" id="p5">
      <img src="images/r2.jpg" %s alt="Terrasse en bois en cours de pose devant une maison en pierre (image d’illustration)" loading="lazy">
      <div><span class="eyebrow">Aménagement extérieur</span><h2 id="h-ext">Vos abords mis en valeur</h2><p>Un extérieur bien pensé prolonge la maison. Parlez-nous de l’espace à aménager, nous étudions le projet avec vous.</p></div>
    </div>
  </div>
</section>

<section class="sec s-cream" aria-label="Ambiances">
  <div class="wrap">
    <div class="gal3" aria-label="Ambiances de jardin (images d’illustration)">
      <img src="images/g1.jpg" %s alt="Évacuation de déchets verts après un chantier (image d’illustration)" loading="lazy">
      <img src="images/g2.jpg" %s alt="Nettoyage d’un massif avec une brouette (image d’illustration)" loading="lazy">
      <img src="images/g3.jpg" %s alt="Allée, pelouse et massifs d’un jardin (image d’illustration)" loading="lazy">
    </div>
    <div class="band b-leaf"><div><h2>Parlons de votre jardin</h2><p>Un appel suffit pour décrire votre projet.</p></div><div class="actions"><a class="btn btn-rope" href="tel:%s">Appeler maintenant</a><a class="btn btn-line" href="contact.html">Écrire un message</a></div></div>
  </div>
</section>
'''%(COM,NOM,TELI,TEL,wh('f1.jpg'),wh('f2.jpg'),wh('f3.jpg'),
 card(1,I_SPADE,'Création de jardin','Conception et aménagement de votre espace vert, selon votre terrain et vos envies.'),
 card(2,I_LEAF,'Plantation','Arbustes, massifs et végétaux installés avec soin.'),
 card(3,I_SUN,'Entretien d’espaces verts','Un suivi régulier pour garder un jardin net et agréable.'),
 wh('r1.jpg'),wh('r2.jpg'),wh('g1.jpg'),wh('g2.jpg'),wh('g3.jpg'),TELI)+tail()
open(D+'/prestations.html','w',encoding='utf8').write(h)
# ENTREPRISE
h=head('L’entreprise · %s à %s'%(NOM,COM),'%s, entreprise de services d’aménagement paysager dirigée par Coralie Michel, à %s.'%(NOM,COM))+hdr('entreprise.html')
h+='''<section class="sec dark rings" aria-labelledby="h1">
  <div class="wrap story">
    <div>
      <span class="eyebrow">L’entreprise</span>
      <h1 id="h1">%s, paysagiste à Bullion</h1>
      <p style="margin-top:1.2rem">%s est une entreprise de services d’aménagement paysager basée à Bullion, dans les Yvelines. Elle est dirigée par Coralie Michel.</p>
      <p class="sig">Coralie Michel, dirigeante</p>
      <div class="actions"><a class="btn btn-rope" href="contact.html">Nous contacter</a></div>
    </div>
  </div>
</section>

<section class="sec s-sage" aria-labelledby="h-who">
  <div class="wrap">
    <div class="head"><span class="eyebrow">En bref</span><h2 id="h-who">Quelques repères sur l’entreprise</h2></div>
    <div class="cards3">
      <article class="card c-white">%s<h3>Dirigeante</h3><p>Coralie Michel dirige l’entreprise.</p></article>
      <article class="card c-white">%s<h3>Activité</h3><p>Services d’aménagement paysager : création, plantation et entretien d’espaces verts.</p></article>
      <article class="card c-white">%s<h3>Localisation</h3><p>Bullion, dans les Yvelines (78).</p></article>
    </div>
  </div>
</section>

<section class="sec s-cream" aria-labelledby="h-proj">
  <div class="wrap">
    <div class="row rev">
      <img src="images/r3.jpg" %s alt="Jardinier aménageant un massif devant une maison moderne (image d’illustration)" loading="lazy">
      <div><span class="eyebrow">Votre projet</span><h2 id="h-proj">Un projet de jardin à Bullion ?</h2><p>Appelez le %s ou utilisez le formulaire de demande de devis : décrivez votre besoin en quelques lignes.</p><div class="actions" style="margin-top:1.2rem"><a class="btn btn-green" href="contact.html">Demander un devis</a><a class="btn btn-rope" href="tel:%s">Appeler le %s</a></div></div>
    </div>
  </div>
</section>
'''%(NOM,NOM,ic(I_USER),ic(I_LEAF),ic(I_PIN),wh('r3.jpg'),TEL,TELI,TEL)+tail()
open(D+'/entreprise.html','w',encoding='utf8').write(h)
# CONTACT
h=head('Contact · %s à %s'%(NOM,COM),'Contactez %s à %s : demande de devis en ligne ou appel au %s.'%(NOM,COM,TEL))+hdr('contact.html')
h+='''<section class="sec s-cream" style="padding-block:clamp(2.5rem,6vw,4rem) 1rem;min-height:0" aria-labelledby="h1">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Contact · %s</span><h1 id="h1">Parlons de votre projet</h1><p>Décrivez votre besoin en quelques lignes : vous obtenez un message prêt à envoyer par SMS ou à copier.</p></div>
  </div>
</section>

<section class="sv sk sk8" aria-labelledby="sv-k"><div class="hv-wrap"><div class="sk8-h"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Quelques lignes suffisent pour décrire votre jardin et votre besoin.</p></div><div class="sk-card"><form class="sk-form" id="kform" novalidate data-name="%s" data-sms="%s" data-tel="%s" data-email=""><div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div><div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div><div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div><div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option><option>Création de jardin</option><option>Plantation</option><option>Entretien d’espaces verts</option><option>Tonte et taille</option><option>Autre demande</option></select><p class="sk-err" id="k-besoin-e" role="alert"></p></div><div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div><button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form><div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l'envoyer. Rien n'est transmis tant que vous n'avez pas validé l'envoi.</p><pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a><button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a><a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div><aside class="sk-side"><ul><li><span>Téléphone</span><a href="tel:%s">%s</a></li><li><span>Commune</span><p>%s</p></li></ul></aside></div></section>
'''%(COM,NOM,TELI,TELI,TELI,TEL,COM)+tail(True)
open(D+'/contact.html','w',encoding='utf8').write(h)
open(D+'/README.md','w',encoding='utf8').write('# %s (maquette)\n\nMaquette de site vitrine, non officielle. Pages : accueil, prestations, entreprise, contact.\n'%NOM)
print('ok',SZ)
