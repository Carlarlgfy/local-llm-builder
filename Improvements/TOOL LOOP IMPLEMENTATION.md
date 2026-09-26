# Local tool loop — experimental

## What changed

The desktop app now offers **Tool loop — experimental, local-model tests** alongside the existing batch builder. This is an internal tool-calling agent, not an MCP client/server implementation. MCP can expose tools; the host must still implement the model/tool/test/repair loop.

The local model makes a short task plan, then works through one task at a time using `list_files`, `read_file`, `write_file`, `run_checks` and `finish_task`. Each result is returned to the model. The host, not a prose claim from the model, decides whether recorded checks passed.

This adopts the relevant pattern documented by:

- [Continue: agent loop](https://docs.continue.dev/ide-extensions/agent/how-it-works): tools, permissions, execution and tool results fed back to the model.
- [Cline SDK sessions](https://docs.cline.bot/cline-sdk/sessions): a repeated model/tool loop within a persistent session.
- [Aider: linting and testing](https://aider.chat/docs/usage/lint-test.html): execute checks and return failures for repair.

No Cline, Continue or Aider dependency is bundled, and there is no general-purpose external MCP server access in this mode.

## Step-by-step execution

1. Load an installed tool-capable model through LM Studio. Start with 32,768 context; a larger context is not a guarantee of better results.
2. Select Tool loop, choose a destination and name, and import a small plan.
3. The local model proposes 1–3 tasks. Each must leave runnable behavioral checks.
4. The host copies the last accepted source into a temporary attempt folder.
5. The model reads files, writes small files, runs checks, reads feedback and repairs failures.
6. Completion requires successful checks on unchanged source. Failed drafts are not promoted.
7. Accepted changes are copied to the output folder, checked there again and checkpointed with Git.
8. All recorded checks run again at the end. The app writes the normal portable launcher and instructions.
9. Use **Run project**, then inspect actual behavior. Model-written checks are not independent acceptance verification.

## Boundaries and recovery

- All project implementation and test source is local-model-authored. App-owned launch helpers and manifests are infrastructure, not generated project implementation.
- Existing application regression tests remain separate. New regression tests for this feature must also come from the local model under the user's current instruction.
- Tool commands use the existing macOS sandbox: no network, no package installs, restricted filesystem access and command time/output limits. Do not treat this prototype as a hardened hostile-code execution service.
- Native tool calls are required. A model listed on disk is not sufficient: load it first, and use one whose LM Studio metadata reports tool support.
- Conversations have an approximate context budget, 30 model turns per task and a repeated-failure stop. Automatic conversation summarization is not implemented.
- Pause/Stop are checked between model requests and tools. An in-flight model request may take up to the request timeout to return.
- Resume retries the unfinished task from the last accepted source. It does not restore a discarded temporary draft.
- `.builder-tool-trace.jsonl` records model responses and tool outcomes locally. `.builder.json` records progress, checks, checkpoints and source hashes. These logs can contain project code; review before sharing.
- The app-owned Sky Hopper acceptance profile is deliberately incompatible with this local-tests-only mode. Use a plain game plan without that profile marker.

## Remaining work before calling this polished

1. Repeat fresh builds across Python, C and a browser game; publish actual success/failure counts, without manual source repairs.
2. Exercise Stop, Resume, failed-check rollback and external-edit conflicts through the native app, not only direct backend runs.
3. Add locally authored regression coverage for full multi-turn tool transcripts, checkpoint promotion and failed promotions.
4. Add bounded exact-match patch tools and better context compaction so repairs do not rewrite whole files or exhaust context.
5. Add real browser gameplay testing and user review for graphical projects. Passing command-line tests does not verify visual quality or enjoyable play.
6. Validate exports on a Linux laptop. Language profiles are not certification of every language, framework or dependency.
7. Review launch commands and dependencies before normal-permission execution. External package installation and arbitrary MCP servers need a separate explicit permission design.
8. Add model/version compatibility checks, a release checklist and reproducible clean-install packaging.

The bundled launcher still depends on the installed Python runtime. This is a macOS prototype, not a self-contained cross-platform desktop distribution.
