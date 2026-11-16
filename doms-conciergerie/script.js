(function(){
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
