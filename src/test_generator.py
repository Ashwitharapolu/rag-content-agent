from generator import generate_lesson


lesson = generate_lesson(
    topic="Introduction to RAG"
)

print("\n" + "=" * 60)
print("GENERATED LESSON")
print("=" * 60)

print(lesson)