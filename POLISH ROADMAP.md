# AI Builder polish roadmap

## Product target

Open one app, drop in a project plan, choose a destination, click Build, and receive a clearly named folder containing working software, instructions, tests, and a launch action. Reopen that project later, describe changes, and confidently return to a previous working version when needed.

This is a prioritized backlog, not a list of features already implemented. Start with reliable output and recovery before adding more frameworks.

## Current testable version

- A macOS app with PDF, Word, Markdown, and text import.
- Local LM Studio planning and sequential code generation.
- C compilation and execution, Python programs, and static websites.
- Bounded repair attempts, test output, and Git checkpoints.
- Follow-up change requests and reopening a project by its path.
- Generated projects currently go to `~/Documents/AI Builder Projects` in the current user's home folder.
- The `Finished Projects` shortcut in this folder opens that location. It currently includes incomplete runs as well as completed ones; inspect each run's status.

Real-model Python and C builds have passed tests and launched successfully. Twelve automated application tests pass. These are initial checks, not a broad reliability benchmark.

## Priority 1 Make every result easy to find and run

- [ ] Add a native destination-folder picker before starting. Remember the last choice and display the exact path throughout the build.
- [ ] Ask for a readable project name instead of generating only random directory names. Handle duplicate names without overwriting files.
- [ ] Give every output folder a consistent structure: source, tests, build output, README, imported plan, and build report. Keep internal logs and state out of the user's main view.
- [ ] Define a project manifest containing language, toolchain, setup steps, build commands, test commands, launch command, working directory, and output paths. Validate it before executing anything.
- [ ] Make Run Project work by project type: launch a C executable, start a Python program, or open a local website. Provide terminal input for interactive command-line programs.
- [ ] Add a completion screen with Open Folder, Run Project, Request Changes, and Copy Run Instructions.
- [ ] Distinguish Building, Failed, Stopped, Checks Passed, and Ready for User Review. Never present failed or incomplete output as a finished product.
- [ ] Preserve build output separately from source so C executables are easy to identify and rebuild.

Done when: a user builds into a chosen folder with spaces in its name, closes the builder, and can still locate and run the output from its README or launcher.

## Priority 2 Make builds recoverable and trustworthy

- [ ] Persist each task transition and command result atomically. Recover after app closure, computer restart, model disconnection, or interrupted compilation.
- [ ] Add a real Resume button that continues the remaining tasks without replanning completed work.
- [ ] Serialize all build and run actions. Prevent double clicks or concurrent requests from starting overlapping jobs.
- [ ] Show changes before and after each task, with a clear record of files added and modified.
- [ ] Add a checkpoint browser and Restore Working Version action. Preserve current work on a recovery branch before restoring.
- [ ] Keep acceptance criteria separate from agent-generated implementation. Map every requirement to automated evidence or an explicit manual check.
- [ ] Detect weak success signals: zero tests, compile-only checks, stale binaries, skipped tests, and deletion or weakening of earlier tests.
- [ ] For C, stop a check sequence after a failed compile so an old executable cannot be mistaken for the newly compiled result. Record source and binary hashes.
- [ ] Rerun meaningful regression checks after changes, including earlier requirements that the new task did not touch.
- [ ] Add context selection for larger projects instead of sending every file or rejecting projects above the current size limit.
- [ ] Make retries explain what failed, what changed, and why another attempt is justified. Stop repetitive failure loops promptly.

Done when: an interrupted build resumes without losing edits, a failed compile cannot pass using an older binary, and restoring a checkpoint reproduces the previously passing result.

## Priority 3 Smooth first launch and everyday use

- [ ] Add an onboarding check for Python, Git, the local model server, available disk space, and the C compiler when needed.
- [ ] Explain missing prerequisites in plain language and provide exact corrective steps.
- [ ] Show which model is selected, whether it is responding, and when a request is still running. Let the user configure a local endpoint.
- [ ] Add a simple language choice: follow the plan, C, Python, or website. Respect that choice in planning, code, tests, and output.
- [ ] Preview imported text and highlight unreadable or unsupported content before starting. Explain scanned-PDF limitations.
- [ ] Replace the pasted-path reopen field with a native folder picker and recent-project cards.
- [ ] Add an editable task preview before execution and allow the user to correct misunderstood requirements.
- [ ] Keep progress understandable: current task, elapsed time, last activity, completed tasks, and whether it is waiting for the model or running a test.
- [ ] Improve Pause and Stop semantics. Cancel inference where supported, terminate child processes reliably, and explain exactly what has stopped.
- [ ] Warn before closing an active build and offer to stop safely or leave it running.
- [ ] Add accessible labels, keyboard navigation, readable contrast, resizable panels, and a compact view for small screens.

Done when: a new user can import a plan, start a build, find its output, request a change, and reopen the project without needing terminal commands or help from the developer.

## Priority 4 Expand the software it can produce

- [ ] Add isolated dependency environments with explicit approval for downloads and installation. Record versions and avoid changing global packages.
- [ ] Add C build adapters for Make and CMake, multi-file layouts, libraries, and debug/release builds. Keep direct Clang support for small projects.
- [ ] Add C diagnostics and sanitizers where supported, including memory-error and undefined-behavior checks.
- [ ] Add templates for useful deliverables: a C command-line tool, a Python utility, a small game, a website, and a simple local web application.
- [ ] Add GUI/game framework support with clear prerequisites and actual visual or interaction testing.
- [ ] Support long-running local servers and previews with reliable stop controls and port management.
- [ ] Add artifact checks for files and documents, beyond command exit codes.
- [ ] Offer packaging appropriate to the target: a runnable folder, an executable, or an application bundle. Explain platform compatibility.

Done when: each supported template has a fresh-environment build test, a launch test, and an example plan that users can reproduce.

## Priority 5 Harden distribution and maintenance

- [ ] Package or manage the runtime so the app does not depend on a fixed Homebrew Python path.
- [ ] Sign and notarize releases for distribution; add versioning, release notes, and an update path.
- [ ] Audit the local API, document parsing, symbolic-link handling, generated subprocesses, tool permissions, and log redaction.
- [ ] Extend resource limits to disk growth, memory, child-process count, and total build time. Keep output logs bounded.
- [ ] Separate model credentials and application settings from generated projects and exports.
- [ ] Add a diagnostics export that excludes document contents and secrets unless the user explicitly includes them.
- [ ] Maintain repeatable quality benchmarks across several local models. Measure usable-output rate, repair attempts, duration, and manual intervention.

Done when: a clean install works on a supported Mac, update/recovery paths are tested, and model-specific reliability is reported from repeated runs.

## Suggested next implementation batch

1. Destination picker, project names, manifest, and completion screen.
2. Recent projects and reliable resume.
3. Independent acceptance evidence, stale-binary protection, and checkpoint restoration.
4. Onboarding and clearer progress/cancellation.
5. Dependency environments and broader project templates.

## Testing checklist for this copy

- [ ] Open the Desktop AI Builder icon with LM Studio running.
- [ ] Drop in `Try C.md`; build, inspect the tests, and run the executable.
- [ ] Drop in `Try First.md`; build and run the Python example.
- [ ] Request one small change and confirm the old behavior still works.
- [ ] Use Open Folder and confirm the output is in Documents / AI Builder Projects.
- [ ] Reopen the project after closing the app and inspect its saved files and history.
- [ ] Record any confusing behavior in `TEST NOTES.md`.
