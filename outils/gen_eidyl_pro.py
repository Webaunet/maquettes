import os, re, glob, shutil, subprocess, zipfile
from PIL import Image, ImageOps

U = '/mnt/user-data/uploads/Maquettes/'
IMG = U + 'Images/Paysagiste/'
MODS = U + 'Squelettes/Modules/'
D = '/home/claude/maquettes/eidyl-pro'
NOM, COM = 'EIDYL PRO', 'Saint-Germain-lès-Corbeil'
TEL, TELI = '06 82 70 60 21', '+33682706021'
SITE = 'https://webaunet.github.io/maquettes/eidyl-pro/'

shutil.rmtree(D, ignore_errors=True)
os.makedirs(D + '/images')
zipfile.ZipFile(U + 'Squelettes/S04.zip').extractall(D)
os.remove(D + '/_SKELETON.md')

# ---------- CSS : palette 8, polices, normalisation
cp = D + '/css/style.css'
s = open(cp, encoding='utf8').read()
n0 = len(s)
s, n = re.subn(r'@media\(prefers-color-scheme:dark\)\{(?:[^{}]*\{[^{}]*\})*\s*\}', '', s)
print('blocs sombres retirés', n)
root = (":root{\n  --vert:#3b4a1f;--vert2:#4a5d27;--sauge:#e8e6cf;--creme:#f6f3e8;--pierre:#e8e6cf;\n"
        "  --or:#c4912a;--or-clair:#c4912a;--encre:#23261a;--texte:#23261a;--blanc:#fffdf8;\n"
        "  --r:28px;--ombre:0 14px 40px rgba(59,74,31,.14);--h-head:76px;\n"
        "  --serif:'Playfair Display',Georgia,serif;--sans:'Lato',system-ui,sans-serif;\n}")
s, n = re.subn(r':root\{.*?\n\}', lambda m: root, s, count=1, flags=re.S)
assert n == 1
s = s.replace('rgba(246,241,230,.94)', 'rgba(246,243,232,.94)').replace('#1c2a22', '#23261a').replace('#f0c772', '#d6a43c')
s, n = re.subn(r'font-weight:\s*(?:5|6|8)00', 'font-weight:700', s)
s, n2 = re.subn(r'font:\s*(?:5|6|8)00 ', 'font:700 ', s)
print('graisses', n, n2)
open(cp, 'w', encoding='utf8').write(s)

r = subprocess.run(['python3', '-I', MODS + 'mod.py', D, 'H3', 'V7', 'A1', 'C3', 'F2', 'K2',
                    '--bg', '#f6f3e8', '--bg2', '#e8e6cf', '--ink', '#23261a', '--mu', '#53563f',
                    '--main', '#3b4a1f', '--acc', '#c4912a', '--accink', '#23261a',
                    '--fh', 'Playfair Display', '--fb', 'Lato', '--fw', '700'], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
s = open(cp, encoding='utf8').read()
s, n = re.subn(r'font-weight:\s*(?:5|6|8)00', 'font-weight:700', s)
s += ('\n/* EIDYL PRO */\n.kicker{color:var(--vert)}.sec-vert .kicker{color:var(--creme)}.logo small{color:var(--texte)}'
      '.hero em{color:var(--vert)}.hero.ch{min-height:0}\n'
      '.sa1-pic{max-width:628px;margin-inline:auto}.sc3-bg img{left:auto;width:min(100%,1408px)}\n'
      '.fiche dd a{display:inline-flex;align-items:center;min-height:44px}\n'
      '@media(max-width:860px){.ap-fiche .photo{display:none}}\n'
      '@media(max-width:620px){.sec{padding:2rem 0 3.5rem}}\n')
open(cp, 'w', encoding='utf8').write(s)

# ---------- JS : espace réservé
jp = D + '/js/main.js'
j = open(jp, encoding='utf8').read()
a = "d\\'Nom de l'entreprise"
assert j.count(a) == 1
open(jp, 'w', encoding='utf8').write(j.replace(a, "d\\'" + NOM))

# ---------- images
def g(p):
    m = sorted(glob.glob(IMG + p)); assert len(m) == 1, (p, m); return m[0]
SRC = dict(mac=g('ma*onerie*'), con=g('conception*'), cre=g('imgi_4_creation*'), ter=g('chantier terrasse*'),
           pla=g('imgi_6_plantation*'), ton=g('imgi_2_tonte*'), ent=g('imgi_7_entretien-jardin*'),
           pav=g('all*pav*'), dal=g('chantier all*e dall*e.jpg'))

def save(k, w, h, name, cx=.5, q=78):
    im = Image.open(SRC[k]).convert('RGB')
    assert im.width >= w and im.height >= h, (k, im.size, w, h)
    ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(cx, .5)).save(D + '/images/' + name, 'JPEG', quality=q, optimize=True, progressive=True)

save('mac', 1400, 600, 'hero.jpg')
save('con', 628, 768, 'a1.jpg', .6)
save('pav', 1408, 768, 'c1.jpg', q=62)
for i, k in enumerate(['cre', 'ter', 'pla', 'ton'], 1):
    save(k, 800, 600, 'p%d.jpg' % i)
for i, k in enumerate(['cre', 'ter', 'pla', 'ent'], 1):
    save(k, 1000, 545, 'l%d.jpg' % i)
for i, k in enumerate(['con', 'dal', 'mac'], 1):
    save(k, 1000, 545, 'mos%d.jpg' % i)
save('ton', 1000, 545, 'ap2.jpg')

# ---------- en-tête commun (tiré du squelette)
sk = {}
for p in ['index', 'prestations', 'a-propos', 'contact']:
    sk[p] = open(D + '/%s.html' % p, encoding='utf8').read()

def head(p, title, desc):
    h = sk[p][:sk[p].index('<main')]
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, h)
    h = h.replace('Aurea Paysages, accueil', NOM + ', accueil').replace('https://webaunet.github.io/aurea-paysages/', SITE)
    h = h.replace('<b>AUREA</b><small>Paysages</small>', '<b>EIDYL</b><small>Pro</small>')
    h = h.replace('+33672766910', TELI).replace('06 72 76 69 10', TEL)
    h = h.replace('#1f3a2e', '#3b4a1f').replace('%231f3a2e', '%233b4a1f').replace('#e3b658', '#c4912a').replace('%23e3b658', '%23c4912a')
    h = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis[^>]*>',
               '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&amp;family=Playfair+Display:wght@700&amp;display=swap">', h)
    assert 'Aurea' not in h and 'AUREA' not in h, p
    return h

FOOT = ('<div class="hf hf2" role="contentinfo"><div class="hv-wrap"><strong>EIDYL PRO</strong><nav aria-label="Pied de page">'
        '<a href="index.html">Accueil</a><a href="prestations.html">Prestations</a><a href="a-propos.html">À propos</a><a href="contact.html">Contact</a></nav>'
        '<a href="tel:%s">%s</a><p class="hf-cop">© EIDYL PRO · %s (91) · Maquette de démonstration</p></div></div>\n' % (TELI, TEL, COM))

def page(p, title, desc, body, extra=''):
    open(D + '/%s.html' % p, 'w', encoding='utf8').write(
        head(p, title, desc) + '<main id="contenu">\n' + body + '\n</main>\n\n' + FOOT + extra + '<script src="js/main.js"></script>\n</body>\n</html>\n')

def curve(col, d):
    return ('<svg class="courbe" style="color:var(--%s);position:absolute;left:0;bottom:-1px" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true">'
            '<path fill="currentColor" d="%s"/></svg>' % (col, d))
CH = 'M0 90V45Q360 -15 720 35T1440 30V90z'
CA = 'M0 45Q360 100 720 45T1440 40V90H0z'
CB = 'M0 40Q400 100 800 40T1440 50V90H0z'
CC = 'M0 50Q360 -10 720 45T1440 35V90H0z'

# ---------- accueil (modules H3 V7 A1 C3)
H3 = ('<section class="hv hv3" aria-labelledby="hv-t"><div class="hv-wrap"><p class="hv-kick">Paysagiste à %s (91)</p>'
      '<h1 id="hv-t">Votre jardin, aménagé et entretenu.</h1>'
      '<p class="hv-lead">EIDYL PRO est une entreprise d\'aménagement paysager à %s, en Essonne. Appelez-nous pour parler de votre projet.</p>'
      '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:%s">Appeler le %s</a><a class="hv-btn hv-btn-s" href="prestations.html">Voir les prestations</a></div></div>'
      '<div class="hv3-strip"><div class="hv-wrap"><img src="images/hero.jpg" width="1400" height="600" alt="Paysagiste montant un muret de pierre et un escalier dans un jardin en pente">'
      '<div class="hv3-card">Intervient à %s<span>Essonne (91)</span></div></div></div></section>') % (COM, COM, TELI, TEL, COM)

SV = [('Création de jardins', 'Conception et aménagement de votre jardin, du plan à la plantation.', 'Paysagiste plantant un massif le long d\'une allée courbe devant une maison moderne'),
      ('Terrasses et allées', 'Terrasses en bois, allées et dallages pour prolonger la maison.', 'Paysagiste posant une terrasse en bois devant une maison en pierre'),
      ('Plantations', 'Arbustes, vivaces et massifs plantés pour embellir votre jardin.', 'Paysagiste plantant un arbuste dans un massif fleuri'),
      ('Entretien du jardin', 'Tonte, taille et suivi régulier pour un jardin net toute l\'année.', 'Jardinier tondant une pelouse devant une maison aux volets bleus')]
cards = ''.join('<article class="sv7-c"><figure><img src="images/p%d.jpg" width="800" height="600" alt="%s"><span class="sv7-n">0%d</span></figure>'
                '<div><h3>%s</h3><p>%s</p><a href="prestations.html#p%d">En savoir plus →</a></div></article>' % (i, a, i, t, d, i)
                for i, (t, d, a) in enumerate(SV, 1))
V7 = ('<section class="sv sv7" aria-labelledby="sv-t"><div class="hv-wrap"><p class="hv-kick">Nos prestations</p><h2 id="sv-t">Aménagement et entretien de jardins</h2>'
      '<p class="hv-lead">Quatre domaines d\'intervention pour créer et garder un beau jardin.</p>'
      '<div class="sv7-track" tabindex="0" role="region" aria-label="Nos prestations, faire défiler">' + cards + '</div></div></section>')

A1 = ('<section class="sv sa1" aria-labelledby="sv-a"><div class="hv-wrap"><figure class="sa1-pic"><img src="images/a1.jpg" width="628" height="768" '
      'alt="Plan de jardin affiché sur une tablette devant un massif et un muret de pierre"></figure><div><p class="hv-kick">À propos</p>'
      '<h2 id="sv-a">Une entreprise locale de paysage.</h2>'
      '<p>EIDYL PRO est une entreprise d\'aménagement paysager basée à %s, en Essonne.</p><p>Elle est dirigée par Clement Konc.</p>'
      '<ul class="sa1-pts"><li><span><strong>Activité</strong> : aménagement paysager.</span></li><li><span><strong>Commune</strong> : %s (91).</span></li>'
      '<li><span><strong>Dirigeant</strong> : Clement Konc.</span></li></ul><a class="hv-btn hv-btn-s" href="a-propos.html">En savoir plus</a></div></div></section>') % (COM, COM)

C3 = ('<section class="sv sc3" aria-labelledby="sv-c"><div class="sc3-bg"><img src="images/c1.jpg" width="1408" height="768" alt=""></div><div class="hv-wrap">'
      '<p class="hv-kick">Contact</p><h2 id="sv-c">Un projet de jardin ? Parlons-en.</h2><p class="hv-lead">Appelez EIDYL PRO ou envoyez votre demande de devis en ligne.</p>'
      '<div class="hv-cta"><a class="hv-btn hv-btn-p" href="tel:%s">Appeler le %s</a><a class="hv-btn hv-btn-s" href="contact.html">Écrire un message</a></div></div></section>') % (TELI, TEL)

page('index', 'EIDYL PRO – Aménagement paysager à %s (91)' % COM,
     'EIDYL PRO, entreprise d\'aménagement paysager à %s (91) : création de jardins, terrasses, plantations et entretien. Appelez le %s.' % (COM, TEL),
     H3 + V7 + A1 + C3)

# ---------- prestations
def ligne(i, title, txt, alt, cls, rev, nxt):
    return ('<section class="sec%s" id="p%d">\n  <div class="wrap">\n<div class="ligne%s"><img loading="lazy" src="images/l%d.jpg" width="1000" height="545" alt="%s"><div><h2>%s</h2><p>%s</p></div></div>\n  </div>\n  %s\n</section>\n'
            % (cls, i, ' rev' if rev else '', i, alt, title, txt, nxt))
PR = ('<section class="hero ph">\n  <div class="wrap">\n    <div>\n      <p class="kicker">Prestations</p>\n      <h1>Créer, aménager, entretenir votre jardin.</h1>\n'
      '      <p class="lead">Du plan à la plantation, EIDYL PRO intervient à %s (91).</p>\n'
      '      <div class="actions"><a class="btn btn-or" href="tel:%s">Appeler le %s</a><a class="btn btn-vert" href="contact.html">Demander un devis</a></div>\n    </div>\n'
      '    <div class="mosaique">\n      <img src="images/mos1.jpg" width="1000" height="545" alt="Plan de jardin affiché sur une tablette devant un massif et un muret de pierre">\n'
      '      <img src="images/mos2.jpg" width="1000" height="545" alt="Chantier d\'une allée dallée devant une maison en pierre, au crépuscule">\n'
      '      <img src="images/mos3.jpg" width="1000" height="545" alt="Paysagiste montant un muret de pierre et un escalier dans un jardin">\n    </div>\n  </div>\n  %s\n</section>\n') % (COM, TELI, TEL, curve('pierre', CH))
PR += ligne(1, 'Création de jardins', 'Conception et aménagement de votre jardin : pelouse, massifs et allées pensés pour votre terrain et votre usage.',
            'Jardin neuf avec pelouse, allée courbe et massifs en cours de plantation', ' sec-pierre', False, curve('creme', CA))
PR += ligne(2, 'Terrasses et allées', 'Terrasses en bois, allées dallées ou pavées : des surfaces qui prolongent la maison et facilitent la circulation.',
            'Pose d\'une terrasse en bois devant une maison en pierre', '', True, curve('vert', CB))
PR += ligne(3, 'Plantations', 'Arbustes, vivaces et massifs plantés pour embellir votre jardin et structurer vos espaces.',
            'Plantation d\'un arbuste dans un massif', ' sec-vert', False, curve('sauge', CC))
PR += ligne(4, 'Entretien du jardin', 'Tonte, taille et suivi régulier pour garder votre jardin net tout au long de l\'année.',
            'Jardin entretenu avec pelouse, massifs et allée de gravier devant une maison en pierre', ' sec-sauge', True, curve('creme', CA))
PR += ('<section class="sec">\n  <div class="wrap"><div class="cta"><h2>Parlons de votre jardin.</h2><p>Un terrain à aménager ou un entretien à confier ? Décrivez votre besoin.</p>'
       '<div class="actions"><a class="btn btn-or" href="tel:%s">Appeler le %s</a><a class="btn btn-ligne" href="contact.html">Demander un devis</a></div></div></div>\n</section>') % (TELI, TEL)
page('prestations', 'Prestations – EIDYL PRO à %s (91)' % COM,
     'Prestations d\'EIDYL PRO à %s (91) : création de jardins, terrasses et allées, plantations et entretien du jardin.' % COM, PR)

# ---------- à propos
AP = ('<section class="hero ch">\n  <div class="wrap one">\n    <div><p class="kicker">À propos</p><h1>EIDYL PRO, paysagiste en Essonne.</h1>\n'
      '    <p class="lead">Entreprise d\'aménagement paysager de %s, dirigée par Clement Konc.</p>\n'
      '    <div class="actions"><a class="btn btn-vert" href="contact.html">Nous contacter</a><a class="btn btn-ligne" href="tel:%s">Appeler le %s</a></div></div>\n  </div>\n  %s\n</section>\n'
      '<section class="sec sec-sauge ap-fiche">\n  <div class="wrap"><div class="apropos">\n'
      '    <div class="fiche"><p class="kicker">En bref</p><h2>L\'entreprise</h2>\n'
      '    <dl><dt>Nom</dt><dd>EIDYL PRO</dd><dt>Activité</dt><dd>Services d\'aménagement paysager</dd><dt>Commune</dt><dd>%s (91)</dd><dt>Dirigeant</dt><dd>Clement Konc</dd>'
      '<dt>Téléphone</dt><dd><a href="tel:%s">%s</a></dd></dl></div>\n'
      '    <div class="photo"><img loading="lazy" src="images/ap2.jpg" width="1000" height="545" alt="Jardinier tondant une pelouse devant une maison aux volets bleus"></div>\n  </div></div>\n  %s\n</section>\n'
      '<section class="sec">\n  <div class="wrap"><div class="cta"><h2>Un projet de jardin ?</h2><p>Décrivez-nous votre terrain et vos envies.</p>'
      '<div class="actions"><a class="btn btn-or" href="tel:%s">Appeler le %s</a><a class="btn btn-ligne" href="contact.html">Demander un devis</a></div></div></div>\n</section>') % (
      COM, TELI, TEL, curve('sauge', CH), COM, TELI, TEL, curve('creme', CA), TELI, TEL)
page('a-propos', 'À propos – EIDYL PRO, paysagiste à %s (91)' % COM,
     'EIDYL PRO, entreprise d\'aménagement paysager à %s (91), dirigée par Clement Konc.' % COM, AP)

# ---------- contact (module K2)
K2 = ('<section class="sv sk sk2" aria-labelledby="sv-k"><div class="hv-wrap sk-grid"><div class="sk-card"><p class="hv-kick">Demande de devis</p><h2 id="sv-k">Parlez-nous de votre projet</h2>'
      '<p class="sk-intro">Décrivez votre besoin : vous obtenez un message prêt à envoyer par SMS ou à copier.</p>'
      '<form class="sk-form" id="kform" novalidate data-name="EIDYL PRO" data-sms="%s" data-tel="%s" data-email="">'
      '<div class="sk-f"><label for="k-nom">Nom</label><input id="k-nom" name="nom" type="text" autocomplete="name" required aria-describedby="k-nom-e"><p class="sk-err" id="k-nom-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-tel">Téléphone</label><input id="k-tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" required aria-describedby="k-tel-e"><p class="sk-err" id="k-tel-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-commune">Commune</label><input id="k-commune" name="commune" type="text" autocomplete="address-level2" required aria-describedby="k-commune-e"><p class="sk-err" id="k-commune-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-besoin">Votre besoin</label><select id="k-besoin" name="besoin" required aria-describedby="k-besoin-e"><option value="">Choisir…</option>'
      '<option>Création de jardin</option><option>Terrasse ou allée</option><option>Plantations</option><option>Entretien du jardin</option><option>Autre demande</option></select><p class="sk-err" id="k-besoin-e" role="alert"></p></div>'
      '<div class="sk-f"><label for="k-msg">Message (facultatif)</label><textarea id="k-msg" name="msg" rows="3"></textarea><p class="sk-err" id="k-msg-e" role="alert"></p></div>'
      '<button class="hv-btn hv-btn-p sk-go" type="submit">Demander un devis</button></form>'
      '<div class="sk-done" hidden tabindex="-1"><h3>Votre demande est prête</h3><p>Choisissez comment l\'envoyer. Rien n\'est transmis tant que vous n\'avez pas validé l\'envoi.</p><pre class="sk-sum"></pre>'
      '<div class="hv-cta"><a class="hv-btn hv-btn-p" data-sms href="sms:">Envoyer par SMS</a><button class="hv-btn hv-btn-s" type="button" data-copy>Copier</button>'
      '<a class="hv-btn hv-btn-s" data-call href="tel:">Appeler</a><a class="hv-btn hv-btn-s" data-mail href="mailto:" hidden>Envoyer par e-mail</a></div>'
      '<button class="sk-back" type="button" data-back>Modifier ma demande</button></div></div>'
      '<aside class="sk-side"><h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:%s">%s</a></li>'
      '<li><span>Commune</span><p>%s (91)</p></li></ul></aside></div></section>') % (TELI, TELI, TELI, TEL, COM)
CT = ('<section class="hero ch">\n  <div class="wrap one">\n    <div><p class="kicker">Contact</p><h1>Parlons de votre projet.</h1>\n'
      '    <p class="lead">Remplissez le formulaire pour obtenir un message prêt à envoyer par SMS, ou appelez-nous directement.</p></div>\n  </div>\n  %s\n</section>\n') % curve('pierre', CH) + K2
page('contact', 'Contact – EIDYL PRO à %s (91)' % COM,
     'Contactez EIDYL PRO à %s (91) : demande de devis en ligne ou appel au %s.' % (COM, TEL), CT,
     extra='<script src="js/k.js" defer></script>\n')
print(sorted(os.listdir(D)), sorted(os.listdir(D + '/images')))
