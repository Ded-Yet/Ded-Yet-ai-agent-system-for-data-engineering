import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from agents.router_agent import route
from tests.router_eval_questions import ROUTER_EVAL_QUESTIONS


def main():
    correct = 0
    total = len(ROUTER_EVAL_QUESTIONS)

    for i, item in enumerate(ROUTER_EVAL_QUESTIONS, 1):
        question = item["question"]
        expected = item["expected"]

        actual = route(question)
        time.sleep(3)

        is_correct = actual == expected
        status = "PASS" if is_correct else "FAIL"
        if is_correct:
            correct += 1

        print(f"[{i}] {status}: \"{question}\" -> expected: {expected}, got: {actual}")

    print(f"\nRouter Accuracy: {correct}/{total} ({correct / total * 100:.1f}%)")


if __name__ == "__main__":
    main()