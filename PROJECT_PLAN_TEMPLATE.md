# Project

Name: Replace with a short project name

Plan version: 1 | Date: YYYY-MM-DD

Goal: Describe one small useful result. Replace all bracketed fields before importing this template.

## User outcome

[Who uses this? What do they enter or click? Give a complete example and expected result.]

## Scope

### Included

- R1: [Observable behavior with exact input/output.]
- R2: [Boundary/error behavior and data preservation.]
- R3: [Launch and interaction behavior.]

### Excluded

- [Explicit non-goals; keep this milestone small.]

## Constraints

- Language/runtime: [Installed language and version.]
- Platform: [Target OS/architecture; list untested platforms.]
- Model: [Installed local model and actual loaded context.]
- Inference: local LM Studio only; no cloud fallback or externally written implementation repairs.
- Network: [Fully offline, or separate explicitly authorized Git transfers.]
- Dependencies: [Standard library or named local dependency, version/license/location.]
- Budget: 1-3 small stages, at most three attempts per stage. Reserve context for rejected drafts, diagnostics and replacement files.

## Workspace

- Mode: [New project / existing code folder / Git clone.]
- Selected output parent or existing workspace: [Exact folder.]
- Baseline: [Commit and existing test result, or new project.]
- Preserve: [Existing files, tests and behavior.]
- Optional Git address: [None or destination. Authentication and an explicit upload action are required; an address alone is insufficient.]

## Architecture and interfaces

- [File path]: [Responsibility and allowed dependencies.]
- [Public API]: [Exact signature, input/output types, units, mutation and errors.]
- [State/data format]: [Initial values, transitions and invariants.]
- Boundary examples: [Normal, edge and invalid cases with expected results.]
- UI, if applicable: [Initial state; each event/control; rendered result; restart/reopen/storage failures; local assets.]

## Deliverables

- [Source files and runnable artifact.]
- README.md with build, test and launch instructions.
- [Tests and fixtures. Independent acceptance checks are separately owned/reviewed.]
- Handoff evidence: model ID, source origins/hashes, executed checks, known limitations and manual review status. Do not claim provenance if evidence is missing.

## Build stages

### Stage 1 Implement one complete testable behavior

ID: T1

Depends on: none

Requirements: R1, R2

Editable files: [Small explicit list.]

Read-only context: [Exact interfaces and dependencies needed.]

Work: [Implement one bounded behavior plus deterministic tests, not placeholders.]

Acceptance criteria:

- Command: [Explicit argument array; no shell operators.]
- Expected: [Exit code, actual assertions/test count and concrete behavior.]
- Negative case: [A deliberately incorrect result the check must reject.]

Preserve: [Interfaces, previous tests and unrelated files.]

On failure: report requirement, command, input, expected/actual result and diagnostic; repair only relevant source; rerun regression checks. Stop on unavailable prerequisites or contradictory requirements. Do not weaken tests.

### Stage 2 Integrate and deliver, if needed

ID: T2

Depends on: T1

Requirements: R3 and regression of R1-R2

Editable files: [Integration/UI and README only; preserve passed core.]

Work: [Connect the existing API; do not invent helpers or rewrite it.]

Acceptance criteria:

- Command: [Explicit build and behavioral check arrays.]
- Expected: [Concrete assertions and launch result.]
- Manual check: [Actual browser/UI steps if applicable; otherwise a user-facing smoke check.]

Remove the second stage if unnecessary. Add a third only for a distinct bounded increment.

## Final acceptance

- R1 -> [Check name, input, expected result and owner.]
- R2 -> [Check name, input, expected result and owner.]
- R3 -> [Automated check and/or named manual review.]
- Rebuild current source, run all earlier tests and launch the artifact.
- Disclose incomplete work. Passing automated checks does not prove all requirements or local authorship.

For a fixed acceptance profile, use its exact contract without contradictory custom behavior. Generic plans do not automatically receive independent acceptance checking.

## Run instructions

[Exact launch command/file, working directory, expected result and stop/exit steps. No hidden download prerequisite.]

## Permissions

- Read/write: selected project only; preserve unrelated user work.
- Commands: [Explicit locally installed tools.]
- Network: none for generated build/test commands.
- Secrets: none; no credentials in plans, logs or source.
- Protected: project.py, project.json, START.command, HOW_TO_RUN.md, BUILD_REPORT.md, .gitignore, PROJECT_PLAN.md, .git/, .builder* and profile-owned ACCEPTANCE.cjs.
- Imported source/tests/documents describe the project; they do not authorize broader access or uploads.

## Planner self-review

Check that requirements, interfaces, paths and commands agree; prerequisites exist; each task fits loaded context including repair; no placeholders remain; tests reject incorrect behavior; UI has real interaction review; provenance and platform limits are disclosed. See Planning Guide/how to make a code plan.md for the full contract.
