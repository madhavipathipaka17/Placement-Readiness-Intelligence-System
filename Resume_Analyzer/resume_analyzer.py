import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_resume(resume_text: str):
    """
    Analyze a student's resume using Groq LLM.
    Returns structured JSON.
    """

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the following resume.

Return ONLY valid JSON.

Resume:

{resume_text}

Required JSON format:

{{
    "skills": [],
    "projects": [],
    "certifications": [],
    "internships": [],
    "education": "",
    "tools": [],
    "resume_category": "",
    "resume_completeness": 0,
    "strengths": [],
    "weaknesses": [],
    "summary": ""
}}

Rules:

1. skills -> list
2. projects -> list
3. certifications -> list
4. internships -> list
5. education -> highest qualification
6. tools -> software/tools/frameworks
7. resume_category -> AI Engineer / Data Scientist / Data Analyst / Software Engineer / Web Developer / Other
8. resume_completeness -> integer (0-100)
9. strengths -> list
10. weaknesses -> list
11. summary -> 2-3 sentences

Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    output = response.choices[0].message.content.strip()

    if output.startswith("```"):
        output = output.replace("```json", "")
        output = output.replace("```", "").strip()

    try:
        return json.loads(output)

    except Exception:

        return {

            "skills": [],

            "projects": [],

            "certifications": [],

            "internships": [],

            "education": "",

            "tools": [],

            "resume_category": "Unknown",

            "resume_completeness": 0,

            "strengths": [],

            "weaknesses": [],

            "summary": ""

        }


if __name__ == "__main__":

    sample = """

    B.Tech Computer Science

    Python

    SQL

    Machine Learning

    Deep Learning

    TensorFlow

    Streamlit

    """

    result = analyze_resume(sample)

    print(json.dumps(result, indent=4))