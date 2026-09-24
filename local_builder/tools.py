from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .policy import validate_command


@dataclass(frozen=True)
class CommandResult:
    command: str
    exit_code: int
    stdout: str
    stderr: str


def run_command(workspace: Path, command: str, timeout: int = 60, output_limit: int = 20_000) -> CommandResult:
    from .desktop import sandbox_command
    root = workspace.resolve()
    argv = validate_command(command)
    code, output = sandbox_command(root, argv, timeout)
    return CommandResult(command, code, output[-output_limit:], '')
