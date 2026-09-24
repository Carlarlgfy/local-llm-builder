"""Fifteen language profiles, not a popularity ranking or certification."""
import shutil
import subprocess

PROFILES = [
    {'id':'C11','name':'C','tools':['clang'],'extensions':['.c','.h'], 'guide':'C11, clang -std=c11 -Wall -Wextra. C assertion tests. Static libraries: compile -c, then ar rcs. Use explicit source filenames.'},
    {'id':'C++','name':'C++','tools':['clang++'],'extensions':['.cpp','.cc','.cxx','.hpp','.h'], 'guide':'C++17 standard library. clang++ -std=c++17 -Wall -Wextra source.cpp -o build/app. Separate assert-based test executable.'},
    {'id':'Python','name':'Python','tools':['python3'],'extensions':['.py'], 'guide':'Python standard library, unittest discovery with at least one test. Launch python3 main.py.'},
    {'id':'JavaScript','name':'JavaScript','tools':['node'],'extensions':['.js','.mjs','.cjs'], 'guide':'Node standard library, node --test tests/test.mjs. Launch node main.mjs. No npm installation.'},
    {'id':'TypeScript','name':'TypeScript','tools':['tsc','node'],'extensions':['.ts','.tsx','.json'], 'guide':'tsc --target ES2020 --module commonjs --outDir build main.ts tests.ts. Self-contained assertion tests without external typings. Test node build/tests.js; launch node build/main.js.'},
    {'id':'Rust','name':'Rust','tools':['rustc'],'extensions':['.rs'], 'guide':'Standard library only. rustc --edition=2021 main.rs -o build/app. rustc --edition=2021 --test main.rs -o build/test_app, then ./build/test_app. No unsafe blocks unless the user explicitly requires them. No crate downloads.'},
    {'id':'Go','name':'Go','tools':['go'],'extensions':['.go','.mod','.sum'], 'guide':'Standard library and local modules only. Create go.mod. go build -o build/app . ; go test ./... ; launch ./build/app. No module downloads.'},
    {'id':'Java','name':'Java','tools':['javac','java'],'extensions':['.java'], 'guide':'JDK standard library only. javac -d build Main.java TestMain.java ; java -ea -cp build TestMain ; launch java -cp build Main. No Maven/Gradle downloads.'},
    {'id':'C#','name':'C#','tools':['dotnet'],'extensions':['.cs','.csproj'], 'guide':'Installed .NET SDK, local projects only. dotnet build --no-restore -o build. Use console assertions in a test project. Launch dotnet build/App.dll. Required restore assets must already exist; network restoration is unavailable.'},
    {'id':'Swift','name':'Swift','tools':['swiftc'],'extensions':['.swift'], 'guide':'Portable standard library and Foundation only. swiftc Main.swift -o build/app. Compile a separate Swift test executable using precondition/assert. Avoid AppKit/UIKit for Linux targets.'},
    {'id':'Kotlin','name':'Kotlin','tools':['kotlinc','java'],'extensions':['.kt'], 'guide':'Kotlin/JVM standard library. kotlinc Main.kt -include-runtime -d build/app.jar. Compile a separate test jar using check assertions; java -jar build/tests.jar. Launch java -jar build/app.jar. No Gradle downloads.'},
    {'id':'Ruby','name':'Ruby','tools':['ruby'],'extensions':['.rb'], 'guide':'Ruby standard library only. Tests should raise exceptions on failures and exit nonzero. ruby tests/test_app.rb; launch ruby main.rb. No gem installation.'},
    {'id':'PHP','name':'PHP','tools':['php'],'extensions':['.php'], 'guide':'PHP CLI standard library only. Explicit test conditions must throw or exit nonzero (do not rely on disabled assert). php tests/test_app.php; launch php main.php. No Composer installation.'},
    {'id':'Lua','name':'Lua','tools':['lua'],'extensions':['.lua'], 'guide':'Lua standard library only. lua tests/test_app.lua using assert. Launch lua main.lua. No LuaRocks installation.'},
    {'id':'R','name':'R','tools':['Rscript'],'extensions':['.R','.r'], 'guide':'Base R only. Rscript tests/test_app.R with stopifnot. Launch Rscript main.R. No package installation.'},
]
ALIASES={'c':'C11','c11':'C11','python':'Python','rust':'Rust','java':'Java','javascript':'JavaScript','typescript':'TypeScript','c++':'C++','go':'Go','c#':'C#','swift':'Swift','kotlin':'Kotlin','ruby':'Ruby','php':'PHP','lua':'Lua','r':'R'}
EXTRA_TOOLS={'ar'}

def profile(identifier):
    identifier=ALIASES.get(identifier.lower(),identifier)
    return next((p for p in PROFILES if p['id']==identifier),None)

def java_home():
    result=subprocess.run(['/usr/libexec/java_home'],capture_output=True,text=True,timeout=10)
    return result.stdout.strip() if result.returncode==0 else None

def tool_path(name):
    if name in ('java','javac'):
        try:
            home=java_home()
            if home:
                from pathlib import Path
                executable=Path(home)/'bin'/name
                return str(executable) if executable.is_file() else None
            return None
        except (OSError,subprocess.SubprocessError): return None
    return shutil.which(name)

def available_profiles():
    result=[]
    for p in PROFILES:
        missing=[name for name in p['tools'] if not tool_path(name)]
        result.append(dict(p,available=not missing,missing=missing))
    return result

def require_profile(identifier):
    p=profile(identifier)
    if identifier in ('auto','static website'): return
    if not p: raise ValueError('Select a supported language')
    missing=[name for name in p['tools'] if not tool_path(name)]
    if missing: raise ValueError(p['name']+' needs these installed tools: '+', '.join(missing)+'. Install them separately, then refresh languages.')
