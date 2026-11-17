import os, re, glob, shutil, subprocess, zipfile
from PIL import Image, ImageOps

S = '/tmp/claude-0/-home-claude/21682f86-10a1-5ad8-b2cf-f1952e1a68f5/scratchpad'
U = '/mnt/user-data/uploads/Maquettes/Images/Paysagiste/'
ZIP = '/mnt/user-data/uploads/Maquettes/Squelettes/S05.zip'
MOD = S + '/modules/mod.py'
D = '/home/claude/maquettes/esa'
TEL, TELI = '06 61 09 05 59', '+33661090559'
SITE = 'https://webaunet.github.io/maquettes/esa/'

# ---- squelette S05 frais
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D + '/images')
zipfile.ZipFile(ZIP).extractall(D)
os.remove(D + '/_SKELETON.md')

# ---- palette et polices imposées (variables :root uniquement) + accent jamais en texte
cp = D + '/css/style.css'
s = open(cp, encoding='utf8').read()

def rep(a, b):
    global s
    assert s.count(a) == 1, a
    s = s.replace(a, b)

rep('--foret:#1f3a2d;--foret-2:#2b4d3c;--sauge:#8fa68a;--sauge-clair:#dfe7d8;',
    '--foret:#1f3d2b;--foret-2:#1f3d2b;--sauge:#4a5a4f;--sauge-clair:#e6ecdc;')
rep('--pierre:#f1ebdf;--pierre-2:#e7dfce;--terre:#b5623b;--terre-fonce:#8f4a29;',
    '--pierre:#e6ecdc;--pierre-2:#dde5d2;--terre:#b4531a;--terre-fonce:#8f3c12;')
rep('--encre:#1b1f1c;--texte:#2c332e;--blanc:#fffdf8;',
    '--encre:#1b2a21;--texte:#1b2a21;--blanc:#f6f1e6;')
rep('--serif:"Fraunces",Georgia,"Times New Roman",serif;--sans:"Inter",',
    '--serif:"Outfit",system-ui,-apple-system,"Segoe UI",sans-serif;--sans:"Figtree",')
s, n = re.subn(r'(?<=[;{])color:var\(--terre\)', 'color:var(--foret)', s)
assert n == 3, n
open(cp, 'w', encoding='utf8').write(s)

# ---- modules imposés
r = subprocess.run(['python3', '-I', MOD, D, 'H5', 'V6', 'A3', 'M4', 'C6', 'F5', 'K2',
                    '--bg', '#f6f1e6', '--bg2', '#e6ecdc', '--ink', '#1b2a21', '--mu', '#4a5a4f',
                    '--main', '#1f3d2b', '--acc', '#b4531a', '--accink', '#ffffff',
                    '--fh', 'Outfit', '--fb', 'Figtree', '--fw', '700'], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
print('mod:', r.stdout.strip()[-200:])
open(cp, 'a', encoding='utf8').write(
    '\n/* E.S.A. */\n.logo small{font-size:1rem}\n'
    '@media(max-width:620px){.hf5-top{display:none}.sv6-big img{aspect-ratio:16/7!important;height:auto!important;object-fit:cover}'
    '.cards .card img{aspect-ratio:16/9;height:auto;object-fit:cover}.sv6 .hv-lead{display:none}.sv6-big div{padding:26px 16px 12px}.sv6-t{padding:10px}.sv6-grid{gap:10px!important}}\n')

# ---- images (6 photos retenues, recadrées aux dimensions des modules)
def g(p):
    m = sorted(glob.glob(U + p))
    assert len(m) == 1, (p, m)
    return m[0]

CRE = g('imgi_4_creation*')
TER = g('*terrasse*')
ALL = g('*pav*carrelage*')
MUR = g('*ma*onerie*')
PLA = g('imgi_6_plantation*')
TON = g('imgi_2_tonte*')

def crop(src, size, cx, out):
    im = ImageOps.fit(Image.open(src).convert('RGB'), size, Image.LANCZOS, centering=(cx, 0.5))
    im.save(D + '/images/' + out, 'JPEG', quality=80, optimize=True, progressive=True)

def fitw(src, maxw, out):
    im = Image.open(src).convert('RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(D + '/images/' + out, 'JPEG', quality=80, optimize=True, progressive=True)
    return im.size

crop(ALL, (800, 1000), 0.5, 'hero.jpg')
crop(CRE, (1000, 1000), 0.4, 'p1.jpg')
crop(TER, (800, 1000), 0.5, 'a1.jpg')
crop(PLA, (600, 600), 0.5, 'a2.jpg')
SZ = {k: fitw(src, 1000, k + '.jpg') for k, src in
      [('creation', CRE), ('terrasse', TER), ('allee', ALL), ('muret', MUR), ('tonte', TON)]}

def dim(k):
    w, h = SZ[k]
    return 'width="%d" height="%d"' % (w, h)

# ---- pages
PHONE_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
             'stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 '
             '19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 '
             '2.1L8.1 9.8a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')

NAV = [('index.html', 'Accueil'), ('prestations.html', 'Prestations'),
       ('approche.html', 'Notre approche'), ('contact.html', 'Contact')]

def header(cur):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == cur else '', t) for h, t in NAV)
    return ('<header class="site-header">\n  <div class="wrap">\n'
            '    <a class="logo" href="' + SITE + '" aria-label="E.S.A., accueil">\n'
            '      <svg viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="18" fill="#1f3d2b"/>'
            '<path d="M14 47c0-19 10-31 37-33-2 23-13 33-31 33" fill="#b4531a"/>'
            '<path d="M14 47C22 36 31 28 44 21" stroke="#f6f1e6" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>\n'
            '      <span><b>E.S.A.</b><small>Montchauvet</small></span>\n    </a>\n'
            '    <nav class="nav" id="menu" aria-label="Navigation principale">' + nav + '</nav>\n'
            '    <div class="header-tools">\n'
            '      <a class="btn btn-terre header-call" href="tel:' + TELI + '" aria-label="Appeler le ' + TEL + '">' + PHONE_SVG + '<span>' + TEL + '</span></a>\n'
            '      <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span></button>\n'
            '    </div>\n  </div>\n</header>\n')

FOOT = ('<footer class="hf hf5" role="contentinfo"><div class="hf5-top"><div class="hv-wrap"><strong>Un projet ? Demandez votre devis.</strong>'
        '<a href="contact.html">Nous contacter</a></div></div><div class="hf5-b"><div class="hv-wrap">'
        '<nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a>'
        '<a href="approche.html">Notre approche</a><a href="contact.html">Contact</a></nav>'
        '<p class="hf-cop">© E.S.A. · Montchauvet (78) · Maquette de démonstration</p></div></div></footer>\n')

def page(fn, title, desc, cur, body, extra=''):
    head = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            "<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
            "%3Crect width='64' height='64' rx='16' fill='%231f3d2b'/%3E%3Cpath d='M14 46c0-18 10-30 36-32-2 22-12 32-30 32' fill='%23b4531a'/%3E%3C/svg%3E\">\n"
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;700&amp;family=Outfit:wght@700&amp;display=swap">\n'
            '<link rel="stylesheet" href="css/style.css">\n</head>\n<body>\n')
    html = head + header(cur) + '<main>\n' + body + '\n</main>\n' + FOOT + extra + '<script src="js/main.js"></script>\n</body>\n</html>\n'
    open(D + '/' + fn, 'w', encoding='utf8').write(html)

H5 = ('<section class="hv hv5" aria-labelledby="hv-t"><div class="hv-wrap"><p class="hv-kick">Services d’aménagement paysager · Montchauvet (78)</p>'
      '<h1 id="hv-t">Aménagement et entretien de vos espaces verts</h1><div class="hv5-rule"></div>'
      '<div class="hv5-grid"><div><p class="hv-lead">E.S.A. crée, aménage et entretient jardins et espaces verts à Montchauvet et dans les Yvelines.</p>'
      '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:' + TELI + '">Appeler le ' + TEL + '</a>'
      '<a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>'
      '<div class="hv5-pic"><img src="images/hero.jpg" width="800" height="1000" alt="Allée en dalles de pierre bordée de massifs (image d’illustration)"></div>'
      '<ul class="hv5-facts"><li><strong>Montchauvet</strong>entreprise locale</li><li><strong>Yvelines</strong>département 78</li>'
      '<li><strong>Devis</strong>sur demande, par téléphone ou en ligne</li></ul></div></div></section>')

V6 = ('<section class="sv sv6" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p>'
      '<h2 id="sv-t">Création, terrasses et entretien de vos jardins</h2>'
      '<p class="hv-lead">Des travaux adaptés à votre terrain, de la conception à l’entretien régulier.</p>'
      '<div class="sv6-grid"><div class="sv6-big"><img src="images/p1.jpg" width="1000" height="1000" alt="Jardin en cours de création avec pelouse et massifs (image d’illustration)">'
      '<div><h3>Création d’espaces verts</h3><p>Conception et aménagement de votre jardin, avec plantations adaptées à votre terrain.</p>'
      '<a href="prestations.html#p1">En savoir plus →</a></div></div>'
      '<div class="sv6-t sv6-t1"><h3>Terrasses en bois</h3><p>Pose de terrasses pour prolonger votre séjour au jardin.</p><a href="prestations.html#p2">En savoir plus →</a></div>'
      '<div class="sv6-t sv6-t2"><h3>Allées et dallages</h3><p>Pose d’allées et de dallages pour circuler dans votre jardin.</p><a href="prestations.html#p3">En savoir plus →</a></div>'
      '<div class="sv6-t sv6-t3"><h3>Maçonnerie paysagère</h3><p>Murets, escaliers et ouvrages en pierre pour structurer le jardin.</p><a href="prestations.html#p4">En savoir plus →</a></div>'
      '<div class="sv6-t sv6-t4"><h3>Entretien de jardin</h3><p>Tonte, taille et désherbage pour garder votre jardin net.</p><a href="prestations.html#p5">En savoir plus →</a></div>'
      '</div></div></section>')

assert V6.count('<div class="sv6-t sv6-t4"><h3>Entretien de jardin</h3><p>Tonte, taille et désherbage pour garder votre jardin net.</p><a href="prestations.html#p5">En savoir plus →</a></div>') == 1
V6 = V6.replace('<div class="sv6-t sv6-t4"><h3>Entretien de jardin</h3><p>Tonte, taille et désherbage pour garder votre jardin net.</p><a href="prestations.html#p5">En savoir plus →</a></div>', '')

A3 = ('<section class="sv sa3" aria-labelledby="sv-a"><div class="hv-wrap"><div><p class="hv-kick">À propos</p>'
      '<h2 id="sv-a">Une entreprise locale, dirigée par Antonio Da Silva</h2>'
      '<p>E.S.A. est une entreprise d’aménagement paysager basée à Montchauvet, dans les Yvelines (78).</p>'
      '<p>Ses travaux couvrent la création, l’aménagement et l’entretien des espaces verts.</p>'
      '<a class="hv-btn hv-btn-p" href="approche.html">Découvrir notre approche</a></div>'
      '<div class="sa3-imgs"><figure class="sa3-i1"><img src="images/a1.jpg" width="800" height="1000" alt="Pose d’une terrasse en bois devant une maison (image d’illustration)"></figure>'
      '<figure class="sa3-i2"><img src="images/a2.jpg" width="600" height="600" alt="Plantation d’un massif par un jardinier (image d’illustration)"></figure></div></div></section>')

M4 = ('<section class="sv sm4" aria-labelledby="sv-m"><div class="hv-wrap"><p class="hv-kick">Notre méthode</p>'
      '<h2 id="sv-m">De l’échange à l’entretien</h2>'
      '<p class="hv-lead">Chaque projet suit les mêmes étapes, expliquées avant le début des travaux.</p>'
      '<div class="sm4-grid"><article class="sm4-c"><span class="sm4-n">1</span><h3>Échange</h3><p>Vous décrivez votre jardin, votre terrain et vos envies.</p></article>'
      '<article class="sm4-c"><span class="sm4-n">2</span><h3>Conseil</h3><p>Nous proposons les travaux adaptés à votre terrain.</p></article>'
      '<article class="sm4-c"><span class="sm4-n">3</span><h3>Réalisation</h3><p>Les travaux sont menés avec soin, selon le devis accepté.</p></article>'
      '<article class="sm4-c"><span class="sm4-n">4</span><h3>Entretien</h3><p>Un suivi régulier de votre jardin, si vous le souhaitez.</p></article></div></div></section>')

C6 = ('<section class="sv sc6" aria-labelledby="sv-c"><div class="hv-wrap"><div><p class="hv-kick">Contact</p>'
      '<h2 id="sv-c">Un projet de jardin&nbsp;? Parlons-en.</h2><p class="hv-lead">Appelez E.S.A. ou envoyez votre demande de devis en ligne.</p>'
      '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:' + TELI + '">Appeler le ' + TEL + '</a>'
      '<a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div></div>'
      '<ul class="sc6-l"><li><a href="tel:' + TELI + '">' + TEL + '</a></li><li>Montchauvet (78)</li></ul></div></section>')

FINAL = ('<section class="final"><div class="section"><div class="wrap"><span class="eyebrow">Votre projet</span>'
         '<h2>Un jardin à créer ou à entretenir ?</h2><p>Appelez E.S.A. ou décrivez votre besoin : nous revenons vers vous.</p>'
         '<a class="tel-big" href="tel:' + TELI + '">' + TEL + '</a>'
         '<div class="cta-row"><a class="btn btn-clair" href="contact.html">Demander un devis</a></div></div></div></section>')

K2 = ('<section class="sv sk sk2" aria-labelledby="sv-k"><div class="hv-wrap sk-grid"><div class="sk-card"><p class="hv-kick">Demande de devis</p>'
      '<h2 id="sv-k">Parlez-nous de votre projet</h2>'
      '<p class="sk-intro">Décrivez votre besoin : vous obtenez un message prêt à envoyer par SMS ou à copier.</p>'
      '<form class="sk-form" id="kform" novalidate data-name="E.S.A." data-sms="' + TELI + '" data-tel="' + TELI + '" data-email="">'
      '<div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option>'
      '<option>Création de jardin</option><option>Entretien de jardin</option><option>Terrasse ou allée</option><option>Maçonnerie paysagère</option><option>Autre demande</option></select>'
      '<p class="sk-err" id="k-besoin-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div>'
      '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>'
      '<div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l’envoyer. Rien n’est transmis tant que vous n’avez pas validé l’envoi.</p>'
      '<pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a>'
      '<button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button><a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a>'
      '<a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div><button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div>'
      '<aside class="sk-side"><h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:' + TELI + '">' + TEL + '</a></li>'
      '<li><span>Commune</span><p>Montchauvet (78)</p></li></ul></aside></div></section>')

# index
page('index.html', 'E.S.A., aménagement paysager à Montchauvet (78)',
     'E.S.A., entreprise d’aménagement paysager à Montchauvet dans les Yvelines (78) : création, terrasses, allées, plantations et entretien de jardins. Appelez le ' + TEL + '.',
     'index.html', H5 + V6 + A3 + C6)

# prestations
cards = [
    ('p1', 'creation', 'Jardin en cours de création avec pelouse et massifs (image d’illustration)', 'Création d’espaces verts',
     'Conception et aménagement de votre jardin, avec plantations adaptées à votre terrain.'),
    ('p2', 'terrasse', 'Pose d’une terrasse en bois (image d’illustration)', 'Terrasses en bois',
     'Pose de terrasses en bois pour prolonger la maison vers le jardin.'),
    ('p3', 'allee', 'Allée en dalles de pierre bordée de massifs (image d’illustration)', 'Allées et dallages',
     'Pose d’allées et de dallages pour circuler dans votre jardin.'),
    ('p4', 'muret', 'Muret de pierre et escalier de jardin (image d’illustration)', 'Maçonnerie paysagère',
     'Murets, escaliers et ouvrages en pierre pour structurer le jardin.'),
    ('p5', 'tonte', 'Jardinier tondant une pelouse (image d’illustration)', 'Entretien de jardin',
     'Tonte, taille et désherbage pour garder votre jardin net.'),
]
def card(c):
    i, k, alt, t, d = c
    return ('<article class="card" id="%s"><img src="images/%s.jpg" %s loading="lazy" alt="%s"><div><h3>%s</h3><p>%s</p></div></article>'
            % (i, k, dim(k), alt, t, d))

groups = [cards[0:2], cards[2:4], cards[4:5]]
bands = ''.join('<section class="section%s" aria-label="Prestations"><div class="wrap"><div class="cards">%s</div></div></section>'
                % (' band' if n % 2 == 0 else '', ''.join(card(c) for c in g)) for n, g in enumerate(groups))
PREST = ('<section class="section" aria-labelledby="h1"><div class="wrap"><div class="head"><span class="eyebrow">Prestations · Montchauvet (78)</span>'
         '<h1 id="h1">Création, aménagement et entretien de vos espaces verts</h1>'
         '<p>De la conception de votre jardin à son entretien régulier, E.S.A. intervient à Montchauvet (78).</p>'
         '<div class="cta-row" style="margin-top:1.4rem"><a class="btn btn-terre" href="contact.html">Demander un devis</a>'
         '<a class="btn btn-ligne" href="tel:' + TELI + '">Appeler le ' + TEL + '</a></div></div></div></section>' + bands + FINAL)
page('prestations.html', 'Prestations · E.S.A. à Montchauvet (78)',
     'Prestations de E.S.A. à Montchauvet (78) : création d’espaces verts, terrasses en bois, allées et dallages, maçonnerie paysagère et entretien de jardin.',
     'prestations.html', PREST)

# approche
APPROCHE = ('<section class="section" aria-labelledby="h1"><div class="wrap"><div class="head"><span class="eyebrow">Notre approche · Montchauvet (78)</span>'
            '<h1 id="h1">Un travail soigné, de l’échange à l’entretien</h1>'
            '<p>E.S.A. vous accompagne à chaque étape de votre projet d’aménagement paysager.</p></div></div></section>'
            + M4 + FINAL)
page('approche.html', 'Notre approche · E.S.A. à Montchauvet (78)',
     'La méthode de E.S.A., entreprise d’aménagement paysager à Montchauvet (78) : échange, conseil, réalisation et entretien de votre jardin.',
     'approche.html', APPROCHE)

# contact
CONTACT = ('<section class="section" style="min-height:0" aria-labelledby="h1"><div class="wrap"><div class="head"><span class="eyebrow">Contact · Montchauvet (78)</span>'
           '<h1 id="h1">Contactez E.S.A. à Montchauvet</h1><p>Décrivez votre projet en quelques lignes, ou appelez directement.</p></div></div></section>' + K2)
page('contact.html', 'Contact · E.S.A. à Montchauvet (78)',
     'Contactez E.S.A. à Montchauvet (78) : demande de devis en ligne ou appel au ' + TEL + '.',
     'contact.html', CONTACT, extra='<script src="js/k.js" defer></script>\n')

print('pages:', sorted(f for f in os.listdir(D) if f.endswith('.html')))
print('images:', sorted((f, os.path.getsize(D + '/images/' + f) // 1024) for f in os.listdir(D + '/images')))

s2 = open(cp, encoding='utf8').read()
s2, n8 = re.subn(r'font:800 ', 'font:700 ', s2)
s2 = s2.replace('font-weight:800', 'font-weight:700')
open(cp, 'w', encoding='utf8').write(s2)
print('graisses 800 ramenées à 700 :', n8)

open(D + '/README.md', 'w', encoding='utf8').write(
    '# E.S.A. (Montchauvet, 78)\n\nMaquette de site vitrine (démonstration, non publiée auprès du client).\n\n'
    'Pages : index, prestations, approche, contact.\n')
