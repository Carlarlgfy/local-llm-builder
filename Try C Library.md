# Portable C library and demo

Build this project entirely in C11, including tests. Target macOS and Linux using the C standard library. Keep it to ONE complete implementation task plus final verification.

## Deliverables

- include/temperature.h declares double celsius_to_fahrenheit(double) and double fahrenheit_to_celsius(double).
- src/temperature.c implements the conversions.
- main.c prints the Fahrenheit equivalent of 20 Celsius.
- tests/test_temperature.c uses assert to check freezing, boiling, and negative temperatures in both directions.
- A reusable static library build/libtemperature.a, built from build/temperature.o.
- README.md explains what the library exports, how to use the header and link the archive, and how to rebuild on macOS or Linux.

## Build and verify

Run commands separately in this order, enumerating source files:

cc -std=c11 -Wall -Wextra -Iinclude -c src/temperature.c -o build/temperature.o
ar rcs build/libtemperature.a build/temperature.o
cc -std=c11 -Wall -Wextra -Iinclude main.c build/libtemperature.a -o build/app
cc -std=c11 -Wall -Wextra -Iinclude tests/test_temperature.c build/libtemperature.a -o build/test_temperature
./build/test_temperature
./build/app

Assertions must pass; the app must print 68 or 68.0. No downloads or external packages. The launch command is ./build/app.
