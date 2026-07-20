import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_resume(resume_text, job_description):

    prompt = f"""
You are an AI Resume Analyzer.

Compare the following Resume with the Job Description.

Resume:
{resume_text}

Job Description:
{job_description}

Analyze both and return ONLY a valid JSON object.

Rules:
1. Return ONLY JSON.
2. No explanation.
3. No markdown.
4. No extra text.

Return these exact keys:

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

Scoring Guidelines:

- Percentages: 0–100
- Missing skill counts: integers
- Scores: 0–100

Be realistic.
"""

    response = model.generate_content(prompt)

    output = response.text.strip()

    # Remove markdown if Gemini returns it
    output = output.replace("```json", "")
    output = output.replace("```", "")
    output = output.strip()

    return json.loads(output)
