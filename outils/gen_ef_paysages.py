import os, re, glob, shutil, subprocess, zipfile
from PIL import Image, ImageOps

S = '/tmp/claude-0/-home-claude/21682f86-10a1-5ad8-b2cf-f1952e1a68f5/scratchpad'
U = '/mnt/user-data/uploads/Maquettes/Images/Paysagiste/'
ZIP = '/mnt/user-data/uploads/Maquettes/Squelettes/S16.zip'
MOD = S + '/modules2/mod.py'
D = '/home/claude/maquettes/ef-paysages'
TEL, TELI = '06 72 98 54 47', '+33672985447'
SITE = 'https://webaunet.github.io/maquettes/ef-paysages/'

# ---- squelette S16 frais
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D + '/images')
zipfile.ZipFile(ZIP).extractall(D)
os.remove(D + '/_SKELETON.md')

# ---- palette et polices imposées (:root) ; accent jamais en texte sur fond clair
cp = D + '/style.css'
s = open(cp, encoding='utf8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

rep("--noir:#14150f; --vert:#5f8a22; --vert-fonce:#2f4a12; --terre:#e9e2d3; --craie:#fbfaf6; --texte:#23251c; --texte-doux:#4d5142;",
    "--noir:#1b1d18; --vert:#b9e04a; --vert-fonce:#1b1d18; --terre:#e4e9d4; --craie:#f4f6ef; --texte:#151712; --texte-doux:#4a4f41;")
rep("--f-titre:'Archivo Black','Archivo',Impact,sans-serif; --f-texte:'Archivo',system-ui,-apple-system,'Segoe UI',sans-serif;",
    "--f-titre:'Cormorant Garamond',Georgia,serif; --f-texte:'Hanken Grotesk',system-ui,-apple-system,'Segoe UI',sans-serif;")
s, n = re.subn(r'(?<![-\w])color:var\(--vert\)', 'color:var(--vert-fonce)', s)
print('accent texte remplacé :', n)
s, n = re.subn(r'background:var\(--vert\);color:#fff', 'background:var(--vert);color:var(--texte)', s)
assert n >= 1, n
open(cp, 'w', encoding='utf8').write(s)

# ---- modules imposés
r = subprocess.run(['python3', '-I', MOD, D, 'H12', 'V8', 'A4', 'M7', 'C10', 'F5', 'K1',
                    '--bg', '#f4f6ef', '--bg2', '#e4e9d4', '--ink', '#151712', '--mu', '#4a4f41',
                    '--main', '#1b1d18', '--acc', '#b9e04a', '--accink', '#151712',
                    '--fh', 'Cormorant Garamond', '--fb', 'Hanken Grotesk', '--fw', '700'],
                   capture_output=True, text=True)
assert r.returncode == 0, r.stderr
print('mod:', r.stdout.strip()[-160:])

s = open(cp, encoding='utf8').read()
s, n8 = re.subn(r'font-weight:\s*(?:[5-9]00|bold|bolder)', 'font-weight:700', s)
s, n9 = re.subn(r'font:(?:[5-9]00) ', 'font:700 ', s)
print('graisses ramenées à 700 :', n8, n9)
s += ('\n/* EF PAYSAGES */\n.logo span{font-family:var(--f-titre);font-size:1.6rem;font-weight:700;color:var(--noir);line-height:1}\n'
      '.btn:hover{color:#f4f6ef}\n'
      '.logo{display:inline-flex;align-items:center;min-height:44px}\n'
      '.ph{box-shadow:0 56px 0 0 var(--terre)}\n'
      '.hv12-bg img{width:min(100%,1408px);margin-left:auto}\n'
      '@media(max-width:820px){.ph{padding-block:40px 48px}.mosaic{aspect-ratio:16/10}}\n')
open(cp, 'w', encoding='utf8').write(s)

# ---- images (aucune agrandie)
def g(p):
    m = sorted(glob.glob(U + p))
    assert len(m) == 1, (p, m)
    return m[0]

CRE = g('imgi_4_creation*')
ALL = g('chantier all*e dall*e.jpg')
PLA = g('imgi_6_plantation*')
CON = g('conception*')
MAC = g('ma*onerie*')

def crop(src, size, cx, out):
    im = Image.open(src).convert('RGB')
    assert im.width >= size[0] and im.height >= size[1], (src, im.size)
    ImageOps.fit(im, size, Image.LANCZOS, centering=(cx, 0.5)).save(
        D + '/images/' + out, 'JPEG', quality=80, optimize=True, progressive=True)

def fit43(src, out):
    im = Image.open(src).convert('RGB')
    w = min(800, im.width)
    h = round(w * 3 / 4)
    assert im.height >= h, (src, im.size)
    ImageOps.fit(im, (w, h), Image.LANCZOS).save(D + '/images/' + out, 'JPEG', quality=80, optimize=True, progressive=True)
    return w, h

HIM = Image.open(MAC).convert('RGB')
HERO = HIM.size
HIM.save(D + '/images/hero.jpg', 'JPEG', quality=62, optimize=True, progressive=True)
crop(CON, (700, 700), 0.5, 'a1.jpg')
SZ = {k: fit43(src, k + '.jpg') for k, src in [('creation', CRE), ('allee', ALL), ('plantation', PLA)]}
print('images:', SZ)

def dim(k):
    w, h = SZ[k]
    return 'width="%d" height="%d"' % (w, h)

# ---- script.js : menu burger seul (le formulaire vit dans js/k.js)
open(D + '/script.js', 'w', encoding='utf8').write(
    "(function(){\n"
    "  var b=document.getElementById('burger'),m=document.getElementById('menu');\n"
    "  function set(o){m.classList.toggle('open',o);b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')}\n"
    "  b.addEventListener('click',function(){set(!m.classList.contains('open'))});\n"
    "  m.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});\n"
    "  document.addEventListener('keydown',function(e){if(e.key==='Escape')set(false)});\n"
    "})();\n")

# ---- pages
PHONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8.1 9.8a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')

NAV = [('index.html', 'Accueil'), ('prestations.html', 'Prestations'), ('contact.html', 'Contact')]

def header(cur):
    nav = ''.join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == cur else '', t) for h, t in NAV)
    return ('<header>\n  <div class="w bar">\n'
            '    <a class="logo" href="index.html" aria-label="EF PAYSAGES, accueil"><span>EF PAYSAGES</span></a>\n'
            '    <nav id="menu" aria-label="Navigation principale"><ul>' + nav + '</ul></nav>\n'
            '    <a class="btn tel" href="tel:' + TELI + '" aria-label="Appeler le ' + TEL + '">&#9990;<span class="num">&nbsp;' + TEL + '</span></a>\n'
            '    <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="menu"><span></span></button>\n'
            '  </div>\n</header>\n')

FOOT = ('<div class="hf hf5" role="contentinfo"><div class="hf5-top"><div class="hv-wrap"><strong>Un projet ? Demandez votre devis.</strong>'
        '<a href="contact.html">Nous contacter</a></div></div><div class="hf5-b"><div class="hv-wrap">'
        '<nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a><a href="contact.html">Contact</a></nav>'
        '<p class="hf-cop">© EF PAYSAGES · Mauchamps (91) · Maquette de démonstration</p></div></div></div>\n')

def page(fn, title, desc, cur, body, extra=''):
    head = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            "<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
            "%3Crect width='64' height='64' rx='16' fill='%231b1d18'/%3E%3Cpath d='M14 46c0-18 10-30 36-32-2 22-12 32-30 32' fill='%23b9e04a'/%3E%3C/svg%3E\">\n"
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@700&amp;family=Hanken+Grotesk:wght@400;700&amp;display=swap">\n'
            '<link rel="stylesheet" href="style.css">\n</head>\n<body>\n')
    html = head + header(cur) + '<main>\n' + body + '\n</main>\n' + FOOT + extra + '<script src="script.js"></script>\n</body>\n</html>\n'
    open(D + '/' + fn, 'w', encoding='utf8').write(html)

H12 = ('<section class="hv hv12 hv-dark" aria-labelledby="hv-t"><div class="hv12-bg"><img src="images/hero.jpg" width="' + str(HERO[0]) + '" height="' + str(HERO[1]) + '" '
       'alt="Maçonnerie paysagère : murets de pierre et escalier dans un jardin"></div><div class="hv-wrap hv12-in"><div class="hv12-txt">'
       '<p class="hv-kick">EF PAYSAGES · Aménagement paysager</p><h1 id="hv-t">Aménagement et entretien de vos espaces verts<em>Mauchamps (91)</em></h1>'
       '<svg class="hv12-line" viewBox="0 0 480 14" aria-hidden="true" focusable="false"><path d="M2 9C90 2 200 12 300 6S440 7 478 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'
       '<div class="hv12-cta"><a class="hv12-pill" href="prestations.html">Nos prestations<span aria-hidden="true">↗</span></a>'
       '<a class="hv12-pill" href="contact.html">Nous contacter<span aria-hidden="true">↗</span></a></div></div>'
       '<div class="hv12-card"><h2 class="hv12-ct">Demande de devis</h2><form class="sk-form" id="kform" novalidate data-name="EF PAYSAGES" data-sms="' + TELI + '" data-tel="' + TELI + '" data-email="">'
       '<div class="sk-f"><label for="h-nom">Nom</label><input id="h-nom" name="nom" type="text" placeholder="Votre nom" autocomplete="name" required aria-describedby="h-nom-e"><p class="sk-err" id="h-nom-e" role="alert"></p></div>'
       '<div class="sk-f"><label for="h-tel">Téléphone</label><input id="h-tel" name="tel" type="tel" placeholder="Votre téléphone" autocomplete="tel" inputmode="tel" required aria-describedby="h-tel-e"><p class="sk-err" id="h-tel-e" role="alert"></p></div>'
       '<div class="sk-f"><label for="h-commune">Commune</label><input id="h-commune" name="commune" type="text" placeholder="Votre commune" autocomplete="address-level2" required aria-describedby="h-commune-e"><p class="sk-err" id="h-commune-e" role="alert"></p></div>'
       '<div class="sk-f"><label for="h-msg">Votre demande</label><textarea id="h-msg" name="msg" rows="2" placeholder="Votre demande (facultatif)"></textarea><p class="sk-err" id="h-msg-e" role="alert"></p></div>'
       '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>'
       '<div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l’envoyer. Rien n’est transmis tant que vous n’avez pas validé l’envoi.</p>'
       '<pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a>'
       '<button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a>'
       '<a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div></div></section>')

V8 = ('<section class="sv sv8" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p>'
      '<h2 id="sv-t">Aménagement, maçonnerie et entretien</h2>'
      '<p class="hv-lead">Des travaux adaptés à votre terrain, de la conception à l’entretien.</p>'
      '<div class="sv8-grid">'
      '<article class="sv8-c sv8-c1"><h3>Aménagement</h3><ul><li>Création de jardins</li><li>Terrasses en bois</li><li>Plantations</li></ul>'
      '<a class="hv-btn hv-btn-s" href="prestations.html#c1">Voir le détail</a></article>'
      '<article class="sv8-c sv8-c2"><h3>Terrassement et maçonnerie</h3><ul><li>Terrassement</li><li>Allées et dallages</li><li>Murets et escaliers</li></ul>'
      '<a class="hv-btn hv-btn-s" href="prestations.html#c2">Voir le détail</a></article>'
      '<article class="sv8-c sv8-c3"><h3>Entretien</h3><ul><li>Tonte de pelouse</li><li>Taille de haies</li><li>Déchets verts</li></ul>'
      '<a class="hv-btn hv-btn-s" href="prestations.html#c3">Voir le détail</a></article>'
      '</div></div></section>')

A4 = ('<section class="sv sa4" aria-labelledby="sv-a"><div class="hv-wrap"><div><p class="hv-kick">À propos</p>'
      '<h2 id="sv-a">Une entreprise locale, dirigée par Emeric Foiry</h2>'
      '<p>EF PAYSAGES est une entreprise d’aménagement paysager basée à Mauchamps, dans l’Essonne (91).</p>'
      '<p>Ses travaux couvrent la création, l’aménagement et l’entretien des espaces verts.</p>'
      '<p class="sa4-sign">Emeric Foiry, dirigeant</p></div>'
      '<figure class="sa4-c"><img src="images/a1.jpg" width="700" height="700" alt="Plan de jardin étudié sur une tablette, avant les travaux (image d’illustration)"></figure>'
      '</div></section>')

M7 = ('<section class="sv sm7" aria-labelledby="sv-m"><div class="hv-wrap"><p class="hv-kick">Notre méthode</p>'
      '<h2 id="sv-m">Un projet cadré avant le premier coup de pelle</h2>'
      '<p class="hv-lead">Chaque chantier suit les mêmes étapes, expliquées avant le démarrage.</p>'
      '<ol class="sm7-l">'
      '<li class="sm7-s"><span class="sm7-n" aria-hidden="true">1</span><div class="sm7-c"><h3>On écoute</h3><p>Vous décrivez votre terrain, vos usages et votre budget.</p></div></li>'
      '<li class="sm7-s"><span class="sm7-n" aria-hidden="true">2</span><div class="sm7-c"><h3>On conçoit</h3><p>Le projet est dessiné et expliqué avant de démarrer.</p></div></li>'
      '<li class="sm7-s"><span class="sm7-n" aria-hidden="true">3</span><div class="sm7-c"><h3>On réalise</h3><p>Terrassement, construction et plantations, selon le devis accepté.</p></div></li>'
      '<li class="sm7-s"><span class="sm7-n" aria-hidden="true">4</span><div class="sm7-c"><h3>On entretient</h3><p>Un suivi régulier de votre jardin, si vous le souhaitez.</p></div></li>'
      '</ol></div></section>')

C10 = ('<section class="sv sc10" aria-labelledby="sv-c"><div class="hv-wrap"><p class="hv-kick">Contact</p>'
       '<h2 id="sv-c">Un projet de jardin&nbsp;? Parlons-en.</h2>'
       '<a class="sc10-tel" href="tel:' + TELI + '">' + TEL + '</a>'
       '<p class="hv-lead">Appelez EF PAYSAGES ou envoyez votre demande de devis en ligne.</p>'
       '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="contact.html">Demander un devis</a>'
       '<a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div>'
       '<p class="sc10-add">Mauchamps (91)</p></div></section>')

EY = {'c1': 'Aménager', 'c2': 'Construire', 'c3': 'Entretenir'}

def cat(id_, title, items, band=''):
    lis = ''.join('<article class="card"><div><h3>%s</h3><p>%s</p></div></article>' % it for it in items)
    return ('<section class="band%s" id="%s" aria-labelledby="t-%s"><div class="w"><div class="head"><span class="eyebrow">%s</span>'
            '<h2 id="t-%s">%s</h2></div><div class="grid">%s</div></div></section>' % (band, id_, id_, EY[id_], id_, title, lis))

# index
page('index.html', 'EF PAYSAGES, aménagement paysager à Mauchamps (91)',
     'EF PAYSAGES, entreprise d’aménagement paysager à Mauchamps dans l’Essonne (91) : création de jardins, terrassement, plantations et entretien. Appelez le ' + TEL + '.',
     'index.html', H12 + V8 + A4 + M7 + C10,
     extra='<script src="js/k.js" defer></script>\n')

# prestations
MOSAIC = ('<div class="mosaic">'
          '<img src="images/creation.jpg" ' + dim('creation') + ' alt="Jardin en cours de création avec pelouse et massifs (image d’illustration)">'
          '<img src="images/allee.jpg" ' + dim('allee') + ' alt="Allée en dalles bordée de massifs (image d’illustration)">'
          '<img src="images/plantation.jpg" ' + dim('plantation') + ' alt="Plantation d’un massif par un jardinier (image d’illustration)">'
          '</div>')
PREST = ('<section class="ph" aria-labelledby="h1"><div class="w"><div><span class="eyebrow">Prestations · Mauchamps (91)</span>'
         '<h1 id="h1">Création, aménagement et entretien de vos espaces verts</h1>'
         '<p>De la conception de votre jardin à son entretien régulier, EF PAYSAGES intervient à Mauchamps (91).</p>'
         '<div class="cta" style="margin-top:24px"><a class="btn" href="contact.html">Demander un devis</a>'
         '<a class="btn ghost" href="tel:' + TELI + '">Appeler le ' + TEL + '</a></div></div>' + MOSAIC + '</div></section>'
         + cat('c1', 'Aménagement', [
             ('Création de jardins', 'Conception et aménagement de votre jardin selon votre terrain.'),
             ('Terrasses en bois', 'Pose de terrasses pour prolonger la maison vers le jardin.'),
             ('Plantations', 'Arbustes, massifs et végétaux choisis pour votre terrain.')], ' terre')
         + cat('c2', 'Terrassement et maçonnerie', [
             ('Terrassement', 'Décaissement, remblai et nivellement avant la création.'),
             ('Allées et dallages', 'Allées et dallages pour circuler dans le jardin.'),
             ('Murets et escaliers', 'Ouvrages en pierre pour structurer le jardin.')])
         + cat('c3', 'Entretien', [
             ('Tonte de pelouse', 'Pelouse tondue régulièrement, bordures reprises.'),
             ('Taille de haies', 'Haies et arbustes taillés, déchets évacués.'),
             ('Déchets verts', 'Branches et tontes chargées et évacuées après le chantier.')], ' sombre')
         + '<section class="band terre"><div class="w"><div class="head"><span class="eyebrow">Votre projet</span>'
         '<h2>Un jardin à créer ou à entretenir ?</h2><p>Appelez EF PAYSAGES ou décrivez votre besoin : nous revenons vers vous.</p>'
         '<div class="cta"><a class="btn" href="tel:' + TELI + '">Appeler le ' + TEL + '</a>'
         '<a class="btn ghost" href="contact.html">Demander un devis</a></div></div></div></section>')
page('prestations.html', 'Prestations · EF PAYSAGES à Mauchamps (91)',
     'Prestations de EF PAYSAGES à Mauchamps (91) : création de jardins, terrassement, allées, plantations et entretien d’espaces verts.',
     'prestations.html', PREST)

# contact
CONTACT = ('<section class="band court" aria-labelledby="h1"><div class="w"><div class="head"><span class="eyebrow">Contact · Mauchamps (91)</span>'
           '<h1 id="h1">Contactez EF PAYSAGES à Mauchamps</h1><p>Décrivez votre projet en quelques lignes, ou appelez directement.</p></div></div></section>'
           '<section class="sv sk sk1" aria-labelledby="sv-k"><div class="hv-wrap sk-grid"><div class="sk-card"><p class="hv-kick">Demande de devis</p>'
           '<h2 id="sv-k">Parlez-nous de votre projet</h2>'
           '<p class="sk-intro">Décrivez votre besoin : vous obtenez un message prêt à envoyer par SMS ou à copier.</p>'
           '<form class="sk-form" id="kform" novalidate data-name="EF PAYSAGES" data-sms="' + TELI + '" data-tel="' + TELI + '" data-email="">'
           '<div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div>'
           '<div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div>'
           '<div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div>'
           '<div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option>'
           '<option>Création de jardin</option><option>Entretien de jardin</option><option>Terrasse ou allée</option><option>Plantation</option><option>Autre demande</option></select>'
           '<p class="sk-err" id="k-besoin-e" role="alert"></p></div>'
           '<div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div>'
           '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>'
           '<div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l’envoyer. Rien n’est transmis tant que vous n’avez pas validé l’envoi.</p>'
           '<pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a>'
           '<button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a>'
           '<a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div>'
           '<aside class="sk-side"><h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:' + TELI + '">' + TEL + '</a></li>'
           '<li><span>Adresse</span><p>Mauchamps (91)</p></li></ul></aside></div></section>')
page('contact.html', 'Contact · EF PAYSAGES à Mauchamps (91)',
     'Contactez EF PAYSAGES à Mauchamps (91) : demande de devis en ligne ou appel au ' + TEL + '.',
     'contact.html', CONTACT, extra='<script src="js/k.js" defer></script>\n')

open(D + '/README.md', 'w', encoding='utf8').write(
    '# EF PAYSAGES (Mauchamps, 91)\n\nMaquette de site vitrine (démonstration, non publiée auprès du client).\n\n'
    'Pages : index, prestations, contact.\n')
print('pages:', sorted(f for f in os.listdir(D) if f.endswith('.html')))
print('images:', sorted(os.listdir(D + '/images')))
