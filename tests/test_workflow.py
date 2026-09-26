import copy
from pathlib import Path
import tempfile
from types import SimpleNamespace
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
        with patch.object(app,'model_json',side_effect=[graph,implementation,implementation]) as model,patch.object(app,'run_checks',side_effect=[RuntimeError('bad test'),[],[],[]]),patch.object(app,'checkpoint',return_value='abc'),patch.object(app,'write_handoff'):
            app.worker('Plan','mock')
            self.assertEqual(model.call_count,3)
            self.assertEqual(app.STATE['status'],'Complete')
            self.assertIn('bad test',model.call_args.args[1])
            self.assertIn('Previous rejected draft',model.call_args.args[1])
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
    def test_identical_failed_repairs_stop_without_false_completion(self):
        graph={'tasks':[{'title':'Implement','goal':'Implement'}]}
        implementation={'files':[{'path':'main.py','content':'print(42)'}], 'checks':[['python3','main.py']], 'launch':['python3','main.py']}
        with patch.object(app,'model_json',side_effect=[graph,implementation,implementation]) as model,patch.object(app,'run_checks',side_effect=RuntimeError('unchanged failure')):
            app.worker('Plan','mock')
        self.assertEqual(model.call_count,3)
        self.assertEqual(app.STATE['status'],'Needs attention')
        self.assertEqual(app.STATE['tasks'][0]['status'],'Needs attention')
        self.assertIn('no progress',app.STATE['error'])
        self.assertFalse((self.root/'main.py').exists(),'Failed isolated attempts must not modify the real project')
    def test_model_failure_marks_active_task_needs_attention(self):
        app.STATE['tasks']=[{'title':'Work','goal':'Work','status':'Queued'}]
        with patch.object(app,'model_json',side_effect=RuntimeError('Server context limit')):
            app.worker('Plan','mock',resume=True)
        self.assertEqual(app.STATE['tasks'][0]['status'],'Needs attention')
    def test_failed_checks_invalidate_old_verification(self):
        app.STATE['verified_fingerprint']='old-pass'
        with patch.object(app,'sandbox_command',return_value=(1,'bad test')):
            with self.assertRaises(RuntimeError):app.run_checks(self.root,[['python3','main.py']])
        self.assertNotIn('verified_fingerprint',app.STATE)
    def test_build_only_cannot_certify_source_for_export(self):
        with patch.object(app,'sandbox_command',return_value=(0,'ok')):
            app.run_checks(self.root,[['python3','main.py']],require_behavior=False)
        self.assertNotIn('verified_fingerprint',app.STATE)
    def test_incomplete_task_blocks_verified_export(self):
        app.STATE['tasks']=[{'status':'Needs attention'}]
        handler=object.__new__(app.Handler);handler.path='/export'
        with self.assertRaisesRegex(ValueError,'all project tasks'):handler.action({})
    def test_push_requires_verified_complete_project(self):
        app.STATE.update(upload_remote='git@example.com:owner/repo.git',tasks=[{'status':'Needs attention'}],status='Needs attention')
        with self.assertRaisesRegex(ValueError,'must pass'):
            app.push_verified(self.root,app.STATE)
    def test_verified_push_uses_new_branch_not_main(self):
        state={'name':'Example App','upload_remote':'git@example.com:owner/repo.git','status':'Complete','tasks':[{'status':'Passed'}],'verified_fingerprint':'same'}
        with patch.object(app,'fingerprint',return_value='same'),patch.object(app,'git',return_value=''),patch('subprocess.run',return_value=SimpleNamespace(returncode=0,stdout='',stderr='')) as run:
            branch=app.push_verified(self.root,state)
        command=run.call_args.args[0]
        self.assertTrue(branch.startswith('ai-builder/example-app-'))
        self.assertIn('HEAD:refs/heads/'+branch,command)
        self.assertNotIn('main',command)
    def test_restore_requires_checkpoint(self):
        with self.assertRaisesRegex(ValueError,'No passing checkpoint'):
            app.restore_checkpoint(self.root,{})

if __name__=='__main__': unittest.main()
