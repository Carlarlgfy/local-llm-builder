from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol

from .models import TaskGraph
from .plan_parser import ParsedPlan


class PlannerAdapter(Protocol):
    def create_task_graph(self, plan: ParsedPlan) -> TaskGraph: ...


class MockAdapter:
    def create_task_graph(self, plan: ParsedPlan) -> TaskGraph:
        return TaskGraph.from_dict({
            "project_name": plan.project_name,
            "tasks": [
                {
                    "id": "task-01", "title": "Create the project structure",
                    "goal": "Create the initial source, test, and documentation files.",
                    "dependencies": [], "files": ["README.md", "todo.py", "tests/test_todo.py"],
                    "acceptance_checks": [{"command": "python3 -m unittest discover -s tests -v", "expected": "exit code 0"}],
                },
                {
                    "id": "task-02", "title": "Implement and verify the CLI",
                    "goal": "Complete the plan behavior and verify all acceptance criteria.",
                    "dependencies": ["task-01"], "files": ["todo.py", "tests/test_todo.py", "README.md"],
                    "acceptance_checks": [{"command": "python3 todo.py --help", "expected": "exit code 0"}],
                },
            ],
        })


class LMStudioAdapter:
    def __init__(self, model: str, base_url: str = "http://127.0.0.1:1234/v1") -> None:
        if not base_url.startswith(("http://127.0.0.1", "http://localhost")):
            raise ValueError("proof of concept permits only a loopback LM Studio URL")
        self.model = model
        self.base_url = base_url.rstrip("/")

    def _request(self, endpoint: str, payload: dict | None = None) -> dict:
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.base_url + endpoint, data=data,
            headers={"Content-Type": "application/json", "Authorization": "Bearer lm-studio"},
            method="GET" if data is None else "POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"could not reach LM Studio at {self.base_url}: {exc}") from exc

    def list_models(self) -> list[str]:
        return [item["id"] for item in self._request("/models").get("data", []) if "id" in item]

    def create_task_graph(self, plan: ParsedPlan) -> TaskGraph:
        schema = json.loads((Path(__file__).parents[1] / "schemas/task_graph.schema.json").read_text())
        prompt = (
            "Convert the project plan into a small ordered task graph. Each task must be independently "
            "verifiable, dependencies may reference only earlier task IDs, and commands must come from the plan.\n\n"
            + plan.text
        )
        payload = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": "You are a project planner. Return only schema-valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_schema", "json_schema": {"name": "task_graph", "strict": True, "schema": schema}},
        }
        response = self._request("/chat/completions", payload)
        try:
            content = response["choices"][0]["message"]["content"]
            return TaskGraph.from_dict(json.loads(content))
        except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
            raise RuntimeError(f"LM Studio returned an invalid task graph: {exc}") from exc
