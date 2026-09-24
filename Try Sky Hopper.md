# Sky Hopper — playable local arcade game

Build an original Flappy Bird-style browser game named Sky Hopper, not using any proprietary artwork. Use one complete implementation task with tests, followed by the builder's final verification. Target this Mac and Linux browsers; no installs, network, libraries, or external assets. Use HTML, CSS, and plain JavaScript. Launch must be ["index.html"].

## Files and architecture
- index.html: accessible title, visible score and best score, instructions, canvas, Start/Restart button and Pause/Resume button. Load game.js with a normal script tag so double-clicking index.html works with file://.
- game.js: deterministic pure game-state functions (createState, flap, update, collision) separated from browser rendering and event handling. Export these via module.exports when running in Node; guard all DOM use with typeof document. Use seconds-based delta time, capped at 0.033, requestAnimationFrame in browser only.
- style.css: polished sky-blue scene, centered responsive 420x600 game, original drawn bird, green obstacles, ground, visible start and game-over overlay, readable control buttons and mobile fit. No external fonts.
- tests/test_game.cjs: Node built-in assert tests exercising actual exported physics, flap, scoring, collision and restart logic.
- tests/test_structure.py: Python unittest checks HTML references existing scripts/styles and has instructions and controls. At least one discovered test.
- README.md: double-click index.html, controls, offline usage and test commands.

## Behavior and acceptance criteria
R1: Start screen waits until Start, Space, click or tap. Space/click/tap flaps only once per action. Prevent Space scrolling; ignore keyboard repeats. Button clicks must not accidentally double-trigger canvas actions.
R2: Gravity pulls a bird down; flap gives negative vertical velocity; pipes move left with a generous 180px gap, spawn repeatedly, and increase score exactly once per passed pipe. Keep gaps safely within the play area. Start gently with first obstacle delayed.
R3: Hitting an obstacle, ceiling, or ground ends the round; display Game over, score and Restart. Restart completely resets position, velocity, pipes, timers and score. Best score persists in localStorage, with try/catch fallback if unavailable.
R4: Pause/resume button and P key freeze simulation; reset frame timing on resume. Space does not restart unexpectedly while paused. Show Ready, Playing, Paused, Game over as visible text.
R5: Keyboard and pointer controls work; browser resize does not change logical physics coordinates. No network requests or uncaught JavaScript exceptions. Canvas has accessible description and nearby instructions.
R6: Actual behavioral tests verify gravity, flap direction, pipe motion, one-time scoring, gap survival, pipe collision, ground collision, pause freeze and restart. Do not claim a substring test proves gameplay.

## Required checks
Use separate argument arrays, no shell syntax:
["node", "tests/test_game.cjs"]
["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]

Implement all requirements together in one task so the game is playable immediately. Keep code concise enough for a local coding model. On failure fix the underlying implementation, preserving these tests and requirements. Do not weaken assertions just to pass. The user will also play-test in a browser.
