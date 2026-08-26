from evaluator import evaluate_lesson
from generator import generate_lesson


lesson = generate_lesson(
    topic="Introduction to RAG"
)

print("\n" + "=" * 60)
print("LESSON TO EVALUATE")
print("=" * 60)

print(lesson)

evaluation = evaluate_lesson(lesson)

print("\n" + "=" * 60)
print("STRUCTURED EVALUATION")
print("=" * 60)

print("Overall:", evaluation.overall_pass)

print("\nAccuracy:")
print(evaluation.accuracy.passed)
print(evaluation.accuracy.reason)

print("\nBeginner Friendly:")
print(evaluation.beginner_friendly.passed)
print(evaluation.beginner_friendly.reason)

print("\nExample Based:")
print(evaluation.example_based.passed)
print(evaluation.example_based.reason)

print("\nJargon Free:")
print(evaluation.jargon_free.passed)
print(evaluation.jargon_free.reason)

print("\nKey Points:")
print(evaluation.key_points.passed)
print(evaluation.key_points.reason)

print("\nCoherent Flow:")
print(evaluation.coherent_flow.passed)
print(evaluation.coherent_flow.reason)

print("\nFailed Checks:")
print(evaluation.failed_checks)