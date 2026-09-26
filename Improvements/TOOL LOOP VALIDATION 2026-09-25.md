# Tool-loop validation — September 25, 2026

## Result

The experimental local tool loop produced working Python and C command-line projects. All generated project implementation and test source came from the locally running Qwen3.5 35B A3B model through LM Studio, loaded with 32,768 context. No assistant-authored implementation or test replacement was used to make the projects pass. The assistant did fix orchestration defects discovered during the trials.

This was a development/debugging session, not a controlled reliability benchmark. It does not establish a success rate for arbitrary plans or confirm a fully autonomous game build.

## Trials and interventions

| Output folder under Documents/AI Builder Projects | Observed outcome |
| --- | --- |
| Local Tool Loop Temperature | Model wrote 25 Python tests, encountered two failing error-message assertions and repaired them. A host bug allowed the final smoke command to replace the suite in the recorded recipe. The host bug was fixed; all original locally selected checks were recovered from the trace and rerun successfully. No project source changed during that recovery. Do not count the initial Complete status as correct full verification. |
| Local Tool Loop Temperature 2 | Initially stopped on repeated malformed command arrays. The host had retained an invalid command, preventing recovery. Validation was moved before recipe accumulation, and Resume was used. The model regenerated its draft, encountered a lowercase-unit behavior failure, repaired its implementation and passed all 34 tests. Final verification retained the suite plus four demo commands. |
| Local Tool Loop C Library | Passed without manual source repairs. Model produced a header, implementation, demo, README and six C assertions. Built an object, static archive, demo and test executable, then passed trial, accepted-folder and final checks. Demo prints that 20 Celsius equals 68 Fahrenheit. |

C source and test hashes matched all five recorded local-model file hashes. Python Temperature 2 hashes matched all four recorded local-model file hashes. App-owned portable helpers are separate from that generated source provenance.

## Verification completed

- App regression suite: **58 tests passed**. This includes the existing 56 tests and two new local-model-authored tests covering path protections and model capability preflight.
- New test module: `tests/test_tool_agent.py`. Initial drafts came from Qwen3.5 35B A3B; Qwen2.5 Coder repaired the import and syntax problems after feedback. No assistant-authored test code was substituted. SHA-256: `f565cd7532539bcba004b513cc12651246d8a7b2c1e401e89e2f7c108af20a0e`.
- Desktop UI JavaScript syntax check passed.
- Desktop app rebuilt; ad-hoc signature verification passed. Packaged tool-agent and UI resources match current source.
- C portable `project.py run` rebuilt and launched the generated demo successfully on this Mac.
- C and Python source ZIPs exported under `Documents/AI Builder Projects/Exports`.
- Git diff whitespace check passed for tracked changes.

Tests written by the implementation model are evidence, not independent proof. Test counts alone do not establish test quality or coverage.

## Try the result

1. Quit any older AI Builder window and reopen **Desktop/AI Builder.app**. Existing running services do not automatically reload rebuilt code.
2. Choose **Tool loop — experimental, local-model tests** for new builds.
3. Qwen3.5 35B A3B is left loaded for experimentation. Do not select the non-tool-capable Qwen2.5 Coder in this mode; it was used separately for test-file editing.
4. Choose a destination and project name, import `Improvements/TRY LOCAL TOOL LOOP.md` or `Try C Library.md`, then Start.
5. To try the completed output immediately, open `Documents/AI Builder Projects/Local Tool Loop C Library` or `Local Tool Loop Temperature 2` and double-click `START.command`. Review generated code first; this launcher uses ordinary account permissions.
6. The same folders can be opened in VS Code. Transfer their source ZIPs to Linux and rebuild there; Linux execution has not been checked in this session.

## Not yet verified / next work

- Repeat fresh builds on the final engine without intervening host fixes. Do not count resumed debugging runs as independent clean successes.
- Native-window drag/drop, Pause/Stop and complete workflow interaction need a fresh manual UI pass. Backend build/resume calls were exercised directly in this session.
- Add local-model-authored transcript tests for recipe accumulation, invalid-command recovery, transactional promotion, rollback and context exhaustion.
- Fully local game generation plus real-browser gameplay and visual review remain outstanding.
- Patch-based edits, conversation compaction, native request cancellation, Linux validation and hardened sandbox review remain on the roadmap.
- The working folder contained substantial pre-existing uncommitted changes. They were preserved. This session did **not** commit or upload the mixed worktree to GitHub.

See `TOOL LOOP IMPLEMENTATION.md` for architecture, upstream sources, limits and the longer polish checklist.
