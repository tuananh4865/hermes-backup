#!/usr/bin/env python3
"""
Hermes Eval Review Generator v1.0
Ported từ anthropics/skills skill-creator/eval-viewer/generate_review.py

Usage:
    python generate_review.py <workspace_dir> --skill-name <name> [--output <path>]

NOTE: This is a STUB. Full implementation reads all eval outputs + creates interactive HTML.
Hermes version: write minimal HTML page listing outputs + benchmark.

For now, this generates a simple HTML file that lists all runs + outputs.
"""
import argparse
import json
import sys
from pathlib import Path


def generate_static_html(workspace_dir: Path, skill_name: str, benchmark_path: Path = None, previous_workspace: Path = None):
    """Generate standalone HTML page with Outputs + Benchmark tabs."""
    outputs_html = []
    for eval_dir in sorted(workspace_dir.glob("eval-*")):
        outputs_html.append(f"<h2>{eval_dir.name}</h2>")
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir():
                continue
            outputs_html.append(f"<h3>Config: {config_dir.name}</h3>")
            for run_dir in sorted(config_dir.glob("run-*")):
                outputs_html.append(f"<h4>{run_dir.name}</h4>")
                gf = run_dir / "grading.json"
                if gf.exists():
                    g = json.loads(gf.read_text())
                    outputs_html.append("<pre>" + json.dumps(g, indent=2) + "</pre>")

    benchmark_html = "<p>No benchmark.json found</p>"
    if benchmark_path and benchmark_path.exists():
        b = json.loads(benchmark_path.read_text())
        benchmark_html = "<pre>" + json.dumps(b, indent=2) + "</pre>"

    html = f"""<!DOCTYPE html>
<html><head><title>Hermes Skill Eval Review - {skill_name}</title>
<style>
body {{ font-family: monospace; max-width: 1200px; margin: 2em auto; padding: 0 1em; }}
.tab {{ padding: 0.5em 1em; cursor: pointer; border: 1px solid #ccc; display: inline-block; }}
.tab.active {{ background: #141413; color: #faf9f5; }}
.content {{ display: none; padding: 1em 0; }}
.content.active {{ display: block; }}
pre {{ background: #faf9f5; padding: 1em; border: 1px solid #141413; overflow-x: auto; }}
h2, h3, h4 {{ margin-top: 1em; }}
</style></head>
<body>
<h1>Hermes Skill Eval Review: {skill_name}</h1>
<p>Workspace: {workspace_dir}</p>
<div>
  <span class="tab active" onclick="showTab('outputs')">Outputs</span>
  <span class="tab" onclick="showTab('benchmark')">Benchmark</span>
</div>
<div id="outputs" class="content active">
{"".join(outputs_html)}
</div>
<div id="benchmark" class="content">
{benchmark_html}
</div>
<script>
function showTab(name) {{
  document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(name).classList.add('active');
  event.target.classList.add('active');
}}
</script>
</body></html>"""
    return html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="Path to workspace/iteration-N/")
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--benchmark", help="Path to benchmark.json")
    parser.add_argument("--output", help="Output HTML path (default: <workspace>/review.html)")
    parser.add_argument("--previous-workspace", help="Previous iteration for diff")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"❌ Workspace not found: {workspace}")
        sys.exit(1)

    output_path = Path(args.output) if args.output else workspace / "review.html"
    benchmark = Path(args.benchmark) if args.benchmark else workspace / "benchmark.json"

    html = generate_static_html(workspace, args.skill_name, benchmark, Path(args.previous_workspace) if args.previous_workspace else None)
    output_path.write_text(html)
    print(f"✅ Wrote: {output_path}")


if __name__ == "__main__":
    main()