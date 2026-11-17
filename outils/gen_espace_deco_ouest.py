import os,re,sys,subprocess
from PIL import Image,ImageDraw
D='/home/claude/maquettes/espace-deco-ouest'
SRC='/mnt/user-data/uploads/Maquettes/Images/Paysagiste/'
MODS='/home/claude/mods/'
os.makedirs(D+'/images',exist_ok=True)
def img(src,out,box=None,size=None,q=80):
    im=Image.open(SRC+src).convert('RGB')
    if box:im=im.crop(box)
    if size:im=im.resize(size,Image.LANCZOS)
    im.save(D+'/images/'+out,quality=q,optimize=True,progressive=True)
    return im.size
W,H=1000,546
img('robot tonte de pelouse.jpg','hero.jpg',size=(1400,764))
img('conception chantier.jpg','p1.jpg',box=(380,0,1148,768),size=(900,900))
img('imgi_4_creation-espace-vert.jpg','a1.jpg',box=(600,0,1240,768),size=(1000,1200))
img('chantier allée dallée.jpg','c1.jpg',size=(1600,900),q=58)
img('imgi_4_creation-espace-vert.jpg','creation.jpg',size=(W,H))
img('chantier terrasse en bois.jpg','terrasse.jpg',size=(W,H))
img('maçonerie paysagère.jpg','maconnerie.jpg',size=(W,H))
img('conception chantier.jpg','plan.jpg',box=(400,100,1408,650),size=(W,H))
img('conception chantier.jpg','muret.jpg',box=(0,60,1008,610),size=(W,H))
img('chantier allée dallée.jpg','allee.jpg',box=(0,218,1008,768),size=(W,H))
img('chantier terrasse en bois.jpg','deck.jpg',box=(400,0,1408,550),size=(W,H))
img('robot tonte de pelouse.jpg','robot.jpg',box=(400,218,1408,768),size=(W,H))
img('imgi_4_creation-espace-vert.jpg','massif.jpg',box=(0,218,1008,768),size=(W,H))
img('maçonerie paysagère.jpg','contact.jpg',box=(200,0,840,768))
im=Image.new('RGBA',(64,64),(0,0,0,0));d=ImageDraw.Draw(im)
d.rounded_rectangle((0,0,63,63),14,fill='#12474f');d.ellipse((14,14,50,50),fill='#e0a02e');d.ellipse((24,24,40,40),fill='#12474f')
im.save(D+'/favicon.png')

TEL='+33777141287';TELT='07 77 14 12 87';TEL2='+33130305358';TEL2T='01 30 30 53 58'
MAIL='espace.deco@espacedeco.com';NOM='ESPACE DECO OUEST'
URL='https://webaunet.github.io/maquettes/espace-deco-ouest/'
FONTS='https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,600..800,100&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap'
def head(title,desc):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#12474f">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''
def header(cur):
    def li(h,t):return f'<li><a href="{h}"'+(' aria-current="page"' if h==cur else '')+f'>{t}</a></li>'
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="{URL}" aria-label="Espace Déco Ouest, accueil">
      <span><b>ESPACE DECO OUEST</b><small>Aménagement paysager · Buc</small></span>
    </a>
    <nav id="menu" aria-label="Navigation principale"><ul>{li('index.html','Accueil')}{li('services.html','Prestations')}{li('contact.html','Contact')}</ul></nav>
    <a class="call" href="tel:{TEL}" aria-label="Appeler le {TELT}">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>
      <span>{TELT}</span>
    </a>
    <button class="burger" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </div>
</header>

<main id="contenu">
'''
def rd(n):
    t=open(MODS+n+'.html',encoding='utf8').read()
    return re.sub(r'<!-- CONSIGNES.*?-->\s*','',t,flags=re.S)
def sub(t,pairs):
    for a,b in pairs:
        assert a in t,a
        t=t.replace(a,b,1)
    return t
FOOT=sub(rd('F6'),[("<strong>Nom de l'entreprise</strong><p>Une phrase de présentation.</p>","<strong>ESPACE DECO OUEST</strong><p>Aménagement paysager à Buc (78).</p>"),
 ('<a href="prestations.html">Prestations</a><a href="a-propos.html">À propos</a>','<a href="services.html">Prestations</a>'),
 ('href="tel:+33000000000">00 00 00 00 00','href="tel:%s">%s'%(TEL,TELT)),
 ('mailto:contact@exemple.fr">contact@exemple.fr','mailto:%s">%s'%(MAIL,MAIL)),
 ('<p>Adresse de la fiche</p>','<p>Chemin des Villaroy aux Loges, 78530 Buc</p>'),
 ("© Nom de l'entreprise · Maquette de démonstration","© Espace Déco Ouest · Maquette de démonstration")])
def tail(extra=''):
    return '</main>\n'+FOOT+'\n<div class="toast" id="toast" role="status" aria-live="polite"></div>\n<script src="script.js"></script>\n'+extra+'</body>\n</html>\n'

# ---------- ACCUEIL
h=sub(rd('H9'),[('Paysagiste à Commune (00)','Aménagement paysager à Buc (78)'),('Titre principal du site','Votre jardin, pensé et aménagé à Buc'),
 ("Deux phrases concrètes sur l'activité et la zone d'intervention.","Espace Déco Ouest est une entreprise d'aménagement paysager installée à Buc, dans les Yvelines. Parlez-nous de votre projet."),
 ('alt="Texte alternatif exact"','alt="Jardin engazonné avec un muret de pierre, un massif fleuri, une allée en dalles et une tondeuse robot, devant une maison" width="1400" height="764"'),
 ('width="1400" height="900" alt','alt'),
 ('href="tel:+33000000000">Appeler le 00 00 00 00 00','href="tel:%s">Appeler le %s'%(TEL,TELT)),('prestations.html','services.html'),
 ("<li><strong>20 ans</strong> d'expérience</li><li><strong>Devis</strong> gratuit</li>","<li><strong>Depuis 2017</strong></li><li><strong>10 à 19</strong> salariés</li>")])
h=h.replace('width="1400" height="764" width="1400" height="900"','width="1400" height="764"')
v=rd('V6')
v=sub(v,[('Titre de la section','Du projet au jardin terminé'),('Une phrase d\'introduction.','Cinq domaines pour aménager et entretenir votre extérieur.'),
 ('alt="Texte alternatif exact"','alt="Plan de jardin affiché sur une tablette, avec un muret de pierre et des massifs en arrière-plan"'),
 ('<h3>Prestation phare</h3><p>Deux phrases concrètes.</p><a href="prestations.html#p1">','<h3>Conception du jardin</h3><p>Un jardin pensé selon votre terrain et vos envies, avant tout chantier.</p><a href="services.html#creer">'),
 ('<h3>Prestation 2</h3><p>Deux phrases concrètes.</p><a href="prestations.html#p2">','<h3>Plantations et massifs</h3><p>Massifs, arbustes et pelouse installés avec soin.</p><a href="services.html#creer">'),
 ('<h3>Prestation 3</h3><p>Deux phrases concrètes.</p><a href="prestations.html#p3">','<h3>Terrasses et allées</h3><p>Terrasses en bois, allées dallées ou pavées pour votre extérieur.</p><a href="services.html#amenager">'),
 ('<h3>Prestation 4</h3><p>Deux phrases concrètes.</p><a href="prestations.html#p4">','<h3>Murets et maçonnerie</h3><p>Murets, marches et ouvrages en pierre intégrés au jardin.</p><a href="services.html#amenager">'),
 ('<h3>Prestation 5</h3><p>Deux phrases concrètes.</p><a href="prestations.html#p5">','<h3>Entretien du jardin</h3><p>Tonte et suivi régulier pour garder pelouse et massifs en forme.</p><a href="services.html#entretenir">')])
a=sub(rd('A7'),[('alt="Texte alternatif exact"','alt="Jardinière plantant dans un massif au bord d\'une pelouse, devant une maison contemporaine"'),
 ('Titre de la section','Une entreprise de paysage à Buc'),
 ('Un paragraphe concret et vérifié sur l\'entreprise.',"Espace Déco Ouest, SARL dirigée par Gérard Poupenay, exerce depuis 2017 dans l'aménagement paysager à Buc."),
 ('Un second paragraphe.',"Pour un projet de jardin ou d'extérieur, vous échangez directement avec l'entreprise par téléphone ou par e-mail."),
 ('<strong>Atout 1</strong> : une phrase.','<strong>Créée en 2017</strong> : SARL basée à Buc.'),('<strong>Atout 2</strong> : une phrase.','<strong>Équipe</strong> : 10 à 19 salariés en 2024.'),
 ('<strong>Atout 3</strong> : une phrase.','<strong>Contact direct</strong> : téléphone ou e-mail.'),('Prénom Nom, dirigeant','Gérard Poupenay, dirigeant')])
c=sub(rd('C3'),[('Une phrase d\'invitation à demander un devis.',"Décrivez votre projet à Espace Déco Ouest : l'entreprise vous répond par téléphone ou par e-mail."),
 ('href="tel:+33000000000">Appeler le 00 00 00 00 00','href="tel:%s">Appeler le %s'%(TEL,TELT))])
open(D+'/index.html','w',encoding='utf8').write(head('Espace Déco Ouest, aménagement paysager à Buc (78) | Jardins et extérieurs','Espace Déco Ouest, entreprise d\'aménagement paysager à Buc (78) : conception de jardin, plantations, terrasses, murets et entretien. Contactez-nous par téléphone ou e-mail.')+header('index.html')+h+'\n'+v+'\n'+a+'\n'+c+'\n'+tail())

# ---------- PRESTATIONS
def tk(l):return '<ul class="ticks">'+''.join(f'<li>{x}</li>' for x in l)+'</ul>'
def fig(s,w,hh,alt,lazy=True):return f'<figure><img src="images/{s}" width="{w}" height="{hh}" alt="{alt}"'+(' loading="lazy"' if lazy else '')+'></figure>'
S=f'''  <section class="phead bg-palm" aria-labelledby="t-h">
    <div class="wrap g2">
      <div>
        <span class="eyebrow">Prestations</span>
        <h1 id="t-h">Un jardin conçu, aménagé, entretenu</h1>
        <p class="lead">Conception, plantations, terrasses, murets et entretien : les domaines d'Espace Déco Ouest à Buc.</p>
        <div class="actions"><a class="btn btn-sun" href="tel:{TEL}">Appeler le {TELT}</a><a class="btn btn-line" href="contact.html">Demander un devis</a></div>
      </div>
      <div class="trio">
        {fig('creation.jpg',W,H,"Jardinière plantant dans un massif au bord d'une pelouse courbe, devant une maison contemporaine",False)}
        {fig('terrasse.jpg',W,H,"Pose d'une terrasse en bois devant une maison en pierre aux volets bleus",False)}
        {fig('maconnerie.jpg',W,H,"Ouvrier montant un muret et des marches en pierre dans un jardin, devant une maison",False)}
      </div>
    </div>
  </section>

  <section class="band bg-chalk" id="creer" aria-labelledby="t-creer">
    <div class="wrap split">
      <div>
        <span class="eyebrow">Créer</span>
        <h2 id="t-creer">Conception et plantations</h2>
        <p>Un jardin pensé selon votre terrain et vos envies, puis planté : massifs, arbustes et pelouse.</p>
        {tk(['Conception du jardin','Création de massifs','Plantation d\'arbustes'])}
        <div class="actions"><a class="btn btn-ink" href="contact.html">Parler de mon projet</a></div>
      </div>
      <div class="duo">{fig('plan.jpg',W,H,"Plan de jardin affiché sur une tablette, tenu à la main devant une table de jardin")}{fig('muret.jpg',W,H,"Pelouse bordée d'un muret de pierre et d'un massif de fleurs, devant une maison")}</div>
    </div>
  </section>

  <section class="band bg-sand" id="amenager" aria-labelledby="t-am">
    <div class="wrap split rev">
      <div>
        <span class="eyebrow">Aménager</span>
        <h2 id="t-am">Terrasses, allées et murets</h2>
        <p>Les ouvrages qui structurent l'extérieur : bois, dalles, pavés et pierre.</p>
        {tk(['Terrasses en bois','Allées dallées ou pavées','Murets et marches en pierre'])}
        <div class="actions"><a class="btn btn-ink" href="contact.html">Demander un devis</a></div>
      </div>
      <div class="duo">{fig('deck.jpg',W,H,"Terrasse en bois en cours de pose le long d'une maison en pierre")}{fig('allee.jpg',W,H,"Allée en dalles de pierre éclairée au crépuscule devant une maison en pierre")}</div>
    </div>
  </section>

  <section class="band bg-lawn" id="entretenir" aria-labelledby="t-ent">
    <div class="wrap split">
      <div>
        <span class="eyebrow">Entretenir</span>
        <h2 id="t-ent">Un jardin suivi dans la durée</h2>
        <p>Le suivi régulier qui garde pelouse et massifs en forme.</p>
        {tk(['Tonte de la pelouse','Entretien des massifs','Tondeuse robot'])}
        <div class="actions"><a class="btn btn-sun" href="tel:{TEL}">Appeler le {TELT}</a></div>
      </div>
      <div class="pair">{fig('robot.jpg',W,H,"Tondeuse robot sur une pelouse, le long d'une allée en dalles et d'un muret fleuri")}{fig('massif.jpg',W,H,"Massif d'arbustes et de graminées bordé de paillage, au bord d'une pelouse")}</div>
    </div>
  </section>

  <section class="band band-ink cta2" id="contact" aria-labelledby="t-c">
    <div class="wrap g2">
      <div>
        <span class="eyebrow">Votre projet</span>
        <h2 id="t-c">Parlons de votre jardin</h2>
        <p>Décrivez votre projet à Espace Déco Ouest : l'entreprise vous répond directement.</p>
        <a class="tel2" href="tel:{TEL}">{TELT}</a>
        <div class="actions"><a class="btn btn-sun" href="contact.html">Écrire un message</a><a class="btn btn-line" href="tel:{TEL}">Appeler</a></div>
      </div>
      <div class="stack-img">{fig('plan.jpg',W,H,"Plan de jardin affiché sur une tablette, tenu à la main").replace('<figure>','').replace('</figure>','')}</div>
    </div>
  </section>
'''
open(D+'/services.html','w',encoding='utf8').write(head('Prestations paysagères à Buc (78) | Espace Déco Ouest','Prestations d\'Espace Déco Ouest à Buc (78) : conception de jardin, plantations, terrasses, allées, murets en pierre et entretien du jardin.')+header('services.html')+S+tail())

# ---------- CONTACT
k=sub(rd('K1'),[('Nom de l\'entreprise" data-sms="+33000000000" data-tel="+33000000000" data-email=""','ESPACE DECO OUEST" data-sms="%s" data-tel="%s" data-email="%s"'%(TEL,TEL,MAIL)),
 ('Une phrase d\'introduction.','Décrivez votre projet : vous choisissez ensuite comment envoyer votre demande à Espace Déco Ouest.'),
 ('<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>','<option>Conception de jardin</option><option>Plantations et massifs</option><option>Terrasse ou allée</option><option>Muret ou maçonnerie</option><option>Entretien du jardin</option>'),
 ('<li><span>Téléphone</span><a href="tel:+33000000000">00 00 00 00 00</a></li>',f'<li><span>Téléphone</span><a href="tel:{TEL}">{TELT}</a><a href="tel:{TEL2}">{TEL2T}</a></li>'),
 ('mailto:contact@exemple.fr">contact@exemple.fr','mailto:%s">%s'%(MAIL,MAIL)),('<p>Adresse de la fiche</p>','<p>Chemin des Villaroy aux Loges, 78530 Buc</p>')])
C=f'''  <section class="phead compact bg-palm" aria-labelledby="t-h">
    <div class="wrap g2">
      <div>
        <span class="eyebrow">Contact</span>
        <h1 id="t-h">Parlons de votre jardin</h1>
        <p class="lead">Un projet d'aménagement paysager à Buc ou aux alentours ? Écrivez à Espace Déco Ouest ou appelez.</p>
        <div class="actions"><a class="btn btn-sun" href="tel:{TEL}">Appeler</a><a class="btn btn-line" href="#kform">Écrire un message</a></div>
      </div>
      <div class="arch">
        <div class="frame"><img src="images/contact.jpg" width="640" height="768" alt="Ouvrier montant un muret et des marches en pierre dans un jardin" style="object-position:50% 50%"></div>
      </div>
    </div>
  </section>

'''
open(D+'/contact.html','w',encoding='utf8').write(head('Contact et demande de devis à Buc (78) | Espace Déco Ouest','Contactez Espace Déco Ouest à Buc (78) pour votre projet de jardin : formulaire de demande de devis, téléphone et e-mail.')+header('contact.html')+C+k+'\n'+tail('<script src="js/k.js" defer></script>\n'))

# ---------- CSS racine (ciblé)
p=D+'/style.css';s=open(p,encoding='utf8').read()
if '--palm:#173f2a' in s:
    for a,b in [('--ink:#0d1d14','--ink:#112a2e'),('--palm:#173f2a','--palm:#12474f'),('--lawn:#2c7a2c','--lawn:#12474f'),('--sun:#f4c430','--sun:#e0a02e'),('--sun-d:#e0b020','--sun-d:#c98f22'),
     ('--chalk:#f8f7f2','--chalk:#f2f7f6'),('--sand:#ece6d3','--sand:#d9ebe7'),('--stone:#dfe7dc','--stone:#d9ebe7'),('--text:#17271e','--text:#112a2e'),('--soft:#44574b','--soft:#44595c')]:
        assert a in s,a;s=s.replace(a,b,1)
    s+='\n.phead.compact{min-height:0}\n@media(min-width:620px) and (max-width:999px){.split .duo figure:nth-child(2),.split .pair figure:nth-child(2){display:none}.split .duo img,.split .pair img{aspect-ratio:5/2;object-fit:cover;width:100%;height:auto;max-height:260px}.split .duo{min-height:0!important;height:auto!important;aspect-ratio:auto!important;display:block!important}.band{padding-block:48px}}\n@media(max-width:820px){.hf6-b p,.hf6-h{display:none}.hf6-g{display:flex;flex-wrap:wrap;gap:6px 22px;align-items:center}.hf6-b{flex:1 1 100%}.hf6-n nav,.hf6-c,.hf6-a{display:flex;flex-wrap:wrap;gap:0 18px}.hf6-a p{margin:0}.hf .hf-cop{margin-top:8px}}\n@media(max-width:560px){.hf6-c a[href^=mailto]{display:none}}\n'
    open(p,'w',encoding='utf8').write(s)
for f in ('realisations.html','_SKELETON.md'):
    if os.path.exists(D+'/'+f):os.remove(D+'/'+f)
open(D+'/README.md','w',encoding='utf8').write('# Espace Déco Ouest (Buc, 78)\n\nMaquette de site vitrine (squelette S19) : accueil, prestations, contact. Maquette de démonstration, non publiée.\n')
print('ok',sorted(os.listdir(D)))

j=D+'/script.js';t=open(j,encoding='utf8').read()
t=t.replace("'06 05 50 79 47'","'%s'"%TELT).replace("'+33605507947'","'%s'"%TEL).replace("'andreipintilii96@gmail.com'","'%s'"%MAIL)
open(j,'w',encoding='utf8').write(t)

s=open(D+'/style.css',encoding='utf8').read();s=re.sub(r'^/\* Concept.*?\*/','/* Espace Déco Ouest : sections en dômes, photos en arche, bleu pétrole et ocre. */',s,count=1);open(D+'/style.css','w',encoding='utf8').write(s)
