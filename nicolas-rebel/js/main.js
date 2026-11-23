(function(){var b=document.querySelector('.burger'),m=document.getElementById('menu');if(!b||!m)return;
function c(){m.classList.remove('open');b.setAttribute('aria-expanded','false')}
b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
m.addEventListener('click',function(e){if(e.target.closest('a'))c()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')c()});
window.addEventListener('resize',function(){if(innerWidth>980)c()})})();
(function(){var f=document.getElementById('f');if(!f)return;
var rules={nom:function(v){return v.trim().length>=2||'Indiquez votre nom.'},tel:function(v){return /^(?:(?:\+|00)33|0)\s?[1-9](?:[\s.-]?\d{2}){4}$/.test(v.trim())||'Indiquez un numéro valide, par exemple 06 33 36 31 17.'},com:function(v){return v.trim().length>=2||'Indiquez votre commune.'},bes:function(v){return v!==''||'Choisissez un besoin.'}};
function chk(k){var el=f.elements[k],r=rules[k](el.value),e=document.getElementById('e-'+k),w=el.closest('.field');
if(r===true){e.textContent='';w.classList.remove('bad');el.removeAttribute('aria-invalid');return true}
e.textContent=r;w.classList.add('bad');el.setAttribute('aria-invalid','true');return false}
Object.keys(rules).forEach(function(k){f.elements[k].addEventListener('blur',function(){chk(k)})});
f.addEventListener('submit',function(ev){ev.preventDefault();var ok=true,first=null;Object.keys(rules).forEach(function(k){if(!chk(k)){ok=false;first=first||f.elements[k]}});
if(!ok){first.focus();return}
var t='Bonjour, demande de devis Nicolas Rebel (Fleur de Vie Paysages).\nNom : '+f.nom.value.trim()+'\nTéléphone : '+f.tel.value.trim()+'\nCommune : '+f.com.value.trim()+'\nBesoin : '+f.bes.value+(f.msg.value.trim()?'\nMessage : '+f.msg.value.trim():'');
var r=document.getElementById('recap');document.getElementById('txt').textContent=t;
document.getElementById('sms').href='sms:+33633363117?&body='+encodeURIComponent(t);r.hidden=false;r.focus();r.scrollIntoView({behavior:'smooth',block:'center'})});
document.getElementById('copy').addEventListener('click',function(){var t=document.getElementById('txt').textContent,m=document.getElementById('cm');
function d(s){m.textContent=s}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){d('Message copié.')},function(){d('Copie impossible : sélectionnez le texte.')})}else{d('Copie impossible : sélectionnez le texte.')}})})();
