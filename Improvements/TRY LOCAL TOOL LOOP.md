# Local tool-loop proof of concept

Build a tiny portable Python 3 temperature-conversion command-line application using only the standard library. Keep this as one implementation task.

Requirements:

- Convert Celsius to Fahrenheit and Fahrenheit to Celsius with documented functions that can be imported without running the CLI.
- The CLI accepts a numeric temperature and a source unit (C or F), prints the converted value with its destination unit, and exits successfully. Invalid units or nonnumeric input must print a helpful error and exit nonzero.
- With no arguments, display a short usage explanation and successful demonstration so the builder's Run project button is useful without interactive input.
- Include a README explaining how to run the program and its tests on macOS and Linux.
- Write your own unittest tests covering freezing, boiling, negative temperatures, round-trip conversion, importing without side effects, CLI valid input, invalid unit and invalid number. Include both function and subprocess CLI tests. Do not use placeholders or tests that simply print success.
- Use a separate tests folder, and run unittest discovery with a nonzero test count. No external dependencies, downloads, network calls, shell scripts or system changes.
- Set the launch command to run your application's no-argument demonstration.

The local model must author every implementation and test file. The builder supplies only orchestration, sandboxing and portable launch helpers. Passing these model-written tests is a smoke test, not independent proof of correctness.

## How to try this plan

In AI Builder, load a tool-capable local model (the current experiment uses Qwen3.5 35B A3B with 32,768 context). Choose **Tool loop — experimental**, choose a destination and project name, then import this document and press Start. Use Run project after checks pass. Keep the generated source folder: it contains the actual application and tests.
