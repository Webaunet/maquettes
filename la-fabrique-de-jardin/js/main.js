(function(){
  var b=document.querySelector('.burger'),n=document.getElementById('menu');
  if(!b||!n)return;
  function set(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o?'true':'false');b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');}
  b.addEventListener('click',function(){set(!n.classList.contains('open'));});
  n.addEventListener('click',function(e){if(e.target.closest('a'))set(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){set(false);b.focus();}});
  window.addEventListener('resize',function(){if(window.innerWidth>980)set(false);});
})();
(function(){
  var f=document.getElementById('cform');if(!f)return;
  var T='+33613967278',rc=document.getElementById('recap'),pre=document.getElementById('recaptxt');
  function bad(id,m){var i=document.getElementById(id),e=document.getElementById('e-'+id);if(!e)return true;e.textContent=m;i.setAttribute('aria-invalid',m?'true':'false');i.closest('.fld').toggleAttribute('data-bad',!!m);return !!m;}
  function val(){var n=f.nom.value.trim(),t=f.tel.value.replace(/[\s.\-]/g,''),c=f.commune.value.trim(),b=f.besoin.value,x=0;
    x+=bad('nom',n.length<2?'Indiquez votre nom.':'');
    x+=bad('tel',/^(\+33|0033|0)[1-9]\d{8}$/.test(t)?'':'Indiquez un numéro français valide, par exemple 06 13 96 72 78.');
    x+=bad('commune',c.length<2?'Indiquez votre commune.':'');
    x+=bad('besoin',b?'':'Choisissez un besoin dans la liste.');
    return x===0;}
  ['nom','tel','commune','besoin'].forEach(function(k){f[k].addEventListener('blur',function(){if(f[k].value||f[k].getAttribute('aria-invalid'))val();});});
  f.addEventListener('submit',function(e){e.preventDefault();
    if(!val()){var first=f.querySelector('[aria-invalid="true"]');if(first)first.focus();return;}
    var m=f.msg.value.trim();
    var txt='Bonjour, je souhaite un contact au sujet de : '+f.besoin.value+'.\nNom : '+f.nom.value.trim()+'\nTéléphone : '+f.tel.value.trim()+'\nCommune : '+f.commune.value.trim()+(m?'\nMessage : '+m:'');
    pre.textContent=txt;document.getElementById('sms').href='sms:'+T+'?&body='+encodeURIComponent(txt);
    f.hidden=true;rc.hidden=false;rc.focus();});
  var ed=document.getElementById('edit');if(ed)ed.addEventListener('click',function(){rc.hidden=true;f.hidden=false;f.nom.focus();});
  document.getElementById('copy').addEventListener('click',function(){var s=document.getElementById('copied'),t=pre.textContent;
    function ok(){s.textContent='Message copié.';}
    function fb(){var r=document.createRange();r.selectNodeContents(pre);var sel=getSelection();sel.removeAllRanges();sel.addRange(r);s.textContent='Texte sélectionné : copiez-le avec Ctrl+C.';}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,fb);}else fb();});
})();
