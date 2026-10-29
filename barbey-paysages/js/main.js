(function(){var b=document.querySelector('.burger'),n=document.getElementById('nav');if(!b||!n)return;
function c(){n.classList.remove('open');b.setAttribute('aria-expanded','false');b.setAttribute('aria-label','Ouvrir le menu')}
b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);b.setAttribute('aria-label',o?'Fermer le menu':'Ouvrir le menu')});
n.addEventListener('click',function(e){if(e.target.closest('a'))c()});
document.addEventListener('keydown',function(e){if(e.key==='Escape'){c();b.focus()}});
matchMedia('(min-width:981px)').addEventListener('change',c);
var y=document.getElementById('an');if(y)y.textContent=new Date().getFullYear()})();
