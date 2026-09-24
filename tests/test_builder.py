from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from local_builder.adapters import MockAdapter
from local_builder.models import TaskGraph
from local_builder.plan_parser import parse_plan
from local_builder.policy import safe_path, validate_command
from local_builder.state import save_task_graph
from local_builder.tools import run_command
from local_builder.git_ops import checkpoint, status


ROOT = Path(__file__).parents[1]
FIXTURE = ROOT / "examples/todo_cli/PROJECT_PLAN.md"


class BuilderTests(unittest.TestCase):
    def test_fixture_plan_is_valid(self):
        plan = parse_plan(FIXTURE)
        self.assertEqual(plan.project_name, "Local Todo CLI")

    def test_mock_planner_creates_valid_graph_and_state(self):
        plan = parse_plan(FIXTURE)
        graph = MockAdapter().create_task_graph(plan)
        self.assertIsInstance(graph, TaskGraph)
        with tempfile.TemporaryDirectory() as directory:
            output = save_task_graph(Path(directory), FIXTURE, graph)
            self.assertTrue(output.exists())

    def test_forward_dependency_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "forward dependencies"):
            TaskGraph.from_dict({"project_name": "x", "tasks": [{
                "id": "task-01", "title": "x", "goal": "x", "dependencies": ["task-02"],
                "files": [], "acceptance_checks": [{"command": "python3 -V", "expected": "exit code 0"}],
            }]})

    def test_workspace_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "escapes workspace"):
                safe_path(Path(directory), "../outside.txt")

    def test_command_policy(self):
        self.assertEqual(validate_command("python3 -m unittest"), ["python3", "-m", "unittest"])
        with self.assertRaises(ValueError):
            validate_command("python3 ok.py && echo unsafe")

    def test_bounded_command_runner(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run_command(Path(directory), "python3 -c 'print(123)'", timeout=5)
            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.stdout.strip(), "123")

    def test_git_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "hello.txt").write_text("hello\n", encoding="utf-8")
            commit = checkpoint(workspace, "task-01", "initial file")
            self.assertEqual(len(commit), 40)
            self.assertEqual(status(workspace), "")


if __name__ == "__main__":
    unittest.main()
