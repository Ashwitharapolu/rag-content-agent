import os
import json

from dotenv import load_dotenv
from groq import Groq

from prompts import EVALUATOR_SYSTEM_PROMPT
from schemas import EvaluationResult

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def evaluate_lesson(lesson: str) -> EvaluationResult:

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": EVALUATOR_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Evaluate the following lesson.

LESSON:

{lesson}

Return ONLY valid JSON.
Do not include markdown.
Do not include ```json.
Do not include any explanation outside the JSON.

The JSON must follow this exact structure:

{{
    "overall_pass": true,
    "accuracy": {{
        "passed": true,
        "reason": "...",
        "improvement": "..."
    }},
    "beginner_friendly": {{
        "passed": true,
        "reason": "...",
        "improvement": "..."
    }},
    "example_based": {{
        "passed": true,
        "reason": "...",
        "improvement": "..."
    }},
    "jargon_free": {{
        "passed": true,
        "reason": "...",
        "improvement": "..."
    }},
    "key_points": {{
        "passed": true,
        "reason": "...",
        "improvement": "..."
    }},
    "coherent_flow": {{
        "passed": true,
        "reason": "...",
        "improvement": "..."
    }},
    "failed_checks": []
}}
"""
            }
        ],
        temperature=0.0
    )

    raw_result = response.choices[0].message.content

    print("\n===== EVALUATOR RAW RESPONSE =====")
    print(raw_result)

    try:
        result = json.loads(raw_result)

        evaluation = EvaluationResult.model_validate(result)

        return evaluation

    except Exception as e:
        print("\nEvaluator parsing error:")
        print(e)

        raise