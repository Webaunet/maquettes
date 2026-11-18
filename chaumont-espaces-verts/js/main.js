(function(){
  var b=document.querySelector('.burger'),n=document.getElementById('nav');
  if(!b||!n)return;
  function set(o){n.classList.toggle('open',o);b.setAttribute('aria-expanded',String(o));b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')}
  b.addEventListener('click',function(){set(!n.classList.contains('open'))});
  n.addEventListener('click',function(e){if(e.target.closest('a'))set(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('open')){set(false);b.focus()}});
  window.addEventListener('resize',function(){if(window.innerWidth>980)set(false)});
})();
(function(){
  var f=document.getElementById('devis');if(!f)return;
  var TEL='+33000000000',R=document.getElementById('recap');
  var rules={nom:function(v){return v.trim().length>=2||'Indiquez votre nom.'},
    tel:function(v){return /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/.test(v.trim())||'Indiquez un numéro valide, par exemple 06 12 34 56 78.'},
    commune:function(v){return v.trim().length>=2||'Indiquez votre commune.'},
    besoin:function(v){return v!==''||'Choisissez votre besoin dans la liste.'}};
  function check(id){var el=f.elements[id],ok=rules[id](el.value),box=el.closest('.field'),m=box.querySelector('.msg');
    box.classList.toggle('err',ok!==true);el.setAttribute('aria-invalid',ok!==true);m.textContent=ok===true?'':ok;return ok===true}
  Object.keys(rules).forEach(function(id){f.elements[id].addEventListener('blur',function(){check(id)})});
  f.addEventListener('submit',function(e){
    e.preventDefault();var all=Object.keys(rules).map(check);
    if(all.indexOf(false)>-1){var first=f.querySelector('.err input,.err select');if(first)first.focus();R.hidden=true;return}
    var t=['Demande de devis (maquette Chaumont Espaces Verts)','Nom : '+f.elements.nom.value.trim(),'Téléphone : '+f.elements.tel.value.trim(),'Commune : '+f.elements.commune.value.trim(),'Besoin : '+f.elements.besoin.value];
    if(f.elements.message.value.trim())t.push('Message : '+f.elements.message.value.trim());
    var txt=t.join('\n');R.querySelector('pre').textContent=txt;
    R.querySelector('.sms').href='sms:'+TEL+'?body='+encodeURIComponent(txt);
    R.hidden=false;R.focus();R.scrollIntoView({behavior:'smooth',block:'nearest'});
    R.dataset.txt=txt});
  R.querySelector('.copy').addEventListener('click',function(){
    var b=this,txt=R.dataset.txt||'',done=function(){b.textContent='Copié ✓';setTimeout(function(){b.textContent='Copier le message'},2200)};
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,sel)}else sel();
    function sel(){var r=document.createRange();r.selectNodeContents(R.querySelector('pre'));var s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Texte sélectionné : copiez-le'}
  });
})();
