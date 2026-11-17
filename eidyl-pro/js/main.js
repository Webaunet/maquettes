(function(){
  var b=document.querySelector('.burger'),n=document.getElementById('menu');
  if(!b||!n)return;
  function set(o){b.setAttribute('aria-expanded',o);n.classList.toggle('open',o);}
  b.addEventListener('click',function(){set(b.getAttribute('aria-expanded')!=='true');});
  n.addEventListener('click',function(e){if(e.target.closest('a'))set(false);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'){set(false);b.focus();}});
  window.addEventListener('resize',function(){if(innerWidth>980)set(false);});
})();
(function(){
  var f=document.getElementById('form');if(!f)return;
  var F=['nom','tel','commune','besoin'],M={nom:'Indiquez votre nom.',tel:'Indiquez un numéro de téléphone valide (10 chiffres).',commune:'Indiquez votre commune.',besoin:'Choisissez votre besoin.'};
  function ok(id,v){v=v.trim();if(!v)return false;if(id==='tel')return /^(?:\+33|0)[1-9](?:[\s.-]?\d{2}){4}$/.test(v);return true;}
  f.addEventListener('submit',function(e){
    e.preventDefault();var bad=null;
    F.forEach(function(id){var el=document.getElementById(id),er=document.getElementById('e-'+id),g=ok(id,el.value);
      el.setAttribute('aria-invalid',g?'false':'true');er.textContent=g?'':M[id];if(!g&&!bad)bad=el;});
    var r=document.getElementById('recap');
    if(bad){r.hidden=true;bad.focus();return;}
    var v=function(i){return document.getElementById(i).value.trim();};
    var t='Bonjour, je souhaite un devis auprès d\'EIDYL PRO.\nNom : '+v('nom')+'\nTéléphone : '+v('tel')+'\nCommune : '+v('commune')+'\nBesoin : '+v('besoin')+(v('msg')?'\nMessage : '+v('msg'):'');
    document.getElementById('recap-txt').style.whiteSpace='pre-line';document.getElementById('recap-txt').textContent=t;
    document.getElementById('sms').href='sms:+33000000000?&body='+encodeURIComponent(t);
    r.hidden=false;r.focus();
  });
  document.getElementById('copier').addEventListener('click',function(){
    var t=document.getElementById('recap-txt').textContent,o=document.getElementById('copie');
    function d(){o.textContent='Demande copiée.';}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(d,function(){o.textContent='Copie impossible : sélectionnez le texte.';});}
    else{o.textContent='Copie impossible : sélectionnez le texte.';}
  });
})();
