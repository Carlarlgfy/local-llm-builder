"""Project manifests, output naming, portable exports, and source fingerprints."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import tempfile
import zipfile
from .project_runner import validate_command, is_build, build_outputs, build_directories

MANAGED = {'project.py','project.json','START.command','HOW_TO_RUN.md','BUILD_REPORT.md','ACCEPTANCE.cjs'}
COMPILERS = {'clang','cc','gcc'}

def new_folder(destination, name):
    parent = Path(destination).expanduser().resolve()
    if not parent.is_dir(): raise ValueError('Choose an existing output folder')
    name = re.sub(r'[^\w -]', '-', name.strip()).strip(' .-')[:70] or 'My Project'
    for suffix in range(1000):
        folder = parent / (name if not suffix else f'{name} {suffix+1}')
        try:
            folder.mkdir()
            return folder
        except FileExistsError: continue
    raise ValueError('Choose another project name')

def output_files(command):
    return build_outputs(command)

def merge_checks(old, new):
    result = list(old)
    for command in new:
        validate_command(command)
        outputs = output_files(command)
        if outputs:
            # A changed compile command replaces the previous recipe for that output.
            matches=[i for i,c in enumerate(result) if set(output_files(c)) & set(outputs)]
            if matches:
                result[matches[0]]=command
                for i in reversed(matches[1:]): result.pop(i)
                continue
        if command not in result: result.append(command)
    return result

def split_checks(checks):
    build=[]; tests=[]
    for command in checks:
        validate_command(command)
        (build if is_build(command) else tests).append(command)
    return build, tests

def source_files(root, outputs=()):
    root = root.resolve()
    ignored_dirs={'.git','__pycache__','.venv','node_modules','exports','build','dist','target','obj','bin'}
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root)
        if any(p in ignored_dirs or p.startswith('.builder') for p in rel.parts): continue
        if path.is_symlink() or not path.is_file() or root not in path.resolve().parents: continue
        if str(rel) in outputs or path.suffix in ('.o','.a','.so','.dylib','.exe','.pyc','.log','.class','.jar','.dll','.pem','.key','.p12') or path.name=='.DS_Store': continue
        if path.name=='.env' or path.name.startswith('.env.'): continue
        if path.stat().st_size>10_000_000: raise ValueError('Source file exceeds 10 MB: '+str(rel))
        with path.open('rb') as f: magic=f.read(4)
        if magic in (b'\x7fELF',b'\xcf\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xca\xfe\xba\xbe',b'\xce\xfa\xed\xfe'): continue
        yield path

def fingerprint(root):
    root=root.resolve()
    digest=hashlib.sha256()
    for path in source_files(root):
        if path.name in MANAGED: continue
        digest.update(str(path.relative_to(root)).encode()); digest.update(path.read_bytes())
    return digest.hexdigest()

def write_handoff(root, state):
    root=root.resolve()
    checks=state.get('checks',[])
    build,tests=split_checks(checks)
    outputs=[p for command in build for p in output_files(command)]
    manifest={'version':1,'name':state.get('name',root.name),'language':state.get('language','auto'),
              'build':build,'test':tests,'launch':state.get('launch',[]),
              'libraries':state.get('libraries',[]),'build_outputs':outputs,
              'build_directories':sorted({directory for command in build for directory in build_directories(command)}),
              'acceptance_profile':state.get('acceptance_profile'),
              'acceptance_suite_sha256':state.get('acceptance_suite_sha256'),
              'manual_review':'Required: visual appearance and real-browser play test.',
              'validated_on':'macOS','linux_validation':'Not run; rebuild and test on Linux.'}
    # Reject symlinks before writing application-managed handoff files.
    for name in MANAGED:
        if (root/name).is_symlink(): raise ValueError('Managed file is a symlink: '+name)
    (root/'project.json').write_text(json.dumps(manifest,indent=2)+'\n')
    shutil.copyfile(Path(__file__).with_name('project_runner.py'),root/'project.py')
    (root/'START.command').write_text('#!/bin/sh\ncd "$(dirname "$0")" || exit 1\npython3 project.py run\nresult=$?\nprintf "\\nPress Enter to close…"\nread answer\nexit "$result"\n')
    (root/'START.command').chmod(0o755)
    (root/'HOW_TO_RUN.md').write_text('''# Run and move this project

In AI Builder, use **Test project**, **Run project**, or **Open in VS Code**.
On this Mac, double-click START.command to run in Terminal, including interactive input.

On macOS or Linux, open a terminal in this folder:

```sh
python3 project.py build
python3 project.py test
python3 project.py run
```

C projects need a C compiler and ar (Xcode Command Line Tools on Mac; your distribution's development tools on Linux). Python projects need Python 3; JavaScript projects need Node. Libraries listed in project.json must be installed for the target platform; pkg-config resolves their compiler/linker flags. No packages are downloaded automatically.

Move the source folder or use Export source ZIP. Mac executables cannot be run directly on Linux: rebuild there. Open the folder in VS Code using File > Open Folder. The exported project does not require AI Builder or LM Studio to build or run.

You can put these source files in a separate GitHub repository and clone it on another computer. GitHub is optional: a ZIP or USB transfer works too. Do not publish credentials, private data, or third-party code without reviewing its license.

project.json contains the recorded build/test/run commands. The portable helper executes those commands with your ordinary account permissions, not inside the builder sandbox. Review generated code before running it on another computer.

This project was checked on macOS. Linux compatibility is intended but must be tested on your Linux computer. Model-written tests cannot prove every requirement is correct.
''')
    (root/'BUILD_REPORT.md').write_text('# Build report\n\nStatus: '+state.get('status','Unknown')+'\n\nSource fingerprint: '+fingerprint(root)+'\n\nPlatform checked: macOS\n\nRecorded checks:\n\n'+''.join('- `'+json.dumps(c)+'`\n' for c in checks)+'\nReview the README and try the actual behavior. Linux testing has not been performed by the local builder.\n')
    if state.get('acceptance_profile'):
        with (root/'BUILD_REPORT.md').open('a') as report:
            report.write('\nIndependent profile: '+state['acceptance_profile']+'\n\nApp-owned tests check physics and simulated UI events. They do not certify visual quality, real-browser compatibility, accessibility, or enjoyable gameplay. Manual review remains required.\n')
    return manifest

def export_project(root, target_dir=None):
    root=root.resolve()
    manifest=json.loads((root/'project.json').read_text())
    directory=Path(target_dir) if target_dir else root.parent/'Exports'
    directory.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix=root.name+'-',suffix='.zip',dir=directory)
    import os
    os.close(fd)
    total=0
    with zipfile.ZipFile(name,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in source_files(root,manifest.get('build_outputs',[])):
            total+=path.stat().st_size
            if total>50_000_000: raise ValueError('Export exceeds 50 MB')
            archive.write(path, str(Path(root.name)/path.relative_to(root)))
    return Path(name)
