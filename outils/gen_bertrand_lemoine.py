# Génère la maquette bertrand-lemoine (S17 + modules H3 V4 A5 C5 F3 K8). Relancer : python3 outils/gen_bertrand_lemoine.py
import re,os,shutil,subprocess
from PIL import Image,ImageDraw
D="/home/claude/maquettes/bertrand-lemoine/"; U="/mnt/user-data/uploads/Maquettes/Squelettes/Modules/"
NAME="Bertrand Lemoine"; COM="Saulx-Marchais (78)"; N="06 08 01 02 61"; T="tel:+33608010261"
LOGO="https://webaunet.github.io/maquettes/bertrand-lemoine/"
rd=lambda p:open(p,encoding="utf-8").read()
def wr(p,s):open(p,"w",encoding="utf-8").write(s)
os.chdir(D)
# --- images
os.makedirs("images",exist_ok=True)
im=Image.open("/mnt/user-data/uploads/Maquettes/Images/Paysagiste/robot tonte de pelouse.jpg").convert("RGB")
im=im.resize((1400,round(im.height*1400/im.width)),Image.LANCZOS);im.save("images/hero.jpg",quality=76,optimize=True,progressive=True)
for n in("terrasse-bois","maconnerie","allee-paves"):
    shutil.copy("/home/claude/babylone-garden/images/%s.jpg"%n,"images/%s.jpg"%n)
f=Image.new("RGBA",(64,64),(59,74,31,255));d=ImageDraw.Draw(f);d.polygon([(32,8),(50,36),(38,36),(46,54),(18,54),(26,36),(14,36)],fill=(196,145,42,255));f.save("images/favicon.png")
sz={n:Image.open("images/%s.jpg"%n).size for n in("hero","terrasse-bois","maconnerie","allee-paves")}
# --- CSS (repart de l'original)
O="/tmp/bl_orig/";os.makedirs(O,exist_ok=True)
if not os.path.exists(O+"style.css.orig"):shutil.copy("css/style.css",O+"style.css.orig")
s=rd(O+"style.css.orig")
s=re.sub(r"^/\*.*?\*/","/* Bertrand Lemoine — maquette. */",s,count=1,flags=re.S)
pal={"forest":"#3b4a1f","forest-deep":"#2a3615","shutter-deep":"#4b4f33","shutter":"#6a6e48","shutter-tint":"#e8e6cf","sage":"#8a9a4b","sage-tint":"#e1e5c8","limestone":"#f6f3e8","tile":"#c4912a","tile-dark":"#7a5612","sun":"#e6c36a","ink":"#23261a"}
for k,v in pal.items():
    s,c=re.subn(r"(--%s\s*:\s*)#[0-9a-fA-F]{3,8}"%re.escape(k),lambda m:m.group(1)+v,s,count=1);assert c==1,k
assert "DM Mono" in s or "Outfit" in s
s=s.replace("DM Mono","DM Serif Display").replace("Outfit","Manrope")
s+="""
/* Bertrand Lemoine */
h1,h2,h3,h4{font-weight:400;font-family:'DM Serif Display',Georgia,serif}
.btn--tile{color:#23261a}
.btn--tile:hover{color:#fff}
section.bg-limestone .btn--ghost{color:var(--forest);border-color:var(--forest)}
.logo{display:inline-flex;align-items:center;min-height:48px;text-decoration:none}
.logo-t{font-family:'DM Serif Display',serif;font-size:1.45rem;line-height:1.1;color:var(--forest)}
@media(max-width:420px){.logo-t{font-size:1.2rem}}
"""
wr("css/style.css",s)
base=rd(U+"_base.css")
vals={"--hv-bg:":"#f6f3e8","--hv-bg2:":"#e8e6cf","--hv-ink:":"#23261a","--hv-mu:":"#53563f","--hv-main:":"#3b4a1f","--hv-acc:":"#c4912a","--hv-acc-ink:":"#23261a","--hv-fh:":"'DM Serif Display',serif","--hv-fb:":"'Manrope',sans-serif","--hv-fw:":"400"}
for k,v in vals.items():base=re.sub(re.escape(k)+r"[^;}]*",lambda m:k+v,base,count=1)
mods=["H3","V4","A5","C5","F3","K8"]
wr("css/style.css",rd("css/style.css")+"\n/* modules */\n"+base+"\n"+rd(U+"K.css")+"\n"+"\n".join(rd(U+m+".css") for m in mods))
os.makedirs("js",exist_ok=True);shutil.copy(U+"K.js","js/k.js")
# --- HTML commun
if not os.path.exists(O+"index.orig.html"):shutil.copy("index.html",O+"index.orig.html")
idx=rd(O+"index.orig.html")
head=idx[:idx.index("<header")]
head=re.sub(r'<link rel="stylesheet" href="https://fonts.*?>','<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;500;600;700&display=swap">',head)
hd=f'''<header class="hd">
  <div class="wrap hd__in">
    <a class="logo" href="{LOGO}" aria-label="{NAME}, retour à l'accueil du site"><span class="logo-t">{NAME}</span></a>
    <nav class="nav" id="menu" aria-label="Navigation principale">
      <ul>
        <li><a href="index.html">Accueil</a></li>
        <li><a href="prestations.html">Prestations</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
    <a class="btn btn--tel" href="{T}" aria-label="Appeler le {N}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg><span>{N}</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
  </div>
</header>
'''
foot=f'''<footer class="hf hf3"><div class="hv-wrap"><strong>{NAME}</strong><nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a><a href="contact.html">Contact</a></nav><div class="hf-c"><a href="{T}">{N}</a></div><p class="hf-cop">© {NAME} · {COM} · Maquette de démonstration</p></div></footer>
'''
def page(title,desc,cur,main,extra=""):
    h=re.sub(r"<title>.*?</title>",f"<title>{title}</title>",head,flags=re.S)
    h=re.sub(r'<meta name="description" content=".*?">',f'<meta name="description" content="{desc}">',h,flags=re.S)
    if 'name="robots"' not in h:h=h.replace("</title>",'</title>\n<meta name="robots" content="noindex, nofollow">',1)
    hh=hd.replace(f'<a href="{cur}">',f'<a href="{cur}" aria-current="page">')
    return h+hh+'<main id="main">\n'+main+"\n</main>\n"+foot+'<script src="js/site.js"></script>\n'+extra+"</body>\n</html>\n"
LEAF='<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21V11M12 11C12 6 8 4 4 4c0 4 2 7 8 7ZM12 14c0-4 3-6 8-6 0 4-2 7-8 6Z"/></svg>'
def v4(t,p,a):return f'<div><div class="sv4-ico">{LEAF}</div><h3>{t}</h3><p>{p}</p><a href="prestations.html#{a}">En savoir plus</a></div>'
w,h_=sz["hero"]
home=f'''<section class="hv hv3" aria-labelledby="hv-t"><div class="hv-wrap"><p class="hv-kick">Aménagement paysager à Saulx-Marchais (78)</p><h1 id="hv-t">Votre jardin, aménagé et entretenu avec soin.</h1><p class="hv-lead">Bertrand Lemoine s'occupe de l'aménagement et de l'entretien de vos espaces extérieurs. Un interlocuteur unique, joignable par téléphone.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="{T}">Appeler le {N}</a><a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>
<div class="hv3-strip"><div class="hv-wrap"><img src="images/hero.jpg" width="{w}" height="{h_}" alt="Pelouse, massif fleuri et muret en pierre devant une maison (image d'illustration)"><div class="hv3-card">Basé à Saulx-Marchais<span>Aménagement et entretien de jardins</span></div></div></div></section>
<section class="sv sv4" id="prestations" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Du plan du jardin à son entretien</h2><p class="hv-lead">Décrivez votre terrain et vos envies, nous vous conseillons.</p>
<div class="sv4-grid">{v4("Conception de jardin","Un plan d'aménagement construit à partir de votre terrain et de vos usages.","conception")}{v4("Terrasses et allées","Terrasse en bois, allée dallée ou pavée : des accès et des espaces de vie soignés.","terrasses")}{v4("Maçonnerie paysagère","Murets, marches et soutènements en pierre pour structurer le jardin.","maconnerie")}{v4("Entretien de jardin","Pelouses, massifs et haies suivis, ponctuellement ou régulièrement.","entretien")}</div></div></section>
<section class="sv sa5" id="entreprise" aria-labelledby="sv-a"><div class="hv-wrap"><p class="hv-kick">L'entreprise</p><h2 id="sv-a">{NAME} en bref</h2><p class="hv-lead">Quelques repères sur l'entreprise.</p><div class="sa5-grid"><article class="sa5-c"><span class="sa5-n">01</span><h3>Dirigeant</h3><p>L'entreprise est dirigée par Bertrand Lemoine.</p></article><article class="sa5-c"><span class="sa5-n">02</span><h3>Activité</h3><p>Services d'aménagement paysager : conception, réalisation et entretien d'espaces verts.</p></article><article class="sa5-c"><span class="sa5-n">03</span><h3>Localisation</h3><p>Basée à Saulx-Marchais, dans les Yvelines (78).</p></article></div></div></section>
<section class="sv sc5" id="contact" aria-labelledby="sv-c"><div class="hv-wrap"><div><p class="hv-kick">Contact</p><h2 id="sv-c">Un projet de jardin ? Parlons-en.</h2><p class="hv-lead">Appelez-nous ou demandez un devis : nous revenons vers vous.</p></div><div><a class="sc5-tel" href="{T}">{N}</a><br><a class="hv-btn" href="contact.html">Demander un devis</a></div></div></section>'''
wr("index.html",page(f"{NAME}, aménagement paysager à Saulx-Marchais (78)",f"{NAME}, services d'aménagement paysager à Saulx-Marchais (78) : conception de jardin, terrasses, maçonnerie paysagère et entretien. Appelez le {N}.","index.html",home))
def fig(n,alt):w,h=sz[n];return f'<figure><img src="images/{n}.jpg" width="{w}" height="{h}" alt="{alt}"></figure>'
def feat(i,c,ic,t,items):return f'<article class="feat feat--{c}" id="{i}"><div class="feat__top"><span class="pastille"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{ic}"/></svg></span><h3>{t}</h3></div><ul class="ticks">'+"".join(f"<li>{x}</li>" for x in items)+"</ul></article>"
pm=f'''<section class="ph" aria-labelledby="h-page"><div class="wrap"><div class="ph__grid"><div><h1 id="h-page">Aménagement et entretien de jardin à Saulx-Marchais</h1><p class="lead">De la conception du jardin à son entretien : terrasses, allées, maçonnerie paysagère et suivi des espaces verts.</p><div class="ph__cta"><a class="btn btn--tile" href="contact.html">Demander un devis</a><a class="btn btn--ghost" href="{T}">Appeler le {N}</a></div></div>
<div class="mosaic">{fig("allee-paves","Allée dallée le long d'un muret en pierre fleuri (image d'illustration)")}{fig("terrasse-bois","Pose d'une terrasse en bois devant une maison en pierre (image d'illustration)")}{fig("maconnerie","Ouvrier montant un muret et des marches en pierre dans un jardin (image d'illustration)")}</div></div></div></section>
<section class="sec band bg-limestone" id="conception" aria-labelledby="h-conception"><div class="wrap"><div class="split"><div><h2 id="h-conception">Conception de jardin</h2><p class="lead">Un jardin réussi commence par un plan, construit à partir de votre terrain et de la façon dont vous voulez l'utiliser.</p><ul class="ticks"><li>Étude de votre terrain</li><li>Plan d'aménagement</li><li>Échange par téléphone sur votre projet</li></ul><p style="margin-top:26px"><a class="btn btn--tile" href="contact.html">Demander un devis</a></p></div>
<section class="panel panel--zone" aria-labelledby="h-liste"><h3 id="h-liste">Nos domaines</h3><p>Aller directement à la prestation qui vous intéresse :</p><ul class="chips chips--links"><li><a href="#terrasses">Terrasses et allées</a></li><li><a href="#maconnerie">Maçonnerie paysagère</a></li><li><a href="#entretien">Entretien de jardin</a></li></ul></section></div></div></section>
<section class="sec band bg-forest" aria-labelledby="h-real"><div class="wrap"><div class="head"><h2 id="h-real">Réalisation et entretien</h2><p class="lead on-dark">Des ouvrages sur mesure et un jardin suivi dans le temps.</p></div>
<div class="feats slider" data-slider="Prestations, faites défiler">{feat("terrasses","sage","M3 10h18M5 10v9M19 10v9M3 14h18","Terrasses et allées",["Terrasse en bois","Allée dallée ou pavée"])}{feat("maconnerie","sun","M3 6h18v12H3zM3 12h18M9 6v6M15 12v6","Maçonnerie paysagère",["Murets en pierre","Marches et soutènements"])}{feat("entretien","sage","M12 21v-9M12 12c0-4 3-6 7-6 0 4-3 6-7 6zM12 15c0-3-2-5-6-5 0 3 2 5 6 5z","Entretien de jardin",["Pelouses et massifs","Haies et arbustes"])}</div></div></section>
<section class="sec band bg-limestone" aria-labelledby="h-fin"><div class="wrap"><div class="head"><h2 id="h-fin">Un projet, un doute ?</h2><p class="lead">Appelez-nous : nous faisons le point sur votre projet de jardin.</p></div><p><a class="btn btn--tile" href="{T}">Appeler le {N}</a> <a class="btn btn--ghost" href="contact.html">Demander un devis</a></p></div></section>'''
wr("prestations.html",page(f"Prestations · {NAME}, Saulx-Marchais (78)","Prestations de Bertrand Lemoine à Saulx-Marchais (78) : conception de jardin, terrasses et allées, maçonnerie paysagère, entretien.","prestations.html",pm))
c=rd(U+"K8.html")
c=c.replace("Nom de l'entreprise",NAME).replace('data-sms="+33000000000" data-tel="+33000000000" data-email=""','data-sms="+33608010261" data-tel="+33608010261" data-email=""')
c=c.replace("Une phrase d'introduction.","Décrivez votre besoin : nous revenons vers vous.")
c=re.sub(r"<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>","<option>Conception de jardin</option><option>Terrasse ou allée</option><option>Maçonnerie paysagère</option><option>Entretien de jardin</option>",c)
c=re.sub(r'<aside class="sk-side">.*?</aside>',f'<aside class="sk-side"><ul><li><span>Téléphone</span><a href="{T}">{N}</a></li><li><span>Commune</span><p>Saulx-Marchais (78)</p></li></ul></aside>',c,flags=re.S)
band=f'''<section class="ph ph--tile" style="min-height:0" aria-labelledby="h-page"><div class="wrap"><div class="ph__grid"><div><h1 id="h-page">Contact et demande de devis</h1><p class="lead">Décrivez votre projet : aménagement ou entretien de jardin. Le récapitulatif se prépare en quelques secondes.</p></div>
<div class="mosaic mosaic--single">{fig("allee-paves","Allée dallée le long d'un muret en pierre fleuri (image d'illustration)")}</div></div></div></section>'''
wr("contact.html",page(f"Contact · {NAME}, Saulx-Marchais (78)","Contactez Bertrand Lemoine à Saulx-Marchais (78) : téléphone et demande de devis pour l'aménagement ou l'entretien de votre jardin.","contact.html",band+"\n"+c,'<script src="js/k.js" defer></script>\n'))
for p in("a-propos.html","amenagement.html","elagage.html","entretien.html","realisations.html","js/contact.js","js/realisations.js"):
    if os.path.exists(p):os.remove(p)
wr("README.md",f"# {NAME} — maquette de site\n\nMaquette (non définitive) du site de {NAME}, Saulx-Marchais (78).\n\nPages : accueil, prestations, contact.\n")
print("ok")
