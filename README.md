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
3. Click **Start build**. The app creates a new project under **Documents / AI Builder Projects**.
4. Follow the task list and activity log. Each task gets up to three generation/test attempts. Passing tasks get Git checkpoints; all collected checks run again at the end.
5. Click **Run project** or **Open folder**. Python output appears in Activity; static HTML opens in your browser.
6. Describe a change in **Make a change** and click **Apply change**. Existing files are included in the model context and prior recorded checks run again.

Use **Pause / Resume** between model calls or commands, and **Stop** to cancel further work. A running inference request may take up to five minutes to return; a running test process is terminated promptly. Keep the app open while building.

To continue an older project, paste its folder path into **Reopen a project folder**. Files, task results, logs, and Git history are saved locally. An interrupted build can be continued through a change request describing what remains. Exact task-level crash resume is not implemented.

## Supported scope

This desktop release supports **C programs**, **Python standard-library applications**, and **static HTML/CSS/JavaScript websites**. It generates runnable projects, not signed installers or universally portable executables. GUI frameworks, package installation, full-stack deployments, scanned-PDF OCR, automatic rollback UI, and arbitrary external tools are not included. For projects with dependencies, install and review those separately.

## Building entirely in C

Specify “Implement the entire project in C11, including tests” in your plan, or drop in **Try C.md**. The agent generates `.c` and `.h` files, compiles with the installed Apple Clang compiler, executes C assertion tests, and launches the resulting executable with **Run project**. C source and headers remain available to the model during follow-up edits. Compiler errors and failing test executables feed into the repair loop.

Use commands such as `clang -std=c11 -Wall -Wextra main.c -o app`, then `./app`. Commands execute separately without shell expansion; list source files explicitly. The `cc` and `gcc` names are mapped to Apple Clang on this Mac. The generated executable targets this Mac; cross-compilation and automatic external-library installation are not provided. The builder itself still uses its existing Python service and native Mac launcher.

Text PDFs are supported through macOS PDFKit. Word import extracts text, not embedded graphics. Plans are limited to 10 MB and 60,000 extracted characters. Current project context is limited to 100,000 characters. Model quality and speed depend on the loaded model and hardware.

“Complete” means the generated automated checks passed, including a final regression run. Those checks are written by the same model: they are useful evidence, not a guarantee that every requirement or visual detail is correct. Review and try the output. The app rejects unittest runs that discover zero tests.

## Local execution

Inference goes only to `127.0.0.1:1234`. Generated command execution uses macOS `sandbox-exec`, disables network access, restricts writes to the project, denies reads of other user folders, and protects Git metadata and the run record. System runtime files remain readable. Generated browser pages opened with **Run project** use your ordinary browser and its normal permissions.

The app requires this Mac's existing `/opt/homebrew/bin/python3`, macOS frameworks, and system Git. The application contains its service/UI resources and can be moved as a unit. It is locally signed, not notarized for general distribution.

## Validation

- Real LM Studio `qwen2.5-coder` build: temperature converter, unit tests, Git checkpoints, final verification.
- Real follow-up: Kelvin conversion added; expanded tests passed.
- Automated checks cover imports, HTTP authentication, path traversal, sandbox network/write denial, protected Git metadata, and the earlier planner.

Run developer tests from this folder:

```sh
python3 -m unittest discover -s tests -v
```

Desktop source is in `local_builder/desktop.py` and `local_builder/ui.html`; the native launcher is `Launcher.swift`. The earlier planning CLI remains available but is separate from the desktop execution path.
