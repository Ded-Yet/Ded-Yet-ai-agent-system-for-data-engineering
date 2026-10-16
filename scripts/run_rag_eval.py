import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from agents.rag_agent import answer_question
from tests.rag_eval_questions import RAG_EVAL_QUESTIONS


def main():
    correct = 0
    total = len(RAG_EVAL_QUESTIONS)

    for i, item in enumerate(RAG_EVAL_QUESTIONS, 1):
        question = item["question"]
        must_contain = item["must_contain"]

        answer = answer_question(question)
        time.sleep(3)

        answer_lower = answer.lower()
        is_correct = all(phrase.lower() in answer_lower for phrase in must_contain)
        status = "PASS" if is_correct else "FAIL"
        if is_correct:
            correct += 1

        print(f"[{i}] {status}: {question}")
        if not is_correct:
            print(f"    Answer: {answer}")
            print(f"    Expected to contain: {must_contain}")

    print(f"\nRAG Accuracy: {correct}/{total} ({correct / total * 100:.1f}%)")


if __name__ == "__main__":
    main()