from PIL import Image
D='/home/claude/maquettes/brossard-fils-jardins-91/'
BASE='https://webaunet.github.io/maquettes/brossard-fils-jardins-91/'
NOM='Brossard Fils (Jardins 91)'
TEL='06 81 54 01 17';TELH='+33681540117';TEL2='07 77 20 60 04';TEL2H='+33777206004'
MAIL='contact@jardins-91.fr'
PAGES=[('index.html','Accueil'),('amenagement.html','Création'),('entretien.html','Entretien'),('a-propos.html','L’entreprise'),('contact.html','Contact')]
PHI='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
def im(n,alt,lazy=True,cls=''):
    w,h=Image.open(D+'images/'+n).size
    return f'<img {cls}src="images/{n}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""} alt="{alt}">'
def head(t,d):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="images/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@500&family=Outfit:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body id="top">
<a class="skip" href="#main">Aller au contenu</a>

<header class="hd">
  <div class="wrap hd__in">
    <a class="logo" href="{BASE}" aria-label="Brossard Fils Jardins 91, retour à l'accueil du site"><img src="images/logo.png" width="206" height="85" alt="Brossard Fils Jardins 91"></a>
'''
def header(cur):
    li=''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a></li>' for h,n in PAGES)
    return f'''    <nav class="nav" id="menu" aria-label="Navigation principale">
      <ul>
        {li}
      </ul>
    </nav>
    <a class="btn btn--tel" href="tel:{TELH}" aria-label="Appeler le {TEL}">{PHI}<span>{TEL}</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
  </div>
</header>

<main id="main">
'''
def footer(k=False):
    nav=''.join(f'<a href="{h}">{n}</a>' for h,n in PAGES)
    sc='<script src="js/site.js"></script>\n'+('<script src="js/k.js" defer></script>\n' if k else '')
    return f'''</main>

<footer class="hf hf5"><div class="hf5-top"><div class="hv-wrap"><strong>Un projet de jardin ? Demandez votre devis.</strong><a href="contact.html">Nous contacter</a></div></div><div class="hf5-b"><div class="hv-wrap"><a class="hf-logo" href="index.html"><img src="images/logo.png" width="206" height="85" alt="Brossard Fils Jardins 91"></a><nav aria-label="Pied de page">{nav}</nav><p class="hf-cop">© Brossard Fils (Jardins 91) · Maquette de site vitrine</p></div></div></footer>

<div class="toast" role="status" aria-live="polite"></div>
{sc}</body>
</html>
'''
def w(n,s): open(D+n,'w',encoding='utf8').write(s)
def ph(h1,lead,b1,b2,imgs,cls='ph'):
    m=''.join(f'<figure>{im(n,a,False)}</figure>' for n,a in imgs)
    return f'''<section class="{cls}" aria-labelledby="h-page">
  <div class="wrap">
    <div class="ph__grid">
      <div>
        <h1 id="h-page">{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="ph__cta">
          <a class="btn btn--tile" href="{b1[1]}">{b1[0]}</a>
          <a class="btn btn--ghost" href="{b2[1]}">{b2[0]}</a>
        </div>
      </div>
      <div class="mosaic">{m}</div>
    </div>
  </div>
</section>
'''
def cta(bg,h,lead,img,alt,sub=''):
    return f'''<section class="sec sec--last band {bg}" aria-labelledby="h-cta">
  <div class="wrap">
    <div class="cta{sub}">
      <div>
        <h2 id="h-cta">{h}</h2>
        <p class="lead">{lead}</p>
        <div class="cta__btns">
          <a class="btn btn--tile" href="contact.html">Demander un devis</a>
          <a class="btn btn--{'line' if sub else 'ghost'}" href="tel:{TELH}">{TEL}</a>
        </div>
      </div>
      <div class="cta__img">{im(img,alt)}</div>
    </div>
  </div>
</section>
'''
A_JARDIN='Allée de gravier bordée de massifs fleuris et de pelouse, devant une maison de village'
A_TONTE='Jardinier tondant la pelouse devant une maison, au milieu de massifs fleuris'
A_PLANT='Jardinier plantant un végétal dans un massif'
A_HAIES='Jardinier taillant une haie avec un taille-haie thermique'
A_ELAG='Élagueur-grimpeur encordé dans un chêne, tronçonneuse en main, au-dessus d’un jardin'
A_CREA='Massif de plantes et pelouse aux bords courbes devant une maison contemporaine'
A_ALLEE='Allée dallée éclairée au crépuscule devant une maison en pierre'
A_FEUIL='Jardinier ramassant les feuilles mortes sur une allée de gravier'
A_DECH='Jardinier chargeant des déchets verts dans une camionnette'
A_DESH='Jardinier désherbant à la main un massif fleuri'
def index():
    s=head('Brossard Fils (Jardins 91) | Paysagiste à Ollainville (91), entretien et création de jardins','Brossard Fils (Jardins 91), entreprise familiale de paysagistes à Ollainville (Essonne) : entretien de jardins, élagage, création et plantation. Plus de 25 ans d’expérience.')+header('index.html')
    s+=f'''<section class="hv hv10" aria-labelledby="hv-t"><div class="hv-wrap hv10-g"><div><p class="hv-kick">Paysagiste à Ollainville (91)</p><h1 id="hv-t">Des jardiniers paysagistes, en famille, en Essonne</h1><p class="hv-lead">Brossard Fils entretient et crée les jardins des particuliers, des syndics et des entreprises, en Essonne et parfois dans toute l’Île-de-France. Plus de 25 ans d’expérience.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="#prestations">Voir les prestations</a></div><ul class="hv10-chips"><li>Entretien de jardin</li><li>Élagage</li><li>Création et plantation</li><li>Pelouse et rocailles</li></ul></div><div class="hv10-w"><div class="hv10-pic">{im('hero.jpg',A_JARDIN,False)}</div><div class="hv10-badge"><strong>25</strong>ans d’expérience</div></div></div></section>
<section class="sv sv6" id="prestations" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Entretenir, créer, élaguer</h2><p class="hv-lead">Pour les particuliers, les syndics et les entreprises du bâtiment.</p><div class="sv6-grid"><div class="sv6-big">{im('p1.jpg',A_TONTE)}<div><h3>Entretien de jardin</h3><p>Taille des haies, bêchage, tontes et débroussaillage, ramassage des feuilles, scarification.</p><a href="entretien.html">En savoir plus →</a></div></div><div class="sv6-t sv6-t1"><h3>Élagage</h3><p>L’élagage de vos arbres, en complément de l’entretien du jardin.</p><a href="entretien.html#elagage">En savoir plus →</a></div><div class="sv6-t sv6-t2"><h3>Création et plantation</h3><p>Plantations diverses pour créer ou transformer votre jardin.</p><a href="amenagement.html#plantation">En savoir plus →</a></div><div class="sv6-t sv6-t3"><h3>Pelouse et nivellement</h3><p>Création de pelouse en plaques ou par semis, nivellement de terrain.</p><a href="amenagement.html#pelouse">En savoir plus →</a></div><div class="sv6-t sv6-t4"><h3>Rocailles et grillage</h3><p>Création de rocaille et pose de grillage.</p><a href="amenagement.html#rocaille">En savoir plus →</a></div></div></div></section>
<section class="sv sm4" id="engagements" aria-labelledby="sv-m"><div class="hv-wrap"><p class="hv-kick">Pourquoi nous choisir ?</p><h2 id="sv-m">Notre priorité : votre satisfaction</h2><p class="hv-lead">Quatre engagements, du premier rendez-vous à la fin du chantier.</p><div class="sm4-grid"><article class="sm4-c"><span class="sm4-n">1</span><h3>L’écoute</h3><p>Nous écoutons votre demande lors d’un rendez-vous pour l’élaboration du devis.</p></article><article class="sm4-c"><span class="sm4-n">2</span><h3>Le conseil</h3><p>Nos conseils vous permettent de réaliser le jardin dont vous avez toujours rêvé.</p></article><article class="sm4-c"><span class="sm4-n">3</span><h3>La qualité et le suivi</h3><p>Nous veillons à la qualité et au suivi de nos chantiers.</p></article><article class="sm4-c"><span class="sm4-n">4</span><h3>Le respect des engagements</h3><p>Ce que nous vous annonçons, nous le tenons.</p></article></div></div></section>
<section class="sv sa3" id="apropos" aria-labelledby="sv-a"><div class="hv-wrap"><div><p class="hv-kick">À propos</p><h2 id="sv-a">Une entreprise familiale, à échelle humaine</h2><p>Bernard Brossard a créé l’entreprise il y a presque 30 ans. Fils d’horticulteur de père en fils, il a transmis la passion du jardin d’agrément et la curiosité des végétaux : couleurs, parfums, formes.</p><p>Après dix ans à ses côtés, Jérémie, rejoint depuis par son frère Charles, a décidé de suivre son exemple.</p><a class="hv-btn hv-btn-p" href="a-propos.html">Découvrir l’entreprise</a></div><div class="sa3-imgs"><figure class="sa3-i1">{im('a1.jpg',A_PLANT)}</figure><figure class="sa3-i2">{im('a2.jpg',A_HAIES)}</figure></div></div></section>
<section class="sv sc3" aria-labelledby="sv-c"><div class="sc3-bg">{im('c1.jpg','',True)}</div><div class="hv-wrap"><p class="hv-kick">Contact</p><h2 id="sv-c">Un projet de jardin ? Parlons-en.</h2><p class="hv-lead">Décrivez votre projet : nous vous répondons pour convenir d’un rendez-vous et établir un devis.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div></div></section>
'''+footer()
    w('index.html',s)
def ic(p): return f'<span class="pastille"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{p}"/></svg></span>'
def amen():
    s=head('Création de jardins en Essonne | Brossard Fils (Jardins 91) à Ollainville','Création et plantation, pelouse en plaques ou par semis, nivellement de terrain, rocailles et pose de grillage : Brossard Fils crée votre jardin en Essonne.')+header('amenagement.html')
    s+=ph('Création de jardins en Essonne','Création et plantation, pelouse en plaques ou par semis, nivellement de terrain, rocailles et pose de grillage.',('Demander un devis','contact.html'),('Voir les prestations','#plantation'),[('creation.jpg',A_CREA),('plantation.jpg',A_PLANT),('allee.jpg',A_ALLEE)])
    s+=f'''
<section class="sec band bg-limestone" id="plantation" aria-labelledby="h-plantation">
  <div class="wrap">
    <div class="split">
      <div>
        <h2 id="h-plantation">Création et plantation</h2>
        <p class="lead">Création de parcs et de jardins : plantation, nivellement de terrain et engazonnement. Nous vous conseillons pour réaliser le jardin dont vous avez toujours rêvé.</p>
        <ul class="ticks">
          <li>Création et plantation diverse</li>
          <li>Création de pelouse</li>
          <li>Nivellement de terrain</li>
          <li>Création de rocaille et pose de grillage</li>
        </ul>
        <p style="margin-top:26px"><a class="btn btn--tile" href="contact.html">Demander un devis</a></p>
      </div>
      <section class="panel panel--zone" aria-labelledby="h-liste">
        <h3 id="h-liste">Les prestations de création</h3>
        <p>Aller directement à la prestation qui vous intéresse :</p>
        <ul class="chips chips--links">
          <li><a href="#pelouse">Création de pelouse</a></li>
          <li><a href="#pelouse">Nivellement de terrain</a></li>
          <li><a href="#rocaille">Rocailles</a></li>
          <li><a href="#rocaille">Pose de grillage</a></li>
        </ul>
      </section>
    </div>
  </div>
</section>

<section class="sec band bg-forest" id="pelouse" aria-labelledby="h-pelouse">
  <div class="wrap">
    <div class="split split--rev">
      <div class="split__img">{im('tonte.jpg',A_TONTE)}</div>
      <div class="on-dark">
        <h2 id="h-pelouse">Pelouse et nivellement</h2>
        <p class="lead">Un terrain bien préparé, puis une pelouse installée en plaques ou par semis.</p>
        <ul class="ticks">
          <li>Création de pelouse en plaques</li>
          <li>Création de pelouse par semis</li>
          <li>Nivellement de terrain</li>
          <li>Engazonnement</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec band bg-tint" id="rocaille" aria-labelledby="h-rocaille">
  <div class="wrap">
    <div class="split">
      <div class="split__img">{im('desherbage.jpg',A_DESH)}</div>
      <div>
        <h2 id="h-rocaille" style="margin-bottom:22px">Rocailles et grillage</h2>
        <div class="mini">
          <div>
            <h3>Création de rocaille</h3>
            <p>Des rocailles pour structurer et décorer votre jardin.</p>
          </div>
          <div>
            <h3>Pose de grillage</h3>
            <p>Pose de grillage pour délimiter votre terrain.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

'''+cta('bg-tile','Un terrain à transformer ?','Décrivez votre projet à l’équipe : nous convenons d’un rendez-vous pour l’élaboration du devis.','creation.jpg',A_CREA)+footer()
    w('amenagement.html',s)
def entr():
    s=head('Entretien de jardin et élagage en Essonne | Brossard Fils (Jardins 91)','Taille des haies, bêchage, tontes, débroussaillage, ramassage des feuilles, scarification et élagage : l’entretien de jardin par Brossard Fils à Ollainville et en Essonne.')+header('entretien.html')
    s+=ph('Entretien de jardin et élagage','Taille des haies, bêchage, tontes et débroussaillage, ramassage des feuilles, scarification et élagage.',('Demander un devis','contact.html'),('Voir l’entretien','#tonte-taille'),[('tonte.jpg',A_TONTE),('haies.jpg',A_HAIES),('feuilles.jpg',A_FEUIL)])
    s+=f'''
<section class="sec band bg-limestone" id="tonte-taille" aria-labelledby="h-tonte">
  <div class="wrap">
    <div class="split">
      <div class="split__img">{im('haies.jpg',A_HAIES)}</div>
      <div>
        <h2 id="h-tonte">Tonte, taille et bêchage</h2>
        <p class="lead">Nous nous déplaçons chez vous pour l’entretien courant du jardin : tonte, taille, nettoyage, bêchage.</p>
        <ul class="ticks">
          <li>Taille des haies</li>
          <li>Bêchage</li>
          <li>Tontes et débroussaillage</li>
          <li>Ramassage des feuilles</li>
          <li>Scarification</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec band bg-forest" id="elagage" aria-labelledby="h-elagage">
  <div class="wrap">
    <div class="split split--rev">
      <div class="split__img">{im('elagage.jpg',A_ELAG)}</div>
      <div class="on-dark">
        <h2 id="h-elagage">Élagage</h2>
        <p class="lead">L’élagage fait partie des prestations de Brossard Fils, pour les particuliers, les syndics et les entreprises.</p>
        <p style="margin-top:22px"><a class="btn btn--tile" href="contact.html">Demander un devis</a></p>
      </div>
    </div>
  </div>
</section>

<section class="sec band bg-tint" id="clients" aria-labelledby="h-service">
  <div class="wrap">
    <div class="split">
      <div>
        <h2 id="h-service" style="margin-bottom:22px">Pour qui travaillons-nous ?</h2>
        <div class="stack">
          <article class="feat feat--sage">
            <div class="feat__top">{ic('M3 11l9-7 9 7M5 10v10h14V10')}<h3>Particuliers</h3></div>
            <p>Entretien régulier ou création de votre jardin, avec un devis établi lors d’un rendez-vous.</p>
          </article>
          <article class="feat feat--shutter">
            <div class="feat__top">{ic('M5 21V4h9v17M14 9h5v12M8 8h3M8 12h3M8 16h3')}<h3>Syndics et entreprises</h3></div>
            <p>Syndics de copropriété, sociétés de construction et entreprises du bâtiment, pour qui nous intervenons aussi en sous-traitance.</p>
          </article>
        </div>
      </div>
      <div class="split__img">{im('feuilles.jpg',A_FEUIL)}</div>
    </div>
  </div>
</section>

'''+cta('bg-sage','Un jardin qui reste beau','Dites-nous ce dont votre jardin a besoin : tonte, taille, débroussaillage ou élagage.','dechets.jpg',A_DECH,' cta--sage')+footer()
    w('entretien.html',s)
def apropos():
    s=head('L’entreprise familiale Brossard Fils (Jardins 91) à Ollainville','Brossard Fils, entreprise familiale de paysagistes à Ollainville (91) : plus de 25 ans d’expérience au service des particuliers, des syndics et des entreprises du bâtiment.')+header('a-propos.html')
    s+=ph('Brossard Fils, une entreprise familiale','Plus de 25 ans d’expérience dans le domaine du paysage, au service des particuliers, des syndics et des entreprises.',('Nos prestations','amenagement.html'),('Nous contacter','contact.html'),[('jardin.jpg',A_JARDIN),('tonte.jpg',A_TONTE),('plantation.jpg',A_PLANT)])
    s+=f'''
<section class="sec band bg-limestone" id="histoire" aria-labelledby="h-histoire">
  <div class="wrap">
    <div class="split">
      <div class="split__img">{im('creation.jpg',A_CREA)}</div>
      <div>
        <h2 id="h-histoire">De père en fils, la passion du jardin</h2>
        <p>La société Brossard Fils reste et restera une entreprise familiale à échelle humaine. Bernard Brossard (père) a créé son entreprise il y a presque 30 ans.</p>
        <p>Fils d’horticulteur de père en fils, il a transmis la passion du jardin d’agrément et la curiosité des végétaux : couleurs, parfums, formes. Jérémie, après dix ans à ses côtés, puis son frère Charles, ont décidé de suivre son exemple.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec band bg-forest" id="clients" aria-labelledby="h-clients">
  <div class="wrap">
    <div class="head">
      <h2 id="h-clients">Pour qui travaillons-nous ?</h2>
      <p class="lead on-dark">Notre expérience et notre rigueur à la disposition de chacun.</p>
    </div>
    <div class="feats slider" data-slider="Clients, faites défiler">
      <article class="feat feat--sage">
        <div class="feat__top">{ic('M3 11l9-7 9 7M5 10v10h14V10')}<h3>Particuliers</h3></div>
        <p>Entretien et création de jardin, après écoute de votre demande lors d’un rendez-vous.</p>
      </article>
      <article class="feat feat--sun">
        <div class="feat__top">{ic('M5 21V4h9v17M14 9h5v12M8 8h3M8 12h3M8 16h3')}<h3>Syndics de copropriété</h3></div>
        <p>Entretien des espaces verts de votre copropriété.</p>
      </article>
      <article class="feat feat--shutter">
        <div class="feat__top">{ic('M3 21h18M6 21V9l6-5 6 5v12M10 21v-6h4v6')}<h3>Entreprises du bâtiment</h3></div>
        <p>Sous-traitance pour des entreprises du bâtiment et de grandes sociétés de construction.</p>
      </article>
    </div>
  </div>
</section>

<section class="sec band bg-tint" id="zone" aria-labelledby="h-zone">
  <div class="wrap">
    <div class="split split--rev">
      <section class="panel panel--zone" aria-labelledby="h-zone-liste">
        <h3 id="h-zone-liste">Où intervenons-nous ?</h3>
        <p>Nous nous déplaçons dans l’Essonne et parfois dans l’ensemble de l’Île-de-France.</p>
        <ul class="chips">
          <li>Ollainville</li><li>Essonne (91)</li><li>Île-de-France</li>
        </ul>
      </section>
      <div>
        <h2 id="h-zone">Entretien, création, rocailles</h2>
        <p>Nous réalisons l’entretien (tonte, taille, nettoyage, bêchage), la création de parcs et de jardins (plantation, nivellement de terrain, engazonnement) et des rocailles.</p>
      </div>
    </div>
  </div>
</section>

'''+cta('bg-tile','Parlons de votre jardin','Notre priorité : la satisfaction de nos clients, avec le respect de nos engagements.','jardin.jpg',A_JARDIN)+footer()
    w('a-propos.html',s)
def contact():
    s=head('Contact et demande de devis | Brossard Fils (Jardins 91) à Ollainville','Contactez Brossard Fils (Jardins 91), paysagistes à Ollainville (91) : téléphone, e-mail ou formulaire de demande de devis.')+header('contact.html')
    s+=f'''<section class="ph ph--tile" style="min-height:0" aria-labelledby="h-page">
  <div class="wrap">
    <div class="ph__grid">
      <div>
        <h1 id="h-page">Contact et demande de devis</h1>
        <p class="lead">Décrivez votre projet : entretien, élagage ou création de jardin. Nous vous répondons pour convenir d’un rendez-vous.</p>
      </div>
      <div class="mosaic mosaic--single">
        <figure>{im('c1.jpg',A_CREA,False)}</figure>
      </div>
    </div>
  </div>
</section>

<section class="sv sk sk1" aria-labelledby="sv-k"><div class="hv-wrap sk-grid"><div class="sk-card"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Indiquez votre commune et votre besoin : nous vous recontactons.</p><form class="sk-form" id="kform" novalidate data-name="{NOM}" data-sms="{TELH}" data-tel="{TELH}" data-email="{MAIL}"><div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div><div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div><div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div><div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option><option>Entretien de jardin</option><option>Élagage</option><option>Création et plantation de jardin</option><option>Pelouse, nivellement ou rocaille</option><option>Autre demande</option></select><p class="sk-err" id="k-besoin-e" role="alert"></p></div><div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div><button class="hv-btn hv-btn-p sk-go" type="submit">Préparer ma demande</button></form><div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l'envoyer. Rien n'est transmis tant que vous n'avez pas validé l'envoi.</p><pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a><button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a><a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div><aside class="sk-side"><h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:{TELH}">{TEL}</a></li><li><span>Autre numéro</span><a href="tel:{TEL2H}">{TEL2}</a></li><li><span>E-mail</span><a href="mailto:{MAIL}">{MAIL}</a></li><li><span>Commune</span><p>Ollainville (91)</p></li></ul></aside></div></section>
'''+footer(True)
    w('contact.html',s)
index();amen();entr();apropos();contact();print('ok')
