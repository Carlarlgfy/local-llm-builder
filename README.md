# AI Builder for this Mac

## Build from source on macOS

This is an early local desktop app for experimenting with coding models. The repository contains source code, documentation, and example plans; compiled app bundles and generated user projects are excluded.

Prerequisites: macOS, Apple Xcode or Command Line Tools with Swift and Clang, Git, Homebrew Python at `/opt/homebrew/bin/python3`, and LM Studio running a local coding model. Node projects additionally require Node at `/opt/homebrew/bin/node`.

```sh
git clone https://github.com/Carlarlgfy/local-llm-builder.git
cd local-llm-builder
sh build_app.sh
open 'AI Builder.app'
```

The build creates an app bundle with its icon and an ad-hoc local signature. It is not a notarized release. The Desktop shortcuts described in `START HERE.md` belong to the original local setup; a fresh checkout uses the generated app in the repository folder.

## Use the app

Double-click **AI Builder.app**. Keep LM Studio's local server running on port 1234.

1. Drop a PDF, Word document, Markdown file, or text file into the window. You can also choose a file or paste a plan.
2. Select your local coding model. The default is `qwen2.5-coder` when available.
3. Enter a project name, choose a destination folder, and click **Start build**. The default is **Documents / AI Builder Projects**. Existing folders are never overwritten.
4. Follow the task list and activity log. Each task gets up to three generation/test attempts. Passing tasks get Git checkpoints; all collected checks run again at the end.
5. Use **Test project**, **Run project**, **Run in Terminal**, **Open folder**, or **Open in VS Code**. C and Python output appears in Activity; Terminal supports interactive input; static HTML opens in your browser.
6. Describe a change in **Make a change** and click **Apply change**. Existing files are included in the model context and prior recorded checks run again.

Use **Pause / Resume** between model calls or commands, and **Stop** to cancel further work. A running inference request may take up to five minutes to return; a running test process is terminated promptly. Keep the app open while building.

To continue an older project, choose it from **Recent projects** or use **Browse**. **Resume build** skips saved passing tasks, retries unfinished work, and reruns the recorded checks. Task results, logs, and Git history stay in the project. If interruption happened between a file edit and its checkpoint, that unfinished task is retried; individual commands are not replayed transactionally.

## Move the result to Linux or another Mac

Use **Export source ZIP** after checks pass. Extract it on the other computer, open its folder in VS Code, and run:

```sh
python3 project.py build
python3 project.py test
python3 project.py run
```

The exported source includes a command manifest (`project.json`), portable helper (`project.py`), build report, and `HOW_TO_RUN.md`. C artifacts are rebuilt on the destination machine; Mac executables are not Linux executables. Install Python 3 and the language's toolchain there. The standalone helper executes reviewed project commands with ordinary account permissions, not the builder sandbox.

GitHub is optional. You may upload the generated source to a separate repository and clone it on your Linux laptop, or transfer the ZIP directly. The builder itself remains a macOS application. Source portability is intended; a successful Mac build does not certify Linux compatibility.

## Supported scope

The strongest tested paths are **C programs and libraries**, **Python standard-library applications**, and small static websites (which still need human visual checks). Fifteen language profiles are available: C, C++, Python, JavaScript, TypeScript, Rust, Go, Java, C#, Swift, Kotlin, Ruby, PHP, Lua and R. Profiles report missing tools; they do not install them or certify framework support. C++, JavaScript, Swift and Ruby have local runtime smoke checks; missing toolchains remain unverified. C# needs a prepared offline restore environment.

It generates runnable source projects, not signed installers or universally portable executables. GUI frameworks, automatic package installation, full-stack deployments, scanned-PDF OCR, and automatic rollback UI are not included. Read **EXPERIMENT CHECKLIST.md** for current limitations and the assisted Sky Hopper trial. The **Planning Guide** folder contains the detailed planning handoff and reusable prompt.

## Building entirely in C

Specify “Implement the entire project in C11, including tests” in your plan, or drop in **Try C.md**. The agent generates `.c` and `.h` files, compiles with the installed Apple Clang compiler, executes C assertion tests, and launches the resulting executable with **Run project**. C source and headers remain available to the model during follow-up edits. Compiler errors and failing test executables feed into the repair loop.

Use commands such as `clang -std=c11 -Wall -Wextra main.c -o app`, then `./app`. Commands execute separately without shell expansion; list source files explicitly. The `cc` and `gcc` names are mapped to Apple Clang on this Mac. The generated executable targets this Mac; cross-compilation and automatic external-library installation are not provided. The builder itself still uses its existing Python service and native Mac launcher.

For a reusable static library, try **Try C Library.md**. The app supports compiling `.o` files, archiving them with `ar rcs`, linking consumer programs, and running their tests. Under **C libraries and dependencies**, you can import a small local source folder (including its license) into `vendor/`. You can also list already-installed `pkg-config` library names; the compiler and portable helper resolve their build/link flags. Missing dependencies are reported before starting. Standard system libraries can be linked directly in the plan. Large library trees, downloading libraries, and package-manager installation are not automated.

Compilation failures stop the entire check sequence. A native executable is accepted as a check only if it was built earlier in the same sequence. Run Project rebuilds recorded compile commands first, so edits do not silently launch an old executable. Export requires a matching source fingerprint from successful checks.

Text PDFs are supported through macOS PDFKit. Word import extracts text, not embedded graphics. Plans are limited to 10 MB and 60,000 extracted characters. Current project context is limited to 100,000 characters. Model quality and speed depend on the loaded model and hardware.

“Complete” means the generated automated checks passed, including a final regression run. Those checks are written by the same model: they are useful evidence, not a guarantee that every requirement or visual detail is correct. Review and try the output. The app rejects unittest runs that discover zero tests.

## Local execution

Inference goes only to `127.0.0.1:1234`. Generated command execution uses macOS `sandbox-exec`, disables network access, restricts writes to the project, denies reads of other user folders, and protects Git metadata and the run record. System runtime files remain readable. Generated browser pages opened with **Run project** use your ordinary browser and its normal permissions.

The app requires this Mac's existing `/opt/homebrew/bin/python3`, macOS frameworks, and system Git. The application contains its service/UI resources and can be moved as a unit. It is locally signed, not notarized for general distribution.

## Validation

- Real LM Studio `qwen2.5-coder` build: temperature converter, unit tests, Git checkpoints, final verification.
- Real follow-up: Kelvin conversion added; expanded tests passed.
- Automated checks cover imports, HTTP authentication, path traversal, sandbox network/write denial, protected Git metadata, and the earlier planner.
- Portable library tests build a static archive, link a consumer, export only source, move it to another folder, then rebuild and test it there.
- Recovery tests cover unfinished-task resume, repair feedback, and stale-binary rejection.

The portable tests run locally on macOS. Linux execution has not been performed here. `ci/portable-projects.yml` is an optional macOS/Linux GitHub Actions template; it is not enabled automatically.

Run developer tests from this folder:

```sh
python3 -m unittest discover -s tests -v
```

Desktop source is in `local_builder/desktop.py` and `local_builder/ui.html`; the native launcher is `Launcher.swift`. The earlier planning CLI remains available but is separate from the desktop execution path.
