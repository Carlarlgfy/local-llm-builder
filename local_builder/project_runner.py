"""Portable project helper copied into generated projects as project.py.

This standalone helper executes the project's reviewed commands on macOS/Linux.
Unlike the builder's internal runner, it is NOT a sandbox.
"""
import argparse
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import webbrowser

COMPILERS = {'cc', 'gcc', 'clang', 'c++', 'g++', 'clang++'}

def is_build(command):
    return command[0] in COMPILERS | {'ar','rustc','swiftc','javac','kotlinc','tsc'} or command[:2] in (['go','build'],['dotnet','build'])

def build_outputs(command):
    validate_command(command)
    if '-o' in command:
        index=command.index('-o')+1
        if index>=len(command): raise ValueError('-o requires a path')
        if command[:2]==['dotnet','build']: return []
        return [command[index]]
    if command[0] in COMPILERS:
        if '-c' in command: return [Path(p).stem+'.o' for p in command[1:] if Path(p).suffix in ('.c','.cpp','.cc','.cxx')]
        return ['a.out']
    if command[0]=='ar':
        if len(command)<4: raise ValueError('Use ar rcs library.a object.o')
        return [command[2]]
    if command[0]=='kotlinc' and '-d' in command: return [command[command.index('-d')+1]]
    return []

def build_directories(command):
    directories={str(Path(p).parent) for p in build_outputs(command) if str(Path(p).parent)!='.'}
    flags=['--outDir']
    if command[0]=='javac': flags.append('-d')
    if command[:2]==['dotnet','build']: flags.append('-o')
    for flag in flags:
        if flag in command: directories.add(command[command.index(flag)+1])
    return sorted(directories)

def validate_command(command):
    if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
        raise ValueError('Commands must be nonempty arrays of strings')
    return command

def translate(command, libraries=()):
    command = list(validate_command(command))
    if command[0] in COMPILERS:
        cpp=command[0] in ('c++','g++','clang++')
        compiler = os.environ.get('CXX' if cpp else 'CC') or shutil.which('c++' if cpp else 'cc') or shutil.which('clang++' if cpp else 'clang') or shutil.which('g++' if cpp else 'gcc')
        if not compiler:
            raise ValueError('Install a C compiler: Xcode Command Line Tools on Mac, or your Linux distribution’s C development tools.')
        command[0] = compiler
        if '-dynamiclib' in command and platform.system() == 'Linux':
            command[command.index('-dynamiclib')] = '-shared'
        elif '-shared' in command and platform.system() == 'Darwin':
            command[command.index('-shared')] = '-dynamiclib'
        if libraries:
            pkg = shutil.which('pkg-config')
            if not pkg: raise ValueError('Install pkg-config and the development packages listed in project.json.')
            flags = ['--cflags'] if '-c' in command else ['--cflags', '--libs']
            response = subprocess.run([pkg, *flags, *libraries], capture_output=True, text=True, check=True)
            command.extend(shlex.split(response.stdout))
    elif command[0] in ('python', 'python3'):
        command[0] = sys.executable
    elif command[0] == 'ar':
        command[0] = shutil.which('ar') or 'ar'
    return command

def run_commands(commands, root, libraries=()):
    for command in commands:
        argv = translate(command, libraries)
        print('+ ' + shlex.join(argv), flush=True)
        subprocess.run(argv, cwd=root, check=True)

def main(argv=None):
    parser = argparse.ArgumentParser(description='Build, test, or run this project on macOS or Linux.')
    parser.add_argument('action', choices=['build','test','run'])
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'project.json').read_text())
    for directory in manifest.get('build_directories', []):
        path = (root / directory).resolve()
        if root not in path.parents: raise ValueError('Build directory escapes the project')
        path.mkdir(parents=True, exist_ok=True)
    libraries = manifest.get('libraries', [])
    run_commands(manifest.get('build', []), root, libraries)
    if args.action == 'test':
        if not manifest.get('test'): raise ValueError('No test commands recorded')
        run_commands(manifest['test'], root, libraries)
    elif args.action == 'run':
        launch = manifest.get('launch', [])
        if not launch: raise ValueError('This is a library project. Run its tests or use the documented consumer example.')
        if len(launch)==1 and launch[0].endswith('.html'):
            webbrowser.open((root / launch[0]).resolve().as_uri())
        else:
            run_commands([launch], root, libraries)
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('Project action failed: '+str(error), file=sys.stderr)
        raise SystemExit(1)
