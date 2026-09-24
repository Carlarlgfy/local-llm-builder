import base64
import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import zipfile
from local_builder import desktop as app

class DesktopTests(unittest.TestCase):
    def test_c_compilation_execution_and_confinement(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'main.c').write_text('#include <stdio.h>\n#include <assert.h>\nint main(void){assert(2+2==4);puts("C works");return 0;}\n')
            code,output=app.sandbox_command(root,['clang','-std=c11','-Wall','-Wextra','main.c','-o','app'])
            self.assertEqual(code,0,output)
            self.assertEqual(app.sandbox_command(root,['./app']),(0,'C works\n'))
            self.assertIn('main.c',app.context(root))
            (root/'escape').symlink_to('/usr/bin/true')
            with self.assertRaises(ValueError): app.sandbox_command(root,['./escape'])
            with self.assertRaises(ValueError): app.sandbox_command(root,['./../outside'])
            (root/'deny.c').write_text('#include <stdio.h>\nint main(void){FILE *f=fopen("/tmp/ai-builder-c-forbidden","w"); if(f){fclose(f);return 1;} return 0;}\n')
            code,output=app.sandbox_command(root,['cc','deny.c','-o','deny'])
            self.assertEqual(code,0,output)
            self.assertEqual(app.sandbox_command(root,['./deny'])[0],0)
    def test_docx_and_text_import(self):
        buffer=io.BytesIO()
        with zipfile.ZipFile(buffer,'w') as z:
            z.writestr('word/document.xml','<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Build a game</w:t></w:r></w:p></w:body></w:document>')
        self.assertEqual(app.extract('plan.docx',buffer.getvalue()),'Build a game')
        self.assertEqual(app.extract('plan.md',b'# Project'),'# Project')
        with self.assertRaises(ValueError): app.extract('bad.exe',b'bad')

    def test_protected_paths(self):
        with tempfile.TemporaryDirectory() as d:
            for path in ('../secret','/etc/passwd','.git/config','.builder.json'):
                with self.assertRaises(ValueError): app.path_in(Path(d),path)

    def test_execution_is_sandboxed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            rc,out=app.sandbox_command(root,['python3','-c','print(42)'])
            self.assertEqual((rc,out.strip()),(0,'42'))
            rc,_=app.sandbox_command(root,['python3','-c','open("/tmp/ai-builder-forbidden-test","w")'])
            self.assertNotEqual(rc,0)
            rc,_=app.sandbox_command(root,['python3','-c','import socket; socket.socket().connect(("127.0.0.1",1234))'])
            self.assertNotEqual(rc,0)
            (root/'.git').mkdir()
            rc,_=app.sandbox_command(root,['python3','-c','open(".git/config","w")'])
            self.assertNotEqual(rc,0)

    def test_api_requires_token(self):
        server=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        url=f'http://127.0.0.1:{server.server_port}'
        try:
            with self.assertRaises(urllib.error.HTTPError) as err: urllib.request.urlopen(url+'/state')
            self.assertEqual(err.exception.code,403)
            err.exception.close()
            req=urllib.request.Request(url+'/state',headers={'X-Builder-Token':app.TOKEN})
            with urllib.request.urlopen(req) as r: self.assertIn('status',json.load(r))
            req=urllib.request.Request(url+'/import',data=json.dumps({'name':'plan.txt','data':base64.b64encode(b'Build a clock').decode()}).encode(),headers={'X-Builder-Token':app.TOKEN})
            with urllib.request.urlopen(req) as r: self.assertEqual(json.load(r)['text'],'Build a clock')
        finally: server.shutdown();server.server_close()

if __name__=='__main__': unittest.main()
