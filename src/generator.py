import os
from dotenv import load_dotenv
from groq import Groq

from prompts import GENERATOR_SYSTEM_PROMPT, build_generator_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_lesson(
    topic: str,
    memory: str = "",
    feedback: str = ""
) -> str:

    prompt = build_generator_prompt(
        topic=topic,
        memory=memory,
        feedback=feedback
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": GENERATOR_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
