from memory import save_memory, get_memory_text
from generator import generate_lesson
from evaluator import evaluate_lesson
from rejection_log import save_rejection


MAX_RETRIES = 2


def run_agent(topic: str, demo_mode: bool = False):

    print("\n" + "=" * 60)
    print("STARTING CONTENT GENERATION AGENT")
    print("=" * 60)

    feedback = ""
    lesson = ""

    # Load persistent memory from previous runs
    memory = get_memory_text()

    for attempt in range(MAX_RETRIES + 1):

        print(f"\n\n===== ATTEMPT {attempt + 1} =====")

        # --------------------------------
        # 1. GENERATE LESSON
        # --------------------------------

        lesson = generate_lesson(
            topic=topic,
            memory=memory,
            feedback=feedback
        )

        print("\nLESSON GENERATED")

        # --------------------------------
        # 2. EVALUATE LESSON
        # --------------------------------

        evaluation = evaluate_lesson(lesson)

        # --------------------------------
        # DEMO MODE
        # --------------------------------
        # Deliberately create one failure so
        # we can demonstrate:
        #
        # FAIL → SAVE MEMORY → FEEDBACK → RETRY
        #
        # This only happens on the first attempt
        # when demo_mode=True.
        # --------------------------------

        if demo_mode and attempt == 0:

            evaluation.overall_pass = False

            if "jargon_free" not in evaluation.failed_checks:
                evaluation.failed_checks.append("jargon_free")

            evaluation.jargon_free.passed = False

            evaluation.jargon_free.reason = (
                "Demo test: technical terms were intentionally "
                "introduced without beginner-friendly explanations."
            )

            evaluation.jargon_free.improvement = (
                "Explain technical terms in simple English "
                "before using them."
            )

            print(
                "\n[DEMO MODE] Intentional evaluator failure "
                "triggered for testing."
            )

        # --------------------------------
        # 3. SHOW EVALUATION
        # --------------------------------

        print("\nEVALUATION RESULT:")
        print("Overall Pass:", evaluation.overall_pass)
        print("Failed Checks:", evaluation.failed_checks)

        # --------------------------------
        # 4. IF LESSON PASSES
        # --------------------------------

        if evaluation.overall_pass:

            print("\n" + "=" * 60)
            print("LESSON PASSED!")
            print("=" * 60)

            return lesson

        # --------------------------------
        # 5. LESSON FAILED
        # --------------------------------

        print("\nLESSON REJECTED.")

        # Save rejection history
        save_rejection(
            attempt=attempt + 1,
            evaluation=evaluation
        )

        # Save learning from failure
        save_memory(evaluation)

        # --------------------------------
        # 6. CREATE FEEDBACK FOR RETRY
        # --------------------------------

        feedback_parts = []

        for check_name in evaluation.failed_checks:

            check = getattr(
                evaluation,
                check_name
            )

            feedback_parts.append(
                f"""
Failed Check: {check_name}

Reason:
{check.reason}

Required Improvement:
{check.improvement}
"""
            )

        feedback = "\n".join(feedback_parts)

        print("\nFEEDBACK SENT TO GENERATOR:")
        print(feedback)

        # --------------------------------
        # 7. REFRESH MEMORY
        # --------------------------------
        # This is important:
        # the next attempt receives the newly
        # saved lesson learned from this failure.
        # --------------------------------

        memory = get_memory_text()

    # --------------------------------
    # 8. MAXIMUM RETRIES REACHED
    # --------------------------------

    print("\n" + "=" * 60)
    print("MAXIMUM RETRIES REACHED")
    print("=" * 60)

    return lesson


if __name__ == "__main__":

    final_lesson = run_agent(
        topic="Introduction to RAG",
        demo_mode=True
    )

    print("\n\nFINAL LESSON:")
    print(final_lesson)