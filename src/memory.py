import json
import os


# Project root
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Persistent memory is stored in data/
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_memory(evaluation):

    print("\n>>> save_memory() was called")
    print("Failed checks received:", evaluation.failed_checks)
    print("Memory file:", MEMORY_FILE)

    os.makedirs(DATA_DIR, exist_ok=True)

    memory = load_memory()

    print("Existing memory:", memory)

    for check_name in evaluation.failed_checks:

        check = getattr(
            evaluation,
            check_name
        )

        memory_entry = {
            "failure_type": check_name,
            "reason": check.reason,
            "improvement": check.improvement
        }

        memory.append(memory_entry)

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nMemory saved to: {MEMORY_FILE}")


def get_memory_text():

    memory = load_memory()

    if not memory:
        return "No previous lessons learned."

    memory_text = []

    for item in memory:

        memory_text.append(
            f"""
Failure type: {item["failure_type"]}

Previous problem:
{item["reason"]}

Recommended improvement:
{item["improvement"]}
"""
        )

    return "\n".join(memory_text)