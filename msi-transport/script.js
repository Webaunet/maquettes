(function(){
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
