from __future__ import annotations

import subprocess
from pathlib import Path


def _git(workspace: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=workspace.resolve(), capture_output=True, text=True, check=False)


def ensure_repository(workspace: Path) -> None:
    root = workspace.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if not (root / '.git').exists():
        result = _git(root, "init")
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or "git init failed")
        _git(root, "config", "user.name", "Local AI Builder")
        _git(root, "config", "user.email", "local-builder@localhost")


def status(workspace: Path) -> str:
    result = _git(workspace, "status", "--short")
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    return result.stdout


def checkpoint(workspace: Path, task_id: str, title: str) -> str:
    ensure_repository(workspace)
    add = _git(workspace, "add", "--all")
    if add.returncode:
        raise RuntimeError(add.stderr.strip() or "git add failed")
    if not status(workspace).strip():
        head = _git(workspace, "rev-parse", "HEAD")
        return head.stdout.strip() if head.returncode == 0 else "no-changes"
    message = f"{task_id} {title}".strip()
    commit = _git(workspace, "commit", "-m", message)
    if commit.returncode:
        raise RuntimeError(commit.stderr.strip() or "git commit failed")
    head = _git(workspace, "rev-parse", "HEAD")
    if head.returncode:
        raise RuntimeError(head.stderr.strip() or "could not read checkpoint")
    return head.stdout.strip()
