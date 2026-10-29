/* Run with Playwright; optional CHROMIUM_EXECUTABLE_PATH for host-provided Chromium. */
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
(async()=>{
 const server=http.createServer((req,res)=>{
  let f=path.join(root,new URL(req.url,'http://local').pathname.replace(/^\/perfume-bronx\//,''));
  try{if(fs.statSync(f).isDirectory())f+='/index.html';res.setHeader('Content-Type',f.endsWith('.css')?'text/css':f.endsWith('.js')?'application/javascript':f.endsWith('.html')?'text/html':'application/octet-stream');res.end(fs.readFileSync(f));}catch{res.statusCode=404;res.end();}
 });
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const origin='http://127.0.0.1:'+server.address().port;
 const b=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_EXECUTABLE_PATH||undefined,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
 try{
 const errors=[];
 const out=process.env.SCREENSHOT_DIR;
 if(out)fs.mkdirSync(out,{recursive:true});
 for(const lang of ['es','en'])for(const width of [320,384,1440]){
  const c=await b.newContext({viewport:{width,height:856},hasTouch:width<500});
  await c.route('**/*',r=>r.request().url().startsWith(origin)?r.continue():r.abort());
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
  await p.goto(origin+`/perfume-bronx/${lang}/academy/khamrah/`);
  assert.equal(await p.locator('.cinema-scene.is-active').count(),1);
  for(let i=1;i<=7;i++){
   await p.locator(`.chapter-link[href="#scene-${i}"]`).click();
   assert.equal(await p.locator('.cinema-scene.is-active').getAttribute('id'),`scene-${i}`);
   await p.waitForTimeout(850);
   assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,`${lang} ${width} scene ${i} overflow`);
   assert.equal(await p.locator('[aria-hidden="true"]').evaluateAll(els=>els.filter(e=>e.classList.contains('cinema-scene')).every(e=>e.inert)),true);
   if(out && lang==='es' && width!==320)await p.screenshot({path:path.join(out,`after-${width}-scene-${i}.png`),fullPage:true});
  }
  await p.locator('.chapter-link[href="#scene-3"]').click();
  await p.locator('[data-tier="1"]').click();
  assert.equal(await p.locator('.tier-reading:visible').count(),1);
  assert.equal(await p.locator('#tier-1').isVisible(),true);
  await p.locator('[data-tier="2"]').focus();await p.keyboard.press('Enter');
  assert.equal(await p.locator('#tier-2').isVisible(),true);
  await p.locator('[data-reset]').click();assert.equal(await p.locator('.tier-reading:visible').count(),3);
  await p.locator('.chapter-link[href="#scene-2"]').click();
  await p.locator('.note-study summary').first().click();
  assert.equal(await p.locator('.note-study[open]').count(),1);
  await p.locator('.chapter-link[href="#scene-6"]').click();
  await p.locator('.choice summary').first().click();assert.equal(await p.locator('.choice[open]').count(),1);
  await p.locator('#title-6').focus();await p.keyboard.press('ArrowRight');
  assert.equal(await p.locator('.cinema-scene.is-active').getAttribute('id'),'scene-7');
  await p.goBack();assert.equal(await p.locator('.cinema-scene.is-active').getAttribute('id'),'scene-6');
  await p.locator('[data-reading]').click();assert.equal(await p.locator('.cinema-scene:visible').count(),7);
  await p.locator('[data-reading]').click();assert.equal(await p.locator('.cinema-scene:visible').count(),1);
  await p.emulateMedia({reducedMotion:'reduce'});
  await p.waitForFunction(()=>document.querySelector('[data-motion]').getAttribute('aria-pressed')==='false');
  assert.equal(await p.locator('[data-motion]').getAttribute('aria-pressed'),'false');
  assert.equal(await p.locator('.is-active').evaluate(el=>getComputedStyle(el).animationName),'none');
  await p.goto(origin+`/perfume-bronx/${lang}/academy/khamrah/?slide=4`);
  assert.equal(await p.locator('.is-active').getAttribute('id'),'scene-4');
  await p.locator('[data-next]').click();assert.equal(new URL(p.url()).searchParams.has('slide'),false);
  await c.close();
 }
 const c=await b.newContext({javaScriptEnabled:false,viewport:{width:384,height:856}});
 const p=await c.newPage();await p.goto(origin+'/perfume-bronx/es/academy/khamrah/');
 assert.equal(await p.locator('.cinema-scene:visible').count(),7);
 assert.equal(await p.locator('.tier-reading:visible').count(),3);
 await p.locator('.choice summary').first().click();assert.equal(await p.locator('.choice[open]').count(),1);
 assert.equal(await p.locator('.cinema-controls').isVisible(),false);
 assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 assert.deepEqual(errors,[]);
 console.log('PASS: ES/EN, 320/384/1440, all seven scenes, no horizontal overflow, pyramid selection/reset, native disclosures, keyboard, Back, legacy links, reading mode, reduced motion, no-JS; zero JS errors.');
 }finally{await b.close();server.close();}
})().catch(e=>{console.error(e);process.exit(1)});
