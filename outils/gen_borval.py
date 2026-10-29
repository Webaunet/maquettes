D='/home/claude/maquettes/borval-paysage/'
BASE='https://webaunet.github.io/maquettes/borval-paysage/'
TEL='06 60 68 37 11';TELH='+33660683711'
ADR='4 rue de la Rémarde, 91530 Saint-Maurice-Montcouronne'
PAGES=[('index.html','Accueil'),('prestations.html','Prestations'),('zone.html','Zone d’intervention'),('contact.html','Contact')]
PHP='<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
SV='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
PIN='<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 43s14-12 14-23a14 14 0 0 0-28 0c0 11 14 23 14 23z"/><circle cx="24" cy="20" r="5"/></svg>'
LOGO='<img src="images/logo.png" width="197" height="150" alt="Borval Paysage">'
def head(t,d):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''
def header(cur):
    nav=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a>' for h,n in PAGES)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{BASE}" aria-label="Borval Paysage, accueil">{LOGO}</a>
    <nav class="nav" id="nav" aria-label="Navigation principale">
      {nav}
    </nav>
    <div class="head-right">
      <a class="btn head-call" href="tel:{TELH}" aria-label="Appeler le {TEL}">{SV%PHP}<span>{TEL}</span></a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="contenu">
'''
def footer(k=False):
    nav=''.join(f'<a href="{h}">{n}</a>' for h,n in PAGES)
    sc='<script src="js/main.js"></script>\n'+('<script src="js/k.js" defer></script>\n' if k else '')
    return f'''</main>
<footer class="hf hf3"><div class="hv-wrap"><a class="hf-logo" href="{BASE}" aria-label="Borval Paysage, accueil">{LOGO}</a><nav aria-label="Pied de page">{nav}</nav><div class="hf-c"><a href="tel:{TELH}">{TEL}</a></div><p class="hf-cop">© Borval Paysage · Maquette de site vitrine</p></div></footer>
{sc}</body>
</html>
'''
def c5(h2='Un projet de jardin ? Parlons-en.',lead='Appelez-nous ou remplissez le formulaire en ligne : nous vous répondons pour établir un devis.'):
    return f'''<section class="sv sc5" aria-labelledby="sv-c"><div class="hv-wrap"><div><p class="hv-kick">Contact</p><h2 id="sv-c">{h2}</h2><p class="hv-lead">{lead}</p></div><div><a class="sc5-tel" href="tel:{TELH}">{TEL}</a><br><a class="hv-btn" href="contact.html">Demander un devis</a></div></div></section>
'''
def write(n,s): open(D+n,'w',encoding='utf8').write(s)

def index():
    s=head('Borval Paysage | Paysagiste à Saint-Maurice-Montcouronne (91), création, entretien et élagage','Borval Paysage, paysagiste à Saint-Maurice-Montcouronne près de Saint-Chéron et Dourdan (Essonne) : création de jardins, contrat d’entretien et élagage.')+header('index.html')
    s+=f'''<section class="hv hv3" aria-labelledby="hv-t"><div class="hv-wrap"><p class="hv-kick">Paysagiste à Saint-Maurice-Montcouronne (91)</p><h1 id="hv-t">Votre jardin créé, entretenu et élagué avec soin</h1><p class="hv-lead">Installé depuis 2016, Borval Paysage crée et entretient les espaces verts des particuliers, des professionnels et des collectivités autour de Saint-Chéron et de Dourdan.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>
<div class="hv3-strip"><div class="hv-wrap"><img src="images/hero.jpg" width="1400" height="600" alt="Jardin contemporain avec massifs de plantes, gazon et allée de gravier devant une maison"><div class="hv3-card">Intervient à Saint-Maurice-Montcouronne<span>Saint-Chéron, Dourdan et alentours</span></div></div></div></section>
<section class="sv sv1" id="prestations" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Élaguer, créer, entretenir</h2><p class="hv-lead">Des prestations sur mesure, adaptées à votre espace vert.</p>
<div class="sv1-grid"><article class="sv1-card"><figure><img src="images/p1.jpg" width="800" height="500" alt="Élagueur grimpeur encordé et casqué dans un grand chêne" loading="lazy"></figure><div><h3>Élagage et abattage</h3><p>Un élagueur grimpeur qualifié, après diagnostic de vos arbres. Dessouchage et rognage de souche également.</p><a href="prestations.html#p1">En savoir plus →</a></div></article>
<article class="sv1-card"><figure><img src="images/p2.jpg" width="800" height="500" alt="Jardinier plantant un végétal dans un massif" loading="lazy"></figure><div><h3>Créations paysagères</h3><p>Massifs, rocailles, plantations, gazon, terrasses et piscines, selon un plan paysager adapté à votre maison.</p><a href="prestations.html#p2">En savoir plus →</a></div></article>
<article class="sv1-card"><figure><img src="images/p3.jpg" width="800" height="500" alt="Jardinier tondant une pelouse devant une maison" loading="lazy"></figure><div><h3>Contrat d’entretien</h3><p>Annuel ou ponctuel, pour résidence principale ou secondaire, avec un cahier des charges selon la saison.</p><a href="prestations.html#p3">En savoir plus →</a></div></article></div></div></section>
<section class="sv sm3" id="methode" aria-labelledby="sv-m"><div class="hv-wrap"><figure class="sm3-pic"><img src="images/m1.jpg" width="800" height="1000" alt="Jardinier désherbant à la main un massif fleuri" loading="lazy"></figure><div><p class="hv-kick">Notre façon de travailler</p><h2 id="sv-m">Étudier, composer, entretenir</h2><p class="hv-lead">Chaque jardin a son potentiel : nous le regardons avant d’agir.</p><ol class="sm3-list"><li><h3>Étude du terrain</h3><p>Avant les travaux, votre jardinier paysagiste étudie le potentiel de votre terrain.</p></li><li><h3>Plan paysager</h3><p>Nous proposons un plan et une composition végétale en harmonie avec le style architectural et la nature environnante.</p></li><li><h3>Diagnostic des arbres</h3><p>Nous diagnostiquons l’état de vos arbres, puis choisissons la technique d’élagage adaptée.</p></li><li><h3>Cahier des charges</h3><p>Pour l’entretien, un cahier des charges détaille les prestations selon la saison et les besoins de votre jardin.</p></li></ol></div></div></section>
<section class="sv sa6" id="apropos" aria-labelledby="sv-a"><div class="hv-wrap"><figure class="sa6-ban"><img src="images/a1.jpg" width="1400" height="600" alt="Allée de gravier bordée de massifs devant une maison de village" loading="lazy"></figure><div class="sa6-card"><p class="hv-kick">À propos</p><h2 id="sv-a">Jardinier paysagiste en Essonne</h2><p>Borval Paysage est implanté depuis 2016 à Saint-Maurice-Montcouronne, près de Saint-Chéron et de Dourdan. L’entreprise assure création, entretien et élagage.</p><p>Partenaire de Jardiniers Professionnels, coopérative de professionnels à domicile, et affiliée aux services à la personne, elle fait bénéficier ses clients d’une réduction d’impôt de 50 %.</p><a class="hv-btn hv-btn-p" href="zone.html">Zone et crédit d’impôt</a></div></div></section>
'''+c5()+footer()
    write('index.html',s)

def prest():
    s=head('Prestations de paysagiste à Saint-Maurice-Montcouronne | Borval Paysage','Élagage et abattage, créations et travaux paysagers, contrat d’entretien de jardin : les prestations de Borval Paysage à Saint-Maurice-Montcouronne, Saint-Chéron et Dourdan.')+header('prestations.html')
    s+=f'''<section class="section s-ivory hero page-hero">
  <div class="wrap">
    <div class="trait" aria-hidden="true"></div>
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Nos prestations</p>
        <h1>Élagage, création et entretien, <em>sur mesure.</em></h1>
        <p class="lead">Borval Paysage intervient à Saint-Maurice-Montcouronne, Saint-Chéron et Dourdan pour les particuliers, les professionnels et les collectivités.</p>
        <div class="cta-row"><a class="btn" href="contact.html">Demander un devis</a><a class="btn ghost" href="tel:{TELH}">Appeler le {TEL}</a></div>
      </div>
      <div class="mosaic" aria-label="Aperçu de nos prestations">
        <div class="m1"><img src="images/p1.jpg" width="800" height="500" alt="Élagueur grimpeur encordé dans un grand chêne" style="object-position:62% 50%"></div>
        <div class="m2"><img src="images/p2.jpg" width="800" height="500" alt="Jardinier plantant un végétal dans un massif"></div>
        <div class="m3"><img src="images/p3.jpg" width="800" height="500" alt="Jardinier tondant une pelouse devant une maison"></div>
      </div>
    </div>
  </div>
</section>

<section class="section s-sage s-curve" id="p1">
  <div class="wrap split">
    <div class="arch-b reveal"><img src="images/dessouchage.jpg" width="900" height="560" loading="lazy" alt="Rognage d’une souche avec une dessoucheuse dans un jardin"></div>
    <div class="reveal">
      <p class="eyebrow">Élagage et abattage</p>
      <h2>Des arbres taillés en toute sécurité.</h2>
      <p class="lead2">Un élagueur grimpeur qualifié et expérimenté diagnostique l’état de vos arbres, puis choisit la technique adaptée.</p>
      <ul class="ticks"><li>Élagage raisonné, sévère, de sécurité ou de mise en forme naturelle</li><li>Abattage d’arbres</li><li>Dessouchage et rognage de souche</li></ul>
    </div>
  </div>
</section>

<section class="section s-forest s-curve on-dark" id="p2">
  <div class="wrap split rev">
    <div class="reveal">
      <p class="eyebrow">Créations et travaux paysagers</p>
      <h2>Un jardin en harmonie avec votre maison.</h2>
      <p class="lead2">Nous étudions le potentiel du terrain, puis proposons un plan paysager et une composition végétale.</p>
      <ul class="ticks"><li>Plantation d’arbres, arbustes, haies et massifs</li><li>Création de rocailles, scarification de terrain</li><li>Plantation de gazon</li><li>Aménagement paysager de terrasses et de piscines</li></ul>
    </div>
    <div class="arch-b reveal"><img src="images/creation.jpg" width="900" height="560" loading="lazy" alt="Massif de plantes et pelouse devant une maison contemporaine" style="object-position:35% 50%"></div>
  </div>
</section>

<section class="section s-ivory s-curve" id="p3">
  <div class="wrap split">
    <div class="arch-b reveal"><img src="images/haies.jpg" width="900" height="560" loading="lazy" alt="Jardinier taillant une haie avec un taille-haie thermique"></div>
    <div class="reveal">
      <p class="eyebrow">Contrat d’entretien</p>
      <h2>Un espace vert suivi, saison après saison.</h2>
      <p class="lead2">Annuel ou ponctuel, pour votre résidence principale ou secondaire : un cahier des charges détaille les prestations selon la saison.</p>
      <ul class="ticks"><li>Tonte de la pelouse, taille de haies et d’arbustes</li><li>Taille et élagage des arbres fruitiers et des haies</li><li>Débroussaillage, engazonnement, scarification</li></ul>
    </div>
  </div>
</section>
'''+c5('Un projet en tête ? Parlons-en.','Appelez-nous ou remplissez le formulaire en ligne pour obtenir un devis.')+footer()
    write('prestations.html',s)

def zone():
    s=head('Zone d’intervention en Essonne | Borval Paysage à Saint-Maurice-Montcouronne','Borval Paysage intervient à Saint-Maurice-Montcouronne, Saint-Chéron, Dourdan, Roinville et alentours, en Essonne. Réduction d’impôt de 50 %.')+header('zone.html')
    chips=''.join(f'<span>{c}</span>' for c in ['Saint-Maurice-Montcouronne','Saint-Chéron','Dourdan','Roinville'])
    ic=lambda p:f'<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
    s+=f'''<section class="section s-ivory hero page-hero">
  <div class="wrap">
    <div class="trait" aria-hidden="true"></div>
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Zone d’intervention</p>
        <h1>Autour de <em>Saint-Maurice-Montcouronne,</em> en Essonne.</h1>
        <p class="lead">Borval Paysage se déplace à Saint-Chéron, à Dourdan et dans les communes alentour pour créer et entretenir votre espace vert.</p>
        <div class="cta-row"><a class="btn" href="contact.html">Vérifier mon secteur</a><a class="btn ghost" href="tel:{TELH}">{TEL}</a></div>
      </div>
      <div class="arch-wrap"><div class="arch"><img src="images/terrasse.jpg" width="900" height="560" alt="Terrasse en bois en cours de pose devant une maison en pierre" style="object-position:40% 50%"></div><div class="stamp"><b>Essonne</b>Depuis Saint-Maurice-Montcouronne</div></div>
    </div>
  </div>
</section>

<section class="section s-forest s-curve on-dark" id="communes">
  <div class="wrap">
    <div class="reveal"><p class="eyebrow">Communes</p><h2>Nos secteurs d’intervention</h2>
    <p class="lead2">Nous intervenons notamment à :</p></div>
    <div class="zone-chips big">{chips}</div>
    <p class="reveal">Votre commune n’apparaît pas ? Appelez-nous : nous vous dirons si nous pouvons nous déplacer.</p>
  </div>
</section>

<section class="section s-sage s-curve" id="clients">
  <div class="wrap">
    <div class="reveal"><p class="eyebrow">Pour qui ?</p><h2>Chaque espace vert,<br>chaque interlocuteur.</h2></div>
    <div class="steps three">
      <div class="step c-moss reveal">{ic('<path d="M6 24L24 8l18 16M12 20v20h24V20"/><path d="M20 40V28h8v12"/>')}<span class="n">Particuliers</span><h3>Votre jardin</h3><p>Résidence principale ou secondaire, entretien annuel ou ponctuel.</p></div>
      <div class="step c-olive reveal">{ic('<path d="M8 40V10h20v30M28 20h12v20M14 16h8M14 24h8M14 32h8"/>')}<span class="n">Professionnels</span><h3>Vos espaces verts</h3><p>Création et entretien des abords de votre activité.</p></div>
      <div class="step c-clay reveal">{ic('<path d="M6 40h36M10 40V22M20 40V22M30 40V22M40 40V22M6 22h36L24 8z"/>')}<span class="n">Collectivités</span><h3>Espaces publics</h3><p>Aménagement paysager et élagage d’espaces verts publics.</p></div>
    </div>
    <p class="note-line reveal">Réduction d’impôt de 50 % : Borval Paysage est affiliée aux services à la personne.</p>
  </div>
</section>
'''+c5('Une question sur votre secteur ?','Appelez-nous ou remplissez le formulaire en ligne : nous vous répondons.')+footer()
    write('zone.html',s)

def contact():
    s=head('Contact et demande de devis | Borval Paysage à Saint-Maurice-Montcouronne','Contactez Borval Paysage, paysagiste à Saint-Maurice-Montcouronne (91) : téléphone ou formulaire de demande de devis.')+header('contact.html')
    s+=f'''<section class="section s-ivory hero page-hero contact-hero">
  <div class="wrap">
    <div class="trait" aria-hidden="true"></div>
    <p class="eyebrow">Contact</p>
    <h1>Demandez votre <em>devis.</em></h1>
    <p class="lead">Appelez-nous ou remplissez le formulaire ci-dessous : nous vous recontactons pour parler de votre projet.</p>
  </div>
</section>
<section class="sv sk sk8" aria-labelledby="sv-k"><div class="hv-wrap"><div class="sk8-h"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2><p class="sk-intro">Indiquez votre commune et votre besoin : nous vous recontactons.</p></div><div class="sk-card"><form class="sk-form" id="kform" novalidate data-name="Borval Paysage" data-sms="{TELH}" data-tel="{TELH}" data-email=""><div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div><div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div><div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div><div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option><option>Élagage ou abattage d’arbres</option><option>Dessouchage</option><option>Création ou aménagement de jardin</option><option>Contrat d’entretien</option><option>Autre demande</option></select><p class="sk-err" id="k-besoin-e" role="alert"></p></div><div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div><button class="hv-btn hv-btn-p sk-go" type="submit">Préparer ma demande</button></form><div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l'envoyer. Rien n'est transmis tant que vous n'avez pas validé l'envoi.</p><pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a><button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a><a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div><aside class="sk-side"><ul><li class="sk-ct">{SV%PHP}<div><span>Téléphone</span><a href="tel:{TELH}">{TEL}</a></div></li><li class="sk-ct">{PIN}<div><span>Adresse</span><p>{ADR}</p></div></li></ul></aside></div></section>
'''+footer(True)
    write('contact.html',s)
index();prest();zone();contact();print('ok')
