from evaluator import evaluate_lesson


bad_lesson = """
# Introduction to RAG

RAG stands for Retrieval-Augmented Generation.

RAG is a system where the language model retrains itself
every time a user asks a question.

The model permanently learns the information from the user's
documents and changes its internal knowledge.

RAG is useful because the model can learn new information
without needing retrieval.

The system simply sends the question to the language model,
and the model generates an answer from its newly learned memory.
"""


evaluation = evaluate_lesson(bad_lesson)


print("\n" + "=" * 60)
print("DELIBERATE FAILURE TEST")
print("=" * 60)

print("\nOverall Pass:", evaluation.overall_pass)

print("\nFailed Checks:")

for check_name in evaluation.failed_checks:

    check = getattr(evaluation, check_name)

    print(f"\n{check_name}")
    print("Reason:", check.reason)
    print("Improvement:", check.improvement)