#!/usr/bin/env python3
# Générateur du site Doms Conciergerie. Usage : python3 gen_doms-conciergerie.py <dossier_sortie> [logo.jpg]
import os, sys
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "doms-conciergerie"
SRC = sys.argv[2] if len(sys.argv) > 2 else "/mnt/user-data/uploads/8bb42f94-image.jpg"
os.makedirs(OUT + "/images", exist_ok=True)

# ---------- logo ----------
im = Image.open(SRC).convert("RGB")
bg = im.getpixel((5, 5))
CREAM = "#%02x%02x%02x" % bg
crop = im.crop((150, 425, 965, 785))
w = 480
h = round(crop.height * w / crop.width)
crop.resize((w, h), Image.LANCZOS).save(OUT + "/images/logo.jpg", quality=80, optimize=True)
ink = (23, 19, 15)
g = crop.convert("L").resize((w, h), Image.LANCZOS)
gb = max(1, im.convert("L").getpixel((5, 5)))
def mk(i):
    return g.point(lambda v: int(bg[i] * (1 - min(v, gb) / gb) + ink[i] * (min(v, gb) / gb)))
Image.merge("RGB", [mk(0), mk(1), mk(2)]).save(OUT + "/images/logo-clair.jpg", quality=80, optimize=True)
key = im.crop((360, 450, 535, 765))
sq = Image.new("RGB", (315, 315), bg)
sq.paste(key, ((315 - 175) // 2, 0))
sq.resize((64, 64), Image.LANCZOS).save(OUT + "/images/favicon.png")
LW, LH = w, h

# ---------- icônes ----------
ICONS = {
 "menage": "M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z",
 "communication": "M4 5h16v11H9l-5 4z M8.5 10.5h7",
 "annonce": "M6 3h9l4 4v14H6z M14 3v5h5 M9 12h7 M9 16h7",
 "livret": "M8 2.5h8a1.5 1.5 0 011.5 1.5v16a1.5 1.5 0 01-1.5 1.5H8A1.5 1.5 0 016.5 20V4A1.5 1.5 0 018 2.5z M10.5 18.5h3 M9.5 7h5 M9.5 10.5h5",
 "blanchisserie": "M5 3h14v18H5z M12 17a4.5 4.5 0 100-9 4.5 4.5 0 000 9z M8 6h.01 M11 6h.01",
 "lancement": "M6 21V4 M6 5h11l-2 3.5 2 3.5H6",
 "deco": "M8 3h8l3 8H5z M12 11v8 M8.5 21h7",
 "consommables": "M3.5 7.5L12 3l8.5 4.5v9L12 21l-8.5-4.5z M3.5 7.5L12 12l8.5-4.5 M12 12v9",
 "reseaux": "M18 8a3 3 0 100-6 3 3 0 000 6z M6 15a3 3 0 100-6 3 3 0 000 6z M18 22a3 3 0 100-6 3 3 0 000 6z M8.6 13.5l6.8 4 M15.4 6.5l-6.8 4",
 "phone": "M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A15 15 0 013 6a2 2 0 012-2z",
 "mail": "M3 5h18v14H3z M3 6l9 7 9-7",
 "pin": "M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z M12 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z",
 "arrow": "M5 12h14 M13 6l6 6-6 6",
 "user": "M12 12a4 4 0 100-8 4 4 0 000 8z M4 21a8 8 0 0116 0",
 "map": "M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z M9 4v14 M15 6v14",
 "copy": "M8 8h12v12H8z M4 16V4h12",
 "send": "M3 11l18-8-8 18-2-8z",
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">' + "".join(
    '<symbol id="i-%s" viewBox="0 0 24 24"><path d="%s"/></symbol>' % (k, v) for k, v in ICONS.items()) + "</svg>"

def ic(n):
    return '<svg class="ic" aria-hidden="true" focusable="false"><use href="#i-%s"/></svg>' % n

# ---------- données ----------
SERVICES = [
 ("menage", "Ménage", "Remise en état complète entre deux séjours.", "Un logement impeccable à chaque arrivée : nettoyage des pièces, remise en place et contrôle avant les voyageurs."),
 ("communication", "Gestion de la communication", "Échanges avec vos voyageurs, avant, pendant et après.", "Nous répondons aux demandes de vos voyageurs et assurons le lien avant, pendant et après le séjour."),
 ("annonce", "Gestion de l'annonce", "Rédaction, mise à jour et suivi de votre annonce.", "Titre, description, règles : nous soignons et maintenons votre annonce pour qu'elle reflète votre logement."),
 ("livret", "Livret d'accueil digital", "Un guide en ligne pour vos voyageurs, avec boutique.", "Un livret consultable sur téléphone, avec les infos du séjour et une boutique d'options pour vos voyageurs."),
 ("blanchisserie", "Gestion de la blanchisserie", "Linge propre, prêt pour chaque arrivée.", "Nous organisons le lavage et la remise en place du linge pour que chaque séjour démarre avec du linge frais."),
 ("lancement", "Lancement Airbnb", "Du projet à la première réservation.", "Nous vous guidons dans la mise en route de votre location : logement, annonce, organisation, premiers voyageurs."),
 ("deco", "Décoration", "Un intérieur chaleureux et cohérent.", "Conseils et mise en place d'une décoration soignée, pensée pour valoriser le logement et séduire les voyageurs."),
 ("consommables", "Gestion des consommables", "Le nécessaire toujours en stock, sans y penser.", "Nous suivons les stocks de produits du quotidien et réapprovisionnons le logement pour qu'il ne manque rien."),
 ("reseaux", "Gestion des réseaux sociaux", "Un logement visible, une marque qui vit en ligne.", "Création et animation de vos publications pour faire connaître votre logement et fidéliser vos voyageurs."),
]
S = {s[0]: s for s in SERVICES}
NAV = [("index.html", "Accueil"), ("presentation.html", "Présentation"), ("services.html", "Services"),
       ("livret-digital.html", "Livret digital"), ("lancement-airbnb.html", "Lancement Airbnb")]
EMAIL = "reseau@doms-conciergerie.fr"
TODO = '<span class="todo">À renseigner</span>'

# ---------- illustrations ----------
HERO_SVG = '''<svg class="hv" viewBox="0 0 480 400" role="img" aria-label="Illustration : une maison, une clé et un livret d'accueil digital">
<circle cx="240" cy="205" r="185" fill="#EBD2BA"/>
<path d="M105 215 L240 105 L375 215 V325 H105 Z" fill="#FFF8F1" stroke="#17130F" stroke-width="6" stroke-linejoin="round"/>
<rect x="212" y="245" width="56" height="80" rx="4" fill="#9A3F1B"/><circle cx="256" cy="288" r="4" fill="#F8E8D9"/>
<rect x="136" y="236" width="48" height="40" rx="4" fill="#EBD2BA" stroke="#17130F" stroke-width="4"/>
<rect x="296" y="236" width="48" height="40" rx="4" fill="#EBD2BA" stroke="#17130F" stroke-width="4"/>
<circle cx="410" cy="80" r="38" fill="#17130F"/><circle cx="410" cy="68" r="9" fill="#EBD2BA"/>
<path d="M402 112h16v100l-8 8-8-8z" fill="#17130F"/>
<rect x="418" y="140" width="16" height="9" fill="#17130F"/><rect x="418" y="160" width="16" height="9" fill="#17130F"/><rect x="418" y="180" width="16" height="9" fill="#17130F"/>
<rect x="30" y="60" width="140" height="96" rx="16" fill="#17130F"/>
<rect x="46" y="80" width="70" height="8" rx="4" fill="#F8E8D9"/><rect x="46" y="100" width="100" height="6" rx="3" fill="#DCCBBB"/><rect x="46" y="114" width="84" height="6" rx="3" fill="#DCCBBB"/>
<circle cx="146" cy="134" r="10" fill="#9A3F1B"/><path d="M141 134l4 4 6-8" fill="none" stroke="#F8E8D9" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''

def phone_svg():
    rows = "".join('<circle cx="64" cy="%d" r="14" fill="#EBD2BA"/><rect x="88" y="%d" width="90" height="8" rx="4" fill="#17130F"/><rect x="88" y="%d" width="64" height="6" rx="3" fill="#A89684"/>' % (y, y - 8, y + 6) for y in (130, 184, 238))
    return '''<svg class="pv" viewBox="0 0 240 400" role="img" aria-label="Illustration d'un livret d'accueil digital sur téléphone">
<rect x="20" y="10" width="200" height="380" rx="32" fill="#F8E8D9"/><rect x="32" y="22" width="176" height="356" rx="22" fill="#FFF8F1"/>
<path d="M32 44a22 22 0 0122-22h132a22 22 0 0122 22v50H32z" fill="#9A3F1B"/><rect x="52" y="48" width="100" height="10" rx="5" fill="#F8E8D9"/><rect x="52" y="68" width="68" height="8" rx="4" fill="#F0B08A"/>
%s<rect x="46" y="278" width="74" height="84" rx="12" fill="#EBD2BA"/><rect x="124" y="278" width="74" height="84" rx="12" fill="#17130F"/>
<circle cx="83" cy="312" r="14" fill="#9A3F1B"/><rect x="58" y="338" width="50" height="8" rx="4" fill="#17130F"/><circle cx="161" cy="312" r="14" fill="#F0B08A"/><rect x="136" y="338" width="50" height="8" rx="4" fill="#F8E8D9"/>
</svg>''' % rows

DECO_KEY = '''<svg class="deco" viewBox="0 0 120 260" aria-hidden="true" focusable="false"><circle cx="60" cy="60" r="50" fill="none" stroke="currentColor" stroke-width="8"/><circle cx="60" cy="48" r="12" fill="currentColor"/><path d="M50 108h20v130l-10 12-10-12z M70 150h22 M70 180h22 M70 210h22" fill="none" stroke="currentColor" stroke-width="8" stroke-linejoin="round"/></svg>'''

# ---------- gabarit ----------
def head(title, desc):
    return ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>%s</title><meta name="description" content="%s"><meta name="robots" content="noindex,nofollow">'
            '<meta name="theme-color" content="%s"><link rel="icon" href="images/favicon.png" type="image/png">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&amp;family=DM+Sans:wght@400;500;700&amp;display=swap">'
            '<link rel="stylesheet" href="style.css"></head>\n') % (title, desc, CREAM)

def header(cur):
    lis = "".join('<li><a href="%s"%s>%s</a></li>' % (u, ' aria-current="page"' if u == cur else "", t) for u, t in NAV)
    return ('<a class="skip" href="#contenu">Aller au contenu</a>\n<header class="site"><div class="wrap hbar">'
            '<a class="logo" href="index.html" aria-label="Doms Conciergerie, accueil"><img src="images/logo.jpg" width="%d" height="%d" alt="Doms Conciergerie"></a>'
            '<nav class="main" id="menu" aria-label="Navigation principale"><ul>%s<li class="m-only"><a class="btn btn-p" href="contact.html#devis">Demander un devis</a></li></ul></nav>'
            '<a class="btn btn-p hcta" href="contact.html#devis">Demander un devis</a>'
            '<button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>'
            '</div></header>\n') % (LW, LH, lis)

FOOTER = ('<footer class="site"><div class="wrap fgrid"><a class="flogo" href="index.html" aria-label="Doms Conciergerie, accueil"><img src="images/logo-clair.jpg" width="%d" height="%d" alt="Doms Conciergerie" loading="lazy"></a>'
          '<nav aria-label="Pied de page"><ul><li><a href="services.html">Services</a></li><li><a href="livret-digital.html">Livret digital</a></li><li><a href="contact.html">Contact</a></li><li><a href="mentions-legales.html">Mentions légales</a></li></ul></nav>'
          '<p class="fmail">%s</p><p class="fcopy">© 2026 Doms Conciergerie · SIREN 105155444</p></div></footer>\n') % (LW, LH, EMAIL)

def page(fname, title, desc, body, cur=None):
    html = head(title, desc) + "<body>\n" + SPRITE + "\n" + header(cur or fname) + '<main id="contenu">\n' + body + "\n</main>\n" + FOOTER + '<script src="script.js"></script>\n</body></html>\n'
    open(os.path.join(OUT, fname), "w", encoding="utf-8").write(html)

def phero(eyebrow, h1, p):
    return '<section class="phero"><div class="wrap"><p class="eyebrow">%s</p><h1>%s</h1><p class="lead">%s</p></div>%s</section>' % (eyebrow, h1, p, DECO_KEY)

def card(key, full=False, compact=False):
    _, t, short, long = S[key]
    return '<article class="sc%s reveal"><span class="ico">%s</span><h3>%s</h3><p>%s</p></article>' % (" compact" if compact else "", ic(key), t, long if full else short)

def cta(title, p):
    return ('<section class="dark acc"><div class="wrap cta"><h2>%s</h2><p>%s</p><div class="btns"><a class="btn btn-p" href="contact.html#devis">Demander un devis</a>'
            '<a class="btn btn-s" href="contact.html#coordonnees">Être rappelé</a></div></div></section>') % (title, p)

def steps(items, cls=""):
    return '<ol class="steps %s">%s</ol>' % (cls, "".join('<li class="reveal"><span class="num">%d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, p) for i, (t, p) in enumerate(items)))

# ---------- accueil ----------
home = '''<section class="hero"><div class="wrap hgrid"><div>
<p class="eyebrow">Conciergerie de locations courte durée</p>
<h1>Votre location, entre de bonnes mains.</h1>
<p class="lead">Ménage, communication, annonce, linge, livret d'accueil digital : Doms Conciergerie s'occupe de tout, pour que vous profitiez de votre logement sans les contraintes.</p>
<div class="btns"><a class="btn btn-p" href="contact.html#devis">Demander un devis</a><a class="btn btn-s" href="contact.html#coordonnees">Être rappelé</a></div>
</div><div class="hvis">%s</div></div></section>

<section class="dark" id="services"><div class="wrap"><p class="eyebrow">Nos services</p><h2>Neuf services, un seul interlocuteur.</h2>
<div class="sgrid">%s</div><p class="more"><a class="btn btn-p" href="services.html">Voir le détail des services</a></p></div></section>

<section class="ivory"><div class="wrap two"><div><p class="eyebrow">Nos engagements</p><h2>Une gestion attentive, du premier message au départ des voyageurs.</h2>
<p>Votre logement est votre bien le plus précieux. Nous le traitons avec le même soin que s'il était le nôtre, avec une organisation simple et des échanges transparents.</p></div>
<ul class="eng">
<li class="reveal"><span class="n">01</span><div><h3>Un interlocuteur unique</h3><p>Un seul point de contact pour toute la gestion de votre logement.</p></div></li>
<li class="reveal"><span class="n">02</span><div><h3>Un logement toujours prêt</h3><p>Propreté, linge, consommables : rien n'est laissé au hasard.</p></div></li>
<li class="reveal"><span class="n">03</span><div><h3>Une communication claire</h3><p>Des échanges simples, avec vous comme avec vos voyageurs.</p></div></li></ul></div></section>

<section class="sand"><div class="wrap"><p class="eyebrow">Notre méthode</p><h2>Quatre étapes pour vous décharger.</h2>%s</div></section>

<section class="dark"><div class="wrap two livret"><div><p class="eyebrow">Livret d'accueil digital</p><h2>Un livret d'accueil qui tient dans la poche de vos voyageurs.</h2>
<p>Accès, équipements, conseils du quartier et boutique d'options : tout est réuni dans un livret en ligne, simple à consulter depuis un téléphone.</p>
<p class="more"><a class="btn btn-p" href="livret-digital.html">Découvrir le livret</a></p></div><div class="pvis">%s</div></div></section>

%s''' % (HERO_SVG, "".join(card(k[0], compact=True) for k in SERVICES),
         steps([("Échange", "Nous faisons connaissance avec vous et votre logement."), ("Mise en place", "Nous définissons ensemble les services utiles."),
                ("Gestion au quotidien", "Nous prenons le relais, jour après jour."), ("Suivi", "Nous restons à votre écoute pour ajuster.")]),
         phone_svg(), cta("Parlons de votre logement.", "Décrivez-nous votre projet : nous vous répondons avec une proposition adaptée."))
page("index.html", "Doms Conciergerie | Conciergerie pour locations courte durée",
     "Doms Conciergerie gère votre location courte durée : ménage, linge, annonce, communication, livret d'accueil digital, décoration et réseaux sociaux.", home)

# ---------- présentation ----------
pres = phero("Présentation", "Une conciergerie pensée pour les hôtes.", "Doms Conciergerie accompagne les propriétaires et investisseurs qui souhaitent proposer un logement accueillant, sans en porter seuls la charge.") + '''
<section class="ivory"><div class="wrap two"><div><p class="eyebrow">Notre approche</p><h2>Votre logement mérite autant d'attention que vos voyageurs.</h2></div>
<div><p>Louer en courte durée demande de la disponibilité, de la rigueur et le sens du détail. Doms Conciergerie prend en charge ces tâches du quotidien : l'accueil, la propreté, le linge, les échanges et la visibilité de votre annonce.</p>
<p>Chaque logement est différent. Nous construisons avec vous une organisation sur mesure, en retenant uniquement les services dont vous avez besoin.</p></div></div></section>
<section class="dark"><div class="wrap"><p class="eyebrow">Nos valeurs</p><h2>Ce qui guide notre travail.</h2><div class="g4">
<article class="sc reveal"><span class="ico">%s</span><h3>Fiabilité</h3><p>Une organisation rigoureuse, pour un logement prêt à chaque arrivée.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Soin du détail</h3><p>Des finitions qui font la différence dans l'avis des voyageurs.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Transparence</h3><p>Des échanges clairs et un suivi régulier avec le propriétaire.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Simplicité</h3><p>Un interlocuteur unique pour tout ce qui touche à votre logement.</p></article></div></div></section>
<section class="sand"><div class="wrap"><p class="eyebrow">Ce que nous prenons en charge</p><h2>Trois domaines d'intervention.</h2><div class="g3">
<article class="sc reveal"><span class="ico">%s</span><h3>Le logement</h3><p>Ménage, linge et consommables.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Les voyageurs</h3><p>Annonce, communication et livret d'accueil.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Le lancement et la visibilité</h3><p>Accompagnement, décoration et réseaux sociaux.</p></article></div>
<p class="more"><a class="btn btn-p" href="services.html">Voir tous les services</a></p></div></section>
''' % (ic("lancement"), ic("deco"), ic("communication"), ic("user"), ic("menage"), ic("livret"), ic("reseaux")) + cta("Un projet de location ?", "Parlons-en : nous définirons ensemble les services qui vous conviennent.")
page("presentation.html", "Présentation | Doms Conciergerie", "Découvrez Doms Conciergerie, conciergerie pour locations courte durée : notre approche, nos valeurs et nos domaines d'intervention.", pres)

# ---------- services ----------
def cat(cls, eb, h2, keys):
    return '<section class="%s"><div class="wrap"><p class="eyebrow">%s</p><h2>%s</h2><div class="g3">%s</div></div></section>' % (cls, eb, h2, "".join(card(k, full=True) for k in keys))
serv = (phero("Nos services", "Tout ce qu'il faut pour une location sereine.", "Choisissez les services dont vous avez besoin, ou confiez-nous l'ensemble de la gestion.")
        + cat("ivory", "Le logement", "Un logement impeccable.", ["menage", "blanchisserie", "consommables"])
        + cat("dark", "Les voyageurs", "Des voyageurs bien accueillis.", ["communication", "annonce", "livret"])
        + cat("sand", "Lancement et visibilité", "Se lancer, se faire remarquer.", ["lancement", "deco", "reseaux"])
        + cta("Quels services pour votre logement ?", "Dites-nous ce dont vous avez besoin, nous vous proposons une offre adaptée."))
page("services.html", "Services | Doms Conciergerie", "Ménage, blanchisserie, consommables, communication, annonce, livret d'accueil digital, lancement Airbnb, décoration et réseaux sociaux.", serv)

# ---------- livret digital ----------
items = [("Arrivée et accès", "Instructions pour entrer simplement dans le logement."), ("Wifi et équipements", "Mode d'emploi des équipements du logement."),
         ("Règles de la maison", "Les consignes essentielles, présentées clairement."), ("Guide du quartier", "Vos adresses et conseils pour découvrir les alentours."),
         ("Contacts utiles", "Les bons numéros, au bon moment."), ("Boutique", "Des options à proposer à vos voyageurs.")]
liv = (phero("Livret d'accueil digital", "Un livret d'accueil simple, beau et toujours à jour.", "Un guide en ligne, consultable depuis le téléphone de vos voyageurs, avec une boutique intégrée.") + '''
<section class="ivory"><div class="wrap"><p class="eyebrow">Ce que contient le livret</p><h2>Les informations utiles, au même endroit.</h2><ul class="items">%s</ul></div></section>
<section class="dark"><div class="wrap two livret"><div><p class="eyebrow">La boutique</p><h2>Proposez des options à vos voyageurs.</h2>
<p>La boutique intégrée au livret permet de présenter des services ou produits complémentaires, selon l'offre que nous définissons ensemble.</p>
<p>Le contenu du livret est personnalisé pour votre logement : nous le rédigeons avec vous et le mettons à jour au fil du temps.</p></div><div class="pvis">%s</div></div></section>
''' % ("".join('<li class="reveal"><span class="n">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, p) for i, (t, p) in enumerate(items)), phone_svg())
       + cta("Un livret pour votre logement ?", "Demandez un devis : nous vous présentons le livret et ses options."))
page("livret-digital.html", "Livret d'accueil digital | Doms Conciergerie", "Un livret d'accueil digital avec boutique intégrée pour vos voyageurs : accès, équipements, règles, guide du quartier et options.", liv)

# ---------- lancement ----------
lan = (phero("Lancement Airbnb", "Du projet à la première réservation.", "Doms Conciergerie vous accompagne dans le lancement de votre location, étape par étape.") + '''
<section class="ivory"><div class="wrap"><p class="eyebrow">Les étapes</p><h2>Un lancement organisé, sans stress.</h2>%s</div></section>
<section class="dark"><div class="wrap"><p class="eyebrow">Ce que vous gagnez</p><h2>Un démarrage plus serein.</h2><div class="g3">
<article class="sc reveal"><span class="ico">%s</span><h3>Du temps</h3><p>Nous gérons les démarches pratiques à votre place.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Une annonce soignée</h3><p>Un logement présenté fidèlement et de façon attractive.</p></article>
<article class="sc reveal"><span class="ico">%s</span><h3>Un relais durable</h3><p>Une fois lancé, nous pouvons assurer la gestion au quotidien.</p></article></div></div></section>
''' % (steps([("Cadrage du projet", "Nous échangeons sur votre logement et vos objectifs."), ("Préparation du logement", "Équipements, linge et décoration, pour accueillir dans de bonnes conditions."),
              ("Création de l'annonce", "Rédaction et mise en forme de votre annonce Airbnb."), ("Organisation", "Ménage, linge, consommables et livret d'accueil digital."),
              ("Mise en ligne", "Publication de l'annonce et suivi des premières réservations.")], "s5"), ic("lancement"), ic("annonce"), ic("user"))
       + cta("Prêt à vous lancer ?", "Parlons de votre projet : nous vous répondons avec une proposition claire."))
page("lancement-airbnb.html", "Lancement Airbnb | Doms Conciergerie", "Doms Conciergerie vous accompagne dans le lancement de votre location Airbnb, de la préparation du logement aux premières réservations.", lan)

# ---------- contact ----------
opts = "".join("<option>%s</option>" % s[1] for s in SERVICES)
contact = phero("Contact", "Parlons de votre logement.", "Remplissez ce formulaire : il prépare votre message, que vous pourrez envoyer ou copier en un geste.") + '''
<section class="ivory" id="devis"><div class="wrap"><div class="fcard">
<h2>Demander un devis</h2>
<!-- À COMPLÉTER PAR LE PROPRIÉTAIRE DU SITE :
     data-email="adresse@exemple.fr"  -> affiche le bouton « Envoyer par e-mail » (mailto:)
     data-sms="0600000000"            -> affiche le bouton « Envoyer par SMS » (sms:)
     data-tel="0600000000"            -> affiche le bouton « Appeler » (tel:)
     Tant qu'un attribut est vide, le bouton correspondant reste masqué. Rien n'est transmis automatiquement. -->
<form id="form-devis" novalidate data-email="" data-sms="" data-tel="">
<div class="field"><label for="nom">Nom et prénom <span class="req" aria-hidden="true">*</span></label><div class="inp">%s<input id="nom" name="nom" type="text" autocomplete="name" required aria-required="true" aria-describedby="e-nom"></div><p class="err" id="e-nom"></p></div>
<div class="field"><label for="tel">Téléphone</label><div class="inp">%s<input id="tel" name="tel" type="tel" autocomplete="tel" inputmode="tel" aria-describedby="e-tel"></div><p class="err" id="e-tel"></p></div>
<div class="field"><label for="mail">E-mail <span class="req" aria-hidden="true">*</span></label><div class="inp">%s<input id="mail" name="mail" type="email" autocomplete="email" required aria-required="true" aria-describedby="e-mail"></div><p class="err" id="e-mail"></p></div>
<div class="field"><label for="srv">Service souhaité</label><div class="inp">%s<select id="srv" name="srv"><option>Plusieurs services / je ne sais pas encore</option>%s</select></div></div>
<div class="field full"><label for="msg">Votre message <span class="req" aria-hidden="true">*</span></label><textarea id="msg" name="msg" rows="4" required aria-required="true" aria-describedby="e-msg" placeholder="Décrivez votre logement et vos besoins"></textarea><p class="err" id="e-msg"></p></div>
<p class="note full">Les champs marqués d'un astérisque (*) sont obligatoires.</p>
<div class="full"><button class="btn btn-p" type="submit">%s Préparer mon message</button></div>
</form>
<div id="resultat" class="result" hidden><h3>Votre message est prêt</h3><textarea id="texte" readonly rows="6" aria-label="Message préparé"></textarea>
<div class="btns"><button class="btn btn-p" type="button" id="copier">%s Copier</button><a class="btn btn-s" id="b-mail" href="#" hidden>%s Envoyer par e-mail</a><a class="btn btn-s" id="b-sms" href="#" hidden>%s Envoyer par SMS</a><a class="btn btn-s" id="b-tel" href="#" hidden>%s Appeler</a></div>
<p class="note" id="etat" role="status"></p></div>
</div></div></section>
<section class="dark" id="coordonnees"><div class="wrap"><p class="eyebrow">Coordonnées</p><h2>Nous joindre.</h2><div class="g3">
<article class="sc"><span class="ico">%s</span><h3>Téléphone</h3><p>Coordonnées à renseigner</p></article>
<article class="sc"><span class="ico">%s</span><h3>E-mail</h3><p>%s</p></article>
<article class="sc"><span class="ico">%s</span><h3>Adresse</h3><p>Coordonnées à renseigner</p></article></div>
<div class="plan"><span class="ico">%s</span><p>Plan à ajouter</p></div></div></section>
''' % (ic("user"), ic("phone"), ic("mail"), ic("deco"), opts, ic("send"), ic("copy"), ic("mail"), ic("communication"), ic("phone"),
       ic("phone"), ic("mail"), EMAIL, ic("pin"), ic("map"))
page("contact.html", "Contact et devis | Doms Conciergerie", "Contactez Doms Conciergerie pour un devis : formulaire de demande, e-mail et coordonnées.", contact)

# ---------- mentions légales ----------
ment = phero("Informations légales", "Mentions légales", "Informations relatives à l'éditeur de ce site.") + '''
<section class="ivory"><div class="wrap narrow"><h2>Éditeur du site</h2><dl class="dl">
<div><dt>Nom</dt><dd>Doms Conciergerie</dd></div><div><dt>Forme juridique</dt><dd>%s</dd></div><div><dt>Siège social</dt><dd>%s</dd></div>
<div><dt>SIREN</dt><dd>105155444</dd></div><div><dt>Directeur de la publication</dt><dd>%s</dd></div><div><dt>E-mail</dt><dd>%s</dd></div><div><dt>Hébergeur</dt><dd>%s</dd></div></dl></div></section>
<section class="sand"><div class="wrap narrow"><h2>Données et propriété</h2>
<p>Ce site ne collecte aucune donnée automatiquement : le formulaire de contact prépare un message que vous choisissez d'envoyer ou de copier.</p>
<p>L'ensemble des contenus du site (textes, visuels, logo) est la propriété de Doms Conciergerie. Toute reproduction sans autorisation est interdite.</p></div></section>
''' % (TODO, TODO, TODO, EMAIL, TODO)
page("mentions-legales.html", "Mentions légales | Doms Conciergerie", "Mentions légales du site de Doms Conciergerie.", ment)

# ---------- CSS ----------
CSS = r'''
:root{--cream:__CREAM__;--ivory:#FFF8F1;--sand:#EBD2BA;--ink:#17130F;--acc:#9A3F1B;--accl:#F0B08A;--mut:#5A4A3E;--mutd:#DCCBBB}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:84px}
body{margin:0;font:400 1rem/1.6 "DM Sans",system-ui,sans-serif;color:var(--ink);background:var(--cream);overflow-x:hidden}
img,svg{max-width:100%}img{height:auto}
h1,h2,h3{font-family:Unbounded,"DM Sans",sans-serif;font-weight:600;line-height:1.18;margin:0 0 .6em;letter-spacing:-.01em}
h1{font-size:clamp(1.7rem,5.2vw,3.1rem)}h2{font-size:clamp(1.35rem,3.4vw,2.05rem)}h3{font-size:1.05rem;font-family:"DM Sans",sans-serif;font-weight:700;margin:0 0 4px}
p{margin:0 0 .9em}.wrap{width:min(1180px,100% - 40px);margin-inline:auto}.narrow{max-width:760px}
section{padding:40px 0}.ivory{background:var(--ivory)}.sand{background:var(--sand)}
.dark{background:var(--ink);color:var(--cream)}.dark p{color:var(--mutd)}
.eyebrow{display:flex;align-items:center;gap:10px;font-weight:700;font-size:1rem;letter-spacing:.08em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}
.eyebrow::before{content:"";width:28px;height:2px;background:currentColor}.dark .eyebrow{color:var(--accl)}
.lead{font-size:1.125rem;color:var(--mut);max-width:60ch}.todo{color:var(--mut);font-style:italic}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 24px;border-radius:999px;font:700 1rem "DM Sans",sans-serif;text-decoration:none;border:2px solid transparent;cursor:pointer;transition:background .2s,color .2s,transform .2s}
.btn:hover{transform:translateY(-2px)}.btn-p{background:var(--ink);color:var(--cream)}.btn-p:hover{background:var(--acc)}
.btn-s{border-color:var(--ink);color:var(--ink);background:transparent}.btn-s:hover{background:var(--ink);color:var(--cream)}
.dark .btn-p{background:var(--cream);color:var(--ink)}.dark .btn-p:hover{background:var(--accl)}.dark .btn-s{border-color:var(--cream);color:var(--cream)}.dark .btn-s:hover{background:var(--cream);color:var(--ink)}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}.more{margin:20px 0 0}
:focus-visible{outline:3px solid var(--acc);outline-offset:3px}.dark :focus-visible{outline-color:var(--accl)}
.ic{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;flex:none}
.skip{position:absolute;left:12px;top:-60px;z-index:100;background:var(--ink);color:var(--cream);padding:0 18px;min-height:44px;display:flex;align-items:center;border-radius:8px}.skip:focus{top:8px}
/* en-tête */
header.site{background:var(--cream);position:sticky;top:0;z-index:50;border-bottom:1px solid rgba(23,19,15,.12)}
.hbar{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:76px}
.logo{display:inline-flex;min-height:44px;align-items:center}.logo img{height:60px;width:auto;display:block}
nav.main ul{list-style:none;display:flex;gap:2px;margin:0;padding:0}
nav.main a:not(.btn){display:flex;align-items:center;min-height:44px;padding:0 12px;text-decoration:none;font-weight:500;color:var(--ink);border-radius:999px}
nav.main a:not(.btn):hover{background:var(--sand)}nav.main a[aria-current=page]{font-weight:700;color:var(--acc)}
.burger{display:none;width:48px;height:48px;border:2px solid var(--ink);border-radius:12px;background:transparent;cursor:pointer;padding:0;flex-direction:column;align-items:center;justify-content:center;gap:5px}
.burger span{display:block;width:22px;height:2px;background:var(--ink);transition:transform .2s,opacity .2s}
.burger[aria-expanded=true] span:nth-child(1){transform:translateY(7px) rotate(45deg)}.burger[aria-expanded=true] span:nth-child(2){opacity:0}.burger[aria-expanded=true] span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
@media(min-width:981px){.m-only{display:none}}
@media(max-width:980px){.burger{display:flex}.hcta{display:none}
 nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:var(--cream);padding:8px 20px 20px;border-bottom:1px solid rgba(23,19,15,.12);box-shadow:0 12px 24px rgba(23,19,15,.12)}
 nav.main.open{display:block}nav.main ul{flex-direction:column;gap:0}nav.main a:not(.btn){padding:0 4px;border-radius:0}.m-only{margin-top:10px}.m-only .btn{width:100%}}
/* accueil */
.hero{padding:28px 0 40px}.hgrid{display:grid;gap:28px;align-items:center}.hvis{display:flex;justify-content:center}.hv{width:100%;max-width:440px;height:auto}
@media(min-width:900px){.hgrid{grid-template-columns:1.1fr .9fr;gap:48px}.hero{padding:48px 0 56px}}
.sgrid{display:grid;gap:10px;margin-top:20px}@media(min-width:640px){.sgrid{grid-template-columns:1fr 1fr}}@media(min-width:1000px){.sgrid{grid-template-columns:repeat(3,1fr)}}
.g3,.g4{display:grid;gap:12px;margin-top:20px}@media(min-width:820px){.g3{grid-template-columns:repeat(3,1fr)}.g4{grid-template-columns:repeat(4,1fr)}}@media(min-width:560px) and (max-width:819px){.g4{grid-template-columns:1fr 1fr}}
.sc{display:grid;grid-template-columns:44px 1fr;column-gap:14px;align-items:start;padding:16px;border-radius:18px;background:var(--cream);border:1px solid rgba(23,19,15,.14)}
.sand .sc{background:var(--ivory)}
.dark .sc{background:rgba(248,232,217,.05);border-color:rgba(248,232,217,.2)}
.sc .ico{grid-row:1/3;width:44px;height:44px;border-radius:12px;background:var(--acc);color:var(--cream);display:grid;place-items:center}
.sc h3{margin:0 0 2px;align-self:center}.sc p{margin:0;grid-column:2}
.sc.compact{padding:10px 14px;align-items:center}.sc.compact .ico{grid-row:1/3}.sc.compact p{display:none}.sc.compact h3{grid-row:1/3;margin:0}
@media(min-width:640px){.sc.compact{padding:16px;align-items:start}.sc.compact p{display:block}.sc.compact h3{grid-row:auto;margin:0 0 2px}}
.two{display:grid;gap:24px;align-items:center}@media(min-width:900px){.two{grid-template-columns:1fr 1fr;gap:56px}}
.eng,.items{list-style:none;margin:0;padding:0;display:grid;gap:10px}.eng li,.items li{display:grid;grid-template-columns:48px 1fr;gap:12px;align-items:start;padding:14px 16px;background:var(--cream);border-radius:16px;border:1px solid rgba(23,19,15,.12)}
.n{font:600 1.1rem Unbounded,sans-serif;color:var(--acc)}.eng p,.items p{margin:0}
.items{margin-top:20px}@media(min-width:760px){.items{grid-template-columns:1fr 1fr}}@media(min-width:1080px){.items{grid-template-columns:repeat(3,1fr)}}
.steps{list-style:none;margin:20px 0 0;padding:0;display:grid;gap:10px}
.steps li{display:grid;grid-template-columns:44px 1fr;gap:14px;align-items:start;padding:14px 16px;background:var(--ivory);border-radius:16px}.sand .steps li{background:var(--ivory)}.ivory .steps li{background:var(--cream)}
.steps p{margin:0}.num{width:44px;height:44px;border-radius:50%;background:var(--ink);color:var(--cream);display:grid;place-items:center;font:600 1rem Unbounded,sans-serif}
@media(min-width:900px){.steps{grid-template-columns:repeat(4,1fr);gap:16px}.steps.s5{grid-template-columns:repeat(5,1fr)}.steps li{grid-template-columns:1fr;padding:20px}}
.livret .pvis{display:flex;justify-content:center}.pv{width:100%;max-width:210px;height:auto}
@media(max-width:899px){.pv{max-width:170px}}
.cta{text-align:center;max-width:720px}.cta .btns{justify-content:center}.dark.acc{background:var(--acc)}.dark.acc p{color:var(--cream)}.dark.acc .btn-p:hover{background:var(--sand)}
/* pages internes */
.phero{position:relative;overflow:hidden;padding:36px 0 32px}.phero .wrap{position:relative;z-index:1}
.deco{position:absolute;right:4%;top:14px;height:240px;width:auto;color:var(--acc);opacity:.14}@media(max-width:700px){.deco{height:170px;right:-10px;opacity:.1}}
/* formulaire */
.fcard{max-width:820px;margin-inline:auto;background:var(--cream);border:1px solid rgba(23,19,15,.14);border-radius:24px;padding:24px 20px}
form{display:grid;gap:14px}@media(min-width:700px){form{grid-template-columns:1fr 1fr}.fcard{padding:32px}.full{grid-column:1/-1}}
.field label{display:block;font-weight:700;margin-bottom:6px}.req{color:var(--acc)}
.inp{position:relative}.inp .ic{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--acc);pointer-events:none}
input,select,textarea{width:100%;min-height:48px;padding:10px 14px;font:400 1rem "DM Sans",sans-serif;color:var(--ink);background:var(--ivory);border:2px solid rgba(23,19,15,.35);border-radius:12px}
.inp input,.inp select{padding-left:48px}textarea{resize:vertical;min-height:110px}
input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid var(--acc);outline-offset:2px;border-color:var(--ink)}
.field.bad input,.field.bad textarea{border-color:#a11d1d}.err{color:#a11d1d;font-weight:500;margin:6px 0 0}.err:empty{display:none}
.note{color:var(--mut);margin:0}.result{margin-top:20px;padding-top:20px;border-top:2px dashed rgba(23,19,15,.25)}.result[hidden],[hidden]{display:none!important}
.plan{margin-top:12px;display:flex;align-items:center;gap:14px;padding:16px;border:2px dashed rgba(248,232,217,.35);border-radius:18px}.plan p{margin:0}.plan .ico{width:44px;height:44px;border-radius:12px;background:var(--acc);color:var(--cream);display:grid;place-items:center}
.dl{margin:16px 0 0;display:grid;gap:8px}.dl div{display:grid;gap:2px;padding:12px 16px;background:var(--cream);border-radius:14px}.dl dt{font-weight:700;color:var(--mut)}.dl dd{margin:0}
@media(min-width:640px){.dl div{grid-template-columns:240px 1fr;gap:16px}}
/* pied de page */
footer.site{background:var(--ink);color:var(--mutd);padding:20px 0}.fgrid{display:grid;gap:4px;align-items:center}
.fgrid .flogo,.fmail{display:none}.fgrid ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:0 6px}
.fgrid a{display:inline-flex;align-items:center;min-height:44px;padding:0 10px;color:var(--cream);text-decoration:none;font-weight:500}.fgrid a:hover{color:var(--accl)}.fgrid li:first-child a{padding-left:0}
.fcopy{margin:0;color:var(--mutd)}footer :focus-visible{outline-color:var(--accl)}
@media(min-width:821px){.fgrid{grid-template-columns:auto 1fr auto;gap:8px 32px}.fgrid .flogo{display:inline-flex;min-height:44px;align-items:center}.flogo img{height:56px;width:auto}.fmail{display:block;margin:0;color:var(--cream)}.fcopy{grid-column:1/-1;font-size:1rem;padding-top:8px;border-top:1px solid rgba(248,232,217,.18)}.fgrid ul{justify-content:center}}
/* animations */
.js .reveal{opacity:0;transform:translateY(14px);transition:opacity .5s ease,transform .5s ease}.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}.js .reveal{opacity:1;transform:none}}
'''.replace("__CREAM__", CREAM)
open(OUT + "/style.css", "w", encoding="utf-8").write(CSS)

# ---------- JS ----------
JS = r'''(function(){
var d=document,r=d.documentElement;r.classList.add('js');
var b=d.querySelector('.burger'),m=d.getElementById('menu');
function setMenu(o){m.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');}
b.addEventListener('click',function(){setMenu(b.getAttribute('aria-expanded')!=='true');});
d.addEventListener('keydown',function(e){if(e.key==='Escape'){setMenu(false);}});
m.addEventListener('click',function(e){if(e.target.closest('a')){setMenu(false);}});
var els=d.querySelectorAll('.reveal');
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target);}});},{threshold:.05});els.forEach(function(e){io.observe(e);});}
else{els.forEach(function(e){e.classList.add('in');});}
var f=d.getElementById('form-devis');if(!f)return;
var RE=/^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.\-]*\d{2}){4}$/,RM=/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
function err(id,msg){var p=d.getElementById('e-'+id),i=d.getElementById(id);p.textContent=msg;i.closest('.field').classList.toggle('bad',!!msg);if(msg){i.setAttribute('aria-invalid','true');}else{i.removeAttribute('aria-invalid');}return !msg;}
function val(){var ok=true,v=function(i){return f.elements[i].value.trim();};
ok=err('nom',v('nom')?'':'Indiquez votre nom.')&&ok;
ok=err('tel',(!v('tel')||RE.test(v('tel')))?'':'Numéro invalide (ex. 06 12 34 56 78).')&&ok;
ok=err('mail',RM.test(v('mail'))?'':'Indiquez une adresse e-mail valide.')&&ok;
ok=err('msg',v('msg')?'':'Écrivez votre message.')&&ok;return ok;}
f.addEventListener('submit',function(e){e.preventDefault();if(!val()){var bad=f.querySelector('[aria-invalid]');if(bad)bad.focus();return;}
var v=function(i){return f.elements[i].value.trim();};
var t='Bonjour,\n\nJe souhaite un devis : '+f.elements.srv.value+'.\n\n'+v('msg')+'\n\nNom : '+v('nom')+'\nE-mail : '+v('mail')+(v('tel')?'\nTéléphone : '+v('tel'):'')+'\n\nMerci.';
d.getElementById('texte').value=t;d.getElementById('resultat').hidden=false;d.getElementById('etat').textContent='';
var em=f.dataset.email,sm=f.dataset.sms,tl=f.dataset.tel,be=d.getElementById('b-mail'),bs=d.getElementById('b-sms'),bt=d.getElementById('b-tel');
be.hidden=!em;if(em){be.href='mailto:'+em+'?subject='+encodeURIComponent('Demande de devis')+'&body='+encodeURIComponent(t);}
bs.hidden=!sm;if(sm){bs.href='sms:'+sm.replace(/\s/g,'')+'?body='+encodeURIComponent(t);}
bt.hidden=!tl;if(tl){bt.href='tel:'+tl.replace(/\s/g,'');}
d.getElementById('resultat').scrollIntoView({behavior:'smooth',block:'nearest'});});
['nom','tel','mail','msg'].forEach(function(i){f.elements[i].addEventListener('input',function(){if(d.getElementById('e-'+i).textContent)val();});});
d.getElementById('copier').addEventListener('click',function(){var ta=d.getElementById('texte'),s=d.getElementById('etat');
function ok(){s.textContent='Message copié.';}function ko(){ta.select();try{d.execCommand('copy');ok();}catch(x){s.textContent='Sélectionnez le texte puis copiez-le.';}}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(ta.value).then(ok,ko);}else{ko();}});
})();
'''
open(OUT + "/script.js", "w", encoding="utf-8").write(JS)

open(OUT + "/README.md", "w", encoding="utf-8").write(
    "# Doms Conciergerie\n\nMaquette du site vitrine de Doms Conciergerie (maquette).\n\nPages : index, presentation, services, livret-digital, lancement-airbnb, contact, mentions-legales.\n\nGénéré par `outils/gen_doms-conciergerie.py`.\n")
print(len([f for f in os.listdir(OUT) if f.endswith(".html")]), "pages")
