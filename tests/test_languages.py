import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from local_builder import desktop as app
from local_builder.languages import PROFILES, require_profile
from local_builder.projects import split_checks, output_files

class LanguageTests(unittest.TestCase):
    def test_fifteen_distinct_profiles(self):
        self.assertEqual(len(PROFILES),15)
        self.assertEqual(len({p['id'] for p in PROFILES}),15)
    def test_missing_tool_fails_before_build(self):
        with patch('local_builder.languages.tool_path',return_value=None):
            with self.assertRaisesRegex(ValueError,'rustc'): require_profile('Rust')
    def test_build_and_test_classification(self):
        build,test=split_checks([['rustc','main.rs','-o','build/app'],['./build/app'],['go','test','./...'],['javac','-d','build','Main.java'],['java','-cp','build','Main']])
        self.assertEqual(len(build),2);self.assertEqual(len(test),3)
        self.assertEqual(output_files(['rustc','main.rs','-o','build/app']),['build/app'])
    def test_installed_runtime_smokes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fixtures=[('main.cpp','#include <iostream>\n#include <cassert>\nint main(){assert(2+2==4);std::cout<<"CPP OK\\n";}\n',['clang++','-std=c++17','main.cpp','-o','app'],['./app'],'CPP OK'),
                      ('main.swift','assert(2+2==4)\nprint("Swift OK")\n',['swiftc','main.swift','-o','swift_app'],['./swift_app'],'Swift OK'),
                      ('main.js','if(2+2!==4)throw Error("bad"); console.log("JS OK");',None,['node','main.js'],'JS OK'),
                      ('main.rb','raise "bad" unless 2+2==4\nputs "Ruby OK"\n',None,['ruby','main.rb'],'Ruby OK')]
            for filename,source,compile_command,launch,expected in fixtures:
                with self.subTest(language=filename):
                    (root/filename).write_text(source)
                    if compile_command:
                        code,out=app.sandbox_command(root,compile_command,120);self.assertEqual(code,0,out)
                    code,out=app.sandbox_command(root,launch);self.assertEqual(code,0,out);self.assertIn(expected,out)

if __name__=='__main__': unittest.main()
