# Ready to experiment - prototype handoff

## Start here

1. Open **AI Builder.app** from your Desktop.
2. In LM Studio, load a coding model and enable the local server on port 1234.
3. Enter a project name and choose **Save new projects in** before starting. The builder creates a new named folder and never overwrites an existing one.
4. Drop a short plan into the app. Start with a small utility or the supplied example plans.
5. After checks pass, use **Open folder**, **Test project**, and **Run project**. Inspect the result yourself before trusting it.
6. Reopen a project from the recent list to request changes. Use **Export source ZIP** to move reviewed source to another computer.

## Sky Hopper trial

The playable game is in `Documents/AI Builder Projects/Sky Hopper`. Double-click `index.html`. Space/click/tap flaps, P pauses, and Start / Restart begins a new round. No engine, server, or downloads are required to play.

**This was an assisted result, not an autonomous success.** The real local model produced a draft, but generated invalid Node/browser assumptions, an undeclared Python dependency, and broken game logic. Direct repairs and independent behavioral assertions were needed. The final Node behavior tests and Python structure tests pass. Browser automation could not open the local file under its security policy, so a human visual/play check remains required.

The test exposed and fixed a builder issue: Node needs metadata access to exact ancestor directories to resolve files. Other user-folder contents remain denied. The destination picker now opens as a sheet in the main window.

## Highest-priority rough edges

Latest polish: 30 application tests pass. The UI shows elapsed inference time and clearer timeout/invalid-response messages; Resume can retry an interrupted planning stage. Language-tool status refreshes, and reopen uses the native in-window folder picker. Immediate inference cancellation is still unfinished.

1. **Independent acceptance checks:** the same model currently writes implementation and tests. Keep requirements separate, detect omitted requirements and weakened assertions, and add visual/browser checks with explicit user review.
2. **Model reliability:** benchmark several installed coding models; smaller models can ignore interfaces, dependencies, and units. Add an editable task preview and a vetted set of small project templates.
3. **Failure classification:** distinguish missing tools, sandbox failures, invalid model JSON, inference timeout, and implementation bugs. Do not spend model repair attempts on an environment failure.
4. **Responsive progress/cancellation:** inference can take minutes; Stop does not immediately cancel an in-flight model request. Add elapsed-time display, streaming and backend cancellation.
5. **Recovery:** checkpoints and resume exist, but there is no friendly checkpoint diff/restore interface or robust crash recovery for every intermediate write.
6. **Toolchain onboarding:** fifteen profiles exist, but only installed runtimes can run. C#, Rust, Java, Kotlin, Go and other missing tools need separately prepared environments. A profile is not proof of framework support.
7. **Security hardening:** this is experimental local execution, not a reviewed hostile-code isolation system. Browser output and Run in Terminal use ordinary user permissions. Avoid secrets, sensitive data, and untrusted large projects.
8. **Portability/distribution:** generated source has portable instructions and ZIP export. The builder itself is macOS-only and depends on the existing Homebrew Python path. Linux end-to-end validation, bundled runtimes, signing and notarization remain unfinished.

## Practical limits

Use 1-3 small tasks, standard libraries, offline fixtures and precise checks. Readable PDFs work; scanned PDFs need OCR. No automatic package installation, arbitrary large app generation, guaranteed autonomous completion, or universal executable/installer packaging is promised.
