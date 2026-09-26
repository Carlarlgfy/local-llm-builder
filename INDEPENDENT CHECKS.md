# Independent acceptance checks

## What changed

`Try Sky Hopper.md` opts into `Acceptance profile: sky-hopper-v1`. This is a narrow, app-owned template with fixed interfaces, not a universal verifier. The builder creates two sequential tasks: pure game logic, then the browser interface. It supplies the contract to the local model and runs its own checker after each task and again at completion.

The model cannot replace or skip the checker through its file edits or command list. The builder regenerates `ACCEPTANCE.cjs` before checking and protects it from writes during command execution. The standalone exported copy is editable by its owner and is not a security boundary. Generated code still runs in the existing macOS sandbox; Node's VM is only a test harness, not a hostile-code isolation guarantee.

## Evidence covered

- Initial state, start and reset; preserved best score.
- Seconds-based gravity and flap; capped time steps and delayed spawning.
- Pipe movement, right-edge scoring exactly once, removal offscreen.
- Surviving the gap versus hitting a pipe, ceiling or ground.
- Pause/resume and freezing ended games.
- Local assets and required controls.
- Simulated button/keyboard/pointer events: start, pause, resume, lose, restart and reopening.
- A single animation loop, drawing activity and blocked-storage handling.

The checker is tested with intentionally broken fixtures, including a fake passing model check, wrong physics, a dead Start button and attempted checker overwrite. An omitted UI cannot complete a profile build.

## What it does NOT establish

The browser-event tests use a small simulated DOM/canvas. They do not run a real browser, judge artwork, verify all accessibility behavior, measure enjoyable difficulty or establish Linux compatibility. A page that draws the wrong picture can still pass the automated drawing-activity check. A human must play the game, resize it and close/reopen it in a real browser. Arbitrary custom features outside this fixed contract need their own checks.

Other project plans retain their existing model-written tests. They do not automatically gain independent requirements verification. Changes to physics or interfaces that contradict this profile will fail it; use another plan/profile for materially different games.

## Recovery

Up to three attempts are allowed per task. If identical source fails identically twice, the builder stops with a no-progress explanation. Model/server errors mark the active task Needs attention. Pick another model or fix the environment, then Resume build; passed tasks are retained. Server rejection details distinguish context limits from generic connection problems. Partial/empty model answers are rejected before writing generated files.

## Reproduce a fresh-model trial

Run `python3 tools/benchmark_sky_hopper.py --model MODEL_ID --runs 2` from the builder repository. It creates uniquely named Sky Hopper Validation folders under Documents / AI Builder Projects, uses the normal worker, and never edits generated implementation files itself. Each project retains its plan, task history, checks and Git checkpoints. A run counts as automated success only if the worker reaches Complete. Automated success still requires the manual review above.

The suite digest is recorded so results from different checker versions can be distinguished. Read the trial report separately; unit tests of the builder are not evidence that a particular local model reliably generates playable games.
