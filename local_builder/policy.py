from __future__ import annotations

import shlex
from pathlib import Path

ALLOWED_EXECUTABLES = {"python", "python3", "node", "clang", "cc", "gcc"}
DENIED_TOKENS = {";", "&&", "||", "|", ">", ">>", "<", "`"}


def safe_path(workspace: Path, candidate: str) -> Path:
    root = workspace.resolve()
    target = (root / candidate).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"path escapes workspace: {candidate}")
    return target


def validate_command(command: str) -> list[str]:
    if any(token in command for token in DENIED_TOKENS):
        raise ValueError("shell operators are not permitted")
    argv = shlex.split(command)
    if not argv or (argv[0] not in ALLOWED_EXECUTABLES and not argv[0].startswith('./')):
        raise ValueError("executable is not allowed")
    return argv
