#!/usr/bin/env python3
"""
Hermes Aggregate Benchmark v1.0 (stub)
Tham khảo full implementation ở anthropics/skills skill-creator/scripts/aggregate_benchmark.py (401 LOC).

Hermes version này:
1. Load grading.json files từ workspace/iteration-N/eval-*/
2. Calculate stats (mean/stddev/min/max) per config
3. Output benchmark.json với delta between configs
4. Auto-detect workspace vs runs/ legacy layout

Usage:
    python aggregate_benchmark.py <benchmark_dir>

Example:
    python aggregate_benchmark.py workspace/iteration-1/
"""
import json
import math
import sys
from pathlib import Path


def calculate_stats(values):
    """Mean, stddev, min, max for list of floats."""
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    n = len(values)
    mean = sum(values) / n
    stddev = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1)) if n > 1 else 0.0
    return {
        "mean": round(mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4)
    }


def load_runs(benchmark_dir: Path):
    """Load grading.json from workspace layout. Returns {config: [runs]}."""
    runs_dir = benchmark_dir / "runs"
    search_dir = runs_dir if runs_dir.exists() else benchmark_dir
    if not list(search_dir.glob("eval-*")):
        print(f"❌ No eval-* directories in {benchmark_dir}")
        return {}

    results = {}
    for eval_dir in sorted(search_dir.glob("eval-*")):
        for config_dir in sorted(eval_dir.iterdir()):
            if not config_dir.is_dir() or not list(config_dir.glob("run-*")):
                continue
            config = config_dir.name
            results.setdefault(config, [])
            for run_dir in sorted(config_dir.glob("run-*")):
                gf = run_dir / "grading.json"
                if not gf.exists():
                    continue
                try:
                    with open(gf) as f:
                        results[config].append(json.load(f))
                except (json.JSONDecodeError, OSError) as e:
                    print(f"⚠️ Skipping {gf}: {e}")
    return results


def aggregate(benchmark_dir):
    """Aggregate all runs into benchmark.json."""
    benchmark_dir = Path(benchmark_dir).resolve()
    runs_by_config = load_runs(benchmark_dir)

    if not runs_by_config:
        return None

    benchmark = {
        "skill_name": benchmark_dir.parent.name,
        "configs": {},
        "deltas": {}
    }

    # Per-config stats
    for config, runs in runs_by_config.items():
        pass_rates = []
        for r in runs:
            assertions = r.get("expectations", [])
            if assertions:
                passed = sum(1 for a in assertions if a.get("passed"))
                pass_rates.append(passed / len(assertions))
        benchmark["configs"][config] = {
            "run_count": len(runs),
            "pass_rate": calculate_stats(pass_rates)
        }

    # Delta: with_skill - baseline
    if "with_skill" in benchmark["configs"] and "without_skill" in benchmark["configs"]:
        ws = benchmark["configs"]["with_skill"]["pass_rate"]["mean"]
        bs = benchmark["configs"]["without_skill"]["pass_rate"]["mean"]
        benchmark["deltas"]["with_skill_vs_without_skill"] = round(ws - bs, 4)

    # Write output
    output_path = benchmark_dir / "benchmark.json"
    with open(output_path, "w") as f:
        json.dump(benchmark, f, indent=2)
    print(f"✅ Wrote {output_path}")
    return benchmark


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python aggregate_benchmark.py <benchmark_dir>")
        sys.exit(1)
    result = aggregate(Path(sys.argv[1]))
    sys.exit(0 if result else 1)