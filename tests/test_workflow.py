import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from local_builder import desktop as app

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.old=copy.deepcopy(app.STATE)
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        app.STATE.clear();app.STATE.update(folder=str(self.root),log=[],tasks=[],error='',launch=[],checks=[])
        app.STOP.clear();app.PAUSE.clear();app.BUSY.clear()
    def tearDown(self):
        app.STATE.clear();app.STATE.update(self.old)
        app.STOP.clear();app.PAUSE.clear();app.BUSY.clear();self.tmp.cleanup()
    def test_fail_fast_never_executes_stale_binary(self):
        (self.root/'app').write_text('old binary')
        with patch.object(app,'sandbox_command',return_value=(1,'compiler failure')) as run:
            with self.assertRaisesRegex(RuntimeError,'remaining commands were skipped'):
                app.run_checks(self.root,[['cc','main.c','-o','app'],['./app']])
            self.assertEqual(run.call_count,1)
    def test_binary_must_be_compiled_in_current_sequence(self):
        with patch.object(app,'sandbox_command') as run:
            with self.assertRaisesRegex(ValueError,'same check sequence'):
                app.run_checks(self.root,[['./stale_test']])
            run.assert_not_called()
    def test_build_only_is_not_behavioral_evidence(self):
        with self.assertRaisesRegex(ValueError,'Compilation alone'):
            app.run_checks(self.root,[['cc','main.c','-o','app']])
    def test_resume_keeps_passed_tasks_and_runs_remaining(self):
        app.STATE['tasks']=[{'title':'Done','goal':'Done','status':'Passed'}, {'title':'Remaining','goal':'Finish','status':'Queued'}]
        response={'files':[{'path':'main.py','content':'print(42)'}], 'checks':[['python3','main.py']], 'launch':['python3','main.py']}
        with patch.object(app,'model_json',return_value=response) as model,patch.object(app,'run_checks'),patch.object(app,'checkpoint',return_value='abc'),patch.object(app,'write_handoff'):
            app.worker('Plan','mock',resume=True)
            self.assertEqual(model.call_count,1)
            self.assertEqual(app.STATE['status'],'Complete')
            self.assertTrue(all(t['status']=='Passed' for t in app.STATE['tasks']))
    def test_failed_check_enters_repair_loop(self):
        graph={'tasks':[{'title':'Implement','goal':'Implement'}]}
        implementation={'files':[{'path':'main.py','content':'print(42)'}], 'checks':[['python3','main.py']], 'launch':['python3','main.py']}
        with patch.object(app,'model_json',side_effect=[graph,implementation,implementation]) as model,patch.object(app,'run_checks',side_effect=[RuntimeError('bad test'),[],[]]),patch.object(app,'checkpoint',return_value='abc'),patch.object(app,'write_handoff'):
            app.worker('Plan','mock')
            self.assertEqual(model.call_count,3)
            self.assertEqual(app.STATE['status'],'Complete')
            self.assertIn('bad test',model.call_args.args[1])
    def test_imported_library_excludes_symlinks_and_binaries(self):
        library=self.root/'external';library.mkdir()
        (library/'lib.c').write_text('int x=1;')
        (library/'LICENSE').write_text('Example license')
        (library/'secret.h').symlink_to('/etc/passwd')
        destination=self.root/'project';destination.mkdir()
        app.import_library(library,destination)
        self.assertTrue((destination/'vendor/external/lib.c').exists())
        self.assertTrue((destination/'vendor/external/LICENSE').exists())
        self.assertFalse((destination/'vendor/external/secret.h').exists())

if __name__=='__main__': unittest.main()
