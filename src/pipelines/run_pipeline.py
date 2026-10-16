import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

STEPS = [
    ("Seed data", "scripts/seed_data.py"),
    ("Data quality checks", "src/pipelines/data_quality_checks.py"),
    ("Transform customer summary", "src/pipelines/transform_customer_summary.py"),
]


def run_step(name: str, script_path: str) -> dict:
    print(f"\n--- Running: {name} ---")
    start = time.time()
    result = subprocess.run(
        [sys.executable, str(ROOT / script_path)],
        capture_output=True,
        text=True,
    )
    duration = round(time.time() - start, 2)

    success = result.returncode == 0
    print(result.stdout)
    if not success:
        print(result.stderr)

    return {
        "step": name,
        "success": success,
        "duration_seconds": duration,
    }


def main():
    print(f"Pipeline run started: {datetime.now(timezone.utc).isoformat()}")
    results = []

    for name, script in STEPS:
        result = run_step(name, script)
        results.append(result)
        if not result["success"]:
            print(f"\nPipeline stopped: '{name}' failed.")
            break

    print("\n--- Pipeline Summary ---")
    for r in results:
        status = "OK" if r["success"] else "FAILED"
        print(f"  [{status}] {r['step']} ({r['duration_seconds']}s)")


if __name__ == "__main__":
    main()