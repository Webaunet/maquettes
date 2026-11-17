#!/usr/bin/env python3
"""Maquette Eric Roche (Egly). Usage : python3 build_eric_roche.py images | site"""
import os, sys, re, shutil, subprocess, zipfile, unicodedata
from PIL import Image, ImageDraw, ImageFont

SRC = '/mnt/user-data/uploads/Maquettes/Images/Paysagiste'
ZIP = '/mnt/user-data/uploads/Maquettes/Squelettes/S09.zip'
OUTILS = os.path.dirname(os.path.abspath(__file__))
SLUG = 'eric-roche'
SITE = '/home/claude/maquettes/' + SLUG
WORK = '/home/claude/work_er'
IMG = WORK + '/img'
NAME = 'Eric Roche'
TEL = '+33672843587'
TEL_FR = '06 72 84 35 87'
TEL2 = '+33164599707'
TEL2_FR = '01 64 59 97 07'
BASE = 'https://webaunet.github.io/maquettes/' + SLUG + '/'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

S_ALLEE = 'alléé pavés carrelage extérieure.jpg'
S_DALLEE = 'chantier allée dallée.jpg'
S_TERRASSE = 'chantier terrasse en bois.jpg'
S_CONCEPTION = 'conception chantier.jpg'
S_MACONNERIE = 'maçonerie paysagère.jpg'
S_TONTE = 'robot tonte de pelouse.jpg'

# sortie, largeur, hauteur (jamais agrandies : sources 1228x768), source
IMAGES = [
    ('hero-1.jpg', 597, 768, S_ALLEE),
    ('hero-2.jpg', 600, 450, S_TERRASSE),
    ('hero-3.jpg', 600, 450, S_TONTE),
    ('a1.jpg', 614, 768, S_MACONNERIE),
    ('a2.jpg', 600, 600, S_DALLEE),
    ('k1.jpg', 628, 768, S_CONCEPTION),
    ('c-creation.jpg', 800, 436, S_ALLEE),
    ('c-terrasse.jpg', 800, 436, S_TERRASSE),
    ('c-entretien.jpg', 800, 436, S_TONTE),
    ('page-hero.jpg', 614, 768, S_ALLEE),
    ('about.jpg', 800, 436, S_DALLEE),
]
ALT = {
    'hero-1.jpg': 'Allée pavée bordée de massifs fleuris et d’un muret en pierre (image d’illustration)',
    'hero-2.jpg': 'Pose de lames de bois d’une terrasse sur un chantier (image d’illustration)',
    'hero-3.jpg': 'Robot de tonte sur une pelouse entourée d’une allée pavée (image d’illustration)',
    'a1.jpg': 'Ouvrier agenouillé près d’un muret et d’un escalier en pierre (image d’illustration)',
    'a2.jpg': 'Allée en dalles de pierre éclairée le soir devant une maison (image d’illustration)',
    'k1.jpg': 'Plan d’un aménagement paysager affiché sur une tablette (image d’illustration)',
    'c-creation.jpg': 'Jardin fleuri bordé d’un muret en pierre et d’une allée pavée (image d’illustration)',
    'c-terrasse.jpg': 'Pose de lames de bois d’une terrasse sur un chantier (image d’illustration)',
    'c-entretien.jpg': 'Robot de tonte sur une pelouse (image d’illustration)',
    'page-hero.jpg': 'Allée pavée bordée de massifs fleuris et d’un muret en pierre (image d’illustration)',
    'about.jpg': 'Allée en dalles de pierre éclairée le soir devant une maison (image d’illustration)',
}
# Skeleton -> palette 5 « Anthracite et vert vif »
BG, BG2, INK, MU, MAIN, ACC, ACCINK, ACCD = '#f4f6ef', '#e4e9d4', '#151712', '#4a4f41', '#1b1d18', '#b9e04a', '#151712', '#9cc02f'
HEX_MAP = {
    '#12301f': MAIN, '#1b4229': MAIN, '#2f6b3a': MAIN, '#a9c487': ACC, '#dfe8cf': BG2, '#f7f2e6': BG,
    '#ece2c8': BG2, '#5a3d27': MU, '#e07a1f': ACC, '#b95f10': ACCD, '#1c2a20': INK, '#ee8b30': ACC,
    '#1a1208': ACCINK, '#fbf3e3': BG, '#f4f8ec': BG, '#e9eedc': BG2, '#e3ebd5': BG2, '#dbe5cb': BG2,
    '#d3dfc2': BG2, '#b9c4b0': BG2, '#2d4034': MAIN, '#34473a': MAIN, '#51635a': MU,
}
EXTRA_CSS = """
/* maquette Eric Roche : texte sombre sur accent vert vif, jamais l'accent en texte sur fond clair */
.eyebrow{color:var(--forest)}
.btn-rope{color:#151712}
.btn-rope:hover{background:#9cc02f;color:#151712}
.grid4.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:980px){.grid4.g2{grid-template-columns:1fr}}
.grid4.g2 .svc:not(.panel) img{aspect-ratio:5/2;object-fit:cover}
@media(max-width:620px){.head p.opt{display:none}}
@media(max-width:420px){.grid4.g2 .svc:not(.panel){grid-template-columns:30% 1fr}.grid4.g2 .svc:not(.panel)>div{padding:.9rem}}
.sc4{background:var(--hv-bg)}
.sk5{padding-top:0}
.svc.panel{display:block;padding:clamp(1.2rem,3vw,2rem);align-self:stretch}
.svc.panel p{margin:.6rem 0 1rem}
.svc ul{margin:.6rem 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:.1rem .9rem}
@media(max-width:1000px){.land .mosaic{max-width:440px;margin-inline:auto}}
.sa3-i1 img{max-width:614px}.sa3-i2 img{max-width:600px}.sk5-pic>img{max-width:628px}.about-media img{max-width:800px}
.sa3-imgs img,.sk5-pic>img,.about-media img{margin-inline:auto}
@media(max-width:980px){.grid4.g2 .svc:not(.panel){display:grid;grid-template-columns:38% 1fr;align-items:stretch}.grid4.g2 .svc:not(.panel) img{height:100%;min-height:110px;aspect-ratio:auto;object-fit:cover;max-width:none}}
.svc li{margin:.2rem 0}
.sec.compact{min-height:0;padding-block:clamp(2.5rem,5vw,4rem)}
.sec+.sec.compact{padding-top:calc(clamp(2.5rem,5vw,4rem) + var(--r)*2)}
.sec.compact .about-media img.main{max-height:300px;object-fit:cover;width:100%}
.hf .hf-cop{max-width:none;text-align:center}
"""
MOD_ARGS = ['--bg', BG, '--bg2', BG2, '--ink', INK, '--mu', MU, '--main', MAIN, '--acc', ACC,
            '--accink', ACCINK, '--fh', 'Outfit', '--fb', 'Figtree', '--fw', '700']


def find_source(name):
    t = unicodedata.normalize('NFC', name)
    for f in os.listdir(SRC):
        if unicodedata.normalize('NFC', f) == t:
            return os.path.join(SRC, f)
    raise SystemExit('Image source introuvable : ' + name)


def crop_resize(path, w, h):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    r = w / h
    if W / H > r:
        nw = int(H * r); x0 = (W - nw) // 2; im = im.crop((x0, 0, x0 + nw, H))
    else:
        nh = int(W / r); y0 = (H - nh) // 2; im = im.crop((0, y0, W, y0 + nh))
    if im.size[0] < w:
        print('  ATTENTION agrandie :', os.path.basename(path), im.size, '->', w)
    return im.resize((w, h), Image.LANCZOS)


def images():
    os.makedirs(IMG, exist_ok=True)
    for out, w, h, src in IMAGES:
        im = crop_resize(find_source(src), w, h)
        d = os.path.join(IMG, out)
        for q in (82, 78, 74):
            im.save(d, 'JPEG', quality=q, optimize=True, progressive=True)
            if os.path.getsize(d) < 250 * 1024:
                break
        print(out, w, h, os.path.getsize(d) // 1024, 'Ko')
    fav = Image.new('RGB', (64, 64), MAIN)
    dr = ImageDraw.Draw(fav)
    f = ImageFont.truetype(FONT_B, 28)
    b = dr.textbbox((0, 0), 'ER', font=f)
    dr.text(((64 - (b[2] - b[0])) / 2 - b[0], (64 - (b[3] - b[1])) / 2 - b[1]), 'ER', font=f, fill=ACC)
    fav.save(os.path.join(IMG, 'favicon.png'))


def head(title, desc):
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<link rel="icon" type="image/png" href="images/favicon.png">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Figtree:wght@400;600;700;800&display=swap">\n'
            '<link rel="stylesheet" href="css/style.css">\n</head>\n<body>\n')


def header(current):
    links = [('index.html', 'Accueil'), ('prestations.html', 'Prestations'),
             ('a-propos.html', 'À propos'), ('contact.html', 'Contact')]
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == current else '', l) for h, l in links)
    return ('<header class="hdr">\n  <div class="wrap">\n'
            '    <a class="brand" href="' + BASE + '" aria-label="Eric Roche, accueil">\n'
            '      <span><b>Eric Roche</b><small>Paysagiste · Egly (91)</small></span>\n    </a>\n'
            '    <nav class="nav" id="nav" aria-label="Navigation principale">' + nav + '</nav>\n'
            '    <a class="call" href="tel:' + TEL + '" aria-label="Appeler le ' + TEL_FR + '">\n'
            '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>\n'
            '      <span>' + TEL_FR + '</span>\n    </a>\n'
            '    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span></span></button>\n'
            '  </div>\n</header>\n')


def footer():
    return ('<div class="hf hf1" role="contentinfo"><div class="hv-wrap"><div><strong>Eric Roche</strong>'
            '<p class="hf-desc">Paysagiste à Egly (91) : aménagement et entretien de jardins.</p></div>'
            '<nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a>'
            '<a href="a-propos.html">À propos</a><a href="contact.html">Contact</a></nav>'
            '<div class="hf-c"><a href="tel:' + TEL + '">' + TEL_FR + '</a><a href="tel:' + TEL2 + '">' + TEL2_FR + '</a></div>'
            '<p class="hf-cop">© Eric Roche · Egly (91) · Maquette de démonstration</p></div></div>\n')


def img(name, w, h, lazy=True, cls=''):
    return ('<img%s src="images/%s" width="%d" height="%d" alt="%s"%s>' %
            (' class="' + cls + '"' if cls else '', name, w, h, ALT[name], ' loading="lazy"' if lazy else ''))


CATS = [
    ('c1', 'c-creation.jpg', 'Création de jardins',
     ['Plantations et massifs', 'Engazonnement', 'Haies et arbustes', 'Aménagement paysager']),
    ('c2', 'c-terrasse.jpg', 'Terrasses et allées',
     ['Terrasses en bois', 'Allées pavées ou dallées', 'Murets en pierre', 'Escaliers extérieurs']),
    ('c3', 'c-entretien.jpg', 'Entretien du jardin',
     ['Tonte de pelouse', 'Taille de haies', 'Désherbage', 'Entretien régulier']),
]


def h4():
    return ('<section class="hv hv4" aria-labelledby="hv-t"><div class="hv-wrap">\n'
            '<div><p class="hv-kick">Paysagiste à Egly (91)</p><h1 id="hv-t">Votre jardin, aménagé avec soin</h1>'
            '<p class="hv-lead">Eric Roche aménage et entretient jardins et espaces verts à Egly, en Essonne. Demandez votre devis par téléphone ou en ligne.</p>'
            '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:' + TEL + '">Appeler le ' + TEL_FR + '</a>'
            '<a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>\n'
            '<div class="hv4-mos">' + img('hero-1.jpg', 597, 768, False) + img('hero-2.jpg', 600, 450, False) +
            img('hero-3.jpg', 600, 450, False) + '<div class="hv4-round"><strong>91</strong>Essonne</div></div></div></section>\n')


def v8():
    cards = ''
    for i, (ident, _, title, items) in enumerate(CATS, 1):
        cards += ('<article class="sv8-c sv8-c%d"><h3>%s</h3><ul>%s</ul><a class="hv-btn hv-btn-s" href="prestations.html#%s">Voir le détail</a></article>' %
                  (i, title, ''.join('<li>' + t + '</li>' for t in items), ident))
    return ('<section class="sv sv8" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p>'
            '<h2 id="sv-t">Nos prestations pour votre jardin</h2>'
            '<p class="hv-lead">Création, terrasses et entretien : trois domaines pour votre extérieur.</p>'
            '<div class="sv8-grid">' + cards + '</div></div></section>\n')


def a3():
    return ('<section class="sv sa3" aria-labelledby="sv-a"><div class="hv-wrap"><div><p class="hv-kick">À propos</p>'
            '<h2 id="sv-a">Un paysagiste installé à Egly</h2>'
            '<p>Eric Roche dirige cette entreprise d’aménagement paysager, installée à Egly, en Essonne.</p>'
            '<p>Elle intervient pour l’aménagement et l’entretien de jardins et d’espaces verts.</p>'
            '<a class="hv-btn hv-btn-p" href="a-propos.html">Découvrir l’entreprise</a></div>'
            '<div class="sa3-imgs"><figure class="sa3-i1">' + img('a1.jpg', 614, 768) + '</figure>'
            '<figure class="sa3-i2">' + img('a2.jpg', 600, 600) + '</figure></div></div></section>\n')


def c4():
    return ('<section class="sv sc4" aria-labelledby="sv-c"><div class="hv-wrap"><div class="sc4-head"><p class="hv-kick">Contact</p>'
            '<h2 id="sv-c">Un projet de jardin&nbsp;? Parlons-en.</h2>'
            '<p class="hv-lead">Appelez-nous ou décrivez votre projet en ligne pour obtenir un devis.</p></div>'
            '<div class="sc4-grid"><div class="sc4-c"><h3>Appelez-nous</h3><a href="tel:' + TEL + '">' + TEL_FR + '</a></div>'
            '<div class="sc4-c sc4-c2"><h3>Écrivez-nous</h3><a href="contact.html">Formulaire de contact</a></div></div></div></section>\n')


def k5():
    opts = ''.join('<option>' + o + '</option>' for o in
                   ['Création de jardin', 'Terrasse ou allée', 'Entretien du jardin', 'Autre demande'])

    def f(i, label, tag, extra=''):
        return ('<div class="sk-f"><label for="k-%s">%s</label>%s<p class="sk-err" id="k-%s-e" role="alert"></p></div>' % (i, label, tag, i))
    form = ('<form class="sk-form" id="kform" novalidate data-name="Eric Roche" data-sms="' + TEL + '" data-tel="' + TEL + '" data-email="">'
            + f('nom', 'Nom', '<input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e">')
            + f('tel', 'Téléphone', '<input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e">')
            + f('commune', 'Commune', '<input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e">')
            + f('besoin', 'Votre besoin', '<select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option>' + opts + '</select>')
            + f('msg', 'Message (facultatif)', '<textarea id="k-msg" name="msg" rows="3"></textarea>')
            + '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>')
    done = ('<div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3>'
            '<p>Choisissez comment l’envoyer. Rien n’est transmis tant que vous n’avez pas validé l’envoi.</p>'
            '<pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a>'
            '<button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button>'
            '<a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a>'
            '<a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div>'
            '<button class="sk-back" type="button" data-back>Modifier ma demande</button></div>')
    return ('<section class="sv sk sk5" aria-labelledby="sv-k"><div class="hv-wrap sk-grid"><div class="sk5-pic">' + img('k1.jpg', 628, 768) +
            '<aside class="sk-side"><h3>Nous joindre directement</h3><ul>'
            '<li><span>Mobile</span><a href="tel:' + TEL + '">' + TEL_FR + '</a></li>'
            '<li><span>Fixe</span><a href="tel:' + TEL2 + '">' + TEL2_FR + '</a></li>'
            '<li><span>Commune</span><p>Egly (91)</p></li></ul></aside></div>'
            '<div class="sk-card"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2>'
            '<p class="sk-intro">Décrivez votre besoin, puis envoyez-le par SMS ou copiez-le.</p>' + form + done +
            '</div></div></section>\n')


def page(title, desc, current, body, scripts):
    return head(title, desc) + header(current) + '<main>\n' + body + '</main>\n' + footer() + scripts + '</body>\n</html>\n'


MAIN_JS = '<script src="js/main.js" defer></script>\n'
K_JS = '<script src="js/k.js" defer></script>\n'
CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M5 12l4.5 4.5L19 7"/></svg>')


def page_index():
    return page('Eric Roche, paysagiste à Egly (91)',
                'Eric Roche, paysagiste à Egly (Essonne) : aménagement et entretien de jardins et d’espaces verts. Demande de devis par téléphone ou en ligne.',
                'index.html', h4() + v8() + a3() + c4(), MAIN_JS)


def page_prestations():
    hero = ('<section class="sec s-sage" aria-labelledby="h1"><div class="wrap land"><div>'
            '<span class="eyebrow">Prestations · Egly (91)</span><h1 id="h1">Nos prestations de paysagiste</h1>'
            '<p style="margin-top:1rem">Création, terrasses et entretien : choisissez le domaine qui correspond à votre jardin.</p>'
            '<div class="actions"><a class="btn btn-rope" href="contact.html">Demander un devis</a>'
            '<a class="btn btn-green" href="tel:' + TEL + '">Appeler le ' + TEL_FR + '</a></div></div>'
            '<div class="mosaic"><img class="a" src="images/page-hero.jpg" width="614" height="768" alt="' + ALT['page-hero.jpg'] + '">'
            '<img class="b" src="images/c-entretien.jpg" width="800" height="436" alt="' + ALT['c-entretien.jpg'] + '" loading="lazy">'
            '<img class="c" src="images/c-terrasse.jpg" width="800" height="436" alt="' + ALT['c-terrasse.jpg'] + '" loading="lazy"></div>'
            '</div></section>\n')
    cards = ''
    for ident, im, title, items in CATS:
        cards += ('<article class="svc" id="' + ident + '"><img src="images/' + im + '" width="800" height="436" alt="' + ALT[im] + '" loading="lazy">'
                  '<div><h3>' + title + '</h3><ul>' + ''.join('<li>' + t + '</li>' for t in items) + '</ul></div></article>\n')
    def card(c):
        ident, im, title, items = c
        return ('<article class="svc" id="' + ident + '"><img src="images/' + im + '" width="800" height="436" alt="' + ALT[im] + '" loading="lazy">'
                '<div><h3>' + title + '</h3><ul>' + ''.join('<li>' + t + '</li>' for t in items) + '</ul></div></article>\n')
    grid = ('<section class="sec s-cream" aria-labelledby="h-serv"><div class="wrap">'
            '<div class="head"><span class="eyebrow">Domaines d’intervention</span><h2 id="h-serv">Création et terrasses</h2>'
            '<p class="opt">Du projet de jardin à la terrasse ou à l’allée, selon votre besoin.</p></div>'
            '<div class="grid4 g2">' + card(CATS[0]) + card(CATS[1]) + '</div></div></section>\n'
            '<section class="sec s-sage" aria-labelledby="h-serv2"><div class="wrap">'
            '<div class="head"><span class="eyebrow">Domaines d’intervention</span><h2 id="h-serv2">Entretien du jardin</h2>'
            '<p class="opt">Un entretien régulier pour garder votre extérieur soigné.</p></div>'
            '<div class="grid4 g2">' + card(CATS[2]) +
            '<div class="svc panel"><h3>Un autre besoin&nbsp;?</h3><p>Décrivez votre projet : nous vous répondons pour établir un devis.</p>'
            '<a class="btn btn-green" href="contact.html">Nous écrire</a></div></div></div></section>\n')
    cta = ('<section class="sec compact dark rings cta" aria-labelledby="h-cta"><div class="wrap"><div class="ctabox">'
           '<span class="eyebrow">Demande de devis</span><h2 id="h-cta">Un jardin, une terrasse, un projet&nbsp;?</h2>'
           '<p style="margin-top:1rem">Décrivez votre besoin, puis appelez l’entreprise ou écrivez-nous.</p>'
           '<div class="actions"><a class="btn btn-rope" href="contact.html">Demander un devis</a>'
           '<a class="btn btn-line" href="tel:' + TEL + '">Appeler le ' + TEL_FR + '</a></div></div></div></section>\n')
    return page('Prestations de paysagiste | Eric Roche à Egly (91)',
                'Création de jardins, terrasses, allées et entretien : les prestations d’Eric Roche, paysagiste à Egly (Essonne).',
                'prestations.html', hero + grid + cta, MAIN_JS)


def page_apropos():
    intro = ('<section class="sec compact s-cream" aria-labelledby="h1"><div class="wrap"><div class="head">'
             '<span class="eyebrow">L’entreprise · Egly (91)</span><h1 id="h1">Un paysagiste installé à Egly</h1>'
             '<p>Eric Roche exerce dans les services d’aménagement paysager, depuis Egly, en Essonne.</p></div></div></section>\n')
    about = ('<section class="sec compact dark rings" aria-labelledby="h-about"><div class="wrap about">'
             '<div class="about-media"><img class="main" src="images/about.jpg" width="800" height="436" alt="' + ALT['about.jpg'] + '" loading="lazy"></div>'
             '<div class="about-card"><span class="eyebrow">Repères</span><h2 id="h-about">Les informations de référence</h2>'
             '<ul><li>' + CHECK + 'Activité : aménagement paysager</li><li>' + CHECK + 'Siège : Egly (Essonne, 91)</li>'
             '<li>' + CHECK + 'Dirigeant : Eric Roche</li></ul>'
             '<div class="actions"><a class="btn btn-rope" href="contact.html">Nous contacter</a></div></div></div></section>\n')
    nxt = ('<section class="sec compact s-sage" aria-labelledby="h-next"><div class="wrap"><div class="head">'
           '<span class="eyebrow">Suite</span><h2 id="h-next">Découvrir les prestations</h2>'
           '<p>Création, terrasses et entretien de jardins.</p></div>'
           '<div class="actions"><a class="btn btn-green" href="prestations.html">Voir les prestations</a></div></div></section>\n')
    return page('À propos | Eric Roche, paysagiste à Egly (91)',
                'Eric Roche, entreprise de services d’aménagement paysager installée à Egly (Essonne).',
                'a-propos.html', intro + about + nxt, MAIN_JS)


def page_contact():
    band = ('<section class="sec s-cream" style="padding-top:clamp(2.5rem,6vw,4rem);padding-bottom:clamp(1.5rem,3vw,2rem);min-height:0" aria-labelledby="h1">'
            '<div class="wrap"><div class="head"><span class="eyebrow">Contact · Egly (91)</span>'
            '<h1 id="h1">Parlons de votre projet</h1>'
            '<p>Préparez votre demande ci-dessous, puis envoyez-la par SMS ou appelez directement.</p></div></div></section>\n')
    return page('Contact et demande de devis | Eric Roche à Egly (91)',
                'Contactez Eric Roche, paysagiste à Egly (Essonne) : appelez le ' + TEL_FR + ' ou préparez votre demande de devis en ligne.',
                'contact.html', band + k5(), K_JS + MAIN_JS)


def site():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(SITE)
    for f in ('arboriculture.html', 'paysage.html', 'entreprise.html', '_SKELETON.md'):
        os.remove(os.path.join(SITE, f))
    os.makedirs(os.path.join(SITE, 'images'))
    for f in os.listdir(IMG):
        shutil.copy(os.path.join(IMG, f), os.path.join(SITE, 'images', f))
    cp = os.path.join(SITE, 'css', 'style.css')
    css = open(cp, encoding='utf8').read()
    pat = re.compile('|'.join(re.escape(k) for k in HEX_MAP), re.I)
    css, n = pat.subn(lambda m: HEX_MAP[m.group(0).lower()], css)
    for a, b in (('rgba(247,242,230', 'rgba(244,246,239'), ('rgba(18,48,31', 'rgba(27,29,24'),
                 ('rgba(169,196,135', 'rgba(185,224,74'), ('rgba(26,18,8', 'rgba(21,23,18')):
        css = css.replace(a, b)
    css = re.sub(r'^/\*.*?\*/', '/* Maquette Eric Roche : feuille de style */', css, count=1, flags=re.S)
    assert css.count("'Fraunces'") == 1, 'Fraunces introuvable'
    css = css.replace("'Fraunces'", "'Outfit'")
    css += EXTRA_CSS
    open(cp, 'w', encoding='utf8').write(css)
    print('couleurs remplacées :', n)
    mp = os.path.join(SITE, 'js', 'main.js')
    js = open(mp, encoding='utf8').read()
    ph = "Nom de l\\'entreprise"
    assert js.count(ph) == 1, 'espace réservé de main.js introuvable'
    open(mp, 'w', encoding='utf8').write(js.replace(ph, NAME))
    subprocess.run([sys.executable, '-I', 'mod.py', SITE, 'H4', 'V8', 'A3', 'C4', 'F1', 'K5'] + MOD_ARGS, cwd=OUTILS, check=True)
    pages = {'index.html': page_index(), 'prestations.html': page_prestations(),
             'a-propos.html': page_apropos(), 'contact.html': page_contact()}
    for name, html in pages.items():
        open(os.path.join(SITE, name), 'w', encoding='utf8').write(html)
    open(os.path.join(SITE, 'README.md'), 'w', encoding='utf8').write(
        '# Eric Roche (Egly)\n\nMaquette de site vitrine (non contractuelle). Pages : accueil, prestations, à propos, contact.\n')
    print('pages :', ', '.join(sorted(os.listdir(SITE))))


if __name__ == '__main__':
    {'images': images, 'site': site}[sys.argv[1]]()
