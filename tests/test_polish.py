import json
import io
import urllib.error
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from local_builder import desktop as app

class PolishTests(unittest.TestCase):
    def setUp(self):
        self.saved=app.STATE.copy()
        app.STOP.clear();app.PAUSE.clear()
    def tearDown(self):
        app.STATE.clear();app.STATE.update(self.saved)
    def test_model_timeout_clears_wait_indicator(self):
        with patch('urllib.request.urlopen',side_effect=TimeoutError('timed out')):
            with self.assertRaisesRegex(RuntimeError,'Check LM Studio'):
                app.model_json('example','Return tasks')
        self.assertNotIn('model_wait_started',app.STATE)
    def test_invalid_model_output_is_actionable(self):
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return json.dumps({'choices':[{'message':{'content':'broken json'}}]}).encode()
        with patch('urllib.request.urlopen',return_value=Response()):
            with self.assertRaisesRegex(RuntimeError,'shorter task'):
                app.model_json('example','Return tasks')
        self.assertNotIn('model_wait_started',app.STATE)
    def test_node_can_resolve_home_project_but_not_sibling_contents(self):
        with tempfile.TemporaryDirectory(prefix='ai-builder-test-',dir=Path.home()) as tmp:
            parent=Path(tmp);root=parent/'project';root.mkdir()
            (parent/'secret.txt').write_text('private test fixture')
            (root/'test.cjs').write_text("const fs=require('node:fs');const assert=require('node:assert/strict');assert.throws(()=>fs.readFileSync('../secret.txt'));console.log('isolated');")
            code,out=app.sandbox_command(root,['node','test.cjs'])
            self.assertEqual(code,0,out)
            self.assertIn('isolated',out)
    def model_response(self,message,finish='stop'):
        return io.BytesIO(json.dumps({'choices':[{'message':message,'finish_reason':finish}]}).encode())
    def test_complete_reasoning_prefix_is_not_treated_as_code(self):
        response=self.model_response({'content':'<think>local draft</think>\n{"tasks": []}'})
        with patch('urllib.request.urlopen',return_value=response):
            self.assertEqual(app.model_json('example','Return tasks'),{'tasks':[]})
    def test_structured_generation_disables_reasoning_budget(self):
        response=self.model_response({'content':'{"tasks": []}'})
        with patch('urllib.request.urlopen',return_value=response) as opened:
            app.model_json('example','Return tasks')
        payload=json.loads(opened.call_args.args[0].data)
        self.assertEqual(payload['reasoning_effort'],'none')
    def test_empty_or_truncated_answer_is_rejected(self):
        for content,finish in [('', 'stop'),('{"tasks":[]}', 'length')]:
            with self.subTest(finish=finish),patch('urllib.request.urlopen',return_value=self.model_response({'content':content},finish)):
                with self.assertRaisesRegex(RuntimeError,'response budget'):
                    app.model_json('example','Return tasks')
    def test_context_rejection_has_specific_recovery_advice(self):
        error=urllib.error.HTTPError('http://127.0.0.1',400,'Bad Request',{},io.BytesIO(b'{"error":"context length exceeded"}'))
        with patch('urllib.request.urlopen',side_effect=error):
            with self.assertRaisesRegex(RuntimeError,'context/output limits'):
                app.model_json('example','Return tasks')
