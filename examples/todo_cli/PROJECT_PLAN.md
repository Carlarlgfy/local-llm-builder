# Project

Name: Local Todo CLI

Goal: Create a small Python command-line application that stores a todo list in a JSON file and requires no third-party packages.

## User outcome

The user can add, list, complete, and remove todo items from a terminal.

## Scope

### Included

- Add a todo with a generated numeric identifier
- List open and completed todos
- Mark a todo complete
- Remove a todo
- Store data in a user-selected JSON file
- Unit tests and a README

### Excluded

- Accounts, synchronization, networking, and graphical interfaces

## Constraints

- Runtime: Python 3.11 or later
- Dependencies: Python standard library only
- Network: none

## Deliverables

- `todo.py`
- `tests/test_todo.py`
- `README.md`

## Build stages

### Stage 1 Storage and domain functions

Depends on: none

Work: Implement JSON loading, saving, adding, completing, and removing.

Acceptance criteria:

- Command: python3 -m unittest discover -s tests -v
- Expected: exit code 0

### Stage 2 Command-line interface

Depends on: Stage 1

Work: Add argparse commands for add, list, complete, and remove.

Acceptance criteria:

- Command: python3 todo.py --help
- Expected: exit code 0 and commands are listed

### Stage 3 Documentation and final verification

Depends on: Stage 2

Work: Write setup and usage instructions and run the complete test suite.

Acceptance criteria:

- Command: python3 -m unittest discover -s tests -v
- Expected: exit code 0

## Run instructions

Run `python3 todo.py --help`, then select a command and pass `--file path/to/todos.json`.

## Permissions

- Read/write: project folder only
- Commands: python3
- Network: none
- Secrets: none
