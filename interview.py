import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None

MODEL = "openai/gpt-oss-20b"


def ask_ai(prompt):
    if client is None:
        raise ValueError("GROQ_API_KEY set nahi hai.")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=1200
    )

    return (
        response.choices[0].message.content
        or "AI se response nahi mila."
    )


def generate_questions(job_role, resume_text):
    prompt = f"""
You are a helpful technical interviewer.

Job role: {job_role}

Resume:
{resume_text[:4000]}

Generate exactly 5 relevant interview questions.
Include technical and project-related questions.
Return one question per line, numbered 1 to 5.
Do not include introductory text.
"""

    return ask_ai(prompt)


def evaluate_answer(question, answer):
    prompt = f"""
Evaluate this candidate's interview answer fairly.

Question: {question}
Candidate's answer: {answer}

Give:
Score: X/10
Feedback: What was good and what needs improvement.
Improved Answer: A short sample answer.

Do not invent candidate experience or skills.
"""

    return ask_ai(prompt)