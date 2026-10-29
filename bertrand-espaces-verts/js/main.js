(function(){
  var b=document.querySelector('.burger'),n=document.getElementById('nav');
  if(!b||!n)return;
  function set(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu');}
  b.addEventListener('click',function(){set(!n.classList.contains('open'));});
  n.addEventListener('click',function(e){if(e.target.closest('a'))set(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){set(false);b.focus();}});
  window.matchMedia('(min-width:981px)').addEventListener('change',function(e){if(e.matches)set(false);});
})();
(function(){
  var f=document.getElementById('devis');if(!f)return;
  var recap=document.getElementById('recap'),pre=document.getElementById('recap-text'),ok=document.getElementById('recap-ok');
  function err(el,msg){var e=document.getElementById(el.id+'-err');e.textContent=msg;el.setAttribute('aria-invalid',msg?'true':'false');return !msg;}
  function check(){
    var n=f.nom,t=f.tel,c=f.commune,b=f.besoin,v=true;
    v=err(n,n.value.trim().length<2?'Indiquez votre nom.':'')&&v;
    v=err(t,/^(?:\+33|0033|0)\s?[1-9](?:[\s.-]?\d{2}){4}$/.test(t.value.trim())?'':'Indiquez un numéro valide, par exemple 06 12 34 56 78.')&&v;
    v=err(c,c.value.trim().length<2?'Indiquez votre commune.':'')&&v;
    v=err(b,b.value?'':'Choisissez un besoin dans la liste.')&&v;
    return v;
  }
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(!check()){var bad=f.querySelector('[aria-invalid=true]');if(bad)bad.focus();return;}
    var txt='Demande de devis - Bertrand Espaces Verts\nNom : '+f.nom.value.trim()+'\nTéléphone : '+f.tel.value.trim()+'\nCommune : '+f.commune.value.trim()+'\nBesoin : '+f.besoin.value+(f.message.value.trim()?'\nMessage : '+f.message.value.trim():'');
    pre.textContent=txt;
    document.getElementById('b-sms').href='sms:+33679155535?&body='+encodeURIComponent(txt);
    recap.classList.add('show');f.hidden=true;recap.querySelector('h2').focus();
  });
  f.addEventListener('input',function(e){if(e.target.getAttribute('aria-invalid')==='true')check();});
  document.getElementById('b-copy').addEventListener('click',function(){
    var t=pre.textContent;
    (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){ok.textContent='Récapitulatif copié.';},function(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);ok.textContent='Texte sélectionné : copiez-le avec Ctrl+C.';});
  });
  document.getElementById('b-edit').addEventListener('click',function(){recap.classList.remove('show');f.hidden=false;f.nom.focus();});
})();
