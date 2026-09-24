from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class AcceptanceCheck:
    command: str
    expected: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "AcceptanceCheck":
        command = value.get("command")
        expected = value.get("expected")
        if not isinstance(command, str) or not command.strip():
            raise ValueError("acceptance check requires a command")
        if not isinstance(expected, str) or not expected.strip():
            raise ValueError("acceptance check requires an expected result")
        return cls(command.strip(), expected.strip())


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    goal: str
    dependencies: tuple[str, ...]
    files: tuple[str, ...]
    acceptance_checks: tuple[AcceptanceCheck, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Task":
        checks = tuple(AcceptanceCheck.from_dict(item) for item in value.get("acceptance_checks", []))
        if not checks:
            raise ValueError("task requires at least one acceptance check")
        task_id = value.get("id")
        title = value.get("title")
        goal = value.get("goal")
        if not all(isinstance(item, str) and item.strip() for item in (task_id, title, goal)):
            raise ValueError("task id, title, and goal must be non-empty strings")
        return cls(
            task_id.strip(), title.strip(), goal.strip(),
            tuple(value.get("dependencies", [])), tuple(value.get("files", [])), checks,
        )


@dataclass(frozen=True)
class TaskGraph:
    project_name: str
    tasks: tuple[Task, ...]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "TaskGraph":
        name = value.get("project_name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("task graph requires project_name")
        tasks = tuple(Task.from_dict(item) for item in value.get("tasks", []))
        if not tasks:
            raise ValueError("task graph requires at least one task")
        ids = [task.id for task in tasks]
        if len(ids) != len(set(ids)):
            raise ValueError("task ids must be unique")
        known: set[str] = set()
        for task in tasks:
            missing = set(task.dependencies) - known
            if missing:
                raise ValueError(f"{task.id} has missing or forward dependencies: {sorted(missing)}")
            known.add(task.id)
        return cls(name.strip(), tasks)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
