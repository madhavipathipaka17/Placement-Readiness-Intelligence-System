import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_job_description(job_description: str):
    """
    Analyze a Job Description using Groq LLM.
    Returns structured JSON.
    """

    prompt = f"""
You are an expert Job Description Analyzer.

Analyze the following Job Description.

JOB DESCRIPTION:

{job_description}

Return ONLY valid JSON.

JSON format:

{{
    "job_title": "",
    "role_category": "",
    "required_skills": [],
    "critical_skills": [],
    "optional_skills": [],
    "tools_and_frameworks": [],
    "soft_skills": [],
    "responsibilities": [],
    "minimum_education": "",
    "minimum_experience": "",
    "keywords": []
}}

Rules:

1. required_skills -> Mandatory technical skills.
2. critical_skills -> Most important skills.
3. optional_skills -> Good to have skills.
4. tools_and_frameworks -> Software, Libraries, Frameworks.
5. soft_skills -> Communication, Leadership etc.
6. responsibilities -> Bullet list.
7. keywords -> Important ATS keywords.
8. Return ONLY JSON.
"""

    try:

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

        data = json.loads(output)

        return data

    except Exception as e:

        print("JD Analyzer Error:", e)

        return {

            "job_title": "",

            "role_category": "",

            "required_skills": [],

            "critical_skills": [],

            "optional_skills": [],

            "tools_and_frameworks": [],

            "soft_skills": [],

            "responsibilities": [],

            "minimum_education": "",

            "minimum_experience": "",

            "keywords": []

        }


if __name__ == "__main__":

    jd = """
    We are hiring a Data Scientist.

    Skills Required:
    Python
    SQL
    Machine Learning
    Deep Learning
    TensorFlow
    Scikit-learn
    NLP
    Git
    Docker

    Good to Have:
    AWS
    Spark

    Responsibilities:
    Build ML Models
    Data Cleaning
    Feature Engineering
    Deploy Models

    Qualification:
    B.Tech/M.Tech Computer Science
    """

    result = analyze_job_description(jd)

    print(json.dumps(result, indent=4))