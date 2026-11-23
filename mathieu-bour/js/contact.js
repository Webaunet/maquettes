(function(){
  var f=document.getElementById('devis');if(!f)return;
  var tel='+33663209103',mail='contact@exemple.fr';
  var rules={
    nom:function(v){return v.trim().length>=2?'':'Indiquez votre nom (2 lettres minimum).'},
    tel:function(v){return /^(?:(?:\+|00)33|0)\s?[1-9](?:[\s.\-]?\d{2}){4}$/.test(v.trim())?'':'Indiquez un numéro valide, par exemple 06 63 20 91 03.'},
    commune:function(v){return v.trim().length>=2?'':'Indiquez votre commune.'},
    besoin:function(v){return v?'':'Choisissez le type de travaux.'}
  };
  function show(el,msg){var e=document.getElementById(el.id+'-err');e.textContent=msg;el.setAttribute('aria-invalid',msg?'true':'false')}
  Object.keys(rules).forEach(function(k){var el=f.elements[k];el.addEventListener('blur',function(){show(el,rules[k](el.value))});el.addEventListener('input',function(){if(el.getAttribute('aria-invalid')==='true')show(el,rules[k](el.value))})});
  var text='';
  f.addEventListener('submit',function(ev){
    ev.preventDefault();var first=null;
    Object.keys(rules).forEach(function(k){var el=f.elements[k],m=rules[k](el.value);show(el,m);if(m&&!first)first=el});
    if(first){first.focus();return}
    var v=function(k){return f.elements[k].value.trim()};
    text='Demande de devis MATHIEU BOUR (GARDEN HOME SERVICES)\nNom : '+v('nom')+'\nTéléphone : '+v('tel')+'\nCommune : '+v('commune')+'\nBesoin : '+v('besoin')+(v('message')?'\nMessage : '+v('message'):'');
    document.getElementById('recap-text').textContent=text;
    document.getElementById('sms').href='sms:'+tel+'?body='+encodeURIComponent(text);
    document.getElementById('mail').href='mailto:'+mail+'?subject='+encodeURIComponent('Demande de devis')+'&body='+encodeURIComponent(text);
    var r=document.getElementById('recap');r.classList.add('show');r.setAttribute('tabindex','-1');r.focus();r.scrollIntoView({behavior:'smooth',block:'nearest'});
  });
  document.getElementById('copy').addEventListener('click',function(){
    var s=document.getElementById('copy-status');
    function ok(){s.textContent='Récapitulatif copié.'}
    function ko(){var rg=document.createRange();rg.selectNodeContents(document.getElementById('recap-text'));var se=getSelection();se.removeAllRanges();se.addRange(rg);s.textContent='Sélectionné : copiez-le avec Ctrl+C.'}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(ok,ko)}else ko();
  });
})();
