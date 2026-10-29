import re
D='/home/claude/maquettes/biovert-jardins/'
BASE='https://webaunet.github.io/maquettes/biovert-jardins/'
TEL='06 19 58 28 76';TELH='+33619582876';MAIL='contact@biovertjardin.com'
ADR='12 avenue des Prés, 78180 Montigny-le-Bretonneux'
PAGES=[('index.html','Accueil'),('prestations.html','Prestations'),('zone.html','Zone d’intervention'),('contact.html','Contact')]
PHP='<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
SV='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
PIN='<svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 43s14-12 14-23a14 14 0 0 0-28 0c0 11 14 23 14 23z"/><circle cx="24" cy="20" r="5"/></svg>'
CLK='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
MLI='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'
def head(t,d):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
'''
def header(cur):
    nav=''.join(f'<a href="{h}"{" aria-current=\"page\"" if h==cur else ""}>{n}</a>' for h,n in PAGES)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="logo" href="{BASE}" aria-label="Biovert Jardins, accueil"><img src="images/logo.png" width="298" height="262" alt="Biovert Jardins"></a>
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
def footer():
    nav=''.join(f'<a href="{h}">{n}</a>' for h,n in PAGES)
    return f'''</main>
<footer class="hf hf2"><div class="hv-wrap"><a class="hf-logo" href="{BASE}" aria-label="Biovert Jardins, accueil"><img src="images/logo.png" width="298" height="262" alt="Biovert Jardins"></a><nav aria-label="Pied de page">{nav}</nav><a href="tel:{TELH}">{TEL}</a><p class="hf-cop">© Biovert Jardins · Maquette de site vitrine</p></div></footer>
<script src="js/main.js"></script>
</body>
</html>
'''
def c6(h2='Un projet de jardin ? Parlons-en.',lead='Demandez votre devis : appelez-nous ou écrivez-nous, du lundi au vendredi de 8h à 18h.'):
    return f'''<section class="sv sc6" aria-labelledby="sv-c"><div class="hv-wrap"><div><p class="hv-kick">Contact</p><h2 id="sv-c">{h2}</h2><p class="hv-lead">{lead}</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div></div><ul class="sc6-l"><li><a href="tel:{TELH}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{ADR}</li></ul></div></section>
'''
def write(n,s): open(D+n,'w',encoding='utf8').write(s)

# ---------- ACCUEIL
def index():
    s=head('Biovert Jardins | Paysagiste à Montigny-le-Bretonneux (78), entretien et création de jardins','Biovert Jardins, paysagiste à Montigny-le-Bretonneux (Yvelines) : entretien de jardins, création de jardins et élagage, avec des pratiques écologiques. Devis sur demande.')+header('index.html')
    s+=f'''<section class="hv hv5" aria-labelledby="hv-t"><div class="hv-wrap"><p class="hv-kick">Paysagiste à Montigny-le-Bretonneux (78)</p><h1 id="hv-t">Un jardin entretenu et aménagé dans le respect du vivant</h1><div class="hv5-rule"></div>
<div class="hv5-grid"><div><p class="hv-lead">Biovert Jardins entretient et crée les jardins des particuliers, copropriétés et entreprises dans les Yvelines : entretien, aménagement paysager et élagage, avec des solutions naturelles.</p><div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:{TELH}">Appeler le {TEL}</a><a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>
<div class="hv5-pic"><img src="images/hero.jpg" width="1100" height="600" alt="Allée de gravier bordée de massifs fleuris et de pelouse, devant une maison de village" style="object-position:62% 50%"></div>
<ul class="hv5-facts"><li><strong>Depuis 2014</strong>entreprise de service à la personne</li><li><strong>Zéro pesticide</strong>solutions naturelles</li><li><strong>Lun – ven</strong>8h – 18h</li></ul></div></div></section>
<section class="sv sv3" id="prestations" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Entretenir, créer, élaguer : un jardin complet</h2><p class="hv-lead">Un suivi régulier ou une intervention ponctuelle, selon vos besoins.</p><div class="sv3-tabs"><input type="radio" name="sv3" id="sv3-1" class="sv3-r skip" checked><input type="radio" name="sv3" id="sv3-2" class="sv3-r skip"><input type="radio" name="sv3" id="sv3-3" class="sv3-r skip"><input type="radio" name="sv3" id="sv3-4" class="sv3-r skip"><div class="sv3-grid"><div class="sv3-list"><label for="sv3-1"><span class="sv3-n">01</span><strong>Contrats d’entretien</strong><span class="sv3-d">Un jardin impeccable toute l’année.</span></label><label for="sv3-2"><span class="sv3-n">02</span><strong>Interventions ponctuelles</strong><span class="sv3-d">Nettoyage, taille, évacuation des déchets verts.</span></label><label for="sv3-3"><span class="sv3-n">03</span><strong>Création de jardins</strong><span class="sv3-d">Massifs, haies, allées, potagers.</span></label><label for="sv3-4"><span class="sv3-n">04</span><strong>Élagage d’arbres</strong><span class="sv3-d">Pour des arbres sains et bien conduits.</span></label></div><div>
<figure class="sv3-v sv3-v1"><img src="images/p1.jpg" width="1100" height="600" alt="Jardinier tondant une pelouse devant une maison bordée de massifs" loading="lazy"><figcaption><h3>Contrats d’entretien</h3><p>Tonte, taille de haies et d’arbustes, désherbage manuel, fertilisation naturelle et paillage : des passages mensuels, bimensuels ou selon vos besoins.</p><a href="prestations.html#p1">En savoir plus →</a></figcaption></figure>
<figure class="sv3-v sv3-v2"><img src="images/p2.jpg" width="1100" height="600" alt="Jardinier ramassant des feuilles mortes sur une allée de gravier" loading="lazy"><figcaption><h3>Interventions ponctuelles</h3><p>Nettoyage de printemps ou d’automne, taille de rajeunissement, évacuation des déchets verts : sans engagement à long terme.</p><a href="prestations.html#p2">En savoir plus →</a></figcaption></figure>
<figure class="sv3-v sv3-v3"><img src="images/p3.jpg" width="1100" height="600" alt="Jardinier plantant des végétaux dans un massif" loading="lazy"><figcaption><h3>Création de jardins</h3><p>Massifs fleuris, potagers, haies, allées, paillis et bordures, avec des plantes locales et une gestion de l’eau.</p><a href="prestations.html#p3">En savoir plus →</a></figcaption></figure>
<figure class="sv3-v sv3-v4"><img src="images/p4.jpg" width="1100" height="600" alt="Élagueur encordé travaillant dans un grand chêne au-dessus d’un jardin" loading="lazy"><figcaption><h3>Élagage d’arbres</h3><p>Biovert Jardins intervient aussi pour l’élagage des arbres de votre jardin.</p><a href="prestations.html#p4">En savoir plus →</a></figcaption></figure>
</div></div></div></div></section>
<section class="sv sm4" id="approche" aria-labelledby="sv-m"><div class="hv-wrap"><p class="hv-kick">Notre approche</p><h2 id="sv-m">Un entretien respectueux de la nature</h2><p class="hv-lead">Un équilibre entre esthétique, efficacité et respect du vivant.</p><div class="sm4-grid"><article class="sm4-c"><span class="sm4-n">1</span><h3>Zéro pesticide</h3><p>Des solutions naturelles pour entretenir vos espaces verts.</p></article><article class="sm4-c"><span class="sm4-n">2</span><h3>Déchets verts valorisés</h3><p>Broyage, paillage et compostage pour nourrir naturellement les sols.</p></article><article class="sm4-c"><span class="sm4-n">3</span><h3>Biodiversité préservée</h3><p>Respect des plantes, des insectes utiles et des pollinisateurs.</p></article><article class="sm4-c"><span class="sm4-n">4</span><h3>Matériel moins impactant</h3><p>Des équipements performants pour limiter les nuisances.</p></article></div></div></section>
<section class="sv sa6" id="apropos" aria-labelledby="sv-a"><div class="hv-wrap"><figure class="sa6-ban"><img src="images/a1.jpg" width="1100" height="600" alt="Jardinier désherbant à la main un massif fleuri" loading="lazy" style="object-position:50% 60%"></figure><div class="sa6-card"><p class="hv-kick">À propos</p><h2 id="sv-a">Votre jardin, toute l’année</h2><p>Implantée dans les Yvelines, l’équipe de Biovert Jardins accompagne les particuliers, les copropriétés et les entreprises. Entreprise de service à la personne déclarée depuis 2014.</p><p>Biovert Jardins soutient aussi le club FC Versailles : engagement, esprit d’équipe et ancrage local.</p><a class="hv-btn hv-btn-p" href="zone.html">Notre zone d’intervention</a></div></div></section>
'''+c6()+footer()
    write('index.html',s)

# ---------- PRESTATIONS
def prest():
    s=head('Prestations de paysagiste dans les Yvelines | Biovert Jardins','Contrats d’entretien de jardins, interventions ponctuelles, création de jardins et élagage : les prestations de Biovert Jardins à Montigny-le-Bretonneux (78).')+header('prestations.html')
    s+=f'''<section class="section s-ivory hero page-hero">
  <div class="wrap">
    <div class="trait" aria-hidden="true"></div>
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Nos prestations</p>
        <h1>Entretien et création de jardins, <em>en harmonie avec la nature.</em></h1>
        <p class="lead">Contrats d’entretien, interventions ponctuelles, création de jardins et élagage : Biovert Jardins prend soin de vos espaces verts dans les Yvelines.</p>
        <div class="cta-row"><a class="btn" href="contact.html">Demander un devis</a><a class="btn ghost" href="tel:{TELH}">Appeler le {TEL}</a></div>
      </div>
      <div class="mosaic" aria-label="Aperçu de nos prestations">
        <div class="m1"><img src="images/p1.jpg" width="1100" height="600" alt="Jardinier tondant une pelouse devant une maison" style="object-position:40% 50%"></div>
        <div class="m2"><img src="images/p3.jpg" width="1100" height="600" alt="Jardinier plantant des végétaux dans un massif"></div>
        <div class="m3"><img src="images/p4.jpg" width="1100" height="600" alt="Élagueur encordé dans un grand chêne"></div>
      </div>
    </div>
  </div>
</section>

<section class="section s-sage s-curve" id="p1">
  <div class="wrap split">
    <div class="arch-b reveal"><img src="images/haies.jpg" width="1100" height="600" loading="lazy" alt="Jardinier taillant une haie avec un taille-haie thermique"></div>
    <div class="reveal">
      <p class="eyebrow">Contrats d’entretien</p>
      <h2>Un jardin impeccable, toute l’année.</h2>
      <p class="lead2">Des passages mensuels, bimensuels ou selon vos besoins, adaptés à la saison, à votre type de jardin et à vos préférences.</p>
      <ul class="ticks"><li>Tonte de pelouse, taille de haies et d’arbustes</li><li>Désherbage manuel et écologique</li><li>Fertilisation naturelle et paillage</li><li>Suivi et soins des plantations</li></ul>
    </div>
  </div>
</section>

<section class="section s-forest s-curve on-dark" id="p2">
  <div class="wrap split rev">
    <div class="reveal">
      <p class="eyebrow">Interventions ponctuelles</p>
      <h2>Un coup de frais, sans engagement.</h2>
      <p class="lead2">Avant un événement, à la sortie de l’hiver ou en préparation de l’été : des interventions ciblées et efficaces.</p>
      <ul class="ticks"><li>Nettoyage de printemps ou d’automne</li><li>Taille de rajeunissement</li><li>Évacuation des déchets verts</li><li>Traitements naturels contre maladies et parasites</li></ul>
    </div>
    <div class="arch-b reveal"><img src="images/dechets.jpg" width="1100" height="600" loading="lazy" alt="Jardinier chargeant des déchets verts dans une camionnette" style="object-position:40% 50%"></div>
  </div>
</section>

<section class="section s-ivory s-curve" id="p3">
  <div class="wrap split">
    <div class="arch-b reveal"><img src="images/creation.jpg" width="1100" height="600" loading="lazy" alt="Jardinier plantant un massif le long d’une pelouse devant une maison contemporaine" style="object-position:35% 50%"></div>
    <div class="reveal">
      <p class="eyebrow">Création de jardins</p>
      <h2>Créer ou transformer votre jardin.</h2>
      <p class="lead2">Un jardin durable, esthétique et fonctionnel, qui respecte la biodiversité.</p>
      <ul class="ticks"><li>Massifs fleuris, potagers ou espaces naturels</li><li>Plantation d’arbres, arbustes et haies</li><li>Paillis, bordures et allées</li><li>Gestion de l’eau et permaculture</li></ul>
    </div>
  </div>
</section>

<section class="section s-sage s-curve" id="p4">
  <div class="wrap split rev">
    <div class="reveal">
      <p class="eyebrow">Élagage d’arbres</p>
      <h2>Des arbres sains, bien conduits.</h2>
      <p class="lead2">Biovert Jardins intervient pour l’élagage des arbres, en complément de l’entretien et de l’aménagement de votre jardin.</p>
      <div class="cta-row" style="margin-top:24px"><a class="btn" href="contact.html">Parler de mon projet</a></div>
    </div>
    <div class="arch-b reveal"><img src="images/p4.jpg" width="1100" height="600" loading="lazy" alt="Élagueur encordé et casqué dans un grand chêne"></div>
  </div>
</section>
'''+c6('Un projet en tête ? Parlons-en.','Décrivez-nous votre jardin : nous vous répondons du lundi au vendredi, de 8h à 18h.')+footer()
    write('prestations.html',s)

# ---------- ZONE
COM=['Versailles','Rambouillet','Chevreuse','Maurepas','Poissy','Saint-Cyr-l’École','Montigny-le-Bretonneux','Marly-le-Roi','Élancourt','Le Chesnay','Jouars-Pontchartrain','Guyancourt','Noisy-le-Roi','Plaisir','Coignières']
def zone():
    s=head('Zone d’intervention dans les Yvelines (78) | Biovert Jardins','Biovert Jardins intervient à Versailles, Rambouillet, Chevreuse, Maurepas, Poissy et dans tout le département des Yvelines.')+header('zone.html')
    chips=''.join(f'<span>{c}</span>' for c in COM)
    s+=f'''<section class="section s-ivory hero page-hero">
  <div class="wrap">
    <div class="trait" aria-hidden="true"></div>
    <div class="hero-grid">
      <div>
        <p class="eyebrow">Zone d’intervention</p>
        <h1>Dans toutes les <em>Yvelines</em>, au plus près de chez vous.</h1>
        <p class="lead">Basée à Montigny-le-Bretonneux, l’équipe de Biovert Jardins se déplace chez les particuliers, les copropriétés et les entreprises.</p>
        <div class="cta-row"><a class="btn" href="contact.html">Vérifier mon secteur</a><a class="btn ghost" href="tel:{TELH}">{TEL}</a></div>
      </div>
      <div class="arch-wrap"><div class="arch"><img src="images/allee.jpg" width="1100" height="600" alt="Allée dallée éclairée au crépuscule devant une maison en pierre" style="object-position:35% 50%"></div><div class="stamp"><b>Yvelines</b>Depuis Montigny-le-Bretonneux</div></div>
    </div>
  </div>
</section>

<section class="section s-forest s-curve on-dark" id="communes">
  <div class="wrap">
    <div class="reveal"><p class="eyebrow">Communes</p><h2>Nos principaux secteurs</h2>
    <p class="lead2">Nous accompagnons les particuliers et les professionnels à :</p></div>
    <div class="zone-chips big">{chips}</div>
    <p class="reveal">Nous pouvons aussi intervenir dans les Yvelines et les départements limitrophes. Votre commune n’apparaît pas ? Appelez-nous.</p>
  </div>
</section>

<section class="section s-sage s-curve" id="infos">
  <div class="wrap">
    <div class="reveal"><p class="eyebrow">Infos pratiques</p><h2>Nous trouver, nous joindre.</h2></div>
    <ul class="direct" style="margin-top:28px;max-width:720px">
      <li><a href="tel:{TELH}">{SV%PHP}<span><small>Service commercial</small>{TEL}</span></a></li>
      <li><div>{CLK}<span><small>Horaires</small>Du lundi au vendredi, 8h – 18h</span></div></li>
      <li><div>{PIN}<span><small>Adresse</small>{ADR}</span></div></li>
      <li><div>{SV%'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>'}<span><small>Service à la personne</small>Déclarée le 24/09/2014 · N° SAP804467553</span></div></li>
    </ul>
  </div>
</section>
'''+c6('Une question sur votre secteur ?','Appelez-nous ou écrivez-nous : nous vous dirons si nous pouvons nous déplacer.')+footer()
    write('zone.html',s)

# ---------- CONTACT
def contact():
    s=head('Contact et demande de devis | Biovert Jardins à Montigny-le-Bretonneux','Contactez Biovert Jardins, paysagiste à Montigny-le-Bretonneux (78) : téléphone, e-mail ou formulaire de demande de devis.')+header('contact.html')
    dl=f'''<li><a href="tel:{TELH}">{SV%PHP}<span><small>Service commercial</small>{TEL}</span></a></li>
          <li><a href="mailto:{MAIL}">{MLI}<span><small>E-mail</small>{MAIL}</span></a></li>
          <li><div>{PIN}<span><small>Adresse</small>{ADR}</span></div></li>'''
    s+=f'''<section class="section s-ivory hero page-hero contact-hero">
  <div class="wrap">
    <div class="trait" aria-hidden="true"></div>
    <div class="contact-grid">
      <div>
        <p class="eyebrow">Contact</p>
        <h1>Demandez votre <em>devis.</em></h1>
        <p class="lead">Dites-nous où vous êtes et ce que vous souhaitez : nous vous recontactons du lundi au vendredi, de 8h à 18h.</p>
        <ul class="direct only-d">
          {dl}
        </ul>
      </div>
      <div class="form-card">
        <form id="devis" novalidate>
          <h2>Votre demande</h2>
          <div class="field"><label for="nom">Nom</label><input id="nom" name="nom" type="text" autocomplete="name" required aria-describedby="err-nom"><p class="error" id="err-nom" role="alert"></p></div>
          <div class="field"><label for="tel">Téléphone</label><input id="tel" name="tel" type="tel" inputmode="tel" autocomplete="tel" required placeholder="06 00 00 00 00" aria-describedby="err-tel"><p class="error" id="err-tel" role="alert"></p></div>
          <div class="field"><label for="commune">Commune du chantier</label><input id="commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="err-commune"><p class="error" id="err-commune" role="alert"></p></div>
          <div class="field"><label for="besoin">Votre besoin</label><select id="besoin" name="besoin" required aria-describedby="err-besoin"><option value="">Choisir…</option><option>Contrat d’entretien de jardin</option><option>Intervention ponctuelle</option><option>Création ou transformation de jardin</option><option>Élagage d’arbres</option><option>Autre projet</option></select><p class="error" id="err-besoin" role="alert"></p></div>
          <div class="field"><label for="message">Message (facultatif)</label><textarea id="message" name="message" rows="3" aria-describedby="err-message"></textarea><p class="error" id="err-message" role="alert"></p></div>
          <button class="btn full" type="submit">Préparer ma demande</button>
        </form>
        <div class="summary" id="summary" hidden tabindex="-1">
          <p class="ok"><svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 25l9 9 19-20"/></svg><span>Demande prête. Envoyez-la en un geste :</span></p>
          <pre id="recap"></pre>
          <div class="sum-actions">
            <a class="btn" id="sms" href="sms:{TELH}">Envoyer par SMS</a>
            <a class="btn ghost" id="mail" href="mailto:{MAIL}">Envoyer par e-mail</a>
            <button class="btn ghost" type="button" id="copy">Copier</button>
            <a class="btn ghost" href="tel:{TELH}">Appeler</a>
          </div>
          <p class="copied" id="copied" role="status"></p>
          <button class="link" type="button" id="edit">Modifier ma demande</button>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section s-forest s-curve on-dark band-end">
  <div class="wrap">
    <div class="reveal"><p class="eyebrow">Nous trouver</p><h2>Biovert Jardins, Yvelines.</h2></div>
    <ul class="direct only-m">
          {dl}
        </ul>
    <p class="lead2" style="max-width:40em">Du lundi au vendredi, de 8h à 18h. Entreprise de service à la personne déclarée le 24/09/2014, N° SAP804467553.</p>
    <div class="cta-row"><a class="btn" href="zone.html">Voir notre zone d’intervention</a></div>
  </div>
</section>
'''+footer()
    write('contact.html',s)
index();prest();zone();contact()
j=open(D+'js/main.js',encoding='utf8').read()
if 'Atmosphère' in j or '0669718436' in j:
    j=j.replace('Demande de devis - Atmosphère Paysage','Demande de devis - Biovert Jardins')
    j=j.replace("document.getElementById('sms').href = 'sms:0669718436?&body=' + encodeURIComponent(t);","document.getElementById('sms').href = 'sms:+33619582876?&body=' + encodeURIComponent(t);\n    document.getElementById('mail').href = 'mailto:contact@biovertjardin.com?subject=' + encodeURIComponent('Demande de devis') + '&body=' + encodeURIComponent(t);")
    open(D+'js/main.js','w',encoding='utf8').write(j)
print('ok')
