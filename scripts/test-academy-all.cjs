const {chromium,webkit}=require('playwright');
const browserType=process.env.BROWSER==='webkit'?webkit:chromium;
const fs=require('fs'),http=require('http'),path=require('path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const products=['khamrah','yara','asad'],lessons=['notes','authenticity','concentration','longevity','oud','care','occasions','gifts'];
(async()=>{
 const server=http.createServer((q,r)=>{try{let f=path.join(root,new URL(q.url,'http://local').pathname.replace(/^\/perfume-bronx\//,''));if(fs.statSync(f).isDirectory())f+='/index.html';r.setHeader('Content-Type',f.endsWith('.css')?'text/css':f.endsWith('.js')?'application/javascript':f.endsWith('.webp')?'image/webp':'text/html');r.end(fs.readFileSync(f))}catch{r.statusCode=404;r.end()}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port;
 const b=await browserType.launch({executablePath:process.env.BROWSER==='webkit'?undefined:process.env.CHROMIUM_EXECUTABLE_PATH||undefined,headless:true,args:process.env.BROWSER==='webkit'?[]:['--no-sandbox','--disable-dev-shm-usage']});
 try{
 const errors=[],missing=[];
 const c=await b.newContext({reducedMotion:'reduce'});await c.route('**/*',r=>r.request().url().startsWith(origin)?r.continue():r.abort());
 const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()===404)missing.push(r.url())});
 for(const width of [384,1440]){await p.setViewportSize({width,height:856});for(const lang of ['es','en']){
  for(const key of [...products,...lessons]){
   const count=products.includes(key)?7:6;
   await p.goto(`${origin}/perfume-bronx/${lang}/academy/${key}/`);
   assert.equal(await p.locator('.cinema-scene').count(),count);
   for(let i=1;i<=count;i++){
    await p.locator(`.chapter-link[href="#scene-${i}"]`).click();
    assert.equal(await p.locator('.is-active').getAttribute('id'),`scene-${i}`);
    assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`${lang}/${key}/${i}@${width}`);
   }
   if(products.includes(key)){
    await p.locator('.chapter-link[href="#scene-3"]').click();await p.locator('[data-tier="2"]').click();
    assert.equal(await p.locator('.tier-reading:visible').count(),1);await p.locator('[data-reset]').click();assert.equal(await p.locator('.tier-reading:visible').count(),3);
   }else{
    await p.locator('.chapter-link[href="#scene-4"]').click();await p.locator('.lesson-checklist input').first().check();assert.equal(await p.locator('.lesson-checklist input:checked').count(),1);
    await p.locator('.chapter-link[href="#scene-5"]').click();await p.locator('[data-exercise-answer="1"] summary').click();assert.equal(await p.locator('[data-exercise-answer="1"][open]').count(),1);
   }
   await p.locator('[data-reading]').click();assert.equal(await p.locator('.cinema-scene:visible').count(),count);
  }
  await p.goto(`${origin}/perfume-bronx/${lang}/academy/`);
  assert.equal(await p.locator('[data-coverflow]').count(),1);assert.equal(await p.locator('.lesson-directory a').count(),8);
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`hub ${lang} ${width}`);
  await p.locator('[data-coverflow] [data-next]').click();assert.equal(await p.locator('[data-perfume="khamrah"]').getAttribute('aria-current'),'true');
  await p.locator('[data-scent-quiz] button').click();assert.equal(await p.locator('[data-quiz-result] a').count(),3);
  await p.locator('.academy-jump a[href="#dictionary"]').click();assert.equal(await p.locator('#dictionary').getAttribute('open'),'');
  await p.locator('[data-compare-check][value="asad"]').check();assert.equal(await p.locator('[data-compare-column]:visible').count(),3);
  if(process.env.SCREENSHOT_DIR){fs.mkdirSync(process.env.SCREENSHOT_DIR,{recursive:true});await p.goto(`${origin}/perfume-bronx/${lang}/academy/`);await p.screenshot({path:path.join(process.env.SCREENSHOT_DIR,`hub-${lang}-${width}.png`),fullPage:true});for(const [key,scene] of [['yara',1],['asad',2],['authenticity',5],['notes',3]]){await p.goto(`${origin}/perfume-bronx/${lang}/academy/${key}/#scene-${scene}`);await p.screenshot({path:path.join(process.env.SCREENSHOT_DIR,`${key}-${lang}-${width}.png`),fullPage:true})}}
 }}
 const nctx=await b.newContext({javaScriptEnabled:false,viewport:{width:384,height:856}});const n=await nctx.newPage();
 for(const lang of ['es','en'])for(const key of [...products,...lessons]){
  await n.goto(`${origin}/perfume-bronx/${lang}/academy/${key}/`);assert.equal(await n.locator('.cinema-scene:visible').count(),products.includes(key)?7:6);assert.equal(await n.locator('.cinema-controls').isVisible(),false);
 }
 await n.goto(`${origin}/perfume-bronx/es/academy/`);assert.equal(await n.locator('.coverflow-card:visible').count(),3);await n.locator('#dictionary summary').click();assert.equal(await n.locator('#dictionary').getAttribute('open'),'');
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);
 console.log('PASS: 24 Academy pages at 384/1440, all scenes, pyramids, eight lesson exercises/checklists, Coverflow, quiz, comparator, anchored topics, no-JS fallback, no horizontal overflow, no 404s and no JS errors.');
 }finally{await b.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
