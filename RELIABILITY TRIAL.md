# Sky Hopper reliability trial - 24 September 2026

## Method

Fresh, uniquely named projects were generated through the normal builder worker and the local LM Studio server. Generated implementation files were not manually repaired. The existing assisted Sky Hopper demo was left unchanged. Each task had at most three attempts and had to pass app-owned checks before checkpointing. No new models or packages were downloaded.

This was an iterative engineering trial, not a controlled model ranking: instructions, diagnostics and checks improved between batches. The two configured models were loaded with an 8,192-token context. An installed model's advertised maximum is not the context actually loaded.

## Results

| Batch | Local model | Fresh runs | Result |
| --- | --- | --- | --- |
| Initial profile | qwen2.5-coder | 2 | Both stopped without completion: incorrect collision behavior; one run also received a server rejection. |
| More explicit contract | qwen/qwen3.5-35b-a3b | 2 | Both responses were rejected as invalid/incomplete before implementation files were applied. |
| Tighter prompts and no-progress detection | qwen2.5-coder | 2 | First run stopped on repeated collision/best-score failures. The second initially appeared to pass, but a corrected UI event harness rejected it on re-verification. |
| Corrected event harness | qwen2.5-coder | 1 | Core stage stopped after repeating the same ceiling-boundary defect. No UI files were requested and the run was not marked complete. |
| Exact ceiling/ground formula | qwen2.5-coder | 1 | Ceiling/ground behavior passed, but core stopped after repeating a pipe-gap collision that ignored the bird radius. The contract now includes the exact overlap formulas. |
| Exact pipe-overlap formulas | qwen2.5-coder | 1 | All three core attempts remained incompatible with the required public state. The run stopped Needs attention and never reached UI generation. |
| Stronger reasoning model | qwen/qwen3.5-35b-a3b | 1 | The model spent its entire response allowance on reasoning and returned no structured answer. No files were applied. The builder now requests reasoning off for structured generation. |
| Reasoning disabled | qwen/qwen3.5-35b-a3b | 1 | The model returned a mostly compatible core, but the repair response was truncated against the loaded 8K context. Independent-template prompts now omit duplicated plan and generic guidance. |
| Compact specialized prompt | qwen/qwen3.5-35b-a3b | 1 | Core passed and was checkpointed after one repair. UI stopped after repeating a start-only animation loop. The UI contract now makes continuous scheduling, raw score text and Ready-state storage loading explicit. |
| Full hardened pipeline | qwen/qwen3.5-35b-a3b | 1 | Fresh core stopped safely on repeated scoring and best-score defects. This run confirms rejection remains strict; it does not establish repeatable autonomous success. |

The reasoning-prefix, empty-answer and server-error diagnostics were improved after the second batch. Those parser changes have unit coverage, but the reasoning-model batch was not rerun with them. The initial server rejection's detailed body was not retained, so its cause is not established.

## What is established

- The independent gate detects broken physics and missing/nonfunctional UI instead of trusting model-written passing tests.
- The model cannot replace the checker through normal generated edits or command writes.
- Repeated identical failures stop; active tasks are labeled Needs attention on model/server failures.
- Failed checks invalidate older verification. Partial builds and build-only checks cannot qualify source for verified export.
- The app has 46 passing automated tests, including intentionally broken acceptance fixtures and recovery cases.
- Re-verification of `Sky Hopper Validation 6` with the corrected harness failed three requirements: best-score preservation, persisted-score rendering, and functional start controls. It is not a verified successful build.
- Fresh run `Sky Hopper Validation 7` correctly stopped as Needs attention after two identical core failures. The contract now states the exact radius-aware ceiling and ground formulas to remove that ambiguity for later runs.
- Fresh run `Sky Hopper Validation 8` also stopped safely. It fixed the previous boundary defect but treated only the bird center as outside the pipe gap; the checker caught the missing radius overlap.
- Fresh run `Sky Hopper Validation 9` produced incompatible state fields across three attempts. The bounded repair loop stopped it; no failing output was certified or exported as verified.
- Fresh run `Sky Hopper Validation 10` returned no code because reasoning consumed its output budget. A direct LM Studio compatibility probe confirmed that `reasoning_effort: none` produces an immediate structured answer, so builder requests now include it.
- Fresh run `Sky Hopper Validation 11` confirmed reasoning was disabled and produced source. Its first repair repeated defects; the next response reached the context/output limit. The specialized repair prompt is now smaller so an 8K loaded context has room for complete source.
- Fresh run `Sky Hopper Validation 12` is the first trial to pass and checkpoint the autonomous core stage. Its UI was rejected before completion because no animation frame was scheduled until Start. The passed core remains resumable.
- The first resume of Validation 12 correctly skipped its passed core but the UI response was truncated. Specialized retry context is now stage-bounded: core sees only `core.js`; UI sees only `index.html` and `game.js`.
- The second resume returned complete responses but attempted to rewrite the checkpointed core during the UI stage. Prompt-only protection was insufficient. The builder now hard-rejects any UI-stage `core.js` edit before files are written.
- Fresh run `Sky Hopper Validation 13` exercised the complete hardened pipeline. The model repeated two core defects, so no checkpoint or completion was issued. Validation 12 remains the only run in this batch that passed the core stage, and no run has passed the full UI gate.

## What is not established

Reliable autonomous generation has not been demonstrated across repeated fresh builds. No fresh run in this trial is currently verified as complete. Unit tests of the builder do not prove model reliability. The UI acceptance harness simulates events and canvas calls; actual browser visuals, playability, keyboard focus, resizing and accessibility still require a person to try the result. Linux has not been exercised here.

## Reproduction and next decision

See INDEPENDENT CHECKS.md and tools/benchmark_sky_hopper.py. The local validation folders retain actual source, state, errors and passing checkpoints. Start with model-response compatibility and enough loaded context, then repeat the same frozen contract and checker. Do not add more project types or claim general-purpose reliability on the basis of one passing run.
