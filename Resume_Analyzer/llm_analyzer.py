import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an ATS Resume Analyzer.

Compare the resume with the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY a JSON object.

Format:

{{
"skill_match_percentage":0,
"critical_skill_match_percentage":0,
"missing_skills_count":0,
"critical_missing_skills_count":0,
"project_relevance_score":0,
"certification_relevance_score":0,
"internship_relevance_score":0,
"resume_completeness_score":0,
"keyword_match_score":0,
"role_category_match_score":0,
"education_score":0
}}

Rules:

- Percentages between 0 and 100.
- Counts must be integers.
- Return JSON only.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    print("\n====== GROQ OUTPUT ======")
    print(text)
    print("=========================\n")

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        text = match.group()

    return json.loads(text)