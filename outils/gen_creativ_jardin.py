import os,re,shutil,zipfile,subprocess
from PIL import Image,ImageDraw,ImageFont
U='/mnt/user-data/uploads/Maquettes'
IM=U+'/Images/Paysagiste/'
MOD=U+'/Squelettes/Modules/'
D='/home/claude/maquettes/creativ-jardin'
NOM='Creativ-Jardin';COM='Tessancourt-sur-Aubette (78)';COMS='Tessancourt-sur-Aubette'
TEL='06 50 06 66 27';TELI='+33650066627'
URL='https://webaunet.github.io/maquettes/creativ-jardin/'
if os.path.exists(D):shutil.rmtree(D)
os.makedirs(D)
zipfile.ZipFile(U+'/Squelettes/S07.zip').extractall(D)
os.remove(D+'/_SKELETON.md');os.remove(D+'/realisations.html')
os.makedirs(D+'/images',exist_ok=True)
SZ={}
def pic(src,name,ratio,focus=.5,maxw=None,q=80):
    im=Image.open(IM+src).convert('RGB');w,h=im.size
    if w/h>ratio:
        nw=int(round(h*ratio));x=int((w-nw)*focus);im=im.crop((x,0,x+nw,h))
    else:
        nh=int(round(w/ratio));y=int((h-nh)*.5);im=im.crop((0,y,w,y+nh))
    if maxw and im.size[0]>maxw:im=im.resize((maxw,round(maxw*im.size[1]/im.size[0])),Image.LANCZOS)
    while True:
        im.save(D+'/images/'+name,quality=q,optimize=True,progressive=True)
        if os.path.getsize(D+'/images/'+name)<245000 or q<=50:break
        q-=5
    SZ[name]=im.size
pic('imgi_4_creation-espace-vert.jpg','hero-1.jpg',597/768,.5)
pic('imgi_7_entretien-jardin.jpg','hero-2.jpg',597/768,.5)
pic('imgi_6_plantation.jpg','hero-3.jpg',597/768,.45)
pic('conception chantier.jpg','m1.jpg',0.8,.5)
pic('imgi_2_tonte.jpg','k1.jpg',1400/600,.5)
pic('imgi_3_entretien-general.jpg','prestations-hero.jpg',16/9,.5)
pic('alléé pavés carrelage extérieure.jpg','allee-pave.jpg',16/9,.5,maxw=800)
pic('imgi_6_plantation.jpg','plantation-massif.jpg',16/9,.5,maxw=800)
pic('imgi_5_feuilles.jpg','feuilles.jpg',16/9,.5,maxw=800)
pic('imgi_1_taille-haies.jpg','taille-haies.jpg',16/9,.5,maxw=800)
fv=Image.new('RGB',(128,128),'#2c3e47');d=ImageDraw.Draw(fv)
try:ft=ImageFont.truetype('DejaVuSerif-Bold.ttf',84)
except Exception:ft=ImageFont.load_default()
d.text((64,66),'C',font=ft,fill='#ffffff',anchor='mm');fv.resize((64,64)).save(D+'/images/favicon.png')
def wh(n):return 'width="%d" height="%d"'%SZ[n]
# ---- skeleton CSS : palette 3, polices 1
p=D+'/css/style.css';s=open(p,encoding='utf8').read()
V={'bg':'#f3f5f2','bg2':'#e1e8e1','card':'#ffffff','ink':'#1c262b','muted':'#4b5a60','line':'#c9d3cb','band':'#2c3e47','band-ink':'#ffffff','band-muted':'#d3dde2','leaf':'#46763f','leaf-ink':'#ffffff','lime':'#46763f'}
for k,v in V.items():
    s,n=re.subn(r'(?<![\w-])(--%s:)\s*#[0-9a-fA-F]{3,8}'%re.escape(k),lambda m:m.group(1)+v,s,count=1);assert n==1,k
for a,b in [('Bricolage Grotesque','Fraunces'),('Figtree','Nunito Sans')]:
    assert s.count(a)>=1,a;s=s.replace(a,b)
s=re.sub(r'/\*[^*]*(Arbre|arbre|Fil|fil de|Puiselet)[^*]*\*/','/* Maquette */',s)
s,n=re.subn(r'color:\s*var\(--leaf\)','color:var(--band)',s);
s,n2=re.subn(r'color:\s*var\(--lime\)','color:var(--band)',s)
open(p,'w',encoding='utf8').write(s)
r=subprocess.run(['python3','-I',MOD+'mod.py',D,'H8','V2','A2','M3','C6','F1','K6','--bg','#f3f5f2','--bg2','#e1e8e1','--ink','#1c262b','--mu','#4b5a60','--main','#2c3e47','--acc','#46763f','--accink','#ffffff','--fh','Fraunces','--fb','Nunito Sans','--fw','700'],capture_output=True,text=True);print(r.stdout.strip());assert r.returncode==0,r.stderr
open(p,'a',encoding='utf8').write('\n/* maquette */\n.logo-txt{font-family:\'Fraunces\',Georgia,serif;font-weight:800;font-size:1.3rem;line-height:1.1;color:var(--band)}\n@media(max-width:980px){.row img{max-height:380px;object-fit:cover}}\n@media(max-width:620px){.sv2-list li{padding:12px 0!important}.sv2-list p{margin:.2rem 0 0!important}.sk6-ban{display:none}}\n')
# ---- JS skeleton : traces
jp=D+'/js/main.js';j=open(jp,encoding='utf8').read()
a="var TEL = '+33000000000', MAIL = 'contact@exemple.fr';";assert j.count(a)==1
j=j.replace(a,"var TEL = '%s', MAIL = '';"%TELI);open(jp,'w',encoding='utf8').write(j)
# ---- pieces
NAV=[('index.html','Accueil'),('prestations.html','Prestations'),('index.html#entreprise','L’entreprise'),('contact.html','Contact')]
def head(t,d,fonts=True):
    return '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#2c3e47">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,800&family=Nunito+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''%(t,d)
def hdr(cur):
    nav=''.join('<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if h==cur else '',l) for h,l in NAV)
    return '''<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="%s" aria-label="%s, accueil"><span class="logo-txt">%s</span></a>
    <nav class="nav" id="nav" aria-label="Navigation principale">%s</nav>
    <a class="btn btn--leaf hdr__call" href="tel:%s" aria-label="Appeler le %s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg><span>%s</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>

<main>
'''%(URL,NOM,NOM,nav,TELI,TEL,TEL)
def foot():
    return '''</main>

<div class="hf hf1" role="contentinfo"><div class="hv-wrap"><div><strong>%s</strong><p class="hf-desc">Création, aménagement et entretien d’espaces verts à %s.</p></div><nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a><a href="index.html#entreprise">L’entreprise</a><a href="contact.html">Contact</a></nav><div class="hf-c"><a href="tel:%s">%s</a></div><p class="hf-cop">© %s · %s · Maquette de démonstration</p></div></div>

'''%(NOM,COMS,TELI,TEL,NOM,COM)
def tail(k=False):return foot()+'<script src="js/main.js"></script>\n'+('<script src="js/k.js" defer></script>\n' if k else '')+'</body>\n</html>\n'
# ---- index : modules
mods={}
mods['H8']=open(MOD+'H8.html',encoding='utf8').read()
mods['V2']=open(MOD+'V2.html',encoding='utf8').read()
mods['A2']=open(MOD+'A2.html',encoding='utf8').read()
mods['M3']=open(MOD+'M3.html',encoding='utf8').read()
mods['C6']=open(MOD+'C6.html',encoding='utf8').read()
mods['K6']=open(MOD+'K6.html',encoding='utf8').read()
def strip_c(t):return re.sub(r'^<!-- CONSIGNES.*?-->\n?','',t,flags=re.S)
h=head('Creativ-Jardin · Paysagiste à %s'%COMS,'Creativ-Jardin, paysagiste à %s (78) : création, aménagement et entretien de jardins. Appelez le %s.'%(COMS,TEL))+hdr('index.html')
H8=strip_c(mods['H8'])
H8=H8.replace('Paysagiste à Commune (00)','Paysagiste à %s'%COM)
H8=H8.replace('Titre principal du site','Des espaces verts créés et entretenus avec soin.')
H8=H8.replace('Deux phrases concrètes sur l\'activité et la zone d\'intervention.','Creativ-Jardin conçoit, aménage et entretient vos espaces verts à %s et dans les environs.'%COMS)
H8=H8.replace('Appeler le 00 00 00 00 00','Appeler le %s'%TEL).replace('tel:+33000000000',"tel:%s"%TELI)
H8=H8.replace('<img src="images/hero-1.jpg" width="700" height="900" alt="Texte alternatif exact">','<img src="images/hero-1.jpg" %s alt="Espace vert nouvellement créé autour d’une maison (image d’illustration)">'%wh('hero-1.jpg'))
H8=H8.replace('<img src="images/hero-2.jpg" width="700" height="900" alt="Texte alternatif exact">','<img src="images/hero-2.jpg" %s alt="Pelouse et massifs d’un jardin entretenu (image d’illustration)">'%wh('hero-2.jpg'))
H8=H8.replace('<img src="images/hero-3.jpg" width="700" height="900" alt="Texte alternatif exact">','<img src="images/hero-3.jpg" %s alt="Jardinier plantant un végétal dans un massif (image d’illustration)">'%wh('hero-3.jpg'))
assert 'Texte alternatif' not in H8 and 'Titre principal' not in H8
V2=strip_c(mods['V2'])
V2=V2.replace('Titre de la section','Création, plantation et entretien de jardin').replace('Une phrase d\'introduction.','Les prestations de %s couvrent la création et l’entretien de vos espaces verts.'%NOM)
items=[('Création de jardin','Conception et aménagement de votre espace vert, selon votre terrain et vos envies.'),('Plantation','Arbustes, massifs et végétaux installés avec soin.'),('Entretien d’espaces verts','Un suivi régulier pour garder votre jardin net et agréable.'),('Tonte et taille de haies','Pelouses et haies entretenues au fil des saisons.')]
for i,(t,x) in enumerate(items,1):
    V2=V2.replace('<h3>Prestation %d</h3><p>Deux phrases concrètes.</p>'%i,'<h3>%s</h3><p>%s</p>'%(t,x))
assert 'Prestation' not in V2 and 'Deux phrases' not in V2
A2=strip_c(mods['A2'])
A2=A2.replace('<section class="sv sa2"','<section id="entreprise" class="sv sa2"',1)
A2=A2.replace('Une phrase forte qui résume l\'engagement de l\'entreprise.','%s est une entreprise d’aménagement paysager basée à %s.'%(NOM,COMS))
A2=A2.replace('Un paragraphe concret et vérifié sur l\'entreprise.','Dirigée par Patrice Bobeze, l’entreprise crée et entretient les espaces verts de particuliers dans la commune et ses environs, dans les Yvelines (78).')
A2=A2.replace('Prénom Nom, dirigeant','Patrice Bobeze, dirigeant')
A2=A2.replace('<li><strong>20 ans</strong>d\'expérience</li><li><strong>Devis</strong>gratuit</li><li><strong>Commune</strong>et alentours</li>','<li><strong>Tessancourt</strong>sur-Aubette (78)</li><li><strong>Création</strong>et entretien de jardins</li><li><strong>Espaces verts</strong>aménagement paysager</li>')
A2=A2.replace('>Une phrase','>Une phrase')
A2=A2.replace('<p class="hv-kick">À propos</p>','<p class="hv-kick">L’entreprise</p>')
assert 'Prénom' not in A2 and 'Devis' not in A2 and '20 ans' not in A2
M3=strip_c(mods['M3'])
M3=M3.replace('<img src="images/m1.jpg" width="800" height="1000" alt="Texte alternatif exact">','<img src="images/m1.jpg" %s alt="Plan d’aménagement d’un jardin étudié sur une tablette (image d’illustration)">'%wh('m1.jpg'))
M3=M3.replace('Notre méthode</p><h2 id="sv-m">Titre de la section</h2><p class="hv-lead">Une phrase d\'introduction.</p>','Notre méthode</p><h2 id="sv-m">Un projet de jardin, étape par étape</h2><p class="hv-lead">De la première discussion à l’entretien, chaque étape est expliquée.</p>')
for t,x in [('Étape 1','Échange : vous décrivez votre terrain et vos attentes.'),('Étape 2','Conseil : nous vous proposons les travaux adaptés.'),('Étape 3','Réalisation : les travaux sont menés avec soin.'),('Étape 4','Entretien : un suivi régulier si vous le souhaitez.')]:
    M3=M3.replace('<h3>%s</h3><p>Deux phrases concrètes.</p>'%t,'<h3>%s</h3><p>%s</p>'%(t.replace('Étape 1','Échange').replace('Étape 2','Conseil').replace('Étape 3','Réalisation').replace('Étape 4','Entretien'),x.split(' : ',1)[1]))
assert 'Étape' not in M3 and 'Deux phrases' not in M3 and 'Titre de' not in M3
C6=strip_c(mods['C6'])
C6=C6.replace('Un projet de jardin&nbsp;? Parlons-en.','Un projet de jardin&nbsp;? Parlons-en.').replace('Une phrase d\'invitation à demander un devis.','Appelez %s ou envoyez votre demande de devis en ligne.'%NOM)
C6=C6.replace('Appeler le 00 00 00 00 00','Appeler le %s'%TEL).replace('tel:+33000000000',"tel:%s"%TELI,2)
C6=C6.replace('<a class="hv-btn hv-btn-s" href="contact.html">','<a class="hv-btn hv-btn-s" href="contact.html">')
C6=re.sub(r'<ul class="sc6-l">.*?</ul>','<ul class="sc6-l"><li><a href="tel:%s">%s</a></li><li>%s</li></ul>'%(TELI,TEL,COM),C6,flags=re.S)
assert 'exemple' not in C6 and '00 00' not in C6
idx_body=H8+'\n\n'+V2+'\n\n'+A2+'\n\n'+M3+'\n\n'+C6+'\n\n'
h+=idx_body+'\n'+tail()
open(D+'/index.html','w',encoding='utf8').write(h)
# ---- prestations
def tile(i,img,alt,t,x,w,hh):return '<li class="tile" id="p%d"><a href="contact.html"><img src="images/%s" width="%d" height="%d" loading="lazy" alt="%s"><h3>%s</h3><p>%s</p></a></li>'%(i,img,w,hh,alt,t,x)
hp=head('Prestations · %s à %s'%(NOM,COMS),'Prestations de %s à %s : création de jardin, plantation, entretien d’espaces verts, tonte et taille de haies.'%(NOM,COMS))+hdr('prestations.html')
hp+='''<section class="hero" aria-labelledby="h1">
  <img class="hero__img" src="images/prestations-hero.jpg" %s alt="Jardin entretenu avec pelouse et massifs (image d’illustration)">
  <div class="wrap">
    <p class="eyebrow">Prestations · %s</p>
    <h1 id="h1">Création, plantation et entretien de vos espaces verts</h1>
    <p class="lead">%s conçoit votre jardin et l’entretient au fil des saisons.</p>
    <div class="hero__cta">
      <a class="btn btn--leaf" href="tel:%s">Appeler le %s</a>
      <a class="btn btn--ghost" href="contact.html">Demander un devis</a>
    </div>
  </div>
</section>

<section class="sec sec--under" aria-labelledby="h-serv">
  <div class="wrap">
    <div class="sec__head">
      <p class="eyebrow">Nos prestations</p>
      <h2 id="h-serv">Quatre savoir-faire pour votre jardin</h2>
      <p>Du projet initial à l’entretien régulier, %s intervient sur votre espace vert.</p>
    </div>
    <ul class="tiles">
      %s
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="sec sec--lift on-band" aria-labelledby="h-cta">
  <div class="wrap">
    <div class="cta">
      <p class="eyebrow">Parlons de votre projet</p>
      <h2 id="h-cta">Un jardin à créer ou à entretenir ?</h2>
      <p>Décrivez-nous votre besoin, nous vous répondons pour convenir d’un rendez-vous.</p>
      <div class="cta__row">
        <a class="btn btn--leaf" href="tel:%s">Appeler le %s</a>
        <a class="btn btn--ghost" href="contact.html">Demander un devis</a>
      </div>
    </div>
  </div>
</section>
</main>

'''%(wh('prestations-hero.jpg'),COM,NOM,TELI,TEL,NOM,
 tile(1,'allee-pave.jpg','Allée en pavés de pierre bordée de massifs (image d’illustration)','Création de jardin',items[0][1],*SZ['allee-pave.jpg']),
 tile(2,'plantation-massif.jpg','Plantation d’un massif par un jardinier (image d’illustration)','Plantation',items[1][1],*SZ['plantation-massif.jpg']),
 tile(3,'feuilles.jpg','Ramassage de feuilles dans un massif (image d’illustration)','Entretien d’espaces verts',items[2][1],*SZ['feuilles.jpg']),
 tile(4,'taille-haies.jpg','Taille d’une haie au taille-haie (image d’illustration)','Tonte et taille de haies',items[3][1],*SZ['taille-haies.jpg']),
 TELI,TEL)
hp=hp.replace('<p>Du projet initial à l’entretien régulier, %s intervient sur votre espace vert.</p>'%NOM,'<p>Du projet initial à l’entretien régulier, %s intervient sur votre espace vert.</p>'%NOM)
hp=hp.replace('<p class="lead">%s conçoit votre jardin et l’entretient au fil des saisons.</p>'%NOM,'<p class="lead">%s conçoit votre jardin et l’entretient au fil des saisons.</p>'%NOM)
hp+=tail()
open(D+'/prestations.html','w',encoding='utf8').write(hp)
# ---- contact
hc=head('Contact · %s à %s'%(NOM,COMS),'Contactez %s à %s : demande de devis en ligne ou appel au %s.'%(NOM,COMS,TEL))+hdr('contact.html')
hc+='''<section class="sec sec--under" style="min-height:0" aria-labelledby="h1">
  <div class="wrap">
    <div class="sec__head">
      <p class="eyebrow">Contact · %s</p>
      <h1 id="h1">Parlons de votre projet</h1>
      <p>Décrivez votre besoin en quelques lignes : vous obtenez un message prêt à envoyer par SMS ou à copier.</p>
    </div>
  </div>
</section>

'''%COM
K=strip_c(mods['K6'])
K=K.replace('<img src="images/k1.jpg" width="1400" height="600" alt="Texte alternatif exact">','<img src="images/k1.jpg" %s alt="Pelouse fraîchement tondue devant un jardin (image d’illustration)">'%wh('k1.jpg'))
K=K.replace('<p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Une phrase d\'introduction.</p>','<p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Quelques lignes suffisent pour décrire votre jardin et votre besoin.</p>')
K=K.replace('data-name="Nom de l\'entreprise" data-sms="+33000000000" data-tel="+33000000000" data-email=""','data-name="%s" data-sms="%s" data-tel="%s" data-email=""'%(NOM,TELI,TELI))
K=K.replace('<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>','<option>Création de jardin</option><option>Plantation</option><option>Entretien d’espaces verts</option><option>Tonte et taille de haies</option>')
K=re.sub(r'<aside class="sk-side">.*?</aside>','<aside class="sk-side"><ul><li><span>Téléphone</span><a href="tel:%s">%s</a></li><li><span>Commune</span><p>%s</p></li></ul></aside>'%(TELI,TEL,COM),K,flags=re.S)
assert 'Besoin 1' not in K and '00 00' not in K and 'exemple' not in K and 'Une phrase' not in K
hc+=K+'\n'+'\n'
hc+=tail(True)
open(D+'/contact.html','w',encoding='utf8').write(hc)
open(D+'/README.md','w',encoding='utf8').write('# %s (maquette)\n\nMaquette de site vitrine, non officielle. Pages : accueil, prestations, contact.\n'%NOM)
print('ok',SZ)
