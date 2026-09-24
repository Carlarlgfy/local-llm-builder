from __future__ import annotations

import argparse
from pathlib import Path

from .adapters import LMStudioAdapter, MockAdapter
from .plan_parser import parse_plan
from .state import save_task_graph


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="local-builder", description="Local AI Project Builder proof of concept")
    sub = root.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate a Markdown handoff plan")
    validate.add_argument("plan", type=Path)
    models = sub.add_parser("models", help="list models loaded in LM Studio")
    models.add_argument("--base-url", default="http://127.0.0.1:1234/v1")
    plan = sub.add_parser("plan", help="create and save a typed task graph")
    plan.add_argument("plan", type=Path)
    plan.add_argument("--workspace", type=Path)
    plan.add_argument("--adapter", choices=("mock", "lmstudio"), default="mock")
    plan.add_argument("--model")
    plan.add_argument("--base-url", default="http://127.0.0.1:1234/v1")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.command == "validate":
        parsed = parse_plan(args.plan)
        print(f"Valid plan: {parsed.project_name}")
        return 0
    if args.command == "models":
        for name in LMStudioAdapter("unused", args.base_url).list_models():
            print(name)
        return 0
    parsed = parse_plan(args.plan)
    workspace = (args.workspace or args.plan.parent).resolve()
    if args.adapter == "lmstudio":
        if not args.model:
            raise SystemExit("--model is required with --adapter lmstudio")
        adapter = LMStudioAdapter(args.model, args.base_url)
    else:
        adapter = MockAdapter()
    graph = adapter.create_task_graph(parsed)
    output = save_task_graph(workspace, parsed.path, graph)
    print(f"Planned {len(graph.tasks)} tasks for {graph.project_name}")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
