import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from agents.sql_agent import generate_sql, run_sql
from tests.eval_questions import EVAL_QUESTIONS


def results_match(a, b) -> bool:
    if a is None or b is None:
        return a == b

    a_values = {tuple(str(v) for v in row) for row in a["rows"]}
    b_values_flat = set()
    for row in b["rows"]:
        for v in row:
            b_values_flat.add(str(v))

    # Every value in the expected row must appear somewhere in the generated row
    for row in a["rows"]:
        if not all(str(v) in b_values_flat for v in row):
            return False
    return True


def main():
    correct = 0
    total = len(EVAL_QUESTIONS)

    for i, item in enumerate(EVAL_QUESTIONS, 1):
        question = item["question"]
        expected_sql = item["expected_sql"]

        generated_sql = generate_sql(question)
        time.sleep(5)

        try:
            expected_result = run_sql(expected_sql)
        except Exception as e:
            print(f"[{i}] ERROR running expected SQL: {e}")
            continue

        try:
            generated_result = run_sql(generated_sql)
        except Exception as e:
            print(f"[{i}] FAIL (generated SQL errored): {question}")
            print(f"    Generated: {generated_sql}")
            print(f"    Error: {e}")
            continue

        is_correct = results_match(expected_result, generated_result)
        status = "PASS" if is_correct else "FAIL"
        if is_correct:
            correct += 1

        print(f"[{i}] {status}: {question}")
        if not is_correct:
            print(f"    Generated: {generated_sql}")
            print(f"    Expected result:  {expected_result}")
            print(f"    Generated result: {generated_result}")

    print(f"\nAccuracy: {correct}/{total} ({correct / total * 100:.1f}%)")


if __name__ == "__main__":
    main()