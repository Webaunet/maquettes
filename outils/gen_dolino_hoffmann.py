import os,re,shutil,zipfile,subprocess
from PIL import Image,ImageDraw,ImageFont
U='/mnt/user-data/uploads/Maquettes'
IM=U+'/Images/Paysagiste/'
MOD=U+'/Squelettes/Modules/'
D='/home/claude/maquettes/dolino-hoffmann'
NOM='Dolino Hoffmann';COM='Mantes-la-Jolie (78)';COMS='Mantes-la-Jolie'
TEL='06 86 01 85 98';TELI='+33686018598'
URL='https://webaunet.github.io/maquettes/dolino-hoffmann/'
if os.path.exists(D):shutil.rmtree(D)
os.makedirs(D)
zipfile.ZipFile(U+'/Squelettes/S10.zip').extractall(D)
os.remove(D+'/_SKELETON.md')
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
pic('imgi_7_entretien-jardin.jpg','hero.jpg',7/3,.5,maxw=1400)
pic('alléé pavés carrelage extérieure.jpg','p1.jpg',3/2,.5,maxw=900)
pic('imgi_6_plantation.jpg','p2.jpg',3/2,.5,maxw=900)
pic('conception chantier.jpg','a1.jpg',1,.5,maxw=700)
pic('imgi_1_taille-haies.jpg','c1.jpg',1,.5)
pic('imgi_4_creation-espace-vert.jpg','creation.jpg',4/3,.5,maxw=800)
pic('chantier terrasse en bois.jpg','terrasse.jpg',4/3,.5,maxw=800)
pic('maçonerie paysagère.jpg','maconnerie.jpg',4/3,.5,maxw=800)
pic('imgi_2_tonte.jpg','entretien.jpg',4/3,.5,maxw=800)
pic('imgi_5_feuilles.jpg','entreprise.jpg',1.8,.5,maxw=1000)
def wh(n):return 'width="%d" height="%d"'%SZ[n]
# ---- skeleton CSS : palette 2, polices 3
p=D+'/css/style.css';s=open(p,encoding='utf8').read()
V={'bg':'#f7efe4','bg2':'#ecdcc6','card':'#ffffff','ink':'#2b211b','muted':'#5f4f44','line':'#d6c7b1','band':'#7a3b22','band-ink':'#fff8ef','band-muted':'#e8d6c4','leaf':'#3f6b4f','leaf-ink':'#ffffff','link':'#7a3b22'}
for k,v in V.items():
    s,n=re.subn(r'(?<![\w-])(--%s:)\s*#[0-9a-fA-F]{3,8}'%re.escape(k),lambda m:m.group(1)+v,s,count=1);assert n==1,k
for a,b in [('Bricolage Grotesque','DM Serif Display'),('Figtree','Manrope')]:
    assert s.count(a)>=1,a;s=s.replace(a,b)
s=re.sub(r'/\*[^*]*(Artivert|Lenaik|Houilles)[^*]*\*/','/* Maquette */',s)
s,_=re.subn(r'color:\s*var\(--leaf\)','color:var(--band)',s)
open(p,'w',encoding='utf8').write(s)
r=subprocess.run(['python3','-I',MOD+'mod.py',D,'H3','V5','A4','M2','C7','F5','K3','--bg','#f7efe4','--bg2','#ecdcc6','--ink','#2b211b','--mu','#5f4f44','--main','#7a3b22','--acc','#3f6b4f','--accink','#ffffff','--fh','DM Serif Display','--fb','Manrope','--fw','400'],capture_output=True,text=True);print(r.stdout.strip());assert r.returncode==0,r.stderr
s=open(p,encoding='utf8').read()
# police à graisse unique : aucun faux gras
s,n=re.subn(r'font-weight:\s*(?:[6-9]00|bold|bolder)','font-weight:400',s);print('gras corrigés',n)
s,n2=re.subn(r'font:\s*(?:[6-9]00|bold)(?=\s)','font:400',s);print('graisses abrégées corrigées',n2)
s+='@media(min-width:800px){.sv5{padding:clamp(40px,5vw,72px) 0}.sv5-row figure{max-height:240px!important}}\n'
s+='\n/* maquette */\nh1,h2,h3,h4,b,strong,dt,th{font-weight:400}\n.logo span b{font-weight:400;color:var(--band)}\n.logo span{font-family:\'DM Serif Display\',Georgia,serif;font-size:1.3rem;line-height:1.1;color:var(--band)}\n@media(max-width:620px){.sv5-row img{aspect-ratio:16/9!important;height:auto!important;object-fit:cover}.sv5-row p{margin:.3rem 0!important}.sv5-more{display:none!important}.hf5-top{display:none!important}.hf5-top{padding:8px 0!important}.hf5-top strong{display:none}.hf5-b{padding:8px 0!important}.hf5-b nav{gap:2px 16px!important;margin:0 0 4px!important}.hf5-b .hf-cop{margin:0!important;font-size:1rem}.tile p{display:none}.tile img{aspect-ratio:16/10;height:auto}}\n'
open(p,'w',encoding='utf8').write(s)
# ---- JS skeleton : traces
jp=D+'/js/main.js';j=open(jp,encoding='utf8').read()
j=re.sub(r"var TEL = '[^']*', MAIL = '[^']*';","var TEL = '%s', MAIL = '';"%TELI,j)
a="pour Nom de l'entreprise";assert j.count(a)==1;j=j.replace(a,'pour '+NOM)
open(jp,'w',encoding='utf8').write(j)
# ---- pièces
NAV=[('index.html','Accueil'),('prestations.html','Prestations'),('entreprise.html','L’entreprise'),('contact.html','Contact')]
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%237a3b22'/%3E%3Cpath d='M16 26V14M16 18c-5 0-8-3-8-8 5 0 8 3 8 8zm0 2c0-4 3-7 8-7 0 5-3 7-8 7z' fill='%23f7efe4'/%3E%3C/svg%3E"
def head(t,d):
    return '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''%(t,d,FAV)
def hdr(cur):
    nav=''.join('<a href="%s"%s>%s</a>'%(h,' aria-current="page"' if h==cur else '',l) for h,l in NAV)
    return '''<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="%s" aria-label="%s, accueil"><span>Dolino <b>Hoffmann</b></span></a>
    <nav class="nav" id="nav" aria-label="Navigation principale">%s</nav>
    <a class="btn btn--leaf hdr__call" href="tel:%s" aria-label="Appeler le %s"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.8a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg><span>%s</span></a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>

<main>
'''%(URL,NOM,nav,TELI,TEL,TEL)
def foot(k=False):
    return '''</main>

<div class="hf hf5" role="contentinfo"><div class="hf5-top"><div class="hv-wrap"><strong>Un projet de jardin ? Demandez votre devis.</strong><a href="contact.html">Nous contacter</a></div></div><div class="hf5-b"><div class="hv-wrap"><nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a><a href="entreprise.html">L’entreprise</a><a href="contact.html">Contact</a></nav><p class="hf-cop">© %s · %s · Maquette de démonstration</p></div></div></div>

<script src="js/main.js"></script>
%s</body>
</html>
'''%(NOM,COM,'<script src="js/k.js" defer></script>\n' if k else '')
def strip_c(t):return re.sub(r'^<!-- CONSIGNES.*?-->\n?','',t,flags=re.S)
def M(n):return strip_c(open(MOD+n+'.html',encoding='utf8').read())
# ---- accueil
h=head('%s · Paysagiste à %s'%(NOM,COMS),'%s, paysagiste à %s (78) : création, aménagement et entretien de jardins. Appelez le %s.'%(NOM,COMS,TEL))+hdr('index.html')
H=M('H3')
H=H.replace('Paysagiste à Commune (00)','Aménagement paysager · %s'%COM)
H=H.replace('Titre principal du site','Des jardins créés, aménagés et entretenus avec soin')
H=H.replace("Deux phrases concrètes sur l'activité et la zone d'intervention.",'%s crée, aménage et entretient jardins et espaces verts à %s et dans les environs.'%(NOM,COMS))
H=H.replace('Appeler le 00 00 00 00 00','Appeler le %s'%TEL).replace('tel:+33000000000',"tel:%s"%TELI)
H=H.replace('<img src="images/hero.jpg" width="1400" height="600" alt="Texte alternatif exact">','<img src="images/hero.jpg" %s alt="Jardin entretenu avec allée, pelouse et massifs fleuris (image d’illustration)">'%wh('hero.jpg'))
H=H.replace('Intervient à Commune<span>et dans un rayon de 30 km</span>','Intervient à %s<span>Yvelines (78) et environs</span>'%COMS)
assert 'Texte alternatif' not in H and 'Titre principal' not in H and 'Commune' not in H
V=M('V5')
V=V.replace('Titre de la section','Création, aménagement et entretien de vos espaces verts').replace("Une phrase d'introduction.",'Des services d’aménagement paysager, de la conception de votre jardin à son entretien.')
V=V.replace('<img src="images/p1.jpg" width="900" height="600" alt="Texte alternatif exact">','<img src="images/p1.jpg" %s alt="Allée en pavés bordée de massifs (image d’illustration)">'%wh('p1.jpg'))
V=V.replace('<img src="images/p2.jpg" width="900" height="600" alt="Texte alternatif exact">','<img src="images/p2.jpg" %s alt="Plantation d’un massif par un jardinier (image d’illustration)">'%wh('p2.jpg'))
V=V.replace('<h3>Prestation 1</h3><p>Deux phrases concrètes sur cette prestation.</p>','<h3>Allées et dallages</h3><p>Pose d’allées et de dallages pour circuler agréablement dans votre jardin.</p>')
V=V.replace('<h3>Prestation 2</h3><p>Deux phrases concrètes sur cette prestation.</p>','<h3>Plantations</h3><p>Arbustes, massifs et végétaux installés avec soin, adaptés à votre terrain.</p>')
V=V.replace('<a href="prestations.html#p3">Prestation 3</a>','<a href="prestations.html#p3">Entretien du jardin</a>').replace('<a href="prestations.html#p4">Prestation 4</a>','<a href="prestations.html#p4">Terrasses en bois</a>').replace('<a href="prestations.html#p5">Prestation 5</a>','<a href="prestations.html#p5">Maçonnerie paysagère</a>')
V=V.replace('<span class="sv5-n">01</span>','<span class="sv5-n">01</span>')
assert 'Prestation ' not in V and 'Deux phrases' not in V and 'Texte alternatif' not in V
A=M('A4')
A=A.replace('<section class="sv sa4"','<section id="entreprise" class="sv sa4"',1)
A=A.replace('Titre de la section','%s, paysagiste à %s'%(NOM,COMS))
A=A.replace("Un paragraphe concret et vérifié sur l'entreprise.",'%s est une entreprise d’aménagement paysager basée à %s, dans les Yvelines (78).'%(NOM,COMS))
A=A.replace('Un second paragraphe.','Elle crée, aménage et entretient les espaces verts de la commune et de ses environs.')
A=A.replace('Prénom Nom, dirigeant','Dolino Hoffmann, dirigeant')
A=A.replace('<img src="images/a1.jpg" width="700" height="700" alt="Texte alternatif exact">','<img src="images/a1.jpg" %s alt="Plan d’aménagement de jardin étudié sur une tablette (image d’illustration)">'%wh('a1.jpg'))
A=A.replace('<p class="hv-kick">À propos</p>','<p class="hv-kick">L’entreprise</p>')
assert 'Titre de' not in A and 'Prénom' not in A and 'Texte alternatif' not in A and 'Un second' not in A
Mm=M('M2')
Mm=Mm.replace('Titre de la section','De l’échange à l’entretien').replace("Une phrase d'introduction.",'Chaque projet de jardin suit les mêmes étapes, expliquées avant d’être menées.')
for t,x in [('Étape 1','Échange : vous décrivez votre jardin et vos attentes.'),('Étape 2','Conseil : nous vous proposons les travaux adaptés à votre terrain.'),('Étape 3','Réalisation : les travaux sont menés avec soin.'),('Étape 4','Entretien : un suivi régulier si vous le souhaitez.')]:
    lab,txt=x.split(' : ',1)
    Mm=Mm.replace('<h3>%s</h3><p>Deux phrases concrètes.</p>'%t,'<h3>%s</h3><p>%s</p>'%(lab,txt))
assert 'Étape' not in Mm and 'Deux phrases' not in Mm and 'Titre de' not in Mm
C=M('C7')
C=C.replace('<img src="images/c1.jpg" width="900" height="900" alt="Texte alternatif exact">','<img src="images/c1.jpg" %s alt="Haie taillée dans un jardin (image d’illustration)">'%wh('c1.jpg'))
C=C.replace("Une phrase d'invitation à demander un devis.",'Appelez %s ou envoyez votre demande de devis en ligne : nous revenons vers vous.'%NOM)
C=C.replace('Appeler le 00 00 00 00 00','Appeler le %s'%TEL).replace('tel:+33000000000',"tel:%s"%TELI)
C=C.replace('<p class="sc7-add">Adresse de la fiche</p>','<p class="sc7-add">%s</p>'%COM)
assert '00 00' not in C and 'Adresse de la fiche' not in C and 'Une phrase' not in C
h+=H+'\n\n'+V+'\n\n'+A+'\n\n'+Mm+'\n\n'+C+'\n\n'+foot()
open(D+'/index.html','w',encoding='utf8').write(h)
# ---- prestations
def tile(i,img,alt,t,x,ww,hh):
    idattr=' id="p%d"'%i if i else ''
    return '<li class="tile"%s><img src="images/%s" %s loading="lazy" alt="%s"><h3>%s</h3><p>%s</p></li>'%(idattr,img,'width="%d" height="%d"'%(ww,hh),alt,t,x)
hp=head('Prestations · %s à %s'%(NOM,COMS),'Prestations de %s à %s : création, aménagement et entretien d’espaces verts, terrasses, allées et maçonnerie paysagère.'%(NOM,COMS))+hdr('prestations.html')
hp+='''<section class="sec sec--under" style="min-height:0" aria-labelledby="h1">
  <div class="wrap">
    <div class="sec__head">
      <p class="eyebrow">Prestations · %s</p>
      <h1 id="h1">Création, aménagement et entretien de vos espaces verts</h1>
      <p>De la conception de votre jardin à son entretien régulier, %s intervient à %s et dans les environs.</p>
      <div class="hero__cta" style="margin-top:1.4rem">
        <a class="btn btn--leaf" href="tel:%s">Appeler le %s</a>
        <a class="btn btn--ghost" href="contact.html">Demander un devis</a>
      </div>
    </div>
    <ul class="tiles">
      %s
      %s
      %s
    </ul>
  </div>
</section>

<section class="sec sec--lift" aria-labelledby="h-serv">
  <div class="wrap">
    <div class="sec__head">
      <p class="eyebrow">Nos prestations</p>
      <h2 id="h-serv">Aménagement et entretien au fil de l’année</h2>
      <p>Chaque intervention est adaptée à votre terrain et à vos envies.</p>
    </div>
    <ul class="tiles">
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
      <p>Appelez %s ou décrivez votre besoin, nous revenons vers vous.</p>
      <div class="cta__row">
        <a class="btn btn--leaf" href="tel:%s">Appeler le %s</a>
        <a class="btn btn--ghost" href="contact.html">Demander un devis</a>
      </div>
    </div>
  </div>
</section>

'''%(COMS,NOM,COMS,TELI,TEL,
 tile(4,'terrasse.jpg','Terrasse en bois en cours de pose devant une maison (image d’illustration)','Terrasses en bois','Une terrasse bien posée prolonge votre séjour dehors.',*SZ['terrasse.jpg']),
 tile(0,'creation.jpg','Jardin en cours de création avec pelouse et massifs (image d’illustration)','Création d’espaces verts','Conception et aménagement de votre espace vert, selon votre terrain.',*SZ['creation.jpg']),
 tile(5,'maconnerie.jpg','Muret de pierre et escalier de jardin (image d’illustration)','Maçonnerie paysagère','Murets, escaliers et ouvrages en pierre pour structurer le jardin.',*SZ['maconnerie.jpg']),
 tile(1,'p1.jpg','Allée en pavés bordée de massifs (image d’illustration)','Allées et dallages','Pose d’allées et de dallages pour circuler dans votre jardin.',*SZ['p1.jpg']),
 tile(2,'p2.jpg','Plantation d’un massif par un jardinier (image d’illustration)','Plantations','Arbustes, massifs et végétaux installés avec soin.',*SZ['p2.jpg']),
 tile(3,'entretien.jpg','Pelouse entretenue devant une maison (image d’illustration)','Entretien du jardin','Tonte, taille et désherbage pour garder votre jardin net.',*SZ['entretien.jpg']),
 COMS,TELI,TEL)
hp+=foot()
open(D+'/prestations.html','w',encoding='utf8').write(hp)
# ---- entreprise
he=head('L’entreprise · %s à %s'%(NOM,COMS),'%s, entreprise d’aménagement paysager à %s (78), dirigée par Dolino Hoffmann.'%(NOM,COMS))+hdr('entreprise.html')
he+='''<section class="sec sec--under" style="min-height:0" aria-labelledby="h1">
  <div class="wrap">
    <div class="sec__head">
      <p class="eyebrow">L’entreprise</p>
      <h1 id="h1">%s, paysagiste à %s</h1>
      <p>%s est une entreprise d’aménagement paysager basée à %s, dans les Yvelines (78). Elle est dirigée par Dolino Hoffmann.</p>
    </div>
  </div>
</section>

<section class="sec sec--lift on-band" aria-labelledby="h-about">
  <div class="wrap about">
    <figure class="about__img">
      <img src="images/entreprise.jpg" %s loading="lazy" alt="Jardin aux feuilles d’automne entretenu par une équipe (image d’illustration)">
      <figcaption>Illustration : entretien d’un espace vert.</figcaption>
    </figure>
    <div class="card">
      <p class="eyebrow">En bref</p>
      <h2 id="h-about">Une entreprise locale</h2>
      <dl class="facts">
        <div><dt>Dirigeant</dt><dd>Dolino Hoffmann</dd></div>
        <div><dt>Siège</dt><dd>%s</dd></div>
        <div><dt>Activité</dt><dd>Services d’aménagement paysager</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="sec sec--lift on-band" aria-labelledby="h-cta">
  <div class="wrap">
    <div class="cta">
      <p class="eyebrow">Un projet à confier ?</p>
      <h2 id="h-cta">Parlons de votre jardin</h2>
      <p>Appelez %s ou écrivez-nous depuis le formulaire de contact.</p>
      <div class="cta__row">
        <a class="btn btn--leaf" href="tel:%s">Appeler le %s</a>
        <a class="btn btn--ghost" href="contact.html">Demander un devis</a>
      </div>
    </div>
  </div>
</section>

'''%(NOM,COMS,NOM,COMS,wh('entreprise.jpg'),COM,NOM,TELI,TEL)
he+=foot()
open(D+'/entreprise.html','w',encoding='utf8').write(he)
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
K=M('K3')
K=K.replace('data-name="Nom de l\'entreprise" data-sms="+33000000000" data-tel="+33000000000" data-email=""','data-name="%s" data-sms="%s" data-tel="%s" data-email=""'%(NOM,TELI,TELI))
K=K.replace('<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>','<option>Création de jardin</option><option>Entretien de jardin</option><option>Plantation</option><option>Aménagement extérieur</option>')
K=re.sub(r'<aside class="sk-side">.*?</aside>','<aside class="sk-side"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Quelques lignes suffisent pour décrire votre jardin et votre besoin.</p><ul><li><span>Téléphone</span><a href="tel:%s">%s</a></li><li><span>Commune</span><p>%s</p></li></ul></aside>'%(TELI,TEL,COM),K,flags=re.S)
K=K.replace('<h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Une phrase d\'introduction.</p>','')
assert 'Besoin 1' not in K and '00 00' not in K and 'exemple' not in K and 'Une phrase' not in K and 'Adresse' not in K
hc+=K+'\n\n'+foot(True)
open(D+'/contact.html','w',encoding='utf8').write(hc)
open(D+'/README.md','w',encoding='utf8').write('# %s (maquette)\n\nMaquette de site vitrine, non officielle. Pages : accueil, prestations, entreprise, contact.\n'%NOM)
print('ok',SZ)
