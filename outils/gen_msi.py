#!/usr/bin/env python3
# Génère le site MSI (dossier msi-transport). Usage : python3 outils/gen_msi.py
# Photos et logo : déjà préparés dans msi-transport (floutage des marques tierces, recadrage 4:3, JPEG q80).
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'msi-transport')
os.makedirs(OUT, exist_ok=True)

NOM = 'MSI – Société Internationale des Services de Transport'
TEL = '+33145612300'
TEL_AFF = '+33 1 45 61 23 00'
MAIL = 'info@msi-prs.fr'
MOBILES = ['+33 6 86 30 89 66', '+33 7 58 68 99 01', '+33 6 16 31 31 76', '+33 6 75 37 66 93']
PARIS = '128 rue La Boétie, 75008 Paris'
MARSEILLE = '24-26 Boulevard Gay-Lussac, 13014 Marseille'

CSS = r"""
:root{--navy:#0B2A55;--navy2:#123A73;--blue:#1A56C7;--blue-d:#1447A6;--sky:#EEF4FC;--sky2:#DCE8F8;--ink:#14233B;--muted:#4A5B73;--red:#C8161D;--line:#D5E0EF;--lt:#8DB8FF;--soft:#C5D6EE;--r:16px}
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%;scroll-padding-top:100px}
body{margin:0;font:400 1.0625rem/1.65 'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:#fff}
img,svg{max-width:100%;display:block}
h1,h2,h3{font-family:'Sora','Manrope',system-ui,sans-serif;font-weight:700;line-height:1.18;margin:0 0 .5em;letter-spacing:-.01em}
h1{font-size:clamp(2rem,5.4vw,3.7rem)}
h2{font-size:clamp(1.6rem,3.6vw,2.4rem)}
h3{font-size:1.2rem}
p{margin:0 0 1em}
a{color:inherit}
.wrap{width:min(100% - 32px,1240px);margin-inline:auto}
:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
.dark :focus-visible,.hero :focus-visible,.site-footer :focus-visible,.topbar :focus-visible,.cta :focus-visible,.page-head :focus-visible,.out :focus-visible,.devis-side :focus-visible{outline-color:#fff}
.skip-link{position:absolute;left:-999px;top:8px;background:#fff;color:var(--navy);padding:12px 16px;z-index:100;border-radius:8px;font-weight:800}
.skip-link:focus{left:8px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:48px;padding:.7rem 1.5rem;border-radius:999px;font:800 1rem/1.2 'Manrope',sans-serif;text-decoration:none;border:2px solid transparent;cursor:pointer;transition:transform .2s,background .2s,color .2s}
.btn-primary{background:var(--blue);color:#fff}
.btn-primary:hover{background:var(--blue-d);transform:translateY(-2px)}
.btn-white{background:#fff;color:var(--navy)}
.btn-white:hover{background:var(--sky2);transform:translateY(-2px)}
.btn-ghost{border-color:#fff;color:#fff}
.btn-ghost:hover{background:rgba(255,255,255,.14)}
.btn-line{border-color:var(--navy);color:var(--navy)}
.btn-line:hover{background:var(--sky)}
/* Barre d'infos */
.topbar{display:none;background:var(--navy);color:#fff}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:44px}
.topbar a,.topbar span{display:inline-flex;align-items:center;min-height:44px;color:#fff;text-decoration:none;font-weight:600}
.topbar a:hover{text-decoration:underline}
.tb-r{display:flex;gap:28px}
@media(min-width:981px){.topbar{display:block}}
/* En-tête */
.site-header{position:sticky;top:0;z-index:50;background:#fff;color:var(--ink);border-bottom:1px solid var(--line);box-shadow:0 4px 18px rgba(11,42,85,.06)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:84px}
.logo{display:flex;align-items:center;gap:12px;text-decoration:none;min-height:48px;color:var(--ink)}
.logo img{height:64px;width:auto;flex:none}
.logo small{display:none;font-size:1rem;flex-direction:column;gap:2px;padding-left:14px;border-left:1px solid var(--line);line-height:1.2}
.logo small b{font:700 1.1rem/1.15 'Sora',sans-serif;color:var(--navy)}
.logo small span{font-weight:700;color:var(--red)}
.burger{width:48px;height:48px;border:0;border-radius:12px;background:transparent;color:var(--navy);cursor:pointer;display:grid;place-items:center}
.burger span,.burger span::before,.burger span::after{display:block;width:24px;height:2px;background:currentColor;position:relative;transition:.25s}
.burger span::before,.burger span::after{content:"";position:absolute;left:0}
.burger span::before{top:-7px}.burger span::after{top:7px}
.burger[aria-expanded=true] span{background:transparent}
.burger[aria-expanded=true] span::before{top:0;transform:rotate(45deg)}
.burger[aria-expanded=true] span::after{top:0;transform:rotate(-45deg)}
.menu{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;padding:8px 16px 24px;border-top:1px solid var(--line);box-shadow:0 14px 26px rgba(11,42,85,.14)}
.menu.open{display:block}
.menu ul{list-style:none;margin:0;padding:0}
.menu a.nl{display:flex;align-items:center;min-height:52px;padding:0 4px;text-decoration:none;font-weight:700;border-bottom:1px solid var(--line)}
.menu a[aria-current=page]{color:var(--blue)}
.menu-ctas{display:grid;gap:10px;margin-top:16px}
.menu-ctas .btn-ghost{border-color:var(--navy);color:var(--navy)}
.menu-ctas .btn-ghost:hover{background:var(--sky)}
.head-ctas{display:none}
.head-ctas .l{display:none}
.head-ctas .btn-ghost{border-color:var(--navy);color:var(--navy)}
.head-ctas .btn-ghost:hover{background:var(--sky)}
@media(min-width:981px){
.burger,.menu-ctas{display:none}
.menu{display:block;position:static;background:none;padding:0;border:0;box-shadow:none}
.menu ul{display:flex;gap:2px}
.menu a.nl{border:0;padding:0 14px;min-height:84px;font-size:1rem}
.menu a.nl:hover{color:var(--blue)}
.menu a[aria-current=page]{box-shadow:inset 0 -4px 0 var(--blue)}
.head-ctas{display:flex;gap:10px}
.head-ctas .btn{min-height:46px;padding:.5rem 1.2rem}
}
@media(min-width:1260px){.logo small{display:flex}}
@media(min-width:1420px){.head-ctas .l{display:inline}.head-ctas .s{display:none}}
/* Sections */
.sec{padding:clamp(32px,5.5vw,76px) 0}
.sky{background:var(--sky)}
.dark{background:var(--navy);color:#fff}
.kicker{display:inline-block;font:800 1rem/1.3 'Manrope',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--blue);margin-bottom:12px}
.kicker::before{content:"";display:inline-block;width:28px;height:3px;background:var(--red);vertical-align:middle;margin-right:10px}
.dark .kicker,.hero .kicker,.page-head .kicker{color:var(--lt)}
.lede{font-size:1.15rem}
.dark .lede,.page-head .lede{color:var(--soft)}
/* Bandeau photo */
.hero{position:relative;color:#fff;background:var(--navy);overflow:hidden}
.hero-bg{position:absolute;top:0;right:0;width:min(100%,1600px);height:100%;object-fit:cover;object-position:70% 25%}
.hero::before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,var(--navy) 0%,rgba(11,42,85,.9) 34%,rgba(11,42,85,.55) 64%,rgba(11,42,85,.18) 100%)}
.hero-in{position:relative;z-index:2;padding:clamp(40px,7vw,104px) 0 clamp(88px,10vw,136px)}
.hero h1 span{display:block;color:var(--lt)}
.hero .lede{max-width:46ch;color:#fff}
.hero-ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
@media(max-width:699px){.hero::before{background:rgba(11,42,85,.78)}}
/* Barre d'icônes */
.quick{position:relative;z-index:3;margin-top:-56px}
.quick-in{background:#fff;border-radius:var(--r);box-shadow:0 20px 50px rgba(11,42,85,.18);display:grid}
.q{display:flex;align-items:center;gap:14px;padding:14px 20px;min-height:76px;text-decoration:none;color:var(--ink);border-top:1px solid var(--line);transition:background .2s}
.q:first-child{border-top:0}
.q:hover{background:var(--sky)}
.qi{flex:none;width:48px;height:48px;border-radius:12px;background:var(--sky);color:var(--blue);display:grid;place-items:center}
.qi svg{width:28px;height:28px}
.q b{display:block;font:700 1.05rem/1.25 'Sora',sans-serif}
.q .t{color:var(--muted);display:block;line-height:1.35}
@media(min-width:700px){.quick-in{grid-template-columns:1fr 1fr}.q:nth-child(2){border-top:0}.q:nth-child(even){border-left:1px solid var(--line)}}
@media(min-width:981px){.quick-in{grid-template-columns:repeat(4,1fr)}.q:nth-child(-n+4){border-top:0}.q{border-left:1px solid var(--line)}.q:first-child{border-left:0}}
/* Cartes de services */
.cards{display:grid;gap:20px;margin-top:28px}
.card{display:block;background:#fff;border-radius:var(--r);overflow:hidden;text-decoration:none;color:var(--ink);box-shadow:0 8px 28px rgba(11,42,85,.1);transition:transform .25s,box-shadow .25s}
.card:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(11,42,85,.18)}
.card-img{position:relative}
.card-img img{display:block;width:100%;height:auto}
.tag{position:absolute;left:0;bottom:0;background:var(--blue);color:#fff;padding:10px 44px 10px 20px;clip-path:polygon(0 0,100% 0,calc(100% - 24px) 100%,0 100%);font:700 1.05rem/1.2 'Sora',sans-serif}
.card-body{padding:16px 22px 18px}
.card-body h3{margin-bottom:.25em}
.card-body p{color:var(--muted);margin:0 0 .4em}
.more-link{display:inline-block;font-weight:800;color:var(--blue)}
@media(max-width:699px){.card{display:grid;grid-template-columns:38% 1fr;align-items:center}.card .tag{display:none}.card-body{padding:10px 16px}.card-body h3{font-size:1.1rem}.card-body p{margin:0}.more-link{display:none}}
@media(min-width:700px){.cards{grid-template-columns:repeat(3,1fr)}}
/* Atouts */
.assets{display:grid;gap:26px;align-items:center}
.badge{display:none;width:260px;aspect-ratio:1;border-radius:50%;background:var(--blue);color:#fff;place-items:center;text-align:center;padding:30px;font:700 1.25rem/1.3 'Sora',sans-serif;margin-inline:auto;box-shadow:0 0 0 12px var(--sky2)}
.atouts{display:grid;gap:20px;margin-top:22px}
.atout{display:flex;gap:16px;align-items:flex-start}
.atout h3{margin:0 0 .15em}
.atout p{margin:0;color:var(--muted)}
@media(min-width:700px){.badge{display:grid}.atouts{grid-template-columns:1fr 1fr;gap:24px 32px}}
@media(min-width:981px){.assets{grid-template-columns:300px 1fr;gap:56px}}
/* Méthode */
.steps{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:12px;counter-reset:s}
.steps li{background:var(--sky);border-radius:var(--r);padding:16px 18px 16px 76px;position:relative}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:18px;top:16px;width:42px;height:42px;border-radius:50%;background:var(--blue);color:#fff;font:700 1.2rem/42px 'Sora',sans-serif;text-align:center}
.steps h3{font-size:1.15rem;margin:0 0 .15em}
.steps p{margin:0;color:var(--muted)}
@media(min-width:700px){.steps{grid-template-columns:repeat(2,1fr)}}
@media(min-width:981px){.steps{grid-template-columns:repeat(4,1fr);gap:18px}.steps li{padding:78px 20px 22px}.steps li::before{left:20px;top:20px}}
/* Zones */
.split{display:grid;gap:22px}
@media(min-width:981px){.split{grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
.ports{display:grid;gap:10px}
.port{border:1px solid rgba(255,255,255,.28);border-radius:var(--r);padding:14px 20px;display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.port b{font:700 1.3rem/1.2 'Sora',sans-serif}
.port span{color:var(--soft)}
/* Appel à l'action */
.cta{background:var(--blue);color:#fff}
.cta-in{display:grid;gap:18px;align-items:center}
.cta h2{margin:0 0 .3em}
.cta p{margin:0}
.btns{display:flex;flex-wrap:wrap;gap:12px}
@media(min-width:981px){.cta-in{grid-template-columns:1.4fr 1fr}.cta .btns{justify-self:end}}
/* Pages internes */
.page-head{position:relative;overflow:hidden;background:linear-gradient(135deg,var(--navy),var(--navy2));color:#fff;padding:clamp(32px,5vw,64px) 0 clamp(36px,5.5vw,68px)}
.page-head::after{content:"";position:absolute;right:-90px;top:-110px;width:380px;height:380px;border-radius:50%;border:44px solid rgba(255,255,255,.06)}
.page-head .wrap{position:relative;z-index:1}
.page-head .lede{max-width:60ch;margin:0}
.facts{display:grid;margin:0}
.facts div{display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-top:1px solid var(--line)}
.facts dt{font-weight:800;color:var(--blue)}
.facts dd{margin:0;text-align:right}
.big{font:600 clamp(1.3rem,3vw,2rem)/1.4 'Sora',sans-serif;max-width:30em;margin:0}
.ph{display:block;width:100%;height:auto;border-radius:var(--r);box-shadow:0 14px 34px rgba(11,42,85,.16)}
.ph.cap{max-width:480px}
.vals{display:grid;gap:14px;margin-top:26px}
.val{background:#fff;border-radius:var(--r);padding:20px 22px;box-shadow:0 6px 20px rgba(11,42,85,.08)}
.val h3{color:var(--blue);margin-bottom:.25em}
.val p{margin:0;color:var(--muted)}
@media(min-width:700px){.vals{grid-template-columns:repeat(3,1fr)}}
.sv{display:grid;gap:20px;align-items:center}
.sv-body ul{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
.sv-body li{padding-left:28px;position:relative}
.sv-body li::before{content:"";position:absolute;left:0;top:.8em;width:14px;height:3px;background:var(--red)}
.sv-body li b{display:block}
@media(min-width:700px){.sv{grid-template-columns:.9fr 1.2fr;gap:40px}.sv.rev{grid-template-columns:1.2fr .9fr}.sv.rev .sv-img{order:2}}
@media(min-width:981px){.sv{gap:64px}}
.flux{display:grid;margin-top:26px}
.tier{background:var(--navy);color:#fff;border-radius:var(--r);padding:18px 20px}
.tier .kicker{color:var(--lt);margin-bottom:8px}
.tier ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.tier li{background:rgba(255,255,255,.14);border-radius:999px;padding:4px 16px;font-weight:700}
.tier-link{height:48px;position:relative}
.tier-link::before{content:"";position:absolute;left:50%;top:6px;bottom:12px;border-left:3px dashed var(--blue);transform:translateX(-50%)}
.tier-link::after{content:"";position:absolute;left:50%;bottom:6px;width:12px;height:12px;border-right:3px solid var(--blue);border-bottom:3px solid var(--blue);transform:translateX(-50%) rotate(45deg)}
@media(min-width:981px){.flux{grid-template-columns:1fr 72px 1fr 72px 1fr}.tier{display:flex;flex-direction:column;justify-content:center;padding:26px}.tier-link{height:auto}.tier-link::before{left:6px;right:14px;top:50%;bottom:auto;border-left:0;border-top:3px dashed var(--blue);transform:translateY(-50%)}.tier-link::after{left:auto;right:6px;top:50%;bottom:auto;transform:translateY(-50%) rotate(-45deg)}}
.note{color:var(--muted);margin:18px 0 0}
.cols{display:grid;gap:14px;margin-top:24px}
.col{background:#fff;border-radius:var(--r);padding:18px 22px;box-shadow:0 6px 20px rgba(11,42,85,.08)}
.col h3{color:var(--blue);margin-bottom:.3em}
.col ul{margin:0;padding:0;list-style:none}
.col li{padding:6px 0;border-top:1px solid var(--line);font-weight:600}
@media(min-width:700px){.cols{grid-template-columns:repeat(3,1fr)}}
/* Contact */
.offices{display:grid;gap:14px;margin-top:22px}
.office{background:#fff;border-radius:var(--r);padding:18px 22px;box-shadow:0 6px 20px rgba(11,42,85,.1);border-left:5px solid var(--blue)}
.office h3{margin-bottom:.2em}
.office p{margin:0;color:var(--muted)}
@media(min-width:700px){.offices{grid-template-columns:1fr 1fr}}
.plan{margin-top:14px;border:2px dashed var(--line);border-radius:var(--r);min-height:96px;display:grid;place-items:center;color:var(--muted);font-weight:700}
.tels{display:grid;gap:10px;margin-top:18px}
.tel{display:flex;align-items:center;gap:12px;min-height:52px;padding:6px 18px;background:#fff;border:1.5px solid var(--line);border-radius:12px;text-decoration:none;font-weight:800;color:var(--navy);transition:border-color .2s,background .2s}
.tel:hover{border-color:var(--blue);background:var(--sky)}
.tel small{font:600 1rem/1 'Manrope',sans-serif;color:var(--muted);min-width:5.5em}
@media(min-width:700px){.tels{grid-template-columns:1fr 1fr}}
@media(min-width:981px){.tels{grid-template-columns:repeat(3,1fr)}}
.devis{display:grid;gap:16px;align-items:start}
.devis-side p{color:var(--muted);margin:0}
.devis-side h2{font-size:clamp(1.7rem,2.6vw,2.2rem)}
.steps-mini{display:none;list-style:none;margin:20px 0 0;padding:0;counter-reset:m}
.steps-mini li{counter-increment:m;position:relative;padding:12px 0 12px 46px;border-top:1px solid rgba(255,255,255,.18)}
.steps-mini li::before{content:counter(m);position:absolute;left:0;top:10px;width:32px;height:32px;border-radius:50%;background:var(--blue);color:#fff;font:700 1rem/32px 'Sora',sans-serif;text-align:center}
.form-card{background:#fff;border-radius:22px;padding:16px;box-shadow:0 20px 50px rgba(11,42,85,.14);border-top:5px solid var(--blue)}
.form{display:grid;gap:12px}
.field{display:grid;gap:4px}
.field label{font-weight:700}
.field label span{color:var(--red)}
.field input,.field textarea{width:100%;min-height:48px;padding:10px 14px 10px 46px;border:1.5px solid #7B8AA0;border-radius:12px;font:inherit;background-color:#FAFCFF;background-repeat:no-repeat;background-position:14px center;background-size:20px;color:var(--ink);transition:border-color .2s,box-shadow .2s,background-color .2s}
.field textarea{padding-left:14px;min-height:90px;resize:vertical}
.field input:hover,.field textarea:hover{border-color:var(--navy)}
.field input:focus,.field textarea:focus{border-color:var(--blue);background-color:#fff;box-shadow:0 0 0 4px rgba(26,86,199,.2);outline:none}
#f-nom{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4 4-7 8-7s8 3 8 7'/%3E%3C/svg%3E")}
#f-soc{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='5' y='3' width='14' height='18' rx='1'/%3E%3Cpath d='M9 8h2M13 8h2M9 12h2M13 12h2M10 21v-4h4v4'/%3E%3C/svg%3E")}
#f-tel{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z'/%3E%3C/svg%3E")}
#f-mail{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='5' width='18' height='14' rx='2'/%3E%3Cpath d='M3 7l9 6 9-6'/%3E%3C/svg%3E")}
#f-besoin{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z'/%3E%3Ccircle cx='12' cy='10' r='2.5'/%3E%3C/svg%3E")}
.field input::placeholder,.field textarea::placeholder{color:#55627A}
.field.bad input,.field.bad textarea{border-color:#9C2A0F;background-color:#FFF6F4}
.err{color:#9C2A0F;font-weight:700;margin:0}
.err:empty{display:none}
.hint{display:none;margin:0;color:var(--muted)}
.form .btn{width:100%;min-height:52px;font-size:1.05rem}
.form .btn svg{width:20px;height:20px;transition:transform .2s}
.form .btn:hover svg{transform:translateX(4px)}
@media(min-width:700px){
.devis-side{background:var(--navy);color:#fff;border-radius:var(--r);padding:26px 28px}
.devis-side p{color:var(--soft)}
.steps-mini{display:block}
.form-card{padding:30px}
.form{grid-template-columns:1fr 1fr;gap:18px}
.field.full,.hint,.form .btn{grid-column:1/-1}
.hint{display:block}
.form .btn{width:auto;justify-self:start;min-width:280px}
}
@media(min-width:981px){.devis{grid-template-columns:.75fr 1.4fr;gap:32px}.devis-side{position:sticky;top:116px;padding:34px}.form-card{padding:38px}}
.out{margin-top:22px;background:var(--navy);color:#fff;border-radius:var(--r);padding:20px}
.out textarea{width:100%;min-height:190px;background:rgba(255,255,255,.08);color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:12px;padding:12px;font:inherit}
.out .btns{margin-top:14px}
.tbd{color:var(--muted);font-style:italic}
.legal{max-width:760px}
.legal h2{font-size:1.5rem}
/* Pied de page */
.site-footer{background:var(--navy);color:var(--soft);padding:14px 0}
.foot{display:grid;gap:4px}
.foot-brand{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.foot-brand b{font:800 1.4rem/1.2 'Sora',sans-serif;color:#fff}
.foot-name{display:none;color:#fff;font-weight:700;margin:0 0 4px}
.foot nav ul{list-style:none;margin:0 0 0 -8px;padding:0;display:flex;flex-wrap:wrap}
.foot nav a,.foot-info a{display:inline-flex;align-items:center;min-height:44px;padding:0 8px;text-decoration:none;color:#fff;font-weight:600}
.foot nav a:hover,.foot-info a:hover{color:var(--lt)}
.foot-info{display:none}
.foot-info p{margin:0 0 .6em}
.foot-info a{padding:0}
@media(min-width:981px){
.site-footer{padding:40px 0 28px}
.foot{grid-template-columns:1.2fr .8fr 1.4fr;gap:48px;align-items:start}
.foot-name{display:block}
.foot nav ul{flex-direction:column;margin-left:-8px}
.foot-info{display:block}
}
/* Animations */
.js .reveal{opacity:0;transform:translateY(14px);transition:opacity .6s,transform .6s}
.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}.js .reveal{opacity:1;transform:none}}
"""

JS = r"""(function(){
var d=document;d.documentElement.classList.add('js');
var b=d.querySelector('.burger'),m=d.getElementById('menu');
if(b&&m){
 b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));b.setAttribute('aria-label',o?'Ouvrir le menu':'Fermer le menu');m.classList.toggle('open',!o)});
 d.addEventListener('keydown',function(e){if(e.key==='Escape'&&m.classList.contains('open')){b.click();b.focus()}});
 window.matchMedia('(min-width:981px)').addEventListener('change',function(e){if(e.matches){m.classList.remove('open');b.setAttribute('aria-expanded','false')}});
}
var rv=d.querySelectorAll('.reveal');
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.1});rv.forEach(function(e){io.observe(e)})}
else{rv.forEach(function(e){e.classList.add('in')})}
var f=d.getElementById('devis-form');if(!f)return;
var out=d.getElementById('devis-out'),ta=d.getElementById('out-msg'),live=d.getElementById('out-live');
function setErr(id,t){var fl=d.getElementById(id).closest('.field');fl.classList.toggle('bad',!!t);d.getElementById(id+'-err').textContent=t||''}
function telOk(v){return /^(\+|00)?\d{8,15}$/.test(v.replace(/[\s.\-()]/g,''))}
function mailOk(v){return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)}
f.addEventListener('submit',function(e){
 e.preventDefault();
 var v=function(id){return d.getElementById(id).value.trim()},ok=true,first=null;
 function bad(id,t){setErr(id,t);ok=false;if(!first)first=id}
 setErr('f-nom');setErr('f-tel');setErr('f-mail');setErr('f-besoin');
 if(!v('f-nom'))bad('f-nom','Indiquez votre nom.');
 if(v('f-tel')&&!telOk(v('f-tel')))bad('f-tel','Numéro invalide : 8 à 15 chiffres, avec ou sans indicatif.');
 if(v('f-mail')&&!mailOk(v('f-mail')))bad('f-mail','Adresse e-mail invalide.');
 if(!v('f-tel')&&!v('f-mail')){bad('f-tel','Indiquez un téléphone ou un e-mail pour vous répondre.')}
 if(!v('f-besoin'))bad('f-besoin','Décrivez brièvement votre trajet ou votre besoin.');
 if(!ok){d.getElementById(first).focus();out.hidden=true;return}
 var t='Demande de devis - MSI\n\nNom : '+v('f-nom')+'\nSociété : '+(v('f-soc')||'-')+'\nTéléphone : '+(v('f-tel')||'-')+'\nE-mail : '+(v('f-mail')||'-')+'\nTrajet / besoin : '+v('f-besoin')+'\nMessage : '+(v('f-msg')||'-');
 ta.value=t;out.hidden=false;
 var em=f.getAttribute('data-email'),sm=f.getAttribute('data-sms'),tl=f.getAttribute('data-tel'),s=encodeURIComponent('Demande de devis - MSI'),bd=encodeURIComponent(t);
 var a=d.getElementById('b-mail'),c=d.getElementById('b-sms'),p=d.getElementById('b-tel');
 a.hidden=!em;if(em)a.href='mailto:'+em+'?subject='+s+'&body='+bd;
 c.hidden=!sm;if(sm)c.href='sms:'+sm+'?body='+bd;
 p.hidden=!tl;if(tl)p.href='tel:'+tl;
 out.scrollIntoView({behavior:'smooth',block:'nearest'});
});
d.getElementById('b-copy').addEventListener('click',function(){
 var done=function(){live.textContent='Message copié.';};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(ta.value).then(done,function(){ta.select();d.execCommand('copy');done()})}
 else{ta.select();d.execCommand('copy');done()}
});
})();
"""

def ico(body):
    return '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>'
SHIP = ico('<path d="M6 40h52l-7 14H13z"/><path d="M14 40V22h28v18"/><path d="M42 40V30h10v10"/><path d="M20 31h16"/><path d="M4 60q4-3 8 0t8 0 8 0 8 0 8 0 8 0 8 0"/>')
TRUCK = ico('<path d="M4 18h34v28H4z"/><path d="M38 28h12l10 10v8H38z"/><circle cx="17" cy="48" r="5"/><circle cx="49" cy="48" r="5"/>')
BOX = ico('<path d="M8 26l24-12 24 12-24 12z"/><path d="M8 26v20l24 12 24-12V26"/><path d="M32 38v20"/>')
GLOBE = ico('<circle cx="32" cy="32" r="24"/><path d="M8 32h48M32 8c-10 12-10 36 0 48M32 8c10 12 10 36 0 48"/>')
SHIELD = ico('<path d="M32 6l20 8v16c0 14-9 24-20 28C21 54 12 44 12 30V14z"/><path d="M23 31l6 6 12-13"/>')
CHAT = ico('<path d="M8 12h48v32H28l-12 10V44H8z"/><path d="M18 24h28M18 32h18"/>')
CLOCK = ico('<circle cx="32" cy="32" r="24"/><path d="M32 18v15l10 6"/>')
COMPASS = ico('<circle cx="32" cy="32" r="24"/><path d="M42 22l-6 14-14 6 6-14z"/>')

def photo(f, w, h, alt, lazy=True, cls='ph'):
    return '<img class="' + cls + '" src="' + f + '" width="' + str(w) + '" height="' + str(h) + '" alt="' + alt + '"' + (' loading="lazy"' if lazy else '') + '>'
ALT_HERO = 'Navire Ro-Ro à quai dans un port, rampe arrière ouverte'
ALT_RORO = 'Rampe d\'embarquement ouverte à l\'arrière d\'un navire Ro-Ro, à quai'
ALT_ROUT = 'Camion avec semi-remorque embarquant par la rampe d\'un navire, au coucher du soleil'
ALT_LOG = 'Engins de chantier sur un terminal portuaire, avec des conteneurs en arrière-plan'
ALT_PRES = 'Semi-remorque frigorifique embarquant par la rampe d\'un navire dans un port'

NAV = [('index.html', 'Accueil'), ('presentation.html', 'Présentation'), ('services.html', 'Services'), ('zones.html', 'Zones'), ('contact.html', 'Contact')]

def page(fn, title, desc, body):
    lis = ''.join('<li><a class="nl" href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == fn else '', t) for h, t in NAV)
    fl = ''.join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV) + '<li><a href="mentions-legales.html">Mentions légales</a></li>'
    html = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + title + '</title><meta name="description" content="' + desc + '"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#0B2A55">'
        '<link rel="icon" href="favicon.png" type="image/png" sizes="64x64"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;800&amp;family=Sora:wght@600;700;800&amp;display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head><body>\n'
        '<a class="skip-link" href="#contenu">Aller au contenu</a>\n'
        '<div class="topbar"><div class="wrap"><span>' + PARIS + ' · Bureau à Marseille</span><div class="tb-r"><a href="tel:' + TEL + '">' + TEL_AFF + '</a><a href="mailto:' + MAIL + '">' + MAIL + '</a></div></div></div>\n'
        '<header class="site-header"><div class="wrap bar"><a class="logo" href="index.html" aria-label="MSI, accueil"><img src="logo-msi.jpg" width="973" height="1307" alt="MSI"><small><b>Société Internationale</b><span>des Services de Transport</span></small></a>\n'
        '<button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span></button>\n'
        '<nav class="menu" id="menu" aria-label="Navigation principale"><ul>' + lis + '</ul>'
        '<div class="menu-ctas"><a class="btn btn-ghost" href="tel:' + TEL + '">Appeler</a><a class="btn btn-primary" href="contact.html#devis">Demander un devis</a></div></nav>\n'
        '<div class="head-ctas"><a class="btn btn-ghost" href="tel:' + TEL + '">Appeler</a><a class="btn btn-primary" href="contact.html#devis"><span class="s">Devis</span><span class="l">Demander un devis</span></a></div></div></header>\n'
        '<main id="contenu">\n' + body + '\n</main>\n'
        '<footer class="site-footer"><div class="wrap foot"><div><div class="foot-brand"><b>MSI</b><span>SASU · Paris – Marseille</span></div><p class="foot-name">Société Internationale des Services de Transport</p></div>'
        '<nav aria-label="Pied de page"><ul>' + fl + '</ul></nav>'
        '<div class="foot-info"><p>Siège : ' + PARIS + '<br>Bureau : ' + MARSEILLE + '</p><a href="tel:' + TEL + '">' + TEL_AFF + '</a><br><a href="mailto:' + MAIL + '">' + MAIL + '</a></div></div></footer>\n</body></html>\n')
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(html)

def cta(h='Un transport à organiser ?', p='Parlez-nous de votre trajet et de vos marchandises.'):
    return ('<section class="cta sec"><div class="wrap cta-in"><div><h2>' + h + '</h2><p>' + p + '</p></div>'
            '<div class="btns"><a class="btn btn-ghost" href="tel:' + TEL + '">Appeler</a><a class="btn btn-white" href="contact.html#devis">Demander un devis</a></div></div></section>')

def head(h1, lede):
    return '<section class="page-head"><div class="wrap"><h1>' + h1 + '</h1><p class="lede">' + lede + '</p></div></section>'

def quick(href, i, t, s):
    return '<a class="q" href="' + href + '"><span class="qi">' + i + '</span><span><b>' + t + '</b><span class="t">' + s + '</span></span></a>'

def card(href, img, tag, t, d):
    return ('<a class="card reveal" href="' + href + '"><div class="card-img">' + img + '<span class="tag">' + tag + '</span></div>'
            '<div class="card-body"><h3>' + t + '</h3><p>' + d + '</p><span class="more-link">En savoir plus →</span></div></a>')

def atout(i, t, d):
    return '<div class="atout reveal"><span class="qi">' + i + '</span><div><h3>' + t + '</h3><p>' + d + '</p></div></div>'

# ---------- Accueil
home = ('<section class="hero"><img class="hero-bg" src="hero-navire.jpg" width="1600" height="900" alt="' + ALT_HERO + '"><div class="wrap hero-in"><span class="kicker">Liaison Europe – Afrique du Nord fiable et régulière</span>'
 '<h1>Transport maritime et routier<span>Europe – Afrique du Nord</span></h1>'
 '<p class="lede">MSI organise le transport de vos marchandises par mer et par route entre la France, l\'Espagne, l\'Italie, le Maroc et l\'Algérie.</p>'
 '<div class="hero-ctas"><a class="btn btn-white" href="contact.html#devis">Demander un devis</a><a class="btn btn-ghost" href="tel:' + TEL + '">Appeler</a></div></div></section>\n'
 '<div class="quick"><div class="wrap quick-in">'
 + quick('services.html#roro', SHIP, 'Maritime Ro-Ro', 'Engins et marchandises roulantes')
 + quick('services.html#routier', TRUCK, 'Transport routier', 'Europe et Afrique du Nord')
 + quick('services.html#logistique', BOX, 'Solutions logistiques', 'Affrètement, douane, stockage')
 + quick('zones.html', GLOBE, 'Zones desservies', 'France, Espagne, Italie, Maroc, Algérie')
 + '</div></div>\n'
 '<section class="sec" id="services"><div class="wrap"><span class="kicker">Nos services</span><h2>Trois savoir-faire, un même objectif</h2><div class="cards">'
 + card('services.html#roro', photo('carte-roro.jpg', 1200, 900, ALT_RORO), 'RO-RO', 'Transport maritime Ro-Ro', 'Véhicules, engins et marchandises roulantes embarqués par rampe.')
 + card('services.html#routier', photo('carte-routier.jpg', 1200, 900, ALT_ROUT), 'ROUTIER', 'Transport routier', 'Fret par camion en Europe et en Afrique du Nord.')
 + card('services.html#logistique', photo('carte-logistique.jpg', 480, 360, ALT_LOG), 'LOGISTIQUE', 'Solutions logistiques', 'Affrètement, commission de transport, dédouanement, stockage.')
 + '</div></div></section>\n'
 '<section class="sec sky"><div class="wrap"><span class="kicker">Nos engagements</span><h2>Un partenaire pour relier les deux rives</h2><div class="assets"><div class="badge">Un interlocuteur à votre écoute</div>'
 '<div class="atouts">'
 + atout(SHIELD, 'Fiabilité', 'Des engagements tenus et un transport organisé avec rigueur.')
 + atout(CHAT, 'Clarté', 'Une information claire à chaque étape, des échanges simples.')
 + atout(CLOCK, 'Réactivité', 'Une réponse adaptée à chaque demande, des formalités anticipées.')
 + atout(COMPASS, 'Accompagnement', 'Un suivi du besoin à la livraison, par mer comme par route.')
 + '</div></div></div></section>\n'
 '<section class="sec"><div class="wrap"><span class="kicker">Méthode</span><h2>Du besoin à la livraison, quatre étapes</h2><ol class="steps">'
 '<li class="reveal"><h3>Votre besoin</h3><p>Marchandises, trajet, contraintes.</p></li>'
 '<li class="reveal"><h3>Le bon mode</h3><p>Mer, route, ou les deux.</p></li>'
 '<li class="reveal"><h3>L\'organisation</h3><p>Affrètement, formalités, documents.</p></li>'
 '<li class="reveal"><h3>L\'acheminement</h3><p>Prise en charge puis livraison.</p></li></ol></div></section>\n'
 '<section class="sec dark"><div class="wrap split"><div><span class="kicker">Zones d\'intervention</span><h2>De la France au Maroc et à l\'Algérie</h2>'
 '<p class="lede">Des liaisons entre l\'Europe et l\'Afrique du Nord, appuyées sur des ports et hubs de référence.</p><a class="btn btn-white" href="zones.html">Voir les zones</a></div>'
 '<div class="ports"><div class="port"><b>Sète</b><span>France</span></div><div class="port"><b>Tanger Med</b><span>Maroc</span></div><div class="port"><b>Casablanca</b><span>Maroc</span></div></div></div></section>\n'
 + cta())
page('index.html', 'MSI – Transport maritime Ro-Ro et routier Europe – Afrique du Nord', 'MSI – Société Internationale des Services de Transport : transport maritime Ro-Ro, routier et solutions logistiques entre la France, l\'Espagne, l\'Italie, le Maroc et l\'Algérie.', home)

# ---------- Présentation
pres = (head('Une société née pour relier les deux rives', 'MSI – Société Internationale des Services de Transport organise le transport de marchandises par route et par mer entre l\'Europe et l\'Afrique du Nord.')
 + '<section class="sec"><div class="wrap split"><div><span class="kicker">Historique</span><h2>Créée en 2024, installée à Paris</h2>'
 '<p>MSI est une société par actions simplifiée unipersonnelle (SASU). Elle a été créée en 2024 et son siège est à Paris, avec un bureau à Marseille.</p><p>Son objet : l\'affrètement et l\'organisation de transports maritimes, terrestres et aériens, avec un point d\'ancrage sur les liaisons Europe – Afrique du Nord.</p></div>'
 '<dl class="facts"><div><dt>Forme</dt><dd>SASU</dd></div><div><dt>Création</dt><dd>2024</dd></div><div><dt>Siège</dt><dd>Paris</dd></div><div><dt>Bureau</dt><dd>Marseille</dd></div></dl></div></section>\n'
 '<section class="sec dark"><div class="wrap split"><div><span class="kicker">Mission</span><p class="big">Relier l\'Europe et l\'Afrique du Nord par des solutions de transport maritime et routier, organisées pour répondre aux besoins de chaque client.</p></div>' + photo('presentation.jpg', 1200, 900, ALT_PRES) + '</div></section>\n'
 '<section class="sec sky"><div class="wrap"><span class="kicker">Valeurs</span><h2>Ce qui guide notre façon de travailler</h2><div class="vals">'
 '<div class="val reveal"><h3>Fiabilité</h3><p>Tenir ses engagements et organiser chaque transport avec rigueur.</p></div>'
 '<div class="val reveal"><h3>Transparence</h3><p>Une information claire, des échanges directs et sans ambiguïté.</p></div>'
 '<div class="val reveal"><h3>Réactivité</h3><p>Anticiper les formalités et répondre vite aux demandes.</p></div></div></div></section>\n'
 '<section class="sec"><div class="wrap"><span class="kicker">Spécialisation</span><h2>Maritime Ro-Ro, routier, logistique</h2>'
 '<p class="lede" style="max-width:60ch">Trois expertises complémentaires pour couvrir le transport de bout en bout, sur un axe géographique précis.</p>'
 '<div class="cols"><div class="col"><h3>Europe</h3><ul><li>France</li><li>Espagne</li><li>Italie</li></ul></div>'
 '<div class="col"><h3>Afrique du Nord</h3><ul><li>Maroc</li><li>Algérie</li></ul></div>'
 '<div class="col"><h3>Ports et hubs</h3><ul><li>Tanger Med</li><li>Casablanca</li><li>Sète</li></ul></div></div></div></section>\n'
 + cta())
page('presentation.html', 'Présentation – MSI, transport Europe – Afrique du Nord', 'MSI, SASU créée en 2024 et basée à Paris, avec un bureau à Marseille : mission, valeurs et spécialisation en transport maritime Ro-Ro, routier et logistique.', pres)

# ---------- Services
def sv(sid, n, img, t, intro, items, alt=False, rev=False):
    li = ''.join('<li>' + x + '</li>' for x in items)
    return ('<section class="sec' + (' sky' if alt else '') + '" id="' + sid + '"><div class="wrap sv' + (' rev' if rev else '') + '"><div class="sv-img">' + img + '</div>'
            '<div class="sv-body"><span class="kicker">Service ' + n + '</span><h2>' + t + '</h2><p>' + intro + '</p><ul>' + li + '</ul></div></div></section>\n')
serv = (head('Nos services', 'Trois services pour organiser le transport de vos marchandises entre l\'Europe et l\'Afrique du Nord.')
 + sv('roro', '01', photo('carte-roro.jpg', 1200, 900, ALT_RORO), 'Transport maritime Ro-Ro', 'Véhicules, engins et marchandises roulantes embarqués par rampe.', ['<b>Véhicules, engins et marchandises roulantes</b>Embarquement par rampe.', '<b>Ports et hubs de référence</b>Tanger Med, Casablanca, Sète.'])
 + sv('routier', '02', photo('carte-routier.jpg', 1200, 900, ALT_ROUT), 'Transport routier', 'Fret par camion en Europe et en Afrique du Nord.', ['<b>Europe</b>France, Espagne, Italie.', '<b>Afrique du Nord</b>Maroc, Algérie.'], True, True)
 + sv('logistique', '03', photo('carte-logistique.jpg', 480, 360, ALT_LOG, True, 'ph cap'), 'Solutions logistiques', 'Les services qui accompagnent le transport.', ['<b>Affrètement</b>Moyens de transport adaptés au besoin.', '<b>Commission de transport</b>Organisation du transport pour le compte du client.', '<b>Dédouanement</b>Accompagnement dans les formalités douanières.', '<b>Stockage</b>Entreposage avant ou après transport.'])
 + cta())
page('services.html', 'Services – Transport maritime Ro-Ro, routier, logistique | MSI', 'Transport maritime Ro-Ro, transport routier et solutions logistiques (affrètement, commission de transport, dédouanement, stockage) avec MSI.', serv)

# ---------- Zones
zon = (head('Zones d\'intervention', 'De la France au Maroc et à l\'Algérie : les pays et les ports de référence de MSI.')
 + '<section class="sec"><div class="wrap"><span class="kicker">Schéma de principe</span><h2>Des flux entre deux rives</h2>'
 '<div class="flux" role="group" aria-label="Schéma de principe : de l\'Europe vers les ports et hubs, puis vers l\'Afrique du Nord">'
 '<div class="tier"><span class="kicker">Europe</span><ul><li>France</li><li>Espagne</li><li>Italie</li></ul></div><div class="tier-link" aria-hidden="true"></div>'
 '<div class="tier"><span class="kicker">Ports et hubs</span><ul><li>Sète</li><li>Tanger Med</li><li>Casablanca</li></ul></div><div class="tier-link" aria-hidden="true"></div>'
 '<div class="tier"><span class="kicker">Afrique du Nord</span><ul><li>Maroc</li><li>Algérie</li></ul></div></div>'
 '<p class="note">Schéma de principe, sans échelle : il n\'indique ni ligne, ni date, ni fréquence.</p></div></section>\n'
 '<section class="sec sky"><div class="wrap"><span class="kicker">Couloirs</span><h2>De la France au Maroc et à l\'Algérie</h2>'
 '<div class="cols"><div class="col"><h3>Europe</h3><ul><li>France</li><li>Espagne</li><li>Italie</li></ul></div>'
 '<div class="col"><h3>Afrique du Nord</h3><ul><li>Maroc</li><li>Algérie</li></ul></div>'
 '<div class="col"><h3>Ports et hubs</h3><ul><li>Tanger Med</li><li>Casablanca</li><li>Sète</li></ul></div></div></div></section>\n'
 + cta('Votre trajet n\'est pas listé ?', 'Décrivez-nous votre besoin, nous étudions votre demande.'))
page('zones.html', 'Zones d\'intervention – France, Maroc, Algérie | MSI', 'Zones desservies par MSI : France, Espagne, Italie, Maroc, Algérie, avec Tanger Med, Casablanca et Sète comme ports et hubs de référence.', zon)

# ---------- Contact
tels = '<a class="tel" href="tel:' + TEL + '"><small>Fixe</small>' + TEL_AFF + '</a>' + ''.join('<a class="tel" href="tel:%s"><small>Mobile</small>%s</a>' % (m.replace(' ', ''), m) for m in MOBILES)
con = (head('Parlons de votre transport', 'Décrivez votre besoin : nous préparons avec vous la meilleure solution entre l\'Europe et l\'Afrique du Nord.')
 + '<section class="sec" id="coordonnees"><div class="wrap"><span class="kicker">Nos bureaux</span><h2>Paris et Marseille</h2>'
 '<div class="offices"><div class="office"><h3>Siège social – Paris</h3><p>' + PARIS + ', France</p></div><div class="office"><h3>Bureau de Marseille</h3><p>' + MARSEILLE + ', France</p></div></div>'
 '<div class="plan">Plan à ajouter</div></div></section>\n'
 '<section class="sec sky"><div class="wrap"><span class="kicker">Joindre MSI</span><h2>Téléphone et e-mail</h2><div class="tels">' + tels + '</div>'
 '<div class="tels"><a class="tel" href="mailto:info@msi-prs.fr"><small>E-mail</small>info@msi-prs.fr</a><a class="tel" href="mailto:operations@msi-prs.fr"><small>Opérations</small>operations@msi-prs.fr</a></div></div></section>\n'
 '<section class="sec" id="devis"><div class="wrap devis"><div class="devis-side"><h2>Demander un devis</h2><p>Quelques lignes suffisent pour étudier votre demande.</p><ul class="steps-mini"><li>Décrivez votre trajet et vos marchandises</li><li>Envoyez-nous votre message</li><li>Nous revenons vers vous avec une proposition</li></ul></div><div class="form-card">\n'
 '<!-- À COMPLÉTER : data-email (info@msi-prs.fr) et data-tel (téléphone fixe) sont renseignés. data-sms est vide : indiquez un numéro mobile au format international pour afficher le bouton SMS.\n'
 '     Chaque bouton (e-mail, SMS, Appeler) n\'apparaît après l\'envoi que si l\'attribut correspondant est renseigné. -->\n'
 '<form class="form" id="devis-form" novalidate data-email="' + MAIL + '" data-sms="" data-tel="' + TEL + '">'
 '<div class="field"><label for="f-nom">Nom <span aria-hidden="true">*</span></label><input id="f-nom" autocomplete="name" aria-required="true" aria-describedby="f-nom-err"><p class="err" id="f-nom-err" role="alert"></p></div>'
 '<div class="field"><label for="f-soc">Société</label><input id="f-soc" autocomplete="organization"></div>'
 '<div class="field"><label for="f-tel">Téléphone</label><input id="f-tel" type="tel" autocomplete="tel" aria-describedby="f-tel-err"><p class="err" id="f-tel-err" role="alert"></p></div>'
 '<div class="field"><label for="f-mail">E-mail</label><input id="f-mail" type="email" autocomplete="email" aria-describedby="f-mail-err"><p class="err" id="f-mail-err" role="alert"></p></div>'
 '<div class="field full"><label for="f-besoin">Trajet ou besoin <span aria-hidden="true">*</span></label><input id="f-besoin" aria-required="true" placeholder="Ex. : véhicules, de Sète vers Tanger Med" aria-describedby="f-besoin-err"><p class="err" id="f-besoin-err" role="alert"></p></div>'
 '<div class="field full"><label for="f-msg">Message</label><textarea id="f-msg"></textarea></div>'
 '<p class="hint">* Obligatoire. Indiquez au moins un téléphone ou un e-mail pour vous répondre.</p>'
 '<button class="btn btn-primary" type="submit">Demander mon devis<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></form>\n'
 '<div class="out" id="devis-out" hidden><label for="out-msg"><b>Votre message est prêt</b></label><textarea id="out-msg" readonly></textarea>'
 '<div class="btns"><button class="btn btn-white" type="button" id="b-copy">Copier</button>'
 '<a class="btn btn-ghost" id="b-mail" href="#" hidden>Envoyer par e-mail</a><a class="btn btn-ghost" id="b-sms" href="#" hidden>SMS</a><a class="btn btn-ghost" id="b-tel" href="#" hidden>Appeler</a></div>'
 '<p id="out-live" role="status" style="margin:10px 0 0"></p></div></div></div></section>')
page('contact.html', 'Contact et devis – MSI', 'Contactez MSI à Paris ou Marseille pour organiser votre transport maritime Ro-Ro ou routier entre l\'Europe et l\'Afrique du Nord et demandez un devis.', con)

# ---------- Mentions légales
leg = (head('Mentions légales', 'Informations légales relatives au site de MSI – Société Internationale des Services de Transport.')
 + '<section class="sec"><div class="wrap legal"><h2>Éditeur du site</h2><p>MSI – Société Internationale des Services de Transport, société par actions simplifiée unipersonnelle (SASU).</p>'
 '<dl class="facts"><div><dt>SIREN</dt><dd>929 651 644</dd></div><div><dt>Siège social</dt><dd>' + PARIS + '</dd></div><div><dt>Bureau</dt><dd>' + MARSEILLE + '</dd></div><div><dt>E-mail</dt><dd>' + MAIL + '</dd></div><div><dt>Téléphone</dt><dd>' + TEL_AFF + '</dd></div>'
 '<div><dt>Responsable de la publication</dt><dd>JE EL Amari</dd></div><div><dt>Hébergeur</dt><dd class="tbd">À renseigner</dd></div></dl></div></section>\n'
 '<section class="sec sky"><div class="wrap legal"><h2>Données personnelles</h2><p>Le formulaire de contact ne transmet aucune donnée automatiquement : le message est préparé sur votre appareil, et c\'est vous qui choisissez de le copier ou de l\'envoyer.</p>'
 '<h2>Propriété intellectuelle</h2><p>Les textes, visuels et éléments graphiques de ce site sont la propriété de MSI ou utilisés avec autorisation. Toute reproduction sans accord préalable est interdite.</p></div></section>')
page('mentions-legales.html', 'Mentions légales – MSI', 'Mentions légales du site de MSI – Société Internationale des Services de Transport, SASU dont le siège est à Paris.', leg)

open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8').write(CSS.strip() + '\n')
open(os.path.join(OUT, 'script.js'), 'w', encoding='utf-8').write(JS)
open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write('# MSI – Société Internationale des Services de Transport\n\nMaquette de site vitrine (non contractuelle).\n\nPages : index, presentation, services, zones, contact, mentions-legales.\n')
print('ok', len(os.listdir(OUT)))
