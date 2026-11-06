#!/usr/bin/env python3
# Génère la maquette MSI (dossier msi-transport). Usage : python3 outils/gen_msi.py
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'msi-transport')
os.makedirs(OUT, exist_ok=True)

# À RENSEIGNER : remplacer par tel:+... quand le numéro est connu (bouton « Appeler » de l'en-tête et des sections)
TEL_HREF = 'contact.html#coordonnees'

CSS = r"""
:root{--nuit:#14161A;--nuit2:#262A31;--sable:#F6F3F1;--sable2:#ECE6E1;--ambre:#FF5A5F;--rouge:#C8161D;--corail:#C8161D;--ink:#1B1D21;--muted:#4A4F57;--soft:#D0D3D8;--r:18px}
*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none!important}
html{-webkit-text-size-adjust:100%;scroll-padding-top:84px}
body{margin:0;font:400 1.0625rem/1.65 'Manrope',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);background:var(--sable)}
img,svg{max-width:100%;display:block}
h1,h2,h3{font-family:'Fraunces',Georgia,serif;font-weight:700;line-height:1.14;margin:0 0 .5em;letter-spacing:-.01em}
h1{font-size:clamp(2.05rem,6vw,3.8rem)}
h2{font-size:clamp(1.7rem,4vw,2.6rem)}
h3{font-size:1.3rem}
p{margin:0 0 1em}
a{color:inherit}
.wrap{width:min(100% - 32px,1180px);margin-inline:auto}
:focus-visible{outline:3px solid var(--corail);outline-offset:3px}
.dark :focus-visible,.dark2 :focus-visible,.site-footer :focus-visible,.tier :focus-visible,.out :focus-visible{outline-color:var(--ambre)}
.skip-link{position:absolute;left:-999px;top:8px;background:var(--ambre);color:var(--nuit);padding:12px 16px;z-index:100;border-radius:8px;font-weight:800}
.skip-link:focus{left:8px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:48px;padding:.7rem 1.4rem;border-radius:999px;font:800 1rem/1.2 'Manrope',sans-serif;text-decoration:none;border:2px solid transparent;cursor:pointer;transition:transform .2s,background .2s}
.btn-primary{background:var(--rouge);color:#fff}
.btn-primary:hover{background:#A91117;transform:translateY(-2px)}
.btn-ghost{border-color:currentColor;color:#fff}
.btn-ghost:hover{background:rgba(255,255,255,.12)}
.btn-dark{background:var(--nuit);color:#fff}
.btn-dark:hover{background:var(--nuit2)}
.btn-line{border-color:var(--nuit);color:var(--nuit)}
.btn-line:hover{background:rgba(11,37,64,.08)}
/* En-tête */
.site-header{position:sticky;top:0;z-index:50;background:#fff;color:var(--ink);border-bottom:1px solid #E4DEDA}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:80px}
.logo{display:flex;align-items:center;gap:12px;text-decoration:none;min-height:48px;color:var(--ink)}
.logo img{height:64px;width:auto;flex:none;transition:transform .25s}
.logo:hover img{transform:scale(1.04)}
.logo small{display:none;flex-direction:column;gap:3px;padding-left:16px;border-left:1px solid #DDD6D0;font-size:1rem;line-height:1.15;color:var(--ink)}
.logo small b{font:700 1.15rem/1.1 'Fraunces',serif}
.logo small span{font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--rouge)}
.site-header .btn-ghost{color:var(--nuit);border-color:var(--nuit)}
.site-header .btn-ghost:hover{background:rgba(0,0,0,.06)}
.burger{width:48px;height:48px;border:0;border-radius:12px;background:transparent;color:var(--ink);cursor:pointer;display:grid;place-items:center}
.burger span,.burger span::before,.burger span::after{display:block;width:24px;height:2px;background:currentColor;position:relative;transition:.25s}
.burger span::before,.burger span::after{content:"";position:absolute;left:0}
.burger span::before{top:-7px}.burger span::after{top:7px}
.burger[aria-expanded=true] span{background:transparent}
.burger[aria-expanded=true] span::before{top:0;transform:rotate(45deg)}
.burger[aria-expanded=true] span::after{top:0;transform:rotate(-45deg)}
.menu{display:none;position:absolute;top:100%;left:0;right:0;background:#fff;padding:8px 16px 24px;border-top:1px solid #E4DEDA;box-shadow:0 12px 24px rgba(0,0,0,.12)}
.menu.open{display:block}
.menu ul{list-style:none;margin:0;padding:0}
.menu a.nl{display:flex;align-items:center;min-height:52px;padding:0 4px;text-decoration:none;font-weight:700;border-bottom:1px solid rgba(0,0,0,.1)}
.menu a[aria-current=page]{color:var(--rouge)}
.menu-ctas{display:grid;gap:10px;margin-top:16px}
.head-ctas{display:none}
@media(min-width:981px){
.burger,.menu-ctas{display:none}
.menu{display:block;position:static;background:none;padding:0;border:0;box-shadow:none}
.menu ul{display:flex;gap:2px}
.menu a.nl{border:0;padding:0 14px;border-radius:999px;min-height:44px}
.menu a.nl:hover{background:rgba(0,0,0,.06)}
.head-ctas{display:flex;gap:10px}
.head-ctas .btn{min-height:44px;padding:.5rem 1.1rem}
}
@media(min-width:1260px){.logo small{display:flex}.logo img{height:72px}.bar{min-height:88px}}
/* Sections */
.dark{background:var(--nuit);color:#fff}
.dark2{background:var(--nuit2);color:#fff}
.alt{background:var(--sable2)}
.sec{padding:clamp(32px,5.5vw,76px) 0}
.kicker{display:inline-block;font:800 1rem/1.3 'Manrope',sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--corail);margin-bottom:12px}
.dark .kicker,.dark2 .kicker{color:var(--ambre)}
.lede{font-size:1.15rem}
.dark .lede,.dark2 .lede{color:var(--soft)}
.hero{position:relative;overflow:hidden;padding:clamp(32px,6vw,80px) 0 0}
.hero-grid{display:grid;gap:20px;align-items:center}
.hero .lede{max-width:48ch}
.hero-ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:22px}
.tags{display:flex;flex-wrap:wrap;gap:8px;list-style:none;margin:22px 0 0;padding:0}
.tags li{border:1px solid rgba(255,255,255,.3);border-radius:999px;padding:4px 14px;font-weight:700}
.ph{display:block;width:100%;height:auto;border-radius:var(--r)}
.hero .ph{box-shadow:0 18px 40px rgba(0,0,0,.45)}
.waves{display:block;width:100%;height:clamp(40px,7vw,90px);margin-top:8px}
@media(min-width:981px){.hero-grid{grid-template-columns:1.05fr .95fr;gap:48px}}
.svc-list{list-style:none;margin:28px 0 0;padding:0;border-top:2px solid var(--nuit)}
.svc-row{display:grid;grid-template-columns:60px 1fr;grid-template-areas:"ico t" "ico d";gap:2px 18px;padding:20px 0;border-bottom:1px solid rgba(11,37,64,.25)}
.svc-num{display:none;grid-area:num;font:700 2.8rem/1 'Fraunces',serif;color:var(--corail)}
.svc-ico{grid-area:ico;width:60px;height:60px;border-radius:16px;background:var(--nuit);color:var(--ambre);display:grid;place-items:center}
.svc-ico svg{width:34px;height:34px}
.svc-t{grid-area:t;font-size:1.25rem;margin:0}
.svc-d{grid-area:d;margin:0;color:var(--muted)}
@media(min-width:981px){.svc-row{grid-template-columns:90px 72px 1fr 1.3fr;grid-template-areas:"num ico t d";align-items:center;gap:0 28px;padding:28px 0}.svc-num{display:block}.svc-ico{width:72px;height:72px}.svc-ico svg{width:40px;height:40px}.svc-t{font-size:1.5rem}}
.more{margin-top:24px}
.eng{display:grid;gap:24px}
.eng-item{padding:16px 0;border-top:1px solid rgba(255,255,255,.22)}
.eng-item h3{color:var(--ambre);margin-bottom:.2em}
.eng-item p{color:var(--soft);margin:0}
@media(min-width:981px){.eng{grid-template-columns:1fr 1.1fr;gap:72px}}
.steps{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:12px;counter-reset:s}
.steps li{background:#fff;border-radius:var(--r);padding:16px 18px 16px 76px;position:relative}
.steps li::before{counter-increment:s;content:counter(s);position:absolute;left:18px;top:16px;width:42px;height:42px;border-radius:50%;background:var(--nuit);color:var(--ambre);font:700 1.3rem/42px 'Fraunces',serif;text-align:center}
.steps h3{font-size:1.2rem;margin:0 0 .15em}
.steps p{margin:0;color:var(--muted)}
@media(min-width:700px){.steps{grid-template-columns:repeat(2,1fr)}}
@media(min-width:981px){.steps{grid-template-columns:repeat(4,1fr);gap:18px}.steps li{padding:78px 20px 24px}.steps li::before{left:20px;top:20px}}
.split{display:grid;gap:22px}
@media(min-width:981px){.split{grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
.ports{display:grid;gap:10px;margin-top:8px}
.port{border:1px solid rgba(255,255,255,.28);border-radius:var(--r);padding:14px 20px;display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.port b{font:700 1.4rem/1.2 'Fraunces',serif}
.port span{color:var(--soft)}
.cta{background:var(--rouge);color:#fff}
.cta .btn-line{border-color:#fff;color:#fff}
.cta .btn-line:hover{background:rgba(255,255,255,.14)}
.cta-in{display:grid;gap:18px;align-items:center}
.cta h2{margin:0 0 .3em}
.cta p{margin:0}
.btns{display:flex;flex-wrap:wrap;gap:12px}
@media(min-width:981px){.cta-in{grid-template-columns:1.4fr 1fr}.cta .btns{justify-self:end}}
/* Pages internes */
.page-head{padding:clamp(32px,5vw,64px) 0 clamp(36px,5.5vw,68px)}
.page-head .lede{max-width:60ch;margin:0}
.facts{display:grid;gap:0;margin:0}
.facts div{display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-top:1px solid rgba(11,37,64,.2)}
.facts dt{font-weight:800;color:var(--corail)}
.facts dd{margin:0;text-align:right}
.big{font:500 clamp(1.4rem,3.4vw,2.3rem)/1.35 'Fraunces',serif;max-width:28em;margin:0}
.vals{display:grid;gap:14px;margin-top:26px}
.val{background:#fff;border-radius:var(--r);padding:20px 22px}
.val h3{color:var(--corail);margin-bottom:.25em}
.val p{margin:0;color:var(--muted)}
@media(min-width:700px){.vals{grid-template-columns:repeat(3,1fr)}}
.sv{display:grid;gap:20px;align-items:stretch}
.sv-ico{align-self:center}
.sv-body ul{list-style:none;padding:0;margin:14px 0 0;display:grid;gap:10px}
.sv-body li{padding-left:28px;position:relative}
.sv-body li::before{content:"";position:absolute;left:0;top:.8em;width:14px;height:3px;background:var(--corail)}
.sv-body li b{display:block}
@media(min-width:700px){.sv{grid-template-columns:.8fr 1.4fr;gap:40px}.sv.rev{grid-template-columns:1.4fr .8fr}.sv.rev .sv-ico{order:2}}
.flux{display:grid;margin-top:26px}
.tier{background:var(--nuit);color:#fff;border-radius:var(--r);padding:18px 20px}
.tier .kicker{color:var(--ambre);margin-bottom:8px}
.tier ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.tier li{background:rgba(255,255,255,.12);border-radius:999px;padding:4px 16px;font-weight:700}
.tier-link{height:48px;position:relative}
.tier-link::before{content:"";position:absolute;left:50%;top:6px;bottom:12px;border-left:3px dashed var(--corail);transform:translateX(-50%)}
.tier-link::after{content:"";position:absolute;left:50%;bottom:6px;width:12px;height:12px;border-right:3px solid var(--corail);border-bottom:3px solid var(--corail);transform:translateX(-50%) rotate(45deg)}
@media(min-width:981px){.flux{grid-template-columns:1fr 72px 1fr 72px 1fr}.tier{display:flex;flex-direction:column;justify-content:center;padding:26px}.tier-link{height:auto}.tier-link::before{left:6px;right:14px;top:50%;bottom:auto;border-left:0;border-top:3px dashed var(--corail);transform:translateY(-50%)}.tier-link::after{left:auto;right:6px;top:50%;bottom:auto;transform:translateY(-50%) rotate(-45deg)}}
.note{color:var(--muted);margin:18px 0 0}
.cols{display:grid;gap:14px;margin-top:24px}
.col{background:#fff;border-radius:var(--r);padding:18px 22px}
.col h3{color:var(--corail);margin-bottom:.3em}
.col ul{margin:0;padding:0;list-style:none}
.col li{padding:6px 0;border-top:1px solid rgba(11,37,64,.15);font-weight:600}
@media(min-width:700px){.cols{grid-template-columns:repeat(3,1fr)}}
.coord{display:grid;gap:12px;margin:22px 0 0}
.coord div{background:#fff;border-radius:var(--r);padding:12px 20px}
.coord dt{font-weight:800;color:var(--corail)}
.coord dd{margin:0;color:var(--muted)}
.plan{margin-top:14px;border:2px dashed rgba(11,37,64,.4);border-radius:var(--r);min-height:96px;display:grid;place-items:center;color:var(--muted);font-weight:700}
@media(min-width:700px){.coord{grid-template-columns:repeat(3,1fr)}}
.tbd{color:var(--muted);font-style:italic}
.devis{display:grid;gap:16px;align-items:start}
.devis-side p{color:var(--muted);margin:0}
.steps-mini{display:none;list-style:none;margin:20px 0 0;padding:0;counter-reset:m}
.steps-mini li{counter-increment:m;position:relative;padding:12px 0 12px 46px;border-top:1px solid rgba(255,255,255,.18)}
.steps-mini li::before{content:counter(m);position:absolute;left:0;top:10px;width:32px;height:32px;border-radius:50%;background:var(--rouge);color:#fff;font:700 1rem/32px 'Fraunces',serif;text-align:center}
.form-card{background:#fff;border-radius:22px;padding:16px;box-shadow:0 20px 50px rgba(20,22,26,.12);border-top:5px solid var(--rouge)}
.form{display:grid;gap:12px}
.field{display:grid;gap:4px}
.field label{font-weight:700}
.field label span{color:var(--rouge)}
.field input,.field textarea{width:100%;min-height:48px;padding:10px 14px 10px 46px;border:1.5px solid #8A8F98;border-radius:12px;font:inherit;background-color:#FBFAF9;background-repeat:no-repeat;background-position:14px center;background-size:20px;color:var(--ink);transition:border-color .2s,box-shadow .2s,background-color .2s}
.field textarea{padding-left:14px;min-height:90px;resize:vertical}
.field input:hover,.field textarea:hover{border-color:var(--nuit)}
.field input:focus,.field textarea:focus{border-color:var(--rouge);background-color:#fff;box-shadow:0 0 0 4px rgba(200,22,29,.18)}
#f-nom{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4 4-7 8-7s8 3 8 7'/%3E%3C/svg%3E")}
#f-soc{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='5' y='3' width='14' height='18' rx='1'/%3E%3Cpath d='M9 8h2M13 8h2M9 12h2M13 12h2M10 21v-4h4v4'/%3E%3C/svg%3E")}
#f-tel{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z'/%3E%3C/svg%3E")}
#f-mail{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='5' width='18' height='14' rx='2'/%3E%3Cpath d='M3 7l9 6 9-6'/%3E%3C/svg%3E")}
#f-besoin{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236B7280' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z'/%3E%3Ccircle cx='12' cy='10' r='2.5'/%3E%3C/svg%3E")}
.field input::placeholder,.field textarea::placeholder{color:#5B6773}
.field.bad input,.field.bad textarea{border-color:#9C2A0F;background-color:#FFF6F4}
.err{color:#9C2A0F;font-weight:700;margin:0}
.err:empty{display:none}
.hint{display:none;margin:0;color:var(--muted)}
.form .btn{width:100%;min-height:52px;font-size:1.05rem}
.form .btn svg{width:20px;height:20px;transition:transform .2s}
.form .btn:hover svg{transform:translateX(4px)}
@media(min-width:700px){
.devis-side{background:var(--nuit);color:#fff;border-radius:var(--r);padding:26px 28px}
.devis-side p{color:var(--soft)}
.steps-mini{display:block}
.form-card{padding:30px}
.form{grid-template-columns:1fr 1fr;gap:18px}
.field.full,.hint,.form .btn{grid-column:1/-1}
.hint{display:block}
.form .btn{width:auto;justify-self:start;min-width:280px}
}
@media(min-width:981px){.devis{grid-template-columns:.75fr 1.4fr;gap:32px}.devis-side{position:sticky;top:104px;padding:34px}.form-card{padding:38px}}
.out{margin-top:22px;background:var(--nuit);color:#fff;border-radius:var(--r);padding:20px}
.out textarea{width:100%;min-height:190px;background:rgba(255,255,255,.08);color:#fff;border:1px solid rgba(255,255,255,.3);border-radius:12px;padding:12px;font:inherit}
.out .btns{margin-top:14px}
.legal{max-width:760px}
.legal h2{font-size:1.5rem}
.legal .facts div{border-color:rgba(11,37,64,.2)}
/* Pied de page */
.site-footer{background:var(--nuit);color:var(--soft);padding:14px 0}
.foot{display:grid;gap:6px}
.foot-brand{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.foot-brand b{font:700 1.4rem/1.2 'Fraunces',serif;color:#fff}
.foot nav ul{list-style:none;margin:0 0 0 -8px;padding:0;display:flex;flex-wrap:wrap}
.foot nav a{display:inline-flex;align-items:center;min-height:44px;padding:0 8px;text-decoration:none;color:#fff;font-weight:600}
.foot nav a:hover{color:var(--ambre)}
.foot p{margin:0}
@media(min-width:981px){.foot{grid-template-columns:auto 1fr auto;align-items:center;gap:32px}.foot nav ul{justify-content:center}}
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

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14161A"/><path d="M10 44q11-14 22 0t22 0" fill="none" stroke="#FF5A5F" stroke-width="5" stroke-linecap="round"/><path d="M14 26q18-16 36 0" fill="none" stroke="#F6F3F1" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 10"/></svg>"""

MARK = '<svg viewBox="0 0 36 36" aria-hidden="true"><rect width="36" height="36" rx="9" fill="#C8161D"/><path d="M5 24q6.5-8 13 0t13 0" fill="none" stroke="#FF5A5F" stroke-width="2.8" stroke-linecap="round"/><path d="M8 14q10-8 20 0" fill="none" stroke="#F6F3F1" stroke-width="2.8" stroke-linecap="round" stroke-dasharray="1 6"/></svg>'

def ico(body):
    return '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>'

SHIP = ico('<path d="M6 40h52l-7 14H13z" fill="currentColor" fill-opacity=".28"/><path d="M14 40V22h28v18"/><path d="M42 40V30h10v10"/><path d="M20 31h16" stroke-dasharray="3 5"/><path d="M4 59q4-3 8 0t8 0 8 0 8 0 8 0 8 0 8 0" stroke-opacity=".55"/>')
TRUCK = ico('<path d="M4 18h34v28H4z" fill="currentColor" fill-opacity=".28"/><path d="M38 28h12l10 10v8H38z" fill="currentColor" fill-opacity=".28"/><path d="M42 32h7l5 6H42z"/><circle cx="17" cy="48" r="5" fill="#14161A"/><circle cx="49" cy="48" r="5" fill="#14161A"/><path d="M2 58h60" stroke-opacity=".5" stroke-dasharray="6 5"/>')
BOX = ico('<path d="M8 26l24-12 24 12-24 12z" fill="currentColor" fill-opacity=".4"/><path d="M8 26v20l24 12V38z" fill="currentColor" fill-opacity=".15"/><path d="M56 26v20L32 58V38z" fill="currentColor" fill-opacity=".28"/><path d="M20 20l24 12"/>')

def photo(f, w, h, alt, lazy=True):
    return '<img class="ph" src="' + f + '" width="' + str(w) + '" height="' + str(h) + '" alt="' + alt + '"' + (' loading="lazy"' if lazy else '') + '>'
HERO_IMG = photo('hero-roro.jpg', 1376, 768, 'Navire Ro-Ro à quai, rampe arrière abaissée, dans un port méditerranéen au coucher du soleil', False)
PH_RORO = photo('service-roro.jpg', 1264, 848, 'Camions et véhicules embarquant par la rampe d\'un navire Ro-Ro dans un port')
PH_ROUTIER = photo('service-routier.jpg', 1264, 848, 'Camion blanc avec semi-remorque sur une route côtière méditerranéenne')
PH_LOG = photo('service-logistique.jpg', 1264, 848, 'Piles de conteneurs et portique sur un terminal portuaire')
PH_PORT = photo('port-presentation.jpg', 1376, 768, 'Port de commerce méditerranéen avec navire de charge à quai et grues portuaires')

WAVES = '<svg class="waves" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path fill="#C8161D" d="M0 30C240 0 480 70 720 30S1200 0 1440 40V90H0Z"/><path fill="#F6F3F1" d="M0 50C240 90 480 10 720 50S1200 90 1440 40V90H0Z"/></svg>'

NAV = [('index.html', 'Accueil'), ('presentation.html', 'Présentation'), ('services.html', 'Services'), ('zones.html', 'Zones'), ('contact.html', 'Contact')]

def page(fn, title, desc, body, cls=''):
    lis = ''.join('<li><a class="nl" href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h == fn else '', t) for h, t in NAV)
    fl = ''.join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV) + '<li><a href="mentions-legales.html">Mentions légales</a></li>'
    html = ('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>' + title + '</title><meta name="description" content="' + desc + '"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#14161A">'
        '<link rel="icon" href="favicon.png" type="image/png" sizes="64x64"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&amp;family=Manrope:wght@400;600;800&amp;display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head><body>\n'
        '<a class="skip-link" href="#contenu">Aller au contenu</a>\n'
        '<header class="site-header"><div class="wrap bar"><a class="logo" href="index.html" aria-label="MSI, accueil"><img src="logo-msi.jpg" width="973" height="1307" alt="MSI"><small><b>Méditerranéenne</b><span>Service Ligne</span></small></a>\n'
        '<button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span></button>\n'
        '<nav class="menu" id="menu" aria-label="Navigation principale"><ul>' + lis + '</ul>'
        '<div class="menu-ctas"><a class="btn btn-ghost" href="' + TEL_HREF + '">Appeler</a><a class="btn btn-primary" href="contact.html#devis">Demander un devis</a></div></nav>\n'
        '<!-- À RENSEIGNER : remplacer le href du bouton « Appeler » par tel:+... (ici et dans le menu mobile) quand le numéro est connu -->\n'
        '<div class="head-ctas"><a class="btn btn-ghost head-call" href="' + TEL_HREF + '">Appeler</a><a class="btn btn-primary" href="contact.html#devis">Devis</a></div></div></header>\n'
        '<main id="contenu">\n' + body + '\n</main>\n'
        '<footer class="site-footer"><div class="wrap foot"><div class="foot-brand"><b>MSI</b><span>Méditerranéenne Service Ligne</span></div>'
        '<nav aria-label="Pied de page"><ul>' + fl + '</ul></nav><p>SASU · siège à Paris</p></div></footer>\n</body></html>\n')
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(html)

def cta(h='Un transport à organiser ?', p='Parlez-nous de votre trajet et de vos marchandises.'):
    return ('<section class="cta sec"><div class="wrap cta-in"><div><h2>' + h + '</h2><p>' + p + '</p></div>'
            '<div class="btns"><a class="btn btn-line" href="' + TEL_HREF + '">Appeler</a><a class="btn btn-dark" href="contact.html#devis">Demander un devis</a></div></div></section>')

def head(h1, lede):
    return '<section class="page-head dark"><div class="wrap"><h1>' + h1 + '</h1><p class="lede">' + lede + '</p></div></section>'

def row(n, i, t, d):
    return '<li class="svc-row reveal"><span class="svc-num">' + n + '</span><span class="svc-ico">' + i + '</span><h3 class="svc-t">' + t + '</h3><p class="svc-d">' + d + '</p></li>'

# ---------- Accueil
home = ('<section class="hero dark"><div class="wrap hero-grid"><div><span class="kicker">Liaison Europe – Afrique du Nord fiable et régulière</span>'
 '<h1>Vos marchandises, de l\'Europe à l\'Afrique du Nord</h1>'
 '<p class="lede">MSI organise le transport de vos marchandises par mer et par route entre la France, l\'Espagne, l\'Italie, le Maroc et l\'Algérie.</p>'
 '<div class="hero-ctas"><a class="btn btn-ghost" href="' + TEL_HREF + '">Appeler</a><a class="btn btn-primary" href="contact.html#devis">Demander un devis</a></div>'
 '<ul class="tags"><li>Maritime Ro-Ro</li><li>Routier</li><li>Logistique</li></ul></div>' + HERO_IMG + '</div>' + WAVES + '</section>\n'
 '<section class="sec" id="services"><div class="wrap"><span class="kicker">Nos services</span><h2>Trois savoir-faire, un même objectif</h2>'
 '<ul class="svc-list">'
 + row('01', SHIP, 'Transport maritime Ro-Ro', 'Véhicules et marchandises roulantes embarqués par rampe.')
 + row('02', TRUCK, 'Transport routier', 'Fret par camion en Europe et en Afrique du Nord.')
 + row('03', BOX, 'Solutions logistiques', 'Affrètement, commission de transport, dédouanement, stockage.')
 + '</ul><div class="more"><a class="btn btn-line" href="services.html">Détail des services</a></div></div></section>\n'
 '<section class="sec dark2"><div class="wrap eng"><div><span class="kicker">Nos engagements</span><h2>Un partenaire pour relier les deux rives</h2></div><div>'
 '<div class="eng-item reveal"><h3>Fiabilité</h3><p>Des engagements tenus et un transport organisé avec rigueur.</p></div>'
 '<div class="eng-item reveal"><h3>Clarté</h3><p>Une information claire à chaque étape, des échanges simples.</p></div>'
 '<div class="eng-item reveal"><h3>Réactivité</h3><p>Une réponse adaptée à chaque demande, des formalités anticipées.</p></div></div></div></section>\n'
 '<section class="sec alt"><div class="wrap"><span class="kicker">Méthode</span><h2>Du besoin à la livraison, quatre étapes</h2><ol class="steps">'
 '<li class="reveal"><h3>Votre besoin</h3><p>Marchandises, trajet, contraintes.</p></li>'
 '<li class="reveal"><h3>Le bon mode</h3><p>Mer, route, ou les deux.</p></li>'
 '<li class="reveal"><h3>L\'organisation</h3><p>Affrètement, formalités, documents.</p></li>'
 '<li class="reveal"><h3>L\'acheminement</h3><p>Prise en charge puis livraison.</p></li></ol></div></section>\n'
 '<section class="sec dark"><div class="wrap split"><div><span class="kicker">Zones d\'intervention</span><h2>De la France au Maroc et à l\'Algérie</h2>'
 '<p class="lede">Des liaisons entre l\'Europe et l\'Afrique du Nord, appuyées sur des ports et hubs de référence.</p><a class="btn btn-primary" href="zones.html">Voir les zones</a></div>'
 '<div class="ports"><div class="port"><b>Sète</b><span>France</span></div><div class="port"><b>Tanger Med</b><span>Maroc</span></div><div class="port"><b>Casablanca</b><span>Maroc</span></div></div></div></section>\n'
 + cta())
page('index.html', 'MSI – Transport maritime Ro-Ro et routier Europe – Afrique du Nord', 'MSI, transporteur basé à Paris : transport maritime Ro-Ro, routier et solutions logistiques entre la France, l\'Espagne, l\'Italie, le Maroc et l\'Algérie.', home)

# ---------- Présentation
pres = (head('Une société née pour relier les deux rives', 'MSI – Méditerranéenne Service Ligne organise le transport de marchandises par route et par mer entre l\'Europe et l\'Afrique du Nord.')
 + '<section class="sec"><div class="wrap split"><div><span class="kicker">Historique</span><h2>Créée en 2024, installée à Paris</h2>'
 '<p>MSI est une société par actions simplifiée unipersonnelle (SASU). Elle a été créée en 2024 et son siège est à Paris.</p><p>Son objet : l\'affrètement et l\'organisation de transports maritimes, terrestres et aériens, avec un point d\'ancrage sur les liaisons Europe – Afrique du Nord.</p></div>'
 '<dl class="facts"><div><dt>Forme</dt><dd>SASU</dd></div><div><dt>Création</dt><dd>2024</dd></div><div><dt>Siège</dt><dd>Paris</dd></div><div><dt>Activité</dt><dd>Transport de marchandises par route et par mer</dd></div></dl></div></section>\n'
 '<section class="sec dark2"><div class="wrap split"><div><span class="kicker">Mission</span><p class="big">Relier l\'Europe et l\'Afrique du Nord par des solutions de transport maritime et routier, organisées pour répondre aux besoins de chaque client.</p></div>' + PH_PORT + '</div></section>\n'
 '<section class="sec"><div class="wrap"><span class="kicker">Valeurs</span><h2>Ce qui guide notre façon de travailler</h2><div class="vals">'
 '<div class="val reveal"><h3>Fiabilité</h3><p>Tenir ses engagements et organiser chaque transport avec rigueur.</p></div>'
 '<div class="val reveal"><h3>Transparence</h3><p>Une information claire, des échanges directs et sans ambiguïté.</p></div>'
 '<div class="val reveal"><h3>Réactivité</h3><p>Anticiper les formalités et répondre vite aux demandes.</p></div></div></div></section>\n'
 '<section class="sec alt"><div class="wrap"><span class="kicker">Spécialisation</span><h2>Maritime Ro-Ro, routier, logistique</h2>'
 '<p class="lede" style="max-width:60ch">Trois expertises complémentaires pour couvrir le transport de bout en bout, sur un axe géographique précis.</p>'
 '<div class="cols"><div class="col"><h3>Europe</h3><ul><li>France</li><li>Espagne</li><li>Italie</li></ul></div>'
 '<div class="col"><h3>Afrique du Nord</h3><ul><li>Maroc</li><li>Algérie</li></ul></div>'
 '<div class="col"><h3>Ports et hubs</h3><ul><li>Tanger Med</li><li>Casablanca</li><li>Sète</li></ul></div></div></div></section>\n'
 + cta())
page('presentation.html', 'Présentation – MSI, transport Europe – Afrique du Nord', 'MSI, SASU créée en 2024 et basée à Paris : mission, valeurs et spécialisation en transport maritime Ro-Ro, routier et logistique.', pres)

# ---------- Services
def sv(n, i, t, intro, items, alt=False, rev=False):
    li = ''.join('<li>' + x + '</li>' for x in items)
    return ('<section class="sec' + (' alt' if alt else '') + '"><div class="wrap sv' + (' rev' if rev else '') + '"><div class="sv-ico">' + i + '</div>'
            '<div class="sv-body"><span class="kicker">Service ' + n + '</span><h2>' + t + '</h2><p>' + intro + '</p><ul>' + li + '</ul></div></div></section>\n')
serv = (head('Nos services', 'Trois services pour organiser le transport de vos marchandises entre l\'Europe et l\'Afrique du Nord.')
 + sv('01', PH_RORO,'Transport maritime Ro-Ro', 'Véhicules et marchandises roulantes embarqués par rampe.', ['<b>Véhicules et marchandises roulantes</b>Embarquement par rampe.', '<b>Ports et hubs de référence</b>Tanger Med, Casablanca, Sète.'])
 + sv('02', PH_ROUTIER,'Transport routier', 'Fret par camion en Europe et en Afrique du Nord.', ['<b>Europe</b>France, Espagne, Italie.', '<b>Afrique du Nord</b>Maroc, Algérie.'], True, True)
 + sv('03', PH_LOG,'Solutions logistiques', 'Les services qui accompagnent le transport.', ['<b>Affrètement</b>Moyens de transport adaptés au besoin.', '<b>Commission de transport</b>Organisation du transport pour le compte du client.', '<b>Dédouanement</b>Accompagnement dans les formalités douanières.', '<b>Stockage</b>Entreposage avant ou après transport.'])
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
 '<section class="sec alt"><div class="wrap"><span class="kicker">Couloirs</span><h2>De la France au Maroc et à l\'Algérie</h2>'
 '<div class="cols"><div class="col"><h3>Europe</h3><ul><li>France</li><li>Espagne</li><li>Italie</li></ul></div>'
 '<div class="col"><h3>Afrique du Nord</h3><ul><li>Maroc</li><li>Algérie</li></ul></div>'
 '<div class="col"><h3>Ports et hubs</h3><ul><li>Tanger Med</li><li>Casablanca</li><li>Sète</li></ul></div></div></div></section>\n'
 + cta('Votre trajet n\'est pas listé ?', 'Décrivez-nous votre besoin, nous étudions votre demande.'))
page('zones.html', 'Zones d\'intervention – France, Maroc, Algérie | MSI', 'Zones desservies par MSI : France, Espagne, Italie, Maroc, Algérie, avec Tanger Med, Casablanca et Sète comme ports et hubs de référence.', zon)

# ---------- Contact
con = (head('Parlons de votre transport', 'Décrivez votre besoin : nous préparons avec vous la meilleure solution entre l\'Europe et l\'Afrique du Nord.')
 + '<section class="sec" id="coordonnees"><div class="wrap"><h2>Coordonnées à renseigner</h2>'
 '<dl class="coord"><div><dt>Adresse</dt><dd class="tbd">À renseigner</dd></div><div><dt>Téléphone</dt><dd class="tbd">À renseigner</dd></div><div><dt>E-mail</dt><dd class="tbd">À renseigner</dd></div></dl>'
 '<div class="plan">Plan à ajouter</div></div></section>\n'
 '<section class="sec alt" id="devis"><div class="wrap devis"><div class="devis-side"><h2>Demander un devis</h2><p>Décrivez votre trajet et vos marchandises.</p><ul class="steps-mini"><li>Remplissez le formulaire</li><li>Copiez le message ou envoyez-le</li><li>Rien n\'est transmis automatiquement</li></ul></div><div class="form-card">\n'
 '<!-- À COMPLÉTER : renseignez les attributs data-email (votre adresse e-mail), data-sms (numéro mobile, format international) et data-tel (numéro de téléphone) du formulaire ci-dessous.\n'
 '     Les boutons « Envoyer par e-mail », « SMS » et « Appeler » n\'apparaissent après l\'envoi que si l\'attribut correspondant est renseigné. Laissés vides, seul « Copier » est proposé. -->\n'
 '<form class="form" id="devis-form" novalidate data-email="" data-sms="" data-tel="">'
 '<div class="field"><label for="f-nom">Nom <span aria-hidden="true">*</span></label><input id="f-nom" autocomplete="name" aria-required="true" aria-describedby="f-nom-err"><p class="err" id="f-nom-err" role="alert"></p></div>'
 '<div class="field"><label for="f-soc">Société</label><input id="f-soc" autocomplete="organization"></div>'
 '<div class="field"><label for="f-tel">Téléphone</label><input id="f-tel" type="tel" autocomplete="tel" aria-describedby="f-tel-err"><p class="err" id="f-tel-err" role="alert"></p></div>'
 '<div class="field"><label for="f-mail">E-mail</label><input id="f-mail" type="email" autocomplete="email" aria-describedby="f-mail-err"><p class="err" id="f-mail-err" role="alert"></p></div>'
 '<div class="field full"><label for="f-besoin">Trajet ou besoin <span aria-hidden="true">*</span></label><input id="f-besoin" aria-required="true" placeholder="Ex. : véhicules, de Sète vers Tanger Med" aria-describedby="f-besoin-err"><p class="err" id="f-besoin-err" role="alert"></p></div>'
 '<div class="field full"><label for="f-msg">Message</label><textarea id="f-msg"></textarea></div>'
 '<p class="hint">* Obligatoire. Indiquez au moins un téléphone ou un e-mail pour vous répondre.</p><button class="btn btn-primary" type="submit">Demander mon devis<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button></form>\n'
 '<div class="out" id="devis-out" hidden><label for="out-msg"><b>Votre message est prêt</b></label><textarea id="out-msg" readonly></textarea>'
 '<div class="btns"><button class="btn btn-primary" type="button" id="b-copy">Copier</button>'
 '<a class="btn btn-ghost" id="b-mail" href="#" hidden>Envoyer par e-mail</a><a class="btn btn-ghost" id="b-sms" href="#" hidden>SMS</a><a class="btn btn-ghost" id="b-tel" href="#" hidden>Appeler</a></div>'
 '<p id="out-live" role="status" style="margin:10px 0 0"></p></div></div></div></section>')
page('contact.html', 'Contact et devis – MSI', 'Contactez MSI pour organiser votre transport maritime Ro-Ro ou routier entre l\'Europe et l\'Afrique du Nord et demandez un devis.', con)

# ---------- Mentions légales
leg = (head('Mentions légales', 'Informations légales relatives au site de MSI – Méditerranéenne Service Ligne.')
 + '<section class="sec"><div class="wrap legal"><h2>Éditeur du site</h2><p>MSI – Méditerranéenne Service Ligne, société par actions simplifiée unipersonnelle (SASU), siège à Paris.</p>'
 '<dl class="facts"><div><dt>SIREN</dt><dd class="tbd">À renseigner</dd></div><div><dt>Adresse du siège</dt><dd class="tbd">À renseigner</dd></div><div><dt>Directeur de la publication</dt><dd class="tbd">À renseigner</dd></div><div><dt>Hébergeur</dt><dd class="tbd">À renseigner</dd></div></dl></div></section>\n'
 '<section class="sec alt"><div class="wrap legal"><h2>Données personnelles</h2><p>Le formulaire de contact ne transmet aucune donnée automatiquement : le message est préparé sur votre appareil, et c\'est vous qui choisissez de le copier ou de l\'envoyer.</p>'
 '<h2>Propriété intellectuelle</h2><p>Les textes, visuels et éléments graphiques de ce site sont la propriété de MSI ou utilisés avec autorisation. Toute reproduction sans accord préalable est interdite.</p></div></section>')
page('mentions-legales.html', 'Mentions légales – MSI', 'Mentions légales du site de MSI – Méditerranéenne Service Ligne, SASU dont le siège est à Paris.', leg)

open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8').write(CSS.strip() + '\n')
open(os.path.join(OUT, 'script.js'), 'w', encoding='utf-8').write(JS)
# logo-msi.jpg et favicon.png : issus du logo fourni (recadrage + optimisation faits hors générateur)
open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write('# MSI – Méditerranéenne Service Ligne\n\nMaquette de site vitrine (non contractuelle).\n\nPages : index, presentation, services, zones, contact, mentions-legales.\n')
print('ok', len(os.listdir(OUT)))
