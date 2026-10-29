// Usage : node test.js <dossier du site> [pages séparées par des virgules]
// Contrôle : débordement, textes <16px, cibles <44px, hauteurs de sections, pied de page, navigation, images, liens, métadonnées.
let pw;try{pw=require('playwright')}catch(e){pw=require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright')}
const {chromium}=pw;const http=require('http'),fs=require('fs'),path=require('path');
const root=path.resolve(process.argv[2]||'.');
const pages=(process.argv[3]?process.argv[3].split(','):fs.readdirSync(root).filter(f=>/\.html$/.test(f)&&!/^[A-Z]\d?\./.test(f)));
const MIME={html:'text/html',css:'text/css',js:'text/javascript',jpg:'image/jpeg',jpeg:'image/jpeg',png:'image/png',webp:'image/webp',svg:'image/svg+xml',ico:'image/x-icon'};
const srv=http.createServer((q,s)=>{let p=path.join(root,decodeURIComponent(q.url.split('?')[0]));if(p.endsWith('/'))p+='index.html';try{s.setHeader('content-type',MIME[p.split('.').pop().toLowerCase()]||'application/octet-stream');s.end(fs.readFileSync(p))}catch(e){s.statusCode=404;s.end()}});
const WS=[[360,740],[390,844],[414,860],[768,1024],[821,900],[980,900],[981,900],[1280,800],[1920,1000]];
(async()=>{await new Promise(r=>srv.listen(0,r));const base='http://localhost:'+srv.address().port+'/';
const b=await chromium.launch();const out=[];
for(const p of pages){
 for(const [w,h] of WS){
  const pg=await b.newPage({viewport:{width:w,height:h}});const miss=[];pg.on('pageerror',e=>miss.push('erreur JS '+e.message.slice(0,80)));pg.on('response',r=>{if(r.status()>=400)miss.push(r.url().replace(base,''))});
  await pg.goto(base+p);await pg.evaluate(()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');document.querySelectorAll('.reveal').forEach(e=>e.classList.add('in'))});await pg.waitForLoadState('networkidle');
  const r=await pg.evaluate(()=>{const R=[],vh=innerHeight,W=document.documentElement.clientWidth;
   if(document.documentElement.scrollWidth>W)R.push('débordement '+document.documentElement.scrollWidth+'>'+W);
   const vis=e=>{const cs=getComputedStyle(e);return cs.display!=='none'&&cs.visibility!=='hidden'&&e.getBoundingClientRect().width>0};
   document.querySelectorAll('body *').forEach(e=>{if(!vis(e)||e.closest('svg,script,style'))return;const cs=getComputedStyle(e);
    if([...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())){const fs=parseFloat(cs.fontSize);if(fs<15.99)R.push('texte '+fs+'px '+e.tagName+'.'+(e.className||'')+' « '+e.textContent.trim().slice(0,25)+' »')}
    if(e.matches('a,button,input:not([type=radio]):not([type=hidden]),select,textarea,summary')&&!e.classList.contains('skip')&&!e.closest('.sv7-track')||(e.tagName==='LABEL'&&e.control&&e.control.type==='radio'&&vis(e))){
     const inline=e.tagName==='A'&&e.closest('p,li')&&getComputedStyle(e).display==='inline';const bb=e.getBoundingClientRect();
     if(!inline&&(bb.height<43.5||bb.width<43.5)&&!(e.tagName==='A'&&e.classList.contains('skip')))R.push('cible '+Math.round(bb.width)+'x'+Math.round(bb.height)+' '+e.tagName+'.'+(e.className||'')+' « '+e.textContent.trim().slice(0,20)+' »')}
    if(e.tagName==='IMG'){if(!e.complete||!e.naturalWidth)R.push('image cassée '+e.getAttribute('src'));else{const bb=e.getBoundingClientRect();if(bb.width>e.naturalWidth+1)R.push('image agrandie '+e.getAttribute('src'));if(!e.hasAttribute('alt'))R.push('alt manquant '+e.getAttribute('src'))}}});
   document.querySelectorAll('main>section,body>section,.hv,.sv').forEach(s=>{if(s.closest('.sv>*,.hv>*'))return;const hh=s.getBoundingClientRect().height;if(hh>vh*1.2+2)R.push('hauteur '+(s.id||s.className)+' '+Math.round(hh/vh*100)+'%')});
   const ft=document.querySelector('footer');if(ft&&innerWidth<=820){const f=ft.getBoundingClientRect().height/vh;if(f>.3)R.push('pied de page '+Math.round(f*100)+'%')}
   const bg=document.querySelector('.burger,[class*=burger],.menu-toggle,button[aria-controls]');if(bg){const bv=getComputedStyle(bg).display!=='none';if(innerWidth<=980&&!bv)R.push('burger absent');if(innerWidth>=981&&bv)R.push('burger présent')}
   if(innerWidth>=981){const lg=document.querySelector('header .logo,header a[class*=logo],header .brand'),nv=document.querySelector('header nav'),cl=document.querySelector('header .head-call,header .call,header a[href^=tel]');
    if(lg&&nv){const a=lg.getBoundingClientRect(),n=nv.getBoundingClientRect();if(a.right>n.left+1)R.push('logo chevauche menu');if(cl){const c=cl.getBoundingClientRect();if(n.right>c.left+1)R.push('menu chevauche bouton appel')}}}
   return R});
  if(miss.length)r.push('404/JS '+[...new Set(miss)].join(','));
  if(r.length)out.push(p+' '+w+' : '+[...new Set(r)].slice(0,8).join(' | '));
  await pg.close()}}
// métadonnées, liens, poids
const pg=await b.newPage();const seen=new Set();
for(const p of pages){const html=fs.readFileSync(path.join(root,p),'utf8');const m=[];
 if(!/<html[^>]*lang="fr"/.test(html))m.push('lang');if(!/<title>[^<]{5,}/.test(html))m.push('title');if(!/<meta name="description" content="[^"]{20,}/.test(html))m.push('description');
 if(!/name="robots" content="noindex/.test(html))m.push('noindex');if((html.match(/<h1[ >]/g)||[]).length!==1)m.push('h1 ≠ 1');if(!/rel="icon"/.test(html))m.push('favicon');
 let tot=0;for(const s of new Set([...html.matchAll(/src="(images\/[^"]+)"/g)].map(x=>x[1]))){try{const z=fs.statSync(path.join(root,s)).size;tot+=z;if(z>250000)m.push('image >250Ko '+s)}catch(e){m.push('image absente '+s)}}
 if(tot>1500000)m.push('poids images '+Math.round(tot/1000)+'Ko');
 await pg.goto(base+p);const hs=await pg.evaluate(()=>[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')));
 for(const h of hs){if(/^(tel|mailto|sms|https?:|javascript)/.test(h)||seen.has(p+h))continue;seen.add(p+h);const [f,id]=h.split('#');const t=f||p;
  if(!fs.existsSync(path.join(root,t))){m.push('lien mort '+h);continue}
  if(id&&/\.html$/.test(t)&&!new RegExp('id="'+id+'"').test(fs.readFileSync(path.join(root,t),'utf8')))m.push('ancre absente '+h)}
 if(m.length)out.push(p+' : '+m.join(' | '))}
console.log(out.length?out.join('\n'):'TOUT OK');await b.close();srv.close()})();
