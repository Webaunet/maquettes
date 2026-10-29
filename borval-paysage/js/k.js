(function(){var f=document.getElementById('kform');if(!f)return;
var done=f.parentNode.querySelector('.sk-done'),sum=done.querySelector('.sk-sum'),D=f.dataset;
var re=/^(?:\+33|0033|0)[1-9](?:[\s.-]?\d{2}){4}$/;
function err(el,m){var e=document.getElementById(el.id+'-e');e.textContent=m;if(m)el.setAttribute('aria-invalid','true');else el.removeAttribute('aria-invalid');return !m}
function ok(){var bad=null,els=f.querySelectorAll('input,select,textarea');
els.forEach(function(el){var v=el.value.trim(),m='';
if(el.required&&!v)m='Ce champ est obligatoire.';else if(el.type==='tel'&&v&&!re.test(v))m='Numéro de téléphone invalide.';
err(el,m);if(m&&!bad)bad=el});
if(bad){bad.focus();return false}return true}
f.addEventListener('submit',function(e){e.preventDefault();if(!ok())return;
var g=function(n){return f.elements[n].value.trim()};
var t='Demande de devis via le site de '+(D.name||'')+'\nNom : '+g('nom')+'\nTéléphone : '+g('tel')+'\nCommune : '+g('commune')+'\nBesoin : '+g('besoin')+(g('msg')?'\nMessage : '+g('msg'):'');
sum.textContent=t;
done.querySelector('[data-sms]').href='sms:'+(D.sms||'')+'?&body='+encodeURIComponent(t);
done.querySelector('[data-call]').href='tel:'+(D.tel||'');
var m=done.querySelector('[data-mail]');if(D.email){m.href='mailto:'+D.email+'?subject='+encodeURIComponent('Demande de devis')+'&body='+encodeURIComponent(t);m.hidden=false}
f.hidden=true;done.hidden=false;done.focus()});
done.querySelector('[data-copy]').addEventListener('click',function(){var b=this,t=sum.textContent;
function s(){b.textContent='Copié ✓';setTimeout(function(){b.textContent='Copier'},2000)}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(s,function(){})}
else{var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy');s()}catch(x){}a.remove()}});
done.querySelector('[data-back]').addEventListener('click',function(){done.hidden=true;f.hidden=false;f.elements.nom.focus()});
f.addEventListener('input',function(e){if(e.target.getAttribute('aria-invalid'))err(e.target,'')});
})();
