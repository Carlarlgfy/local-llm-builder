from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import TaskGraph


def save_task_graph(workspace: Path, source_plan: Path, graph: TaskGraph) -> Path:
    state_dir = workspace.resolve() / ".local-builder"
    state_dir.mkdir(parents=True, exist_ok=True)
    output = state_dir / "tasks.json"
    run = {
        "version": 1,
        "status": "planned",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_plan": str(source_plan.resolve()),
        "project_name": graph.project_name,
        "tasks": graph.to_dict()["tasks"],
    }
    output.write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    return output
