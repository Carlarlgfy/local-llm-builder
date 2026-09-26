# Sky Hopper - independently checked local game

Acceptance profile: sky-hopper-v1

## Goal
Build an original Flappy Bird-style game that opens by double-clicking index.html on this Mac. Use HTML, CSS and plain JavaScript, with no downloads, dependencies or proprietary assets.

## Execution
The builder selects its two-stage Sky Hopper contract:
1. Generate core.js with pure, testable state and physics.
2. Generate index.html, game.js, style.css and README.md; keep the core working.

The app supplies exact function signatures, state fields, physics constants, DOM IDs and event conventions to the model. Its ACCEPTANCE.cjs file is app-owned, regenerated before checking, and cannot be edited by the agent. This is a specific validated-template route, not a generic verifier of arbitrary plans.

## Requirements
R1: Ready screen; Space, tap or Start starts play. Restart resets score, position, velocity, pipes and timer while preserving the best score.
R2: Seconds-based gravity/flapping; moving pipes with generous gaps; score exactly once per passed pipe.
R3: Pipe, ceiling and ground collisions end play; show Game over; preserve best score.
R4: P and Pause/Resume freeze and resume simulation without duplicate animation loops.
R5: Responsive canvas, visible score/best/status, readable controls, offline assets, original drawn bird and scenery. Ignore repeated keydown and tolerate blocked localStorage.
R6: Tests must run before checkpointing. On failure, fix the implementation without weakening or replacing independent checks.

## Acceptance evidence
The app checks core behavior plus simulated browser events for start, pause, resume, loss, restart and reopening. Tests also check local assets and storage-error handling. Launch must be ["index.html"].

## Manual review
Automated checks do not certify visual quality, real-browser compatibility, accessibility or enjoyable difficulty. Play several rounds, try keyboard and pointer controls, resize the window, close/reopen the page, and check the best score. Report these results separately from automated evidence.
