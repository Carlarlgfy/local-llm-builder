"""App-owned acceptance profiles. These check contracts, not arbitrary intent."""
import re
from pathlib import Path

PROFILE = 'sky-hopper-v1'
RUNNER = 'ACCEPTANCE.cjs'
CONTRACT = '''
Acceptance profile: sky-hopper-v1
Use exactly core.js for pure CommonJS game logic and game.js for browser bindings.
core.js must also expose window.SkyCore when loaded as a classic browser script.
Export createState(best=0), start(state), flap(state), togglePause(state),
update(state, dtSeconds, random=Math.random), collision(state).
State fields: birdY=270, birdVelocity=0, pipes=[], score=0, bestScore=best,
gameStatus='ready', timer=0. Allowed statuses: ready, playing, paused, gameover.
start mutates the EXISTING state, resets everything except bestScore, and sets playing.
flap only while playing sets velocity=-300 pixels/second. Gravity=850 pixels/second^2.
update only while playing; clamp dt to [0,0.033]. Add gravity then move bird.
Logical canvas: 420x600. Ground y=565. Bird center x=90, radius=14.
Pipe objects: {x,y,scored:false}; width=64; gap=180 centered at y.
Spawn every 1.7 simulated seconds at x=430, y=160+random()*240; move left 145px/s.
collision returns boolean: ceiling when birdY-14<=0, ground when birdY+14>=565,
or bird bounding-box versus pipe rectangles. For each pipe, horizontal overlap is
90+14>pipe.x && 90-14<pipe.x+64. During horizontal overlap, collide above the gap
when birdY-14<pipe.y-90 or below the gap when birdY+14>pipe.y+90.
On collision update sets gameover. Score each pipe ONCE after its right edge <76.
Never score a collision frame. bestScore stays >= score. Remove offscreen pipes.
togglePause only switches playing/paused. Ready and gameover are unchanged.
No DOM, storage, require calls, or timers in core.js; no package dependencies.
Guard exports explicitly: if(typeof module!=='undefined' && module.exports) module.exports=api;
if(typeof window!=='undefined') window.SkyCore=api; where api contains all six functions.
collision(state) takes ONE argument and checks ALL state.pipes itself. Check ceiling and
ground even when pipes is empty. update must call collision(state) outside the pipe loop.
Scoring uses pipe.x+64<76, NOT pipe.x<76. Clamp negative dt to zero.

UI stage only: index.html loads core.js then game.js as classic local scripts.
Use canvas id game-canvas width=420 height=600; visible text nodes score, best, status;
buttons start-button and pause-button; style.css; README.md.
game.js gets window.SkyCore and may call ONLY createState, start, flap, togglePause,
update and collision. Derive visible labels directly from state.gameStatus; never invent
helpers such as getStatusText. Own one state and schedule ONE requestAnimationFrame
immediately at script load. Every frame schedules exactly one next frame in every status;
never start another loop from an input handler. Convert milliseconds to seconds, call
core.update, and draw bird/pipes/ground.
Use getElementById and addEventListener; canvas pointerdown starts or flaps;
Space (event.code='Space') on document starts/flaps, prevents default, ignores repeat;
P (KeyP) toggles pause. Start button starts/restarts; Pause button toggles.
Never register a document click flap handler (would double-handle buttons).
Read localStorage before createState so Ready displays the saved best immediately.
Do not call core.start during initialization or page load. The initial frame must remain
ready until Start, Space or canvas pointerdown input explicitly starts the game.
Render score and best as raw decimal strings only (for example "0" and "12") and
status to textContent on every frame and after input.
Visible status is Ready, Playing, Paused or Game over. Pause button says Resume while paused.
Try/catch localStorage read/write using key sky-hopper-best, save on gameover.
Render Ready immediately, reset timestamp when starting or resuming; no extra RAF loops.
No external assets, fetch, modules, packages, downloads. Keep UI simple and responsive.
Do not create or edit ACCEPTANCE.cjs: the app supplies and protects independent checks.
'''

UI_CONTRACT = '''
The core stage is complete. Write ONLY index.html, style.css, game.js and README.md.
Use window.SkyCore as the existing API: createState(best=0) returns a Ready state;
start(state) mutates it into Playing and resets score/position; flap(state) applies
an impulse only in Playing; togglePause(state) switches Playing/Paused;
update(state, seconds) advances physics and changes gameStatus to gameover on collision.
The core already handles collisions, pipes, score and bestScore. Do not implement it again.
State contains birdY, birdVelocity, pipes, score, bestScore, gameStatus, timer.
Statuses are lowercase ready, playing, paused, gameover. Pipes have x, y, scored.
Draw at 420x600, ground y=565, bird center x=90 radius=14, pipes width 64 and gap 180
centered at pipe.y. Create attractive original canvas scenery without external assets.
''' + CONTRACT.split('UI stage only:')[1]

def selected(plan):
    matches=re.findall(r'^Acceptance profile:\s*(\S+)\s*$',plan,re.MULTILINE)
    if not matches:return None
    if matches != [PROFILE]:raise ValueError('Unknown or duplicate acceptance profile. Supported: '+PROFILE)
    return PROFILE

def tasks():
    return [dict(title='Implement independently tested game logic',goal='Write core.js only, satisfying the pure game contract. No DOM or localStorage. Checks may be omitted because the app runs its own core suite.',status='Queued'),
            dict(title='Connect playable UI and verify controls',goal='Keep core.js working. Add index.html, game.js, style.css and README.md following the exact UI contract. Launch ["index.html"]. The app tests core and simulated UI independently.',status='Queued')]

def install(root):
    target=Path(root)/RUNNER
    if target.is_symlink():raise ValueError('Acceptance runner cannot be a symlink')
    target.write_text(SCRIPT)

SCRIPT = r'''// Owned by AI Builder; regenerated before every acceptance run.
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
let passed=0;
function test(name,fn){try{fn();passed++;console.log('PASS '+name)}catch(e){console.error('FAIL '+name+': '+e.message);process.exitCode=1}}
const source=fs.readFileSync('core.js','utf8');
const box={module:{exports:{}},console:{log(){}}};vm.createContext(box);
vm.runInContext(source,box,{timeout:1000});const g=box.module.exports;
for(const n of ['createState','start','flap','togglePause','update','collision'])assert.equal(typeof g[n],'function','Missing export '+n);
function fresh(){const s=g.createState(7);g.start(s);return s}
test('R1 initial state and start reset',()=>{const browserCore={window:{}};vm.createContext(browserCore);vm.runInContext(source,browserCore,{timeout:1000});assert.equal(typeof browserCore.window.SkyCore.createState,'function','Browser export missing; guard module.exports with typeof module');let s=g.createState(7);assert.equal(s.gameStatus,'ready');assert.equal(s.birdY,270);assert.equal(s.score,0);assert.equal(s.bestScore,7);g.start(s);assert.equal(s.gameStatus,'playing');s.score=4;s.timer=1;s.pipes.push({x:1,y:1});s.birdY=500;g.start(s);assert.equal(s.score,0);assert.equal(s.timer,0);assert.equal(s.birdY,270);assert.equal(s.birdVelocity,0);assert.equal(s.pipes.length,0);assert.equal(s.bestScore,7)});
test('R2 real-time gravity and flap',()=>{let s=fresh();g.update(s,.02,()=>.5);assert(Math.abs(s.birdVelocity-17)<1e-8);assert(Math.abs(s.birdY-270.34)<1e-8);g.flap(s);assert.equal(s.birdVelocity,-300);let y=s.birdY;g.update(s,.02,()=>.5);assert(s.birdY<y)});
test('R2 capped delta and delayed spawn',()=>{let s=fresh();g.update(s,99,()=>.5);assert(s.birdVelocity<=28.06);assert.equal(s.pipes.length,0);s=fresh();s.timer=1.69;g.update(s,.02,()=>.5);assert.equal(s.pipes.length,1);assert.equal(s.pipes[0].y,280);assert(s.pipes[0].x>420)});
test('R2 pipe motion and exactly-once scoring',()=>{let s=fresh();s.pipes=[{x:70,y:270,scored:false}];g.update(s,.01,()=>.5);assert.equal(s.score,0,'Do not score until the RIGHT edge (x+64) passes x=76');s.pipes=[{x:10,y:270,scored:false}];g.update(s,.01,()=>.5);assert.equal(s.score,1);assert(s.pipes[0].x<10);for(let i=0;i<10;i++)g.update(s,.01,()=>.5);assert.equal(s.score,1);s.pipes=[{x:-70,y:270,scored:true}];g.update(s,.01,()=>.5);assert.equal(s.pipes.length,0)});
test('R3 gaps survive but pipe edges collide',()=>{let s=fresh();s.pipes=[{x:80,y:270,scored:false}];assert.equal(g.collision(s),false,'Bird at y=270 is inside the gap');s.birdY=180;assert.equal(g.collision(s),true,'Bird at y=180 overlaps the top pipe: fixed bird X=90, radius=14. State has no birdX field. collision takes ONLY state.');g.update(s,.01,()=>.5);assert.equal(s.gameStatus,'gameover','update must apply pipe collisions');assert.equal(s.score,0)});
test('R3 ceiling and ground end game; best retained',()=>{for(const y of [10,560]){let s=fresh();s.birdY=y;s.score=9;g.update(s,.01,()=>.5);assert.equal(s.gameStatus,'gameover','Ceiling/ground collision must end play even when pipes is empty');assert.equal(s.bestScore,9,'On gameover update bestScore=max(bestScore,score), here max(7,9)=9, BEFORE returning');g.start(s);assert.equal(s.bestScore,9);assert.equal(s.score,0)}});
test('R4 paused and ended games are frozen',()=>{let s=fresh();g.togglePause(s);assert.equal(s.gameStatus,'paused');let before=JSON.stringify(s);g.update(s,.03);g.flap(s);assert.equal(JSON.stringify(s),before);g.togglePause(s);assert.equal(s.gameStatus,'playing');s.gameStatus='gameover';before=JSON.stringify(s);g.update(s,.03);g.flap(s);g.togglePause(s);assert.equal(JSON.stringify(s),before)});
if(process.argv[2]==='ui'){
  const html=fs.readFileSync('index.html','utf8');
  test('R5 offline files and real controls',()=>{assert(/name=["']viewport["']/.test(html));for(const id of ['game-canvas','start-button','pause-button','score','best','status'])assert(html.includes('id="'+id+'"')||html.includes("id='"+id+"'"),'Missing '+id);assert(html.includes('core.js')&&html.indexOf('core.js')<html.indexOf('game.js'));assert(!/(?:https?:)?\/\//.test(html),'External URL in HTML');assert(fs.readFileSync('style.css','utf8').trim().length>30);assert(fs.readFileSync('README.md','utf8').length>30)});
  function browser(storageBlocked=false){
    const elements={},handlers={},queue=[],writes=[];let draws=0;
    const ctx=new Proxy({createLinearGradient:()=>({addColorStop(){}})}, {get:(t,k)=>k in t?t[k]:()=>{draws++},set:(t,k,v)=>{t[k]=v;return true}});
    for(const id of ['game-canvas','start-button','pause-button','score','best','status'])elements[id]={textContent:'',width:420,height:600,style:{},disabled:false,handlers:{},getContext:()=>ctx,addEventListener(type,fn){(this.handlers[type]??=[]).push(fn)}};
    const doc={hidden:false,getElementById:id=>{assert(elements[id],'Unexpected element '+id);return elements[id]},addEventListener(type,fn){(handlers[type]??=[]).push(fn)}};
    const b={document:doc,console:{log(){}},localStorage:{getItem:()=>{if(storageBlocked)throw Error('Storage disabled');return '12'},setItem:(k,v)=>{if(storageBlocked)throw Error('Storage disabled');writes.push([k,v])}},requestAnimationFrame:fn=>{queue.push(fn);return queue.length},performance:{now:()=>0}};b.window=b;vm.createContext(b);
    vm.runInContext(source,b,{timeout:1000});vm.runInContext(fs.readFileSync('game.js','utf8'),b,{timeout:1000});
    function frame(t){assert.equal(queue.length,1,'Exactly one animation loop required');b.__frame=queue.shift();b.__time=t;vm.runInContext('__frame(__time)',b,{timeout:1000})}
    function fire(target,type,code,repeat=false){b.__handlers=(target==='document'?handlers:elements[target].handlers)[type]||[];assert(b.__handlers.length>0,'No handler for '+target+' '+type);b.__event={type,code,key:code==='Space'?' ':code==='KeyP'?'p':'',repeat,preventDefault(){}};vm.runInContext('__handlers.forEach(f=>f(__event))',b,{timeout:1000})}
    return {elements,frame,fire,writes,queue,draws:()=>draws};
  }
  test('R1 R3 R4 UI start, pause, resume, lose, restart, reopen',()=>{let b=browser();b.frame(0);assert.match(b.elements.status.textContent,/ready/i);assert.equal(Number(b.elements.best.textContent),12);b.fire('start-button','click');b.frame(16);assert.match(b.elements.status.textContent,/playing/i);b.fire('document','keydown','KeyP');b.frame(32);assert.match(b.elements.status.textContent,/paused/i);b.fire('document','keydown','Space');b.frame(48);assert.match(b.elements.status.textContent,/paused/i);b.fire('pause-button','click');b.frame(64);assert.match(b.elements.status.textContent,/playing/i);for(let i=1;i<=180;i++)b.frame(64+i*16);assert.match(b.elements.status.textContent,/game.?over/i);assert(b.writes.some(([k])=>k==='sky-hopper-best'),'Best score was not saved');b.fire('start-button','click');b.frame(3100);assert.match(b.elements.status.textContent,/playing/i);assert.equal(Number(b.elements.score.textContent),0);assert(b.draws()>0,'Nothing drawn');let reopened=browser();reopened.frame(0);assert.match(reopened.elements.status.textContent,/ready/i);assert.equal(Number(reopened.elements.best.textContent),12)});
  test('R5 Space and pointer start, repeats ignored, blocked storage safe',()=>{let b=browser(true);b.frame(0);b.fire('document','keydown','Space',true);b.frame(16);assert.match(b.elements.status.textContent,/ready/i);b.fire('document','keydown','Space');b.frame(32);assert.match(b.elements.status.textContent,/playing/i);b=browser(true);b.frame(0);b.fire('game-canvas','pointerdown');b.frame(16);assert.match(b.elements.status.textContent,/playing/i);for(let i=1;i<=180;i++)b.frame(16+i*16);assert.match(b.elements.status.textContent,/game.?over/i)});
}
if(!process.exitCode)console.log('ACCEPTANCE PASSED: '+passed+' independent checks ('+process.argv[2]+'). Visual review still required.');
'''
