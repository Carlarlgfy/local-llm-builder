import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from local_builder import acceptance, desktop as app

# A deliberately tiny reference fixture for TESTING THE CHECKER, never sent to the model.
CORE = '''
const api={
 createState:(best=0)=>({birdY:270,birdVelocity:0,pipes:[],score:0,bestScore:best,gameStatus:'ready',timer:0}),
 start(s){Object.assign(s,this.createState(s.bestScore));s.gameStatus='playing'},
 flap(s){if(s.gameStatus==='playing')s.birdVelocity=-300},
 togglePause(s){if(s.gameStatus==='playing')s.gameStatus='paused';else if(s.gameStatus==='paused')s.gameStatus='playing'},
 collision(s){return s.birdY<=14||s.birdY>=551||s.pipes.some(p=>104>p.x&&76<p.x+64&&(s.birdY-14<p.y-90||s.birdY+14>p.y+90))},
 update(s,dt,random=Math.random){if(s.gameStatus!=='playing')return;dt=Math.max(0,Math.min(dt,.033));s.birdVelocity+=850*dt;s.birdY+=s.birdVelocity*dt;s.timer+=dt;if(s.timer>=1.7){s.timer-=1.7;s.pipes.push({x:430,y:160+random()*240,scored:false})}s.pipes.forEach(p=>p.x-=145*dt);if(this.collision(s)){s.gameStatus='gameover';s.bestScore=Math.max(s.bestScore,s.score);return}for(const p of s.pipes){if(!p.scored&&p.x+64<76){s.score++;p.scored=true}}s.bestScore=Math.max(s.bestScore,s.score);s.pipes=s.pipes.filter(p=>p.x+64>0)}
};if(typeof module!=='undefined')module.exports=api;else window.SkyCore=api;
'''

class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.old=copy.deepcopy(app.STATE);self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        app.STATE.clear();app.STATE.update(folder=str(self.root),log=[],tasks=[],acceptance_profile=acceptance.PROFILE,acceptance_stage='core')
        app.STOP.clear();app.PAUSE.clear()
        (self.root/'core.js').write_text(CORE)
    def tearDown(self):
        app.STATE.clear();app.STATE.update(self.old);self.tmp.cleanup()
    def test_correct_core_passes_independent_checks_without_model_tests(self):
        evidence=app.run_checks(self.root,[])
        self.assertIn('7 independent checks',evidence[-1]['output'])
    def test_bad_physics_is_rejected_even_when_model_check_says_pass(self):
        (self.root/'core.js').write_text(CORE.replace('850*dt','0.25*dt'))
        with self.assertRaisesRegex(RuntimeError,'real-time gravity'):
            app.run_checks(self.root,[['node','-e','console.log("PASS")']])
    def test_runner_is_restored_and_cannot_be_overwritten_by_generated_code(self):
        (self.root/acceptance.RUNNER).write_text('process.exit(0)')
        app.run_checks(self.root,[])
        self.assertEqual((self.root/acceptance.RUNNER).read_text(),acceptance.SCRIPT)
        code,out=app.sandbox_command(self.root,['node','-e',"require('node:fs').writeFileSync('ACCEPTANCE.cjs','process.exit(0)')"])
        self.assertNotEqual(code,0,out)
    def test_browser_ui_is_required_at_final_stage(self):
        app.STATE['acceptance_stage']='ui'
        with self.assertRaisesRegex(RuntimeError,'index.html'):
            app.run_checks(self.root,[])
    def browser_fixture(self):
        (self.root/'index.html').write_text('<meta name="viewport"><canvas id="game-canvas"></canvas><button id="start-button"></button><button id="pause-button"></button><p id="score"></p><p id="best"></p><p id="status"></p><script src="core.js"></script><script src="game.js"></script>')
        (self.root/'style.css').write_text('body { background: skyblue; color: black; }')
        (self.root/'README.md').write_text('Open index.html. Space flaps; P pauses. No network needed.')
        (self.root/'game.js').write_text('''
const g=window.SkyCore;let best=0;try{best=Number(localStorage.getItem('sky-hopper-best'))||0}catch(e){}
let s=g.createState(best),last=null;
const el=id=>document.getElementById(id);
function render(){el('score').textContent=String(s.score);el('best').textContent=String(s.bestScore);el('status').textContent={ready:'Ready',playing:'Playing',paused:'Paused',gameover:'Game over'}[s.gameStatus];el('game-canvas').getContext('2d').fillRect(0,0,1,1)}
function start(){g.start(s);last=null;render()}
function input(){if(s.gameStatus==='ready'||s.gameStatus==='gameover')start();else g.flap(s)}
function pause(){g.togglePause(s);last=null;render()}
el('start-button').addEventListener('click',start);el('pause-button').addEventListener('click',pause);el('game-canvas').addEventListener('pointerdown',input);
document.addEventListener('keydown',e=>{if(e.type!=='keydown'||e.repeat)return;if(e.code==='Space'){e.preventDefault();input()}if(e.code==='KeyP')pause()});
function frame(t){g.update(s,last===null?0:(t-last)/1000);last=t;if(s.gameStatus==='gameover')try{localStorage.setItem('sky-hopper-best',s.bestScore)}catch(e){}render();requestAnimationFrame(frame)}
render();requestAnimationFrame(frame);
''')
        app.STATE['acceptance_stage']='ui'
    def test_simulated_ui_suite_accepts_working_handlers(self):
        self.browser_fixture()
        evidence=app.run_checks(self.root,[])
        self.assertIn('10 independent checks',evidence[-1]['output'])
    def test_simulated_ui_rejects_nonfunctional_start_button(self):
        self.browser_fixture()
        target=self.root/'game.js'
        target.write_text(target.read_text().replace("addEventListener('click',start)","addEventListener('click',()=>{})"))
        with self.assertRaisesRegex(RuntimeError,'UI start'):
            app.run_checks(self.root,[])
    def test_profile_opt_in_is_explicit_and_validated(self):
        self.assertIsNone(acceptance.selected('make a bird game'))
        self.assertEqual(acceptance.selected('Acceptance profile: sky-hopper-v1'),acceptance.PROFILE)
        with self.assertRaises(ValueError):acceptance.selected('Acceptance profile: fake')
    def test_specialized_context_is_bounded_by_stage(self):
        (self.root/'game.js').write_text('game')
        (self.root/'index.html').write_text('page')
        (self.root/'style.css').write_text('large irrelevant style')
        core=app.acceptance_context(self.root,'core')
        ui=app.acceptance_context(self.root,'ui')
        self.assertIn('core.js',core);self.assertNotIn('game.js',core)
        self.assertIn('game.js',ui);self.assertIn('index.html',ui)
        self.assertNotIn('core.js',ui);self.assertNotIn('style.css',ui)
    def test_ui_stage_cannot_edit_checkpointed_core(self):
        with self.assertRaisesRegex(ValueError,'checkpointed core.js'):
            app.validate_acceptance_edit('ui','core.js')
        with self.assertRaisesRegex(ValueError,'checkpointed core.js'):
            app.validate_acceptance_edit('ui','src/core.js')
        app.validate_acceptance_edit('core','core.js')
        app.validate_acceptance_edit('ui','game.js')
    def test_worker_does_not_complete_when_model_omits_ui(self):
        app.STATE['language']='static website'
        response={'files':[],'checks':[['node','-e','console.log("PASS")']],'launch':['index.html']}
        with patch.object(app,'model_json',return_value=response) as model,patch.object(app,'checkpoint',return_value='example'):
            app.worker('Acceptance profile: sky-hopper-v1','mock')
        self.assertEqual(app.STATE['status'],'Needs attention')
        self.assertEqual(app.STATE['tasks'][0]['status'],'Passed')
        self.assertEqual(app.STATE['tasks'][1]['status'],'Needs attention')
        self.assertIn('index.html',app.STATE['error'])
        self.assertFalse(app.BUSY.is_set())
        prompts=[call.args[1] for call in model.call_args_list]
        self.assertTrue(prompts)
        self.assertTrue(all('User requirements:' not in prompt for prompt in prompts))
        self.assertTrue(all('MANDATORY contract:' in prompt for prompt in prompts))

if __name__=='__main__':unittest.main()
