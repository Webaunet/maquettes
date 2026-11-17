import os,re,shutil,subprocess,zipfile
from PIL import Image,ImageDraw,ImageFont
U='/mnt/user-data/uploads/Maquettes/'
IMG=U+'Images/Paysagiste/'
MOD=U+'Squelettes/Modules/'
D='/home/claude/maquettes/boisumeau-paysage/'
BASE='https://webaunet.github.io/maquettes/boisumeau-paysage/'
NOM='Boisumeau Paysage';TEL='06 14 51 01 81';TELH='+33614510181'
PAGES=[('index.html','Accueil'),('prestations.html','Prestations'),('contact.html','Contact')]
PHP='<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
SVP=f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PHP}</svg>'

# --- 1. squelette
if os.path.exists(D):shutil.rmtree(D)
os.makedirs(D)
zipfile.ZipFile(U+'Squelettes/S07.zip').extractall(D)
for f in ('_SKELETON.md','realisations.html','index.html','prestations.html','contact.html'):
    p=D+f
    if os.path.exists(p):os.remove(p)
os.makedirs(D+'images',exist_ok=True)

# --- 2. CSS : variables et polices (remplacements ciblés)
p=D+'css/style.css';s=open(p,encoding='utf8').read()
def rep(a,b):
    global s
    assert a in s,'cible absente: '+a[:50]
    s=s.replace(a,b,1)
rep('--bg:#f5f3ec; --bg2:#e6e5d6; --card:#ffffff; --ink:#1b2418; --muted:#4a5545; --line:#cfcdbb;','--bg:#f6f3e8; --bg2:#e8e6cf; --card:#ffffff; --ink:#23261a; --muted:#53563f; --line:#d4d0b4;')
rep('--band:#2e3c29; --band-ink:#f1f2e6; --band-muted:#c6cfb8;\n--leaf:#e0952f; --leaf-ink:#1f1608; --lime:#b5c81e; --sage:#7d8667; --link:#2e3c29;','--band:#3b4a1f; --band-ink:#f6f3e8; --band-muted:#d3d6b8;\n--leaf:#c4912a; --leaf-ink:#23261a; --lime:#8a9a4b; --sage:#7a8450; --link:#3b4a1f;')
rep('--c1:#e3ebb5; --c2:#cfdcc4; --c3:#f3d9b0; --c4:#d3dde0;','--c1:#e8e6cf; --c2:#e1e5c8; --c3:#f1e0b4; --c4:#dde3d6;')
rep('--shadow:0 10px 30px rgba(27,36,24,.12);','--shadow:0 10px 30px rgba(35,38,26,.12);')
rep('"Bricolage Grotesque","Trebuchet MS",system-ui,sans-serif','"DM Serif Display",Georgia,serif')
rep('"Figtree","Segoe UI",system-ui,sans-serif','"Manrope","Segoe UI",system-ui,sans-serif')
rep('--bg:#12170f; --bg2:#1a2116; --card:#212a1c; --ink:#ebeee1; --muted:#b0baa4; --line:#303b29;','--bg:#171910; --bg2:#20231a; --card:#2a2d20; --ink:#ecebd9; --muted:#bcbea3; --line:#3a3e2a;')
rep('--band:#2e3c29; --band-ink:#f1f2e6; --band-muted:#c6cfb8; --link:#d7e58a;','--band:#3b4a1f; --band-ink:#f6f3e8; --band-muted:#d3d6b8; --link:#e6c36a;')
rep('--c1:#3a4416; --c2:#26382a; --c3:#4a3718; --c4:#27363b;','--c1:#3a3e1f; --c2:#2b3a22; --c3:#4a3a16; --c4:#2c3a38;')
s=s.replace("/* Au fil de l'arbre — feuille commune. Concept : feuille et cime ; bandes sombres à bords courbes, cartes en forme de feuille. */",'/* Boisumeau Paysage : feuille commune */')
open(p,'w',encoding='utf8').write(s)

# --- 3. images
def img(src,dst,w,crop=None,q=80):
    i=Image.open(IMG+src).convert('RGB')
    if crop:i=i.crop(crop)
    if i.width>w:i=i.resize((w,round(i.height*w/i.width)),Image.LANCZOS)
    i.save(D+'images/'+dst,quality=q,optimize=True,progressive=True)
    return i.size
SZ={}
SZ['hero']=img('imgi_7_entretien-jardin.jpg','hero.jpg',1408,q=60)
SZ['conception']=img('conception chantier.jpg','conception.jpg',1000)
SZ['creation']=img('imgi_4_creation-espace-vert.jpg','creation.jpg',1000)
SZ['plantation']=img('imgi_6_plantation.jpg','plantation.jpg',1000)
SZ['haies']=img('imgi_1_taille-haies.jpg','haies.jpg',1000)
SZ['tonte']=img('imgi_2_tonte.jpg','tonte.jpg',1000)
SZ['terrasse']=img('chantier terrasse en bois.jpg','terrasse.jpg',1000)
SZ['feuilles']=img('imgi_5_feuilles.jpg','feuilles.jpg',1000)
# favicon
fv=Image.new('RGB',(64,64),'#3b4a1f');d=ImageDraw.Draw(fv)
try:f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',40)
except Exception:f=ImageFont.load_default()
d.text((32,32),'B',fill='#e6c36a',font=f,anchor='mm');fv.save(D+'images/favicon.png')
def im(k,alt,extra='',lazy=True):
    w,h=SZ[k];return f'<img src="images/{k}.jpg" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""} alt="{alt}"{extra}>'

# --- 4. pages
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
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''
def header(cur):
    nav=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a>' for h,n in PAGES)
    return f'''<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="{BASE}" aria-label="{NOM}, accueil">{NOM}</a>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      {nav}
    </nav>
    <a class="btn btn--leaf hdr__call" href="tel:{TELH}" aria-label="Appeler le {TEL}">{SVP}<span>{TEL}</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
  </div>
</header>

<main>
'''
def footer(k=False):
    li=''.join(f'<li><a href="{h}">{n}</a></li>' for h,n in PAGES)
    sc='<script src="js/main.js"></script>\n'+('<script src="js/k.js" defer></script>\n' if k else '')
    return f'''</main>
<footer class="hf hf4"><div class="hv-wrap"><div><strong>{NOM}</strong><p class="hf-desc">Aménagement paysager à Gif-sur-Yvette (91).</p></div><ul>{li}</ul><ul><li><a href="tel:{TELH}">{TEL}</a></li></ul><p class="hf-cop">© {NOM} · Maquette de démonstration</p></div></footer>
{sc}</body>
</html>
'''
def W(n,s):open(D+n,'w',encoding='utf8').write(s)
ICO='<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
LEAF='<path d="M12 21V11M12 11C12 6 8 4 4 4c0 4 2 7 8 7ZM12 14c0-4 3-6 8-6 0 4-2 7-8 6Z"/>'
PEN='<path d="M4 20h4L19 9a2.1 2.1 0 0 0-3-3L5 17z"/><path d="M14 7l3 3"/>'
CUT='<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>'
BOX='<path d="M3 17h18M5 17V9h14v8M9 9V5h6v4"/>'
SV=[('conception',PEN,'Conception de jardin','Un projet d’aménagement pensé à partir de votre terrain et de vos envies.'),
    ('plantations',LEAF,'Plantations et massifs','Création de massifs, plantation d’arbustes, de vivaces et d’arbres.'),
    ('entretien',CUT,'Entretien de jardin','Pelouse, haies et massifs suivis, ponctuellement ou régulièrement.'),
    ('terrasses',BOX,'Terrasses et allées','Terrasse en bois, allée et abords aménagés autour de la maison.')]
def v4():
    c=''.join(f'<div><div class="sv4-ico">{ICO%p}</div><h3>{t}</h3><p>{d}</p><a href="prestations.html#{i}">En savoir plus</a></div>' for i,p,t,d in SV)
    return f'<section class="sv sv4" id="prestations" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Du projet de jardin à son entretien</h2><p class="hv-lead">Décrivez votre terrain et vos envies : nous vous conseillons.</p>\n<div class="sv4-grid">{c}</div></div></section>\n'
def c6(h2='Un projet de jardin ? Parlons-en.',lead='Appelez-nous ou écrivez-nous : nous revenons vers vous pour votre devis.'):
    return f'<section class="sv sc6" id="contact" aria-labelledby="sv-c"><div class="hv-wrap"><div><p class="hv-kick">Contact</p><h2 id="sv-c">{h2}</h2><p class="hv-lead">{lead}</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="contact.html">Demander un devis</a></div></div><ul class="sc6-l"><li><a href="tel:{TELH}">{TEL}</a></li><li>Gif-sur-Yvette (91)</li></ul></div></section>\n'

def index():
    s=head('Boisumeau Paysage · Aménagement paysager à Gif-sur-Yvette (91)','Boisumeau Paysage, aménagement paysager à Gif-sur-Yvette (91) : conception de jardin, plantations, entretien, terrasses et allées. Appelez le 06 14 51 01 81.')+header('index.html')
    s+=f'''<section class="hv hv2 hv-dark" aria-labelledby="hv-t"><div class="hv2-bg">{im('hero','Jardin de campagne avec pelouse, massifs fleuris et allée de gravier devant une maison (image d’illustration)',lazy=False)}</div>
<div class="hv-wrap hv2-in"><p class="hv-kick">Aménagement paysager à Gif-sur-Yvette (91)</p><h1 id="hv-t">Un jardin aménagé et entretenu avec soin.</h1><p class="hv-lead">Stéphane Boisumeau conçoit, aménage et entretient les espaces extérieurs à Gif-sur-Yvette, en Essonne. Un seul interlocuteur, joignable par téléphone.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>
<ul class="hv-wrap hv2-stats"><li><strong>Stéphane Boisumeau</strong> dirigeant</li><li><strong>Gif-sur-Yvette</strong> Essonne (91)</li><li><strong>Aménagement</strong> et entretien de jardins</li></ul></section>
'''
    s+=v4()
    s+='''<section class="sv sa5" id="entreprise" aria-labelledby="sv-a"><div class="hv-wrap"><p class="hv-kick">L’entreprise</p><h2 id="sv-a">Boisumeau Paysage en bref</h2><p class="hv-lead">Quelques repères sur l’entreprise.</p><div class="sa5-grid"><article class="sa5-c"><span class="sa5-n">01</span><h3>Dirigeant</h3><p>L’entreprise est dirigée par Stéphane Boisumeau.</p></article><article class="sa5-c"><span class="sa5-n">02</span><h3>Activité</h3><p>Services d’aménagement paysager : conception, plantation et entretien d’espaces verts.</p></article><article class="sa5-c"><span class="sa5-n">03</span><h3>Localisation</h3><p>Basée à Gif-sur-Yvette, dans l’Essonne (91).</p></article></div></div></section>
'''
    s+=c6()+footer()
    W('index.html',s)

def ill(k,alt,cap=True):
    return f'<figure class="ill" style="margin:0">{im(k,alt+" (image d’illustration)")}<p class="src">Image d’illustration.</p></figure>'
def checks(l):return '<ul class="checks">'+''.join(f'<li>{x}</li>' for x in l)+'</ul>'
def prest():
    s=head('Prestations · Boisumeau Paysage à Gif-sur-Yvette (91)','Conception de jardin, plantations et massifs, entretien, terrasses et allées : les prestations de Boisumeau Paysage à Gif-sur-Yvette (91).')+header('prestations.html')
    ph=lambda k,a:f'<figure>{im(k,a+" (image d’illustration)",lazy=False)}</figure>'
    s+=f'''<section class="phead sec--under" aria-labelledby="h1">
  <div class="wrap phead__in">
    <div>
      <p class="eyebrow">Nos prestations</p>
      <h1 id="h1">Conception, plantations, entretien et terrasses</h1>
      <p class="lead">Quatre domaines pour aménager et entretenir votre jardin, à Gif-sur-Yvette et alentour.</p>
      <div class="hero__cta"><a class="btn btn--leaf" href="tel:{TELH}">{SVP}Appeler le {TEL}</a><a class="btn btn--ghost" href="contact.html">Demander un devis</a></div>
    </div>
    <div class="mosaic">
      {ph('creation','Jardinier posant une bordure dans un massif devant une maison moderne')}
      {ph('haies','Jardinier taillant une haie avec un taille-haie thermique')}
      {ph('tonte','Jardinier tondant une pelouse devant une maison')}
    </div>
  </div>
</section>

<section class="sec sec--lift sec--under sec--stone" id="conception" aria-labelledby="h-co">
  <div class="wrap split">
    {ill('conception','Plan de jardin affiché sur une tablette, devant une terrasse et un muret en pierre')}
    <div>
      <p class="eyebrow">Prestation 1</p>
      <h2 id="h-co">Conception de jardin</h2>
      <p class="mut">Un jardin réussi commence par un plan. Décrivez votre terrain et vos envies, nous vous conseillons.</p>
      {checks(['Étude de votre terrain','Plan d’aménagement','Choix des végétaux'])}
    </div>
  </div>
</section>

<section class="sec sec--lift sec--under" id="plantations" aria-labelledby="h-pl">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Prestation 2</p>
      <h2 id="h-pl">Plantations et massifs</h2>
      <p class="mut">Des massifs et des plantations adaptés à votre jardin et à votre exposition.</p>
      {checks(['Création de massifs','Plantation d’arbustes et de vivaces','Plantation d’arbres'])}
    </div>
    {ill('plantation','Jardinier plantant un arbuste dans un massif')}
  </div>
</section>

<section class="sec sec--lift sec--under on-band" id="entretien" aria-labelledby="h-en">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Prestation 3</p>
      <h2 id="h-en">Entretien de jardin</h2>
      <p class="mut">Un jardin agréable demande un suivi régulier, en intervention ponctuelle ou à intervalles réguliers.</p>
      {checks(['Tonte de la pelouse','Taille de haies et d’arbustes','Ramassage de feuilles','Désherbage des massifs'])}
    </div>
    <div class="pair">
      {im('haies','Jardinier taillant une haie devant une maison en pierre (image d’illustration)')}
      {im('feuilles','Jardinier ramassant des feuilles dans une allée de gravier (image d’illustration)')}
    </div>
  </div>
</section>

<section class="sec sec--lift sec--under sec--stone" id="terrasses" aria-labelledby="h-te">
  <div class="wrap split">
    {ill('terrasse','Terrasse en bois en cours de pose devant une maison en pierre')}
    <div>
      <p class="eyebrow">Prestation 4</p>
      <h2 id="h-te">Terrasses et allées</h2>
      <p class="mut">Des accès et des espaces de vie extérieurs soignés, pour profiter de votre jardin.</p>
      {checks(['Terrasse en bois','Allée','Aménagement des abords'])}
    </div>
  </div>
</section>

<section class="sec sec--lift on-band" aria-labelledby="h-fin">
  <div class="wrap">
    <div class="strip">
      <h2 id="h-fin">Un projet de jardin ?</h2>
      <p>Dites-nous ce dont vous avez besoin : nous revenons vers vous pour établir un devis.</p>
      <div class="cta__row"><a class="btn btn--dark" href="tel:{TELH}">{SVP}Appeler le {TEL}</a><a class="btn btn--ghost" href="contact.html">Demander un devis</a></div>
    </div>
  </div>
</section>
'''+footer()
    W('prestations.html',s)

def contact():
    s=head('Contact et demande de devis · Boisumeau Paysage à Gif-sur-Yvette (91)','Contactez Boisumeau Paysage, aménagement paysager à Gif-sur-Yvette (91) : téléphone ou formulaire de demande de devis.')+header('contact.html')
    s+=f'''<section class="chead sec--under" style="min-height:0" aria-labelledby="h1">
  <div class="wrap chead__in">
    <div>
      <p class="eyebrow">Contact</p>
      <h1 id="h1">Parlons de votre jardin</h1>
      <p class="lead">Décrivez votre projet : le récapitulatif se prépare en quelques secondes, vous l’envoyez par SMS.</p>
    </div>
    <figure class="chead__img">{im('feuilles','Jardinier ramassant des feuilles dans une allée de gravier (image d’illustration)',lazy=False)}<figcaption>Image d’illustration.</figcaption></figure>
  </div>
</section>
<section class="sv sk sk9" aria-labelledby="sv-k"><div class="hv-wrap sk9-w"><div class="sk9-h"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2></div><div class="sk-card"><form class="sk-form" id="kform" novalidate data-name="{NOM}" data-sms="{TELH}" data-tel="{TELH}" data-email=""><div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div><div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div><div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div><div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option><option>Conception de jardin</option><option>Plantations et massifs</option><option>Entretien de jardin</option><option>Terrasse ou allée</option><option>Autre demande</option></select><p class="sk-err" id="k-besoin-e" role="alert"></p></div><div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div><button class="hv-btn hv-btn-p sk-go" type="submit">Préparer ma demande</button></form><div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l'envoyer. Rien n'est transmis tant que vous n'avez pas validé l'envoi.</p><pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a><button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a><a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div><aside class="sk-side"><ul><li><span>Téléphone</span><a href="tel:{TELH}">{TEL}</a></li><li><span>Commune</span><p>Gif-sur-Yvette (91)</p></li></ul></aside></div></section>
'''+footer(True)
    W('contact.html',s)
index();prest();contact()

# --- 5. modules (CSS + k.js)
r=subprocess.run(['python3','-I',MOD+'mod.py',D,'H2','V4','A5','C6','F4','K9','--bg','#f6f3e8','--bg2','#e8e6cf','--ink','#23261a','--mu','#53563f','--main','#3b4a1f','--acc','#c4912a','--accink','#23261a','--fh','DM Serif Display','--fb','Manrope','--fw','400'],capture_output=True,text=True);print(r.stdout,r.stderr)
assert r.returncode==0
open(D+'css/style.css','a',encoding='utf8').write('''
/* DM Serif Display : une seule graisse ; logo texte */
h1,h2,h3,h4,.logo,.sa5-n,.step .n{font-weight:400}
.logo{font-size:1.375rem}
''')
open(D+'README.md','w',encoding='utf8').write('# Boisumeau Paysage\n\nMaquette de site vitrine (démonstration) : accueil, prestations, contact.\n')
print('ok')
