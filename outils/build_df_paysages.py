#!/usr/bin/env python3
"""Maquette D&F Paysages (Brunoy). Usage : python3 build_df_paysages.py images | site"""
import os, sys, re, shutil, subprocess, zipfile, unicodedata
from PIL import Image, ImageDraw, ImageFont

SRC = '/mnt/user-data/uploads/Maquettes/Images/Paysagiste'
ZIP = '/mnt/user-data/uploads/Maquettes/Squelettes/S09.zip'
OUTILS = os.path.dirname(os.path.abspath(__file__))
SITE = '/home/claude/maquettes/df-paysages'
WORK = '/home/claude/work'
IMG = WORK + '/img'
TEL = '+33611438262'
TEL_FR = '06 11 43 82 62'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

SRC_ALLEE = 'alléé pavés carrelage extérieure.jpg'
SRC_DALLEE = 'chantier allée dallée.jpg'
SRC_TERRASSE = 'chantier terrasse en bois.jpg'
SRC_CONCEPTION = 'conception chantier.jpg'
SRC_MACONNERIE = 'maçonerie paysagère.jpg'
SRC_TONTE = 'robot tonte de pelouse.jpg'

# nom de sortie, largeur, hauteur, source
IMAGES = [
    ('hero.jpg', 1228, 768, SRC_ALLEE),
    ('k1.jpg', 1400, 600, SRC_MACONNERIE),
    ('c1.jpg', 768, 768, SRC_CONCEPTION),
    ('a1.jpg', 614, 768, SRC_MACONNERIE),
    ('a2.jpg', 600, 600, SRC_DALLEE),
    ('p1.jpg', 800, 500, SRC_CONCEPTION),
    ('p2.jpg', 800, 500, SRC_TERRASSE),
    ('p3.jpg', 800, 500, SRC_TONTE),
    ('svc-creation.jpg', 800, 436, SRC_ALLEE),
    ('svc-terrasse.jpg', 800, 436, SRC_TERRASSE),
    ('svc-tonte.jpg', 800, 436, SRC_TONTE),
    ('svc-maconnerie.jpg', 800, 436, SRC_MACONNERIE),
    ('about.jpg', 800, 436, SRC_ALLEE),
]

# Texte alternatif (à relire après la planche contact)
ALT = {
    'hero.jpg': 'Allée pavée bordée de massifs fleuris et d’un muret en pierre (image d’illustration)',
    'k1.jpg': 'Escalier et muret en pierre dans un jardin en pente (image d’illustration)',
    'c1.jpg': 'Plan d’un aménagement paysager affiché sur une tablette (image d’illustration)',
    'a1.jpg': 'Ouvrier agenouillé près d’un muret et d’un escalier en pierre (image d’illustration)',
    'a2.jpg': 'Personne marchant sur une allée en dalles de pierre, éclairée le soir (image d’illustration)',
    'p1.jpg': 'Plan d’un aménagement paysager affiché sur une tablette (image d’illustration)',
    'p2.jpg': 'Pose de lames de bois d’une terrasse sur un chantier (image d’illustration)',
    'p3.jpg': 'Robot de tonte sur une pelouse entourée d’une allée pavée (image d’illustration)',
    'svc-creation.jpg': 'Jardin fleuri bordé d’un muret en pierre et d’une allée pavée (image d’illustration)',
    'svc-terrasse.jpg': 'Pose de lames de bois d’une terrasse sur un chantier (image d’illustration)',
    'svc-tonte.jpg': 'Robot de tonte sur une pelouse (image d’illustration)',
    'svc-maconnerie.jpg': 'Ouvrier agenouillé près d’un muret et d’un escalier en pierre (image d’illustration)',
    'about.jpg': 'Allée pavée bordée de massifs fleuris et d’un muret en pierre (image d’illustration)',
}

# Palette du squelette -> palette imposée « Ardoise et sauge » (rôles : voir _SKELETON.md)
HEX_MAP = {
    '#12301f': '#2c3e47', '#1b4229': '#2c3e47', '#2f6b3a': '#46763f', '#a9c487': '#e1e8e1',
    '#dfe8cf': '#e1e8e1', '#f7f2e6': '#f3f5f2', '#ece2c8': '#e1e8e1', '#5a3d27': '#4b5a60',
    '#e07a1f': '#46763f', '#b95f10': '#46763f', '#1c2a20': '#1c262b', '#ee8b30': '#2c3e47',
    '#1a1208': '#ffffff', '#fbf3e3': '#f3f5f2', '#f4f8ec': '#f3f5f2', '#e9eedc': '#e1e8e1',
    '#e3ebd5': '#e1e8e1', '#dbe5cb': '#e1e8e1', '#d3dfc2': '#e1e8e1', '#b9c4b0': '#e1e8e1',
    '#2d4034': '#2c3e47', '#34473a': '#2c3e47', '#51635a': '#4b5a60',
}
EXTRA_CSS = """
/* maquette D&F Paysages : accent jamais en texte sur fond clair, texte blanc sur accent */
.eyebrow{color:var(--forest)}
.btn-rope{color:#ffffff}
.btn-rope:hover{background:var(--forest)}
.about-media img,.sa3-i1 img,.sa3-i2 img,.sc7-ph img{max-width:100%;margin-inline:auto}
.about-media img{max-width:800px}
.sa3-i1 img{max-width:614px}
.sa3-i2 img{max-width:600px}
.sc7-ph img{max-width:768px}
.grid4.g2{grid-template-columns:repeat(2,1fr)}
.grid4.g2 .svc img{aspect-ratio:5/2}
.sec.compact .about-media img.main{max-height:300px;object-fit:cover;width:100%}
@media(max-width:1000px){.land .mosaic{max-width:440px;margin-inline:auto}.sec.compact{padding-block:2rem}.sec+.sec.compact{padding-top:calc(2rem + var(--r)*2)}.sec.compact .about-media img.main{max-height:220px}.grid4.g2 .svc img{aspect-ratio:3/1}}
.sec.compact{min-height:0;padding-block:clamp(2.5rem,5vw,4rem)}
.sec+.sec.compact{padding-top:calc(clamp(2.5rem,5vw,4rem) + var(--r)*2)}
.sa3{background:var(--hv-bg)}
.sc7{background:var(--hv-bg2)}
.sc7-card{background:var(--hv-bg)}
.hf3 .hf-cop{max-width:none;text-align:center}
@media(max-width:619px){.grid4.g2{grid-template-columns:1fr}}
"""
MOD_ARGS = ['--bg', '#f3f5f2', '--bg2', '#e1e8e1', '--ink', '#1c262b', '--mu', '#4b5a60',
            '--main', '#2c3e47', '--acc', '#46763f', '--accink', '#ffffff',
            '--fh', 'Fraunces', '--fb', 'Nunito Sans', '--fw', '700']


def find_source(name):
    target = unicodedata.normalize('NFC', name)
    for f in os.listdir(SRC):
        if unicodedata.normalize('NFC', f) == target:
            return os.path.join(SRC, f)
    raise SystemExit('Image source introuvable : ' + name)


def crop_resize(path, w, h):
    im = Image.open(path).convert('RGB')
    W, H = im.size
    ratio = w / h
    if W / H > ratio:
        nw = int(H * ratio)
        x0 = (W - nw) // 2
        im = im.crop((x0, 0, x0 + nw, H))
    else:
        nh = int(W / ratio)
        y0 = (H - nh) // 2
        im = im.crop((0, y0, W, y0 + nh))
    if im.size[0] < w:
        print('  ATTENTION agrandie :', os.path.basename(path), im.size, '->', w)
    return im.resize((w, h), Image.LANCZOS)


def images():
    os.makedirs(IMG, exist_ok=True)
    for out, w, h, src in IMAGES:
        p = find_source(src)
        im = crop_resize(p, w, h)
        dest = os.path.join(IMG, out)
        for q in (80, 76, 72):
            im.save(dest, 'JPEG', quality=q, optimize=True, progressive=True)
            if os.path.getsize(dest) < 250 * 1024:
                break
        print(out, w, h, os.path.getsize(dest) // 1024, 'Ko')
    # favicon monogramme
    fav = Image.new('RGB', (64, 64), '#2c3e47')
    d = ImageDraw.Draw(fav)
    f = ImageFont.truetype(FONT_B, 30)
    box = d.textbbox((0, 0), 'DF', font=f)
    d.text(((64 - (box[2] - box[0])) / 2 - box[0], (64 - (box[3] - box[1])) / 2 - box[1]), 'DF', font=f, fill='#ffffff')
    fav.save(os.path.join(IMG, 'favicon.png'))
    # planche contact : 6 images sources, 400 px
    sources = [SRC_ALLEE, SRC_DALLEE, SRC_TERRASSE, SRC_CONCEPTION, SRC_MACONNERIE, SRC_TONTE]
    sheet = Image.new('RGB', (1200, 700), '#ffffff')
    sd = ImageDraw.Draw(sheet)
    lf = ImageFont.truetype(FONT_B, 18)
    for i, s in enumerate(sources):
        thumb = crop_resize(find_source(s), 400, 300)
        x, y = (i % 3) * 400, (i // 3) * 350
        sheet.paste(thumb, (x, y))
        sd.text((x + 8, y + 306), '%d  %s' % (i + 1, s[:38]), font=lf, fill='#1c262b')
    sheet.save(WORK + '/planche_contact.jpg', 'JPEG', quality=85)
    print('planche :', WORK + '/planche_contact.jpg')


# ---------- gabarits HTML ----------

def head(title, desc):
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>' + title + '</title>\n'
            '<meta name="description" content="' + desc + '">\n'
            '<meta name="robots" content="noindex, nofollow">\n'
            '<link rel="icon" type="image/png" href="images/favicon.png">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Nunito+Sans:wght@400;700&display=swap">\n'
            '<link rel="stylesheet" href="css/style.css">\n</head>\n<body>\n')


def header(current):
    links = [('index.html', 'Accueil'), ('prestations.html', 'Prestations'),
             ('a-propos.html', 'À propos'), ('contact.html', 'Contact')]
    nav = ''
    for href, label in links:
        aria = ' aria-current="page"' if href == current else ''
        nav += '<a href="' + href + '"' + aria + '>' + label + '</a>'
    return ('<header class="hdr">\n  <div class="wrap">\n'
            '    <a class="brand" href="https://webaunet.github.io/maquettes/df-paysages/" aria-label="D&amp;F Paysages, accueil">\n'
            '      <span><b>D&amp;F Paysages</b><small>Paysagiste · Brunoy (91)</small></span>\n    </a>\n'
            '    <nav class="nav" id="nav" aria-label="Navigation principale">' + nav + '</nav>\n'
            '    <a class="call" href="tel:' + TEL + '" aria-label="Appeler le ' + TEL_FR + '">\n'
            '      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>\n'
            '      <span>' + TEL_FR + '</span>\n    </a>\n'
            '    <button class="burger" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span></span></button>\n'
            '  </div>\n</header>\n')


SKDONE = ('<div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3>'
          '<p>Choisissez comment l’envoyer. Rien n’est transmis tant que vous n’avez pas validé l’envoi.</p>'
          '<pre class="sk-sum"></pre><div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a>'
          '<button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button>'
          '<a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a>'
          '<a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div>'
          '<button class="sk-back" type="button" data-back>Modifier ma demande</button></div>')

SVG_CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12l4.5 4.5L19 7"/></svg>')


def footer():
    return ('<div class="hf hf3" role="contentinfo"><div class="hv-wrap"><strong>D&amp;F Paysages</strong>'
            '<nav aria-label="Pied de page"><a href="index.html">Accueil</a><a href="prestations.html">Prestations</a>'
            '<a href="a-propos.html">À propos</a><a href="contact.html">Contact</a></nav>'
            '<div class="hf-c"><a href="tel:' + TEL + '">' + TEL_FR + '</a></div>'
            '<p class="hf-cop">© D&amp;F Paysages · Brunoy (91) · Maquette de démonstration</p></div></div>\n')


def h12():
    return ('<section class="hv hv12 hv-dark" aria-labelledby="hv-t"><div class="hv12-bg">'
            '<img src="images/hero.jpg" width="1228" height="768" alt="' + ALT['hero.jpg'] + '"></div>'
            '<div class="hv-wrap hv12-in"><div class="hv12-txt"><p class="hv-kick">D&amp;F Paysages</p>'
            '<h1 id="hv-t">Aménagement et entretien de vos espaces verts<em>Brunoy (91)</em></h1>'
            '<svg class="hv12-line" viewBox="0 0 480 14" aria-hidden="true" focusable="false"><path d="M2 9C90 2 200 12 300 6S440 7 478 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'
            '<div class="hv12-cta"><a class="hv12-pill" href="prestations.html">Nos prestations<span aria-hidden="true">↗</span></a>'
            '<a class="hv12-pill" href="contact.html">Nous contacter<span aria-hidden="true">↗</span></a></div></div>'
            '<div class="hv12-card"><h2 class="hv12-ct">Demande de devis</h2>'
            '<form class="sk-form" id="kform" novalidate data-name="D&amp;F Paysages" data-sms="' + TEL + '" data-tel="' + TEL + '" data-email="">'
            '<div class="sk-f"><label for="h-nom">Nom</label><input id="h-nom" name="nom" type="text" placeholder="Votre nom" autocomplete="name" required aria-describedby="h-nom-e"><p class="sk-err" id="h-nom-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="h-tel">Téléphone</label><input id="h-tel" name="tel" type="tel" placeholder="Votre téléphone" autocomplete="tel" inputmode="tel" required aria-describedby="h-tel-e"><p class="sk-err" id="h-tel-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="h-commune">Commune</label><input id="h-commune" name="commune" type="text" placeholder="Votre commune" autocomplete="address-level2" required aria-describedby="h-commune-e"><p class="sk-err" id="h-commune-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="h-msg">Votre demande</label><textarea id="h-msg" name="msg" rows="2" placeholder="Votre demande (facultatif)"></textarea><p class="sk-err" id="h-msg-e" role="alert"></p></div>'
            '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>' + SKDONE +
            '</div></div></section>\n')


def v1():
    cards = [
        ('p1.jpg', 'prestations.html#p1', 'Création d’espaces verts', 'Plantations, massifs et aménagement du jardin selon votre projet.'),
        ('p2.jpg', 'prestations.html#p2', 'Terrasses et allées', 'Pose de terrasses en bois et d’allées en pavés ou dallées.'),
        ('p3.jpg', 'prestations.html#p3', 'Entretien et tonte', 'Tonte de pelouse, débroussaillage et entretien régulier du jardin.'),
    ]
    body = ''
    for img, href, title, text in cards:
        body += ('<article class="sv1-card"><figure><img src="images/' + img + '" width="800" height="500" alt="' + ALT[img] + '" loading="lazy"></figure>'
                 '<div><h3>' + title + '</h3><p>' + text + '</p><a href="' + href + '">En savoir plus →</a></div></article>\n')
    return ('<section class="sv sv1" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p>'
            '<h2 id="sv-t">Ce que nous réalisons pour votre jardin</h2>'
            '<p class="hv-lead">Création, aménagement et entretien d’espaces verts, selon votre projet.</p>'
            '<div class="sv1-grid">' + body + '</div></div></section>\n')


def a3():
    return ('<section class="sv sa3" aria-labelledby="sv-a"><div class="hv-wrap"><div>'
            '<p class="hv-kick">À propos</p><h2 id="sv-a">Une entreprise de paysagisme installée à Brunoy</h2>'
            '<p>D&amp;F Paysages exerce dans les services d’aménagement paysager, depuis son siège à Brunoy, dans l’Essonne.</p>'
            '<p>L’entreprise est dirigée par Victor Jorge.</p>'
            '<a class="hv-btn hv-btn-p" href="a-propos.html">Découvrir l’entreprise</a></div>'
            '<div class="sa3-imgs"><figure class="sa3-i1"><img src="images/a1.jpg" width="614" height="768" alt="' + ALT['a1.jpg'] + '" loading="lazy"></figure>'
            '<figure class="sa3-i2"><img src="images/a2.jpg" width="600" height="600" alt="' + ALT['a2.jpg'] + '" loading="lazy"></figure></div></div></section>\n')


def c7():
    return ('<section class="sv sc7" aria-labelledby="sv-c"><div class="hv-wrap"><div class="sc7-card">'
            '<figure class="sc7-ph"><img src="images/c1.jpg" width="768" height="768" alt="' + ALT['c1.jpg'] + '" loading="lazy"></figure>'
            '<div class="sc7-tx"><p class="hv-kick">Contact</p><h2 id="sv-c">Un projet de jardin&nbsp;? Parlons-en.</h2>'
            '<p class="hv-lead">Décrivez votre projet en quelques lignes, puis choisissez comment nous l’envoyer.</p>'
            '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:' + TEL + '">Appeler le ' + TEL_FR + '</a>'
            '<a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div>'
            '<p class="sc7-add">D&amp;F Paysages · Brunoy (91)</p></div></div></div></section>\n')


def k6():
    return ('<section class="sv sk sk6" aria-labelledby="sv-k"><div class="hv-wrap">'
            '<figure class="sk6-ban"><img src="images/k1.jpg" width="1400" height="600" alt="' + ALT['k1.jpg'] + '"></figure>'
            '<div class="sk-card"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2>'
            '<p class="sk-intro">Décrivez votre besoin, puis envoyez-le par SMS ou copiez-le.</p>'
            '<form class="sk-form" id="kform" novalidate data-name="D&amp;F Paysages" data-sms="' + TEL + '" data-tel="' + TEL + '" data-email="">'
            '<div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e">'
            '<option value="">Choisir…</option><option>Création d’espaces verts</option><option>Terrasse ou allée</option>'
            '<option>Entretien et tonte</option><option>Autre demande</option></select><p class="sk-err" id="k-besoin-e" role="alert"></p></div>'
            '<div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div>'
            '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>' + SKDONE +
            '</div><aside class="sk-side"><ul><li><span>Téléphone</span><a href="tel:' + TEL + '">' + TEL_FR + '</a></li>'
            '<li><span>Siège</span><p>Brunoy (91)</p></li></ul></aside></div></section>\n')


def page(title, desc, current, body, scripts):
    return head(title, desc) + header(current) + '<main>\n' + body + '</main>\n' + footer() + scripts + '</body>\n</html>\n'


MAIN_JS = '<script src="js/main.js" defer></script>\n'
K_JS = '<script src="js/k.js" defer></script>\n'


def page_index():
    body = h12() + v1() + a3() + c7()
    return page('D&amp;F Paysages, paysagiste à Brunoy (91)',
                'D&amp;F Paysages, entreprise d’aménagement paysager à Brunoy (Essonne) : création, aménagement et entretien d’espaces verts. Demande de devis en ligne.',
                'index.html', body, K_JS + MAIN_JS)


def page_prestations():
    hero = ('<section class="sec s-sage" aria-labelledby="h1"><div class="wrap land"><div>'
            '<span class="eyebrow">Prestations · Brunoy (91)</span><h1 id="h1">Nos prestations de paysagiste</h1>'
            '<p style="margin-top:1rem">Création, aménagement et entretien d’espaces verts, pour votre jardin.</p>'
            '<div class="actions"><a class="btn btn-rope" href="contact.html">Demander un devis</a>'
            '<a class="btn btn-green" href="tel:' + TEL + '">Appeler le ' + TEL_FR + '</a></div></div>'
            '<div class="mosaic"><img class="a" src="images/hero.jpg" width="1228" height="768" alt="' + ALT['hero.jpg'] + '">'
            '<img class="b" src="images/svc-tonte.jpg" width="800" height="436" alt="' + ALT['svc-tonte.jpg'] + '" loading="lazy">'
            '<img class="c" src="images/svc-maconnerie.jpg" width="800" height="436" alt="' + ALT['svc-maconnerie.jpg'] + '" loading="lazy"></div>'
            '</div></section>\n')
    items = [
        ('p1', 'svc-creation.jpg', 'Création d’espaces verts', 'Plantations, massifs et aménagement du jardin selon votre projet.'),
        ('p2', 'svc-terrasse.jpg', 'Terrasses et allées', 'Pose de terrasses en bois et d’allées en pavés ou dallées.'),
        ('p3', 'svc-tonte.jpg', 'Entretien et tonte', 'Tonte de pelouse, débroussaillage et entretien régulier du jardin.'),
        ('p4', 'svc-maconnerie.jpg', 'Maçonnerie paysagère', 'Murets, escaliers et ouvrages en pierre intégrés au jardin.'),
    ]
    def cards_of(sub):
        out = ''
        for ident, img, title, text in sub:
            out += ('<article class="svc" id="' + ident + '"><img src="images/' + img + '" width="800" height="436" alt="' + ALT[img] + '" loading="lazy">'
                    '<div><h3>' + title + '</h3><p>' + text + '</p></div></article>\n')
        return out
    grid = ('<section class="sec s-cream" aria-labelledby="h-serv"><div class="wrap">'
            '<div class="head"><span class="eyebrow">Domaines d’intervention</span><h2 id="h-serv">Création et aménagement</h2>'
            '<p>Du projet de jardin à la terrasse ou à l’allée, selon votre besoin.</p></div>'
            '<div class="grid4 g2">' + cards_of(items[:2]) + '</div></div></section>\n'
            '<section class="sec s-sage" aria-labelledby="h-serv2"><div class="wrap">'
            '<div class="head"><span class="eyebrow">Domaines d’intervention</span><h2 id="h-serv2">Entretien et ouvrages en pierre</h2>'
            '<p>Tonte, entretien du jardin et maçonnerie paysagère.</p></div>'
            '<div class="grid4 g2">' + cards_of(items[2:]) + '</div></div></section>\n')
    cta = ('<section class="sec dark rings cta" aria-labelledby="h-cta"><div class="wrap"><div class="ctabox">'
           '<span class="eyebrow">Demande de devis</span><h2 id="h-cta">Un jardin, une terrasse, un projet&nbsp;?</h2>'
           '<p style="margin-top:1rem">Décrivez votre besoin, puis appelez l’entreprise ou écrivez-nous.</p>'
           '<div class="actions"><a class="btn btn-rope" href="contact.html">Demander un devis</a>'
           '<a class="btn btn-line" href="tel:' + TEL + '">Appeler le ' + TEL_FR + '</a></div></div></div></section>\n')
    return page('Prestations de paysagiste | D&amp;F Paysages à Brunoy (91)',
                'Création, aménagement et entretien d’espaces verts par D&amp;F Paysages à Brunoy (Essonne) : terrasses, allées, tonte et entretien de jardin.',
                'prestations.html', hero + grid + cta, MAIN_JS)


def page_apropos():
    intro = ('<section class="sec s-cream" aria-labelledby="h1"><div class="wrap"><div class="head">'
             '<span class="eyebrow">L’entreprise · Brunoy (91)</span><h1 id="h1">Une entreprise d’aménagement paysager à Brunoy</h1>'
             '<p>D&amp;F Paysages exerce dans le secteur des services d’aménagement paysager, depuis Brunoy, en Essonne.</p>'
             '</div></div></section>\n')
    about = ('<section class="sec compact dark rings" aria-labelledby="h-about"><div class="wrap about">'
             '<div class="about-media"><img class="main" src="images/about.jpg" width="800" height="436" alt="' + ALT['about.jpg'] + '" loading="lazy"></div>'
             '<div class="about-card"><span class="eyebrow">Repères</span><h2 id="h-about">Les informations de référence</h2>'
             '<ul><li>' + SVG_CHECK + 'Secteur d’activité : services d’aménagement paysager</li>'
             '<li>' + SVG_CHECK + 'Siège : Brunoy (Essonne, 91)</li>'
             '<li>' + SVG_CHECK + 'Dirigeant : Victor Jorge</li></ul>'
             '<div class="actions"><a class="btn btn-rope" href="contact.html">Nous contacter</a></div></div></div></section>\n')
    nxt = ('<section class="sec compact s-sage" aria-labelledby="h-next"><div class="wrap"><div class="head">'
           '<span class="eyebrow">Suite</span><h2 id="h-next">Découvrir les prestations</h2>'
           '<p>Création, aménagement et entretien d’espaces verts.</p></div>'
           '<div class="actions"><a class="btn btn-green" href="prestations.html">Voir les prestations</a></div></div></section>\n')
    return page('À propos | D&amp;F Paysages, paysagiste à Brunoy (91)',
                'D&amp;F Paysages, entreprise de services d’aménagement paysager installée à Brunoy (Essonne), dirigée par Victor Jorge.',
                'a-propos.html', intro + about + nxt, MAIN_JS)


def page_contact():
    band = ('<section class="sec s-cream" style="padding-top:clamp(2.5rem,6vw,4rem);padding-bottom:clamp(1.5rem,3vw,2rem);min-height:0" aria-labelledby="h1">'
            '<div class="wrap"><div class="head"><span class="eyebrow">Contact · Brunoy (91)</span>'
            '<h1 id="h1">Parlons de votre projet</h1>'
            '<p>Préparez votre demande dans le formulaire ci-dessous, puis envoyez-la par SMS ou appelez l’entreprise.</p>'
            '</div></div></section>\n')
    return page('Contact et demande de devis | D&amp;F Paysages à Brunoy (91)',
                'Contactez D&amp;F Paysages à Brunoy (Essonne) : appelez le ' + TEL_FR + ' ou préparez votre demande de devis en ligne.',
                'contact.html', band + k6(), K_JS + MAIN_JS)


def site():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE)
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(SITE)
    for f in ('arboriculture.html', 'paysage.html', 'entreprise.html', '_SKELETON.md'):
        os.remove(os.path.join(SITE, f))
    os.makedirs(os.path.join(SITE, 'images'), exist_ok=True)
    for f in os.listdir(IMG):
        shutil.copy(os.path.join(IMG, f), os.path.join(SITE, 'images', f))
    # CSS : palette et polices imposées (une seule passe, pas de chaînage)
    cp = os.path.join(SITE, 'css', 'style.css')
    css = open(cp, encoding='utf8').read()
    pat = re.compile('|'.join(re.escape(k) for k in HEX_MAP), re.I)
    css, n = pat.subn(lambda m: HEX_MAP[m.group(0).lower()], css)
    css = css.replace('rgba(247,242,230', 'rgba(243,245,242').replace('rgba(18,48,31', 'rgba(44,62,71')
    css = re.sub(r'^/\*.*?\*/', '/* Maquette D&F Paysages : feuille de style */', css, count=1, flags=re.S)
    assert css.count("'Figtree'") == 1, 'police Figtree introuvable'
    css = css.replace("'Figtree'", "'Nunito Sans'")
    css += EXTRA_CSS
    open(cp, 'w', encoding='utf8').write(css)
    print('couleurs remplacées :', n)
    # squelette : apostrophe non échappée dans js/main.js (erreur de syntaxe qui bloque tout le script)
    mp = os.path.join(SITE, 'js', 'main.js')
    js = open(mp, encoding='utf8').read()
    assert js.count("l'entreprise") == 1, 'apostrophe de main.js introuvable'
    open(mp, 'w', encoding='utf8').write(js.replace("l'entreprise", "l’entreprise"))
    # modules (ajoute leur CSS à style.css et copie js/k.js)
    subprocess.run([sys.executable, '-I', 'mod.py', SITE, 'H12', 'V1', 'A3', 'C7', 'F3', 'K6'] + MOD_ARGS,
                   cwd=OUTILS, check=True)
    # pages
    pages = {'index.html': page_index(), 'prestations.html': page_prestations(),
             'a-propos.html': page_apropos(), 'contact.html': page_contact()}
    for name, html in pages.items():
        open(os.path.join(SITE, name), 'w', encoding='utf8').write(html)
    print('pages :', ', '.join(sorted(os.listdir(SITE))))


if __name__ == '__main__':
    {'images': images, 'site': site}[sys.argv[1]]()
