import json
import os


# Project root = folder containing src/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
LOG_FILE = os.path.join(OUTPUT_DIR, "rejection_log.json")


def save_rejection(
    attempt: int,
    evaluation
):

    print(f"\nRejection saved to: {LOG_FILE}")


    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r", encoding="utf-8") as file:
            logs = json.load(file)

    else:
        logs = []

    failed_checks = []

    for check_name in evaluation.failed_checks:

        check = getattr(evaluation, check_name)

        failed_checks.append({
            "check": check_name,
            "reason": check.reason,
            "improvement": check.improvement
        })

    logs.append({
        "attempt": attempt,
        "status": "REJECTED",
        "failed_checks": failed_checks
    })

    with open(
        LOG_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            logs,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nRejection saved to: {LOG_FILE}")