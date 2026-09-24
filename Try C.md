# C temperature converter

Implement this entire project in C11, including tests. Use only the C standard library.

- converter.h declares celsius_to_fahrenheit and fahrenheit_to_celsius.
- converter.c implements both functions with double precision.
- main.c prints the Fahrenheit equivalent of 20 Celsius.
- tests/test_converter.c uses assert to verify freezing, boiling, and negative temperatures in both directions.
- README.md documents compilation, tests, and running the executable.

Build and run these commands sequentially:

clang -std=c11 -Wall -Wextra main.c converter.c -o app
clang -std=c11 -Wall -Wextra -I. tests/test_converter.c converter.c -o test_converter
./test_converter
./app

Acceptance: all commands exit successfully, assertions pass, and app prints 68 or 68.0. Launch command: ./app.

Use one implementation task followed by final verification. No Python code, external dependencies, or downloads.
