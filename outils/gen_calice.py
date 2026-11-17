import re,os
B='/home/claude/build/'; M=B+'mods/'; D='/home/claude/maquettes/calice-espaces-verts/'
rd=lambda p:open(p,encoding='utf8').read()
N='CALICE ESPACES VERTS'; T1='06 95 03 38 73'; U1='+33695033873'; T2='01 49 10 05 05'; U2='+33149100505'
URL='https://webaunet.github.io/maquettes/calice-espaces-verts/'
orig=rd(B+'s08/index.html')
hdr=re.search(r'<header class="top">.*?</header>',orig,re.S).group(0)
PH=re.search(r'<svg viewBox="0 0 24 24".*?</svg>',re.search(r'<a class="btn btn-apricot call".*?</a>',hdr,re.S).group(0),re.S).group(0)
PAGES=[('index.html','Accueil'),('prestations.html','Prestations'),('a-propos.html','À propos'),('contact.html','Contact')]
def header(cur):
    h=hdr
    h=re.sub(r'<a class="logo".*?</a>','<a class="logo" href="%s" aria-label="%s, accueil"><img src="images/logo.png" width="105" height="52" alt="%s"></a>'%(URL,N,N),h,count=1,flags=re.S)
    nav=lambda c,a:'<nav class="%s" %s>%s</nav>'%(c,a,''.join('<a href="%s"%s>%s</a>'%(u,' aria-current="page"' if u==cur else '',t) for u,t in PAGES))
    h=re.sub(r'<nav class="nav".*?</nav>',nav('nav','aria-label="Navigation principale"'),h,flags=re.S)
    h=re.sub(r'<nav class="menu".*?</nav>',nav('menu','id="menu" aria-label="Menu mobile"'),h,flags=re.S)
    h=h.replace('+33683648818',U1).replace('06 83 64 88 18',T1)
    return h
def head(title,desc):
    return '''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="images/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
'''%(title,desc)
def footer():
    f=rd(M+'F1.html')
    f=f.replace("<strong>Nom de l'entreprise</strong>",'<a class="hf-logo" href="index.html"><img src="images/logo.png" width="97" height="48" alt="%s"></a>'%N)
    f=f.replace("Une phrase de présentation.","Élagage, abattage, création et entretien d'espaces verts à Viry-Châtillon (91).")
    f=re.sub(r'<div class="hf-c">.*?</div>','<div class="hf-c"><a href="tel:%s">%s</a><a href="tel:%s">%s</a></div>'%(U1,T1,U2,T2),f,flags=re.S)
    f=f.replace("© Nom de l'entreprise","© %s · Viry-Châtillon (91)"%N)
    return f
def page(cur,title,desc,main,extra=''):
    return head(title,desc)+header(cur)+'\n<main id="contenu">\n'+main+'\n</main>\n'+footer()+'\n<script src="js/main.js"></script>\n'+extra+'</body>\n</html>\n'
def img(src,w,h,alt,lazy=True,cls=''):
    from PIL import Image
    w,h=Image.open(D+'images/'+src).size
    return '<img src="images/%s" width="%d" height="%d" alt="%s"%s%s>'%(src,w,h,alt,' loading="lazy"' if lazy else ' fetchpriority="high"',' class="%s"'%cls if cls else '')
LINE=lambda u,t:'<a class="line" href="tel:%s">%s%s</a>'%(u,PH,t)
def cta_band(eb,h2,p,btn_txt='Écrire un message'):
    return '''<section class="band band-leaf" id="contact-final"><div class="wrap cta-band"><div><span class="eyebrow">%s</span><h2 style="margin-top:14px">%s</h2><p>%s</p><div class="cta" style="margin-top:28px"><a class="btn btn-apricot" href="contact.html">%s</a></div></div><div class="cta-card">%s%s<p style="color:var(--muted);margin:0;font-size:1rem">Viry-Châtillon (91)</p></div></div></section>'''%(eb,h2,p,btn_txt,LINE(U1,T1),LINE(U2,T2))
def panel(id,src,alt,h3,items):
    return '<article class="panel" id="%s">%s<div class="in"><h3>%s</h3><ul class="ticks">%s</ul></div></article>'%(id,img(src,1000,545,alt),h3,''.join('<li>%s</li>'%i for i in items))
# ---------- INDEX
H=rd(M+'H8.html')
H=H.replace('Paysagiste à Commune (00)',"Entreprise d'élagage · Viry-Châtillon (91)").replace('Titre principal du site',"L'arbre au cœur de notre métier")
H=H.replace("Deux phrases concrètes sur l'activité et la zone d'intervention.","Élagage, abattage, création et entretien d'espaces verts à Viry-Châtillon et dans un rayon de 20 km autour de Savigny-sur-Orge.")
H=H.replace('+33000000000',U1).replace('00 00 00 00 00',T1)
alts=["Élagueur encordé travaillant dans le houppier d'un grand chêne","Équipe d'élagage avec son matériel étalé au pied d'un arbre, à côté du camion","Jardin paysager aménagé avec massifs et allée courbe devant une maison contemporaine"]
for a in alts:H=H.replace('Texte alternatif exact',a,1)
H=H.replace('width="700" height="900"','width="597" height="768"')
V=rd(M+'V6.html')
V=V.replace('Titre de la section',"Des arbres aux espaces verts, une seule équipe.").replace("Une phrase d'introduction.","Quatre domaines d'intervention pour les particuliers, les copropriétés et leurs espaces extérieurs.")
V=V.replace('images/p1.jpg" width="900" height="900"','images/p1.jpg" width="1000" height="640"').replace('Texte alternatif exact',"Élagueur encordé taillant les branches d'un grand chêne",1)
V=V.replace('Prestation phare','Élagage').replace('Deux phrases concrètes.',"Taille et entretien des arbres, y compris les plus grands : l'arbre est au cœur du métier de l'entreprise.",1)
V=V.replace('prestations.html#p1','prestations.html#elagage')
for i,(h,t,a) in enumerate([("Abattage","Abattage d'arbres, même en terrain difficile ou dangereux, pour sécuriser vos espaces extérieurs.","abattage"),("Création d'espaces verts","Transformer et embellir un extérieur, quelle que soit sa surface, avec une ambiance naturelle personnalisée.","creation"),("Entretien d'espaces verts","Un suivi régulier des jardins et des espaces verts, pour particuliers et copropriétés.","entretien")],2):
    V=V.replace('<h3>Prestation %d</h3><p>Deux phrases concrètes.</p><a href="prestations.html#p%d">'%(i,i),'<h3>%s</h3><p>%s</p><a href="prestations.html#%s">'%(h,t,a))
V=re.sub(r'<div class="sv6-t sv6-t4">.*?</div>','',V,flags=re.S)
A=rd(M+'A4.html').replace('Titre de la section',"Une entreprise de Viry-Châtillon, dirigée par Arnaud Bouille.")
A=A.replace("Un paragraphe concret et vérifié sur l'entreprise.","CALICE ESPACES VERTS intervient à Viry-Châtillon (91) et dans les communes alentour, dans un rayon de 20 km autour de Savigny-sur-Orge. L'entreprise est spécialisée dans les travaux paysagers, avec l'arbre au cœur de son métier.").replace("Un second paragraphe.","Elle sécurise les extérieurs en retirant les végétaux fragiles ou gênants, puis les transforme et les embellit, quelle que soit leur surface. Ses clients sont des particuliers et des copropriétés.")
A=A.replace('Prénom Nom, dirigeant','Arnaud Bouille, dirigeant').replace('Texte alternatif exact',"Chantier d'abattage dans un jardin avec arbre au sol et camionnette")
Mm=rd(M+'M1.html').replace('Notre méthode','Ce que disent nos clients').replace('Titre de la section',"Une intervention qui laisse un jardin net.").replace("Une phrase d'introduction.","Les avis laissés par des clients de l'entreprise reviennent sur quatre points.")
for i,(h,t) in enumerate([("Des conseils","Le chantier est précédé de conseils, relevés par plusieurs clients."),("Un travail rapide et soigné","Des interventions décrites comme rapides, fiables et soignées."),("Un chantier nettoyé","Le nettoyage du jardin et du toit après l'intervention est salué."),("Un suivi dans la durée","Certains clients font appel à l'entreprise depuis plusieurs années.")],1):
    Mm=Mm.replace('<h3>Étape %d</h3><p>Deux phrases concrètes.</p>'%i,'<h3>%s</h3><p>%s</p>'%(h,t))
C=rd(M+'C2.html').replace('Un projet de jardin ? Parlons-en.',"Un arbre à élaguer, un jardin à créer ?").replace("Une phrase d'invitation à demander un devis.","Décrivez votre projet à l'entreprise : appelez ou écrivez, nous vous répondons.").replace('+33000000000',U1).replace('00 00 00 00 00',T1)
C=re.sub(r'<div><span>E-mail</span>.*?</div>','<div><span>Téléphone fixe</span><a href="tel:%s">%s</a></div>'%(U2,T2),C,flags=re.S).replace('Adresse de la fiche','Viry-Châtillon (91)').replace('<span>Adresse</span>','<span>Commune</span>')
idx=page('index.html',"CALICE ESPACES VERTS, élagage et espaces verts à Viry-Châtillon (91)","CALICE ESPACES VERTS, entreprise d'élagage, d'abattage, de création et d'entretien d'espaces verts à Viry-Châtillon (91).",'\n'.join([H,V,A,Mm,C]))
# ---------- PRESTATIONS
mos='<div class="mosaic">%s%s%s</div>'%(img('chantier-abattage.jpg',1000,545,"Chantier d'abattage dans un jardin, avec arbre au sol et camionnette",False,'m1'),img('elagage-chene.jpg',1000,545,"Élagueur encordé travaillant dans un chêne au-dessus d'un quartier pavillonnaire",False,'m2'),img('entretien-jardin.jpg',1000,545,"Jardin entretenu avec allée de gravier, pelouse et massifs devant une maison",False,'m3'))
pm='''<section class="page-head"><div class="wrap ph-grid"><div><span class="eyebrow">Prestations</span><h1 style="margin-top:18px">Arbres, jardins et <em>espaces verts</em>.</h1><p class="lead">CALICE ESPACES VERTS intervient à Viry-Châtillon et dans un rayon de 20 km autour de Savigny-sur-Orge : élagage, abattage, création et entretien d'espaces verts.</p><div class="cta"><a class="btn btn-apricot" href="contact.html">Demander un devis</a><a class="btn btn-line" href="tel:%s">%sAppeler</a></div></div>%s</div></section>
<section class="band band-cream" id="arbres"><div class="wrap"><div class="sec-head"><span class="eyebrow">Les arbres</span><h2>Élaguer, abattre, sécuriser.</h2><p>L'arbre est au cœur du métier de l'entreprise, y compris quand le terrain est difficile.</p></div><div class="trio">%s%s%s</div></div></section>
<section class="band band-sage" id="creation"><div class="wrap"><div class="sec-head"><span class="eyebrow">Créer</span><h2>Un extérieur transformé, quelle que soit sa surface.</h2></div><article class="row"><div class="row-img duo">%s%s</div><div class="row-txt"><h3>Création d'espaces verts</h3><p>L'entreprise transforme et embellit vos extérieurs, quelle que soit leur surface, pour leur apporter une ambiance naturelle personnalisée.</p><a class="btn btn-dark" href="contact.html">Parler de mon projet</a></div></article></div></section>
<section class="band band-cream" id="entretien"><div class="wrap"><div class="sec-head"><span class="eyebrow">Entretenir</span><h2>Des espaces verts suivis dans la durée.</h2></div><article class="row rev"><div class="row-img duo">%s%s</div><div class="row-txt"><h3>Entretien d'espaces verts</h3><p>Entretien de jardins de particuliers et d'espaces verts de copropriété : un suivi régulier qui garde les lieux nets et soignés.</p><a class="btn btn-dark" href="contact.html">Demander un devis</a></div></article></div></section>
<section class="band band-sage" id="zone"><div class="wrap about"><div class="about-photo">%s</div><div class="about-card"><span class="eyebrow">Zone d'intervention</span><h2>Autour de Viry-Châtillon.</h2><p>L'entreprise intervient dans un rayon de 20 km autour de Savigny-sur-Orge, en Essonne. Pour savoir si votre commune est desservie, un appel suffit.</p><a class="line-link" href="tel:%s">%s%s</a></div></div></section>
%s'''%(U1,PH,mos,
 panel('elagage','elagage-houppier.jpg',"Élagueur encordé dans le houppier d'un grand chêne devant une maison",'Élagage',["Taille et entretien des arbres","Interventions en hauteur, même complexes","Arbres de particuliers et de copropriétés"]),
 panel('abattage','chantier-abattage.jpg',"Chantier d'abattage avec arbre au sol dans un jardin",'Abattage',["Abattage d'arbres dangereux ou gênants","Terrains difficiles pris en charge","Espaces extérieurs sécurisés"]),
 panel('securisation','equipe-materiel.jpg',"Équipe avec cordes et matériel d'élagage au pied d'un grand arbre",'Sécurisation des extérieurs',["Végétaux fragiles retirés","Végétaux gênants éliminés","Conseils avant l'intervention"]),
 img('creation-jardin.jpg',1000,545,"Jardinier plantant dans un massif au bord d'une pelouse sinueuse devant une maison contemporaine"),img('plantation.jpg',1000,546,"Jardinier plantant un arbuste dans un massif fleuri"),
 img('tonte.jpg',1000,558,"Tonte d'une pelouse devant une maison et ses massifs"),img('taille-haies.jpg',1000,545,"Taille d'une haie au taille-haie dans un jardin"),
 img('conception.jpg',1000,545,"Jardin aménagé avec muret de pierre, massifs et pelouse devant une maison"),U1,PH,T1,
 cta_band('Votre projet',"Un devis pour vos arbres ou vos espaces verts.","Décrivez votre besoin : nous vous répondons pour en discuter."))
pres=page('prestations.html',"Prestations d'élagage et d'espaces verts à Viry-Châtillon | CALICE ESPACES VERTS","Élagage, abattage, création et entretien d'espaces verts à Viry-Châtillon (91) : les prestations de CALICE ESPACES VERTS.",pm)
# ---------- A PROPOS
Q='<svg viewBox="0 0 64 64" fill="none" stroke="#56d22d" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 40c0-12 6-20 16-22M10 40h14V28H10M36 40c0-12 6-20 16-22M36 40h14V28H36"/></svg>'
ids=[("Commune","Viry-Châtillon (91)"),("Dirigeant","Arnaud Bouille"),("Activité","Aménagement paysager"),("Spécialité","L'arbre : élagage, abattage"),("Clients","Particuliers et copropriétés"),("Zone","20 km autour de Savigny-sur-Orge")]
av=[("Valérie M.","« Excellent travail répondant à mes attentes. »"),("Joëlle L.","« Fiable, soigné, raisonnable. Une équipe adorable, un travail remarquable, un nettoyage minutieux du jardin et du toit. »"),("Céline M.","« Clients depuis 5 ans chez Calice espaces verts, nous ne sommes jamais déçus par les résultats ! »")]
ap='''<section class="page-head"><div class="wrap ph-grid"><div><span class="eyebrow">À propos</span><h1 style="margin-top:18px">L'arbre au cœur de notre <em>métier</em>.</h1><p class="lead">CALICE ESPACES VERTS est une entreprise de travaux paysagers installée à Viry-Châtillon, dirigée par Arnaud Bouille.</p><div class="cta"><a class="btn btn-apricot" href="contact.html">Nous contacter</a><a class="btn btn-line" href="prestations.html">Voir les prestations</a></div></div><div class="arch">%s</div></div></section>
<section class="band band-cream" id="en-bref"><div class="wrap"><div class="sec-head"><span class="eyebrow">L'entreprise en bref</span><h2>Une entreprise de proximité en Essonne.</h2></div><div class="idcards">%s</div></div></section>
<section class="band band-moss" id="avis"><div class="wrap"><div class="sec-head"><span class="eyebrow">Avis de clients</span><h2>Ce que disent ceux qui nous ont fait confiance.</h2><p>Extraits d'avis publiés par des clients de l'entreprise.</p></div><div class="trio principles">%s</div></div></section>
<section class="band band-sage" id="intervention"><div class="wrap about"><div class="about-photo">%s</div><div class="about-card"><span class="eyebrow">Sécuriser, transformer, embellir</span><h2>Des extérieurs en sécurité, puis embellis.</h2><p>L'entreprise retire les végétaux fragiles ou gênants, puis transforme et embellit les espaces, quelle que soit leur surface.</p><a class="btn btn-dark" href="prestations.html" style="justify-self:start">Voir les prestations</a></div></div></section>
%s'''%(img('equipe-materiel.jpg',1000,545,"Équipe d'élagage avec cordes et matériel au pied d'un grand arbre, camionnette en arrière-plan",False),
 ''.join('<div class="idc"><span>%s</span><b>%s</b></div>'%i for i in ids),
 ''.join('<div class="pr">%s<h3>%s</h3><p>%s</p></div>'%(Q,n,t) for n,t in av),
 img('elagage-chene.jpg',1000,545,"Élagueur encordé dans un chêne au-dessus de jardins pavillonnaires"),
 cta_band('Faisons connaissance',"Le plus simple : en parler.","Un appel ou un message, et nous étudions votre projet."))
apage=page('a-propos.html',"À propos de CALICE ESPACES VERTS, élagage à Viry-Châtillon (91)","CALICE ESPACES VERTS, entreprise de travaux paysagers à Viry-Châtillon (91) : l'arbre au cœur du métier, avis de clients.",ap)
# ---------- CONTACT
K=rd(M+'K4.html')
K=K.replace("Nom de l'entreprise",N).replace('data-sms="+33000000000" data-tel="+33000000000"','data-sms="%s" data-tel="%s"'%(U1,U1))
K=K.replace('<option>Besoin 1</option><option>Besoin 2</option><option>Besoin 3</option>',"<option>Élagage d'arbre</option><option>Abattage d'arbre</option><option>Création d'espaces verts</option><option>Entretien d'espaces verts</option>")
K=K.replace("Une phrase d'introduction.","Décrivez votre besoin : un récapitulatif est préparé, à envoyer par SMS ou à copier. Rien n'est transmis sans votre validation.")
side='<h3>Nous joindre directement</h3><ul><li><span>Téléphone</span><a href="tel:%s">%s</a></li><li><span>Téléphone fixe</span><a href="tel:%s">%s</a></li><li><span>Commune</span><p>Viry-Châtillon (91)</p></li></ul>'%(U1,T1,U2,T2)
K=re.sub(r'<h3>Nous joindre directement</h3><ul>.*?</ul>',side,K,flags=re.S)
SV=lambda p:'<svg viewBox="0 0 64 64" fill="none" stroke="#261717" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'%p
prep='''<section class="band band-sage" id="preparer"><div class="wrap"><div class="sec-head"><span class="eyebrow">Pour un échange efficace</span><h2>Trois choses utiles à nous dire.</h2></div><div class="seasons three"><div class="season s1">%s<h3>L'arbre ou l'espace</h3><p>Le type d'arbre concerné, ou la surface approximative du jardin à créer ou entretenir.</p></div><div class="season s2">%s<h3>Votre besoin</h3><p>Élagage, abattage, création ou entretien : ce que vous souhaitez faire.</p></div><div class="season s4">%s<h3>Des photos</h3><p>Quelques vues du lieu aident à préparer la réponse.</p></div></div></div></section>'''%(SV('<path d="M32 56V30M32 30c-12 0-20-8-20-18 12 0 20 6 20 18ZM32 38c10 0 18-6 18-16-10 0-18 5-18 16Z"/>'),SV('<path d="M10 14h44v26H30l-12 10V40H10Z"/>'),SV('<rect x="8" y="16" width="48" height="36" rx="6"/><circle cx="32" cy="34" r="9"/><path d="M22 16l4-6h12l4 6"/>'))
cm='''<section class="page-head compact" style="min-height:0"><div class="wrap"><span class="eyebrow">Contact</span><h1 style="margin-top:18px">Parlons de votre <em>projet</em>.</h1><p class="lead" style="margin-bottom:0">Un arbre à élaguer ou à abattre, un jardin à créer ou à entretenir à Viry-Châtillon : appelez ou remplissez le formulaire ci-dessous.</p></div></section>
'''+K+'\n'+prep
cont=page('contact.html',"Contact et devis | CALICE ESPACES VERTS, Viry-Châtillon (91)","Contactez CALICE ESPACES VERTS à Viry-Châtillon (91) pour un devis : élagage, abattage, création ou entretien d'espaces verts.",cm,'<script src="js/k.js" defer></script>\n')
for n,c in [('index.html',idx),('prestations.html',pres),('a-propos.html',apage),('contact.html',cont)]:open(D+n,'w',encoding='utf8').write(c)
print('ok')
