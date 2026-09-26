# AI Builder: precise and efficient local software generation

Assessment and implementation roadmap | 25 September 2026

## Decision in brief

Improve the execution loop before expanding the range of software it promises to build. The failures involve model mistakes, insufficient context/output space, incomplete feedback and imperfect verification. A larger model or a longer prompt alone will not address all four.

The goal is repeatable software generation and repair using installed local models, with measurable correctness, bounded time/memory use, no cloud fallback and no undisclosed external source-code repairs. This is a roadmap, not a claim that its proposed features are implemented. A separate human/assistant-authored plan and app-owned tests are compatible with local-generated implementation, but must be disclosed.

## Evidence and limits

This assessment inspected local source, the reliability report, saved project state and the current test suite. No fresh model benchmark was run during this documentation update, no generated game files were edited, and no models were loaded or unloaded.

- `RELIABILITY TRIAL.md` records 13 fresh validation runs across qwen2.5-coder and qwen/qwen3.5-35b-a3b. Prompts and checkers changed between batches: these are debugging trials, not a controlled ranking or comparable model success-rate sample.
- Saved projects under `Documents/AI Builder Projects/Sky Hopper Validation*` corroborate invalid/empty responses, public-interface mistakes, collision and score defects, and UI failures. Validation 6 retains recheck output rather than a complete original run record; do not infer its missing metadata.
- Validation 10 returned no complete code; 11 exhausted its response budget; 12 checkpointed the core but did not finish the UI. The report attributes reasoning/context problems using contemporaneous diagnostics. Not every old run retains enough telemetry to reconstruct token use or exact settings.
- The report says the trial models were loaded with 8,192-token contexts. Current `model_json` requests 10,000 output tokens without adapting to loaded context and prompt size. This is a budgeting risk, not proof of the cause of every server rejection.
- `Flappy Bird Test - Transactional` is marked Complete, and the user reports the game works. Its known history includes local-model core code and externally authored UI. Its saved state has no complete per-file local provenance. It is an assisted demonstration, not an entirely local-generated success.
- Current verification: `python3 -m unittest discover -s tests -v` ran 56 tests in 6.033 seconds with all passing on this Mac. This tests builder behavior and fixtures, not reliable autonomous model output. Recent model-manager and provenance changes still need dedicated coverage and live integration testing.

### Current source versus delivered application

The repository is a dirty development tree with earlier in-progress changes. A source feature being present does not prove the packaged Desktop app contains it or that it passed live-model/browser testing. This update changes documentation only, apart from regenerating the guide PDF. Do not label the roadmap delivered based on these edits.

Already present: local inference endpoint; strict-JSON requests; three task attempts; temporary trial workspaces; checkpoint/resume; fresh-source verification for export; one narrow app-owned game acceptance profile; tailored response errors. Recently added source includes compact UI prompts, rejected-draft hashing, initial model-response logging/file hashes, and model inventory/load/unload controls. These require regression and end-to-end evidence before release claims.

## Diagnosed problems

| Problem | Evidence and consequence | Improvement IDs |
| --- | --- | --- |
| Context and output budgeting | Trials used 8K loaded contexts; prompts include source plus rejected drafts; fixed 10K response allowance. Truncation can occur before a useful repair arrives. | I01, I02, I03 |
| Exact contract violations | Wrong state fields, signatures, radius boundaries, scoring order and best-score updates recur in saved failures. Syntactically valid code is not enough. | I04, I05, I09 |
| Ineffective repairs | Repeated defects and whole-file regeneration consume attempts. Earlier no-progress logic compared unchanged accepted source; current source instead hashes rejected drafts. | I06, I07, I08 |
| UI integration is distinct work | Missing animation scheduling, unusable controls and persistence/rendering errors remain after core logic passes. | I09, I10 |
| Checker mistakes distort results | Validation 6's apparent success was invalidated after harness correction. Simulated events lack some real-browser semantics. | I09, I10, I15 |
| Generic checks lack independence | Outside the game profile, the coding model proposes implementation and checks. A pass can omit user requirements. | I05, I09 |
| Scope/protection mismatch | UI prompt says ONLY certain files, but generic allowed-file enforcement is absent; worker ignores core edits in UI while a lower-level validator would reject them. | I04, I07 |
| Requirement loss in specialized mode | The fixed game profile bypasses general planning; prompts use its contract rather than arbitrary plan additions or requested changes. Extra requirements can be silently absent. | I04, I05 |
| Incomplete provenance | A Complete badge does not establish who wrote each file. Initial response hashes do not yet prove all delivered files match accepted local outputs. | I11, I12 |
| Cancellation and recovery limits | Blocking inference may continue after Stop; final multi-file writes are not a crash-safe transaction. Resume skips passed tasks without a new dependency analysis. | I08, I13, I14 |
| Missing comparable measurements | Settings/checkers changed across trials; elapsed time alone does not identify prompt, inference, repair or test cost. | I15, I16 |

The historical trials support the listed symptoms. Broader claims about model families, ideal context sizes or which model is best remain hypotheses until measured under frozen conditions.

## Priority 0: establish trustworthy generation

Each item has an implementation owner area and a completion test. All are open unless explicitly marked as partially present. P0 items should precede additional languages/frameworks.

### I01 - Model capability and readiness preflight

Owner: model manager and request client. Dependency: none.

Read installed identity and actual loaded instance/context. Run a tiny structured-response probe before a long build; verify supported schema and reasoning controls, not only server reachability. Record backend/model settings when available. Require correct local endpoint and toolchain; report missing readiness without creating a half-built project. Cache successful probes keyed by settings/version and invalidate when they change.

Done when: unloaded model, unreachable server, unsupported schema and mismatched instance each produce a distinct actionable message and no implementation request. A supported local model passes the probe. No automatic cloud fallback.

### I02 - Token-aware context and output budgets

Owner: request client and context builder. Dependency: I01.

Use backend token counting when available, otherwise a conservative clearly labeled estimate. Enforce input + reserved output + safety margin <= actual loaded context. Include schema/instruction overhead and possible reasoning. Replace the fixed 10K maximum with a bounded per-task allowance. If a complete file cannot fit, split the task or ask to reload with a tested larger context; never silently truncate source or acceptance requirements.

Done when: near-limit normal and repair requests are rejected or reduced before inference; test both small and larger configured windows. Record the estimate/actual usage where available. Avoid raising context blindly into memory pressure.

### I03 - Task-specific context with a visible manifest

Owner: context selection. Dependencies: I02, I04.

Send relevant source, exact dependency interfaces, active requirements and concise failure evidence. Deduplicate plan text; label accepted code versus rejected drafts. Surface omitted/oversized files instead of silently dropping them. UI tasks need their HTML, CSS, bindings and stable core API; current specialized context only selects index.html/game.js. Start with deterministic file/dependency rules; do not require a vector database.

Done when: every request records included/excluded paths and reason; a needed oversized file blocks or is explicitly chunked; cross-file repair fixtures retain required imports and API context. Compare token use and success against full-context baseline, without assuming savings improve correctness.

### I04 - Machine-validated task contracts and edit boundaries

Owner: plan import, task compiler, file validator. Dependency: none; use I01 for execution readiness.

Compile plans into stable requirement/task IDs, dependencies, editable files, read-only interfaces, checks and launch metadata. Add a preview before generation. Reject inconsistent units/signatures, missing prerequisites and unsupported profile changes. Validate the complete response's paths, types, duplicates, file set and launch before writing. Make attempted protected edits a consistent, visible policy outcome rather than relying on prompt wording.

Done when: a UI-stage core rewrite, an unexpected file, duplicate path, invented dependency or missing required deliverable is caught before application. Custom requests incompatible with sky-hopper-v1 are surfaced, not silently ignored. Preserve existing plan-import workflows.

### I05 - Requirement-to-evidence ledger

Owner: plan compiler and reporting. Dependency: I04.

Track each requirement through planned task, accepted implementation, automated evidence and named manual review. Treat passing compilation as build evidence only. Show uncovered/unsupported requirements explicitly. A second local-model review may help find omissions but is not independent proof.

Done when: a missing requirement prevents an unqualified requirements-complete label even if all selected checks pass. Manual visual review remains pending until recorded. Profile-specific claims cannot be applied to generic projects.

### I06 - Classify failures before choosing a retry

Owner: worker and diagnostics. Dependencies: I01, I04.

Separate transport/server, resource/context, schema, prerequisite, policy, compilation, behavioral, checker and cancellation failures. Give implementation repair a compact packet: requirement, command, input, expected/actual, relevant source and allowed edits. Keep full logs locally; bound prompt excerpts. Retry only transient failures within a small transport budget. Do not spend code attempts on missing compilers or invalid settings.

Done when: fixture failures select the right recovery action; truncation is never patched into source; missing tools cause no new code generation; a failed behavior supplies its reproducer. No unbounded retries hidden inside the three-attempt task limit.

### I07 - Verify that a repair changed the rejected candidate

Owner: worker and tests. Dependencies: I04, I06.

The source now hashes pending drafts rather than the unchanged accepted workspace. Add regression tests for different repairs with the same failure, identical repairs, reordered file lists and temporary paths. Compare canonical path/content maps, check commands and normalized failure identity. First repair fixes the focused defect; the next must justify a distinct strategy within the existing attempt cap. Always run regression checks before acceptance.

Done when: changed candidates with the same remaining assertion are not prematurely stopped; identical relevant code/checks/failure stop reliably. Earlier passing behavior cannot be traded away. This recent source fix is not yet backed by all these targeted tests.

### I08 - Preserve accepted work transactionally

Owner: workspace/checkpoint manager. Dependencies: I04, I07.

Keep current isolated trials. Add a durable apply journal, atomic staging where practical, file-hash preconditions and crash recovery around multi-file application/checkpointing. Detect concurrent user edits before replacing source. On resume, bind task/check evidence to source, contract and checker hashes; invalidate dependent stages when they changed. Current resume skips Passed status without that full analysis.

Done when: injected interruption at each apply step leaves recoverable old or new state, never silently mixed source marked verified. A user edit is preserved and prompts reconciliation. Restored checkpoints reproduce recorded checks.

### I09 - Trustworthy independent checks beyond one game

Owner: acceptance framework. Dependencies: I04, I05.

Version app-owned requirement checks separately from generated implementation. Add small independently specified CLI/data/website profiles with normal, edge and invalid cases. Prove each important gate with known-good and intentionally broken fixtures. Review false failures as checker bugs, not reasons to weaken requirements. Recheck earlier successes whenever the checker changes.

Done when: each supported profile rejects deliberate defects, omissions and fake model-written passing tests; evidence includes checker hash, source hash and executed assertions. Generic projects remain explicitly less verified until their acceptance specification is independently reviewed.

### I10 - Real-browser interaction gate

Owner: browser verification. Dependency: I09.

Keep fast pure-logic checks, then run the actual page with real events: initial display, Start, pause/resume, restart, keyboard repeat, pointer input, storage persistence/failure and narrow viewport. Capture console errors and external requests; use an isolated browser profile with network blocked for offline acceptance. Do not call an ordinary browser network-isolated merely because compilation is sandboxed.

Done when: a dead button, duplicate loop, missing script, blank canvas or remote dependency fails the relevant check. Compare simulated fixtures against browser behavior, including event.target/currentTarget and handler binding. Retain human playability/accessibility review; automated screenshots are not a complete visual-quality verdict.

### I11 - Verifiable local-generated provenance

Owner: request audit, file application and export. Dependencies: I04, I08.

Extend the existing response log/file hashes into a run manifest: model instance, local endpoint, available settings, prompt hash, accepted response hash, original file origins, applied bytes, final source hash and checker results. Distinguish local-generated implementation, imported code, app infrastructure and external edits. Rehash at completion/export; missing or changed evidence downgrades provenance independently of test status.

Done when: every claimed local-generated implementation file maps to accepted local response bytes, and a manual edit invalidates that claim. A pre-existing/template file is not relabeled generated. A fresh game with HTML, CSS and both JS files produced locally passes checks without assistant source repair. This is audit evidence, not tamper-proof attestation.

### I12 - Protect local-only operation and private logs

Owner: request routing, sandbox and export policy. Dependencies: I01, I11.

Make local inference a validated setting with no silent remote fallback; test that redirects cannot send prompts off-machine. Separate inference, dependency installation, Git transfer and generated-app networking permissions. Treat imported plans/repository comments as task data, never new authority. Raw response logs can contain source/private text: keep them local, excluded from normal exports and Git, with explicit diagnostic-sharing consent and retention limits.

Done when: remote endpoint/redirect and attempted network use fail closed in local-only modes; authorized Git transfer remains separately selectable. Export/diagnostic tests exclude audit logs and secret fixtures. Local generation does not falsely imply the produced app is safe.

## Priority 1: efficiency and everyday stability

### I13 - Model loading that cannot disrupt a build

Owner: model-manager UI/service. Dependency: I01. Status: initial implementation present, live validation pending.

Show actual loaded instances/context, selected coding instance, operation progress and errors. Serialize load/unload with builds. Require explicit unload and preserve other apps' instances. Already-loaded models must not silently claim a requested context change occurred. On timeout refresh actual server state before offering retry. Benchmark memory pressure and load time without inventing memory figures.

Done when: double clicks, stale inventory, timeout, load failure and unloading during a build behave safely; the UI remains responsive; loaded context shown equals server state.

### I14 - Responsive progress, cancellation and bounded resources

Owner: inference client, worker and subprocess runner. Dependencies: I06, I08, I13.

Stream progress where supported without applying partial JSON. Distinguish request sent, generating, checking, applying and checkpointing. Request cancellation if supported; otherwise label cancellation pending, block overlapping work and discard late responses. Bound run time, output/log size, disk growth and subprocess lifetimes; preserve resumability after limits.

Done when: Stop never accepts a late draft, spawned checks terminate safely, UI stays usable, and interruption tests preserve last accepted work. Measure cancellation latency; do not promise backend cancellation if unsupported.

### I15 - Frozen local benchmark and honest scoreboard

Owner: tools/benchmark_sky_hopper.py and benchmark fixtures. Dependencies: I05, I09-I11, I16.

Freeze app revision, plan, checker, model/quantization, loaded context, sampling settings and hardware. Separate warm/cold runs and assisted/unassisted outcomes. Start with the game, one CLI and one small existing-code change. Use fresh folders; do not hide failures through manual resume or source edits. Add a change-preservation benchmark, not only greenfield generation.

Done when: every run records full inputs/settings or explicitly unknown fields, attempts, outcome, evidence and assistance. Run at least five fresh repetitions per tested configuration for initial comparison; report counts and variability, not a universal model ranking. Larger evaluation is required for strong reliability claims.

### I16 - Measure where time and tokens go

Owner: telemetry and reporting. Dependency: I01.

Record load/probe/prompt/inference/test/apply time separately, actual token usage when available, response termination, attempts, files changed, test totals and manual intervention. Keep logs bounded and local. Optimize full-file responses only after measuring waste. Consider guarded patches with exact base hashes later; malformed/stale patches must fail without modification.

Done when: a slow build can be attributed to measured stages; a candidate optimization improves median end-to-end time or resource use without lowering acceptance success on the frozen suite. Fast invalid output is not progress.

## Priority 2: expand after the baseline is reliable

### I17 - Context and dependency-aware incremental editing

Build a repository map and dependency-aware affected-test selection. Initially rerun all final checks; optimize subsets only with demonstrated coverage. Add patch mode with preconditions after I08/I16, not as an unvalidated shortcut. Preserve existing code style and user changes.

Done when: a small change avoids unrelated rewrites, stale patch bases are rejected, and hidden cross-file dependency fixtures still trigger required checks.

### I18 - Local model role routing, only if measured useful

Compare one model against a local planner/coder/reviewer pipeline using the same frozen tasks and total resource budget. Include model-switch cost and shared-memory pressure. Never treat agreement between local agents as acceptance evidence. Keep the simpler single-model default until the alternative wins measured end-to-end reliability or efficiency.

Done when: repeated runs demonstrate the gain, disclose cost/latency, and retain independent checks and no cloud fallback. This is an experiment, not a recommended automatic multi-agent rollout.

### I19 - Reproducible dependency and portability support

Record runtime/package versions and licenses. Offer offline cached dependencies first; network installation requires separate permission and isolation. Test clean exported source on each claimed target OS before claiming support. Add profiles individually rather than listing toolchains as proof of tested framework support.

Done when: an export rebuilds/tests in a clean prepared environment with no hidden machine-specific dependency. Untested platforms are clearly labeled.

### I20 - Maintain the planning contract with releases

Owner: documentation plus release checks. Dependencies: I04, I05.

Keep Planning Guide/how to make a code plan.md as the editable source, regenerate its PDF, and align PROJECT_PLAN_TEMPLATE.md with actual parser/worker behavior. Update examples, limits, protected files, local-only policy and release status whenever behavior changes. Add automated consistency checks for documented limits and fixture plans. Archive dated trial reports; do not rewrite historical evidence as if new features existed then.

Done when: a release includes matching guide/template/app capabilities and no unsupported guarantees. This document and guide v0.4 are the first documentation update; automated synchronization is not implemented.

## Implementation order and release gates

1. Baseline integrity: I01, I04, I06, I07, I16; cover recent in-progress changes with targeted tests. Preserve the current 56-test baseline.
2. Reliable requests and repair: I02, I03, I08; prove resource limits, changed-repair handling and interrupted application in fault-injection tests.
3. Truthful local completion: I05, I09-I12; produce a fresh entirely local game, verify provenance and play it in a real browser. No manual implementation edits to make this demonstration pass.
4. Repeatability and usability: I13-I15; then frozen repeated trials. Do not declare general reliability after one working game.
5. Broader capability: I17-I20, with documentation maintenance continuing throughout.

Suggested initial promotion target, not an achieved metric: at least 4 of 5 fresh runs per selected small template complete within the attempt cap, zero source edits by an external coding assistant, zero accepted intentionally broken fixtures, and matching provenance for every claimed generated implementation file. Report absolute median/range of duration plus manual review outcomes. Five runs are a development gate, not statistical proof of broad reliability.

## Measurement definitions

- First-attempt pass rate: tasks accepted on first candidate / attempted tasks; report by template/configuration.
- Autonomous completion: fresh runs satisfying all required automated checks with no external code repair / all started fresh runs. Report blocked runs separately but do not silently remove them from the denominator.
- Repair conversion: failed first candidates that pass within the allowed task budget / failed first candidates.
- False completion: accepted outputs later shown to violate required acceptance; retain original checker version and corrected recheck outcome.
- Provenance coverage: verified local-generated implementation files / files claimed local-generated; also report imported/app-supplied/unknown files.
- Efficiency: end-to-end elapsed time, phase durations, tokens if available, attempts and memory measurements; report missing metrics as unknown.
- Manual review: pending/pass/fail with reviewer/time and concrete observations; separate from automated completion.

## What not to do

Do not hide failures by loosening checks, hand-authoring missing UI or calling assisted output local-generated. Do not enlarge every prompt or context window without measurement. Do not automatically download models/packages, push source, unload another app's model or move inference to the cloud. Do not expand to large frameworks before small tasks pass repeatably.

## Evidence locations for maintainers

- `local_builder/desktop.py`: model_json, context, acceptance_context, worker, trial_workspace, run_checks and export gates.
- `local_builder/acceptance.py`: fixed contract, UI_CONTRACT and simulated checker.
- `local_builder/model_manager.py` and `local_builder/ui.html`: model lifecycle source under development.
- `tests/test_acceptance.py`, `tests/test_workflow.py`, `tests/test_polish.py`: verification/repair fixtures and current gaps.
- `RELIABILITY TRIAL.md`, `INDEPENDENT CHECKS.md`: dated trial interpretation and coverage limits.
- `Documents/AI Builder Projects/Sky Hopper Validation*` and `Flappy Bird Test - Transactional`: saved local run evidence; inspect .builder.json and logs without modifying them.

This assessment relies on this project's local evidence. It does not assert undocumented capabilities or current comparative rankings of external products/models.
