import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from local_builder import projects

class PortableProjectTests(unittest.TestCase):
    def test_folder_names_do_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            first=projects.new_folder(tmp,'../My App')
            (first/'keep.txt').write_text('user data')
            second=projects.new_folder(tmp,'../My App')
            self.assertNotEqual(first,second)
            self.assertEqual(first.parent,Path(tmp).resolve())
            self.assertEqual((first/'keep.txt').read_text(),'user data')

    def test_recipe_replacement(self):
        original=[['clang','old.c','-o','app'],['./app']]
        revised=[['clang','new.c','-o','app'],['./app']]
        self.assertEqual(projects.merge_checks(original,revised),revised)

    def test_portable_library_build_test_move_and_export(self):
        with tempfile.TemporaryDirectory(prefix='library test ') as tmp:
            root=Path(tmp)/'Source project';root.mkdir()
            (root/'value.h').write_text('int twice(int x);\n')
            (root/'value.c').write_text('#include "value.h"\nint twice(int x){return x*2;}\n')
            (root/'main.c').write_text('#include <stdio.h>\n#include "value.h"\nint main(void){printf("%d\\n",twice(21));return 0;}\n')
            (root/'test.c').write_text('#include <assert.h>\n#include "value.h"\nint main(void){assert(twice(0)==0);assert(twice(21)==42);assert(twice(-2)==-4);return 0;}\n')
            commands=[['cc','-std=c11','-c','value.c','-o','build/value.o'],
                      ['ar','rcs','build/libvalue.a','build/value.o'],
                      ['cc','main.c','build/libvalue.a','-o','build/app'],
                      ['cc','test.c','build/libvalue.a','-o','build/test'],['./build/test']]
            state={'name':'Portable Library','checks':commands,'launch':['./build/app'],'status':'Complete'}
            projects.write_handoff(root,state)
            result=subprocess.run([sys.executable,'project.py','test'],cwd=root,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            (root/'.env').write_text('DO_NOT_EXPORT=secret')
            (root/'.builder.json').write_text('private local logs')
            (root/'leak.txt').symlink_to(root/'.env')
            archive=projects.export_project(root,Path(tmp)/'Exports')
            with zipfile.ZipFile(archive) as z:
                names=z.namelist()
                self.assertFalse(any('/build/' in p or '.env' in p or 'leak.txt' in p or '.builder' in p for p in names))
                destination=Path(tmp)/'Other computer';z.extractall(destination)
            moved=destination/root.name
            result=subprocess.run([sys.executable,'project.py','run'],cwd=moved,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertEqual(result.stdout.splitlines()[-1],'42')
            result=subprocess.run([sys.executable,'project.py','test'],cwd=moved,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_source_fingerprint_changes_on_edit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'main.c').write_text('old')
            old=projects.fingerprint(root)
            (root/'main.c').write_text('new')
            self.assertNotEqual(old,projects.fingerprint(root))

    def test_linux_and_mac_shared_library_flags(self):
        from local_builder.project_runner import translate
        with patch('platform.system',return_value='Linux'),patch('shutil.which',return_value='/usr/bin/cc'):
            result=translate(['clang','-dynamiclib','a.c','-o','build/liba.dylib'])
            self.assertIn('-shared',result);self.assertNotIn('-dynamiclib',result)

if __name__=='__main__': unittest.main()
