# 🎯 Placement Readiness Intelligence System (PRIS)

AI + ML powered platform that analyzes a student's resume against a specific job description, detects skill gaps, predicts placement readiness, and generates a personalized improvement roadmap — all through an interactive Streamlit dashboard.

**Domain:** EdTech · Placement Analytics · Resume Intelligence · Career Readiness

---

## 📌 Problem Statement

Students often apply for placement opportunities without knowing whether their resume actually matches a company's job description. They may have the right skills, projects, or certifications, but the resume may not clearly reflect them. Placement officers and trainers, meanwhile, struggle to manually compare every student resume against every job description to judge who is ready, partially ready, or not ready for a role.

PRIS solves this by letting a user upload a resume and paste a job description — the system then extracts and compares both, flags missing skills, and produces a machine-learning-based readiness score along with a concrete improvement plan.

---

## ✨ Key Features

- 📄 **Resume PDF ingestion** — extracts raw text from any uploaded resume PDF
- 🧠 **AI resume analysis** (Groq LLM) — extracts skills, projects, certifications, internships, education, tools, strengths, weaknesses, and a summary
- 📋 **AI job description analysis** (Groq LLM) — extracts job title, role category, required/critical/optional skills, tools & frameworks, soft skills, responsibilities, and ATS keywords
- 🔍 **Skill gap analysis** — matched skills, missing skills, critical missing skills, optional missing skills, and a prioritized "skills to learn first" list
- 📊 **ML-based placement readiness score** — a trained classifier (Random Forest / scikit-learn) predicts one of four readiness categories with a confidence breakdown
- 🗺️ **Personalized improvement plan** — resume suggestions, job preparation suggestions, a 7-day plan, and a 30-day plan
- 📥 **Downloadable PDF report** — a full report combining the score, features, skill gaps, and improvement plan
- 🖥️ **Interactive Streamlit dashboard** — tabbed UI (Overview, Resume Analysis, JD Analysis, Skill Gap, Improvement Plan, Report) with skill chips, a readiness score card, and a confidence chart

---

## 🏗️ Architecture / Pipeline

```
Resume PDF ─┐
            ├─► Text Extraction (PyMuPDF)
Job Desc ───┘
            │
            ▼
   Resume Analyzer (Groq LLM)      JD Analyzer (Groq LLM)
            │                              │
            └──────────────┬───────────────┘
                            ▼
                  Skill Gap Analyzer
                            │
                            ▼
                   Feature Builder (11 ML features)
                            │
                            ▼
             Placement Readiness ML Model (scikit-learn)
                            │
                            ▼
        Improvement Plan Generator + PDF Report Generator
                            │
                            ▼
                  Streamlit Dashboard (app.py)
```

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| UI / Dashboard | Streamlit |
| LLM Analysis | Groq API (`llama-3.3-70b-versatile`) |
| Resume Parsing | PyMuPDF (`fitz`) |
| ML Model | scikit-learn (Random Forest Classifier) |
| Feature/Model Storage | joblib (`.pkl`) |
| Charts | Altair |
| PDF Report Generation | ReportLab |
| Config | python-dotenv |

---

## 📂 Project Structure

```
Resume_Analyzer/
├── app.py                    # Main Streamlit dashboard
├── resume_parser.py          # PDF text extraction
├── resume_analyzer.py        # LLM-based resume analysis
├── jd_analyzer.py            # LLM-based job description analysis
├── skill_gap_analyzer.py     # Resume-vs-JD skill gap + feature computation
├── feature_builder.py        # Converts features into a model-ready DataFrame
├── predictor.py               # Loads trained ML model and predicts readiness
├── improvement_plan.py       # Generates resume/job-prep suggestions and 7/30-day plans
├── report_generator.py       # Builds the downloadable PDF report
├── models/
│   ├── placement_readiness_model.pkl
│   ├── readiness_label_encoder.pkl
│   └── feature_names.pkl
├── uploads/                  # Uploaded resume PDFs (runtime)
├── requirements.txt
└── .env                       # API keys (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Resume_Analyzer
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

### 5. Run the app
```bash
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`.

---

## 🖱️ How to Use

1. Upload a student resume (PDF) on the left.
2. Paste the target job description on the right (or click **Load Sample Job Description**).
3. Click **Analyze Resume**.
4. Review the readiness score, resume analysis, JD analysis, and skill gap across the tabs.
5. Open the **Improvement Plan** tab for the 7-day and 30-day roadmap.
6. Download the full PDF report from the **Report** tab.

---

## 🤖 Machine Learning Model

- **Input:** 11 numerical features derived from the LLM-extracted resume and JD data (`skill_match_percentage`, `critical_skill_match_percentage`, `missing_skills_count`, `critical_missing_skills_count`, `project_relevance_score`, `certification_relevance_score`, `internship_relevance_score`, `resume_completeness_score`, `keyword_match_score`, `role_category_match_score`, `education_score`)
- **Target:** `readiness_label`
- **Labels:** Highly Ready · Moderately Ready · Needs Improvement · Not Ready Yet
- **Algorithm:** Random Forest Classifier (scikit-learn)
- **Output:** Predicted readiness category + confidence (%) for each class

---

## 📊 Project Evaluation Metrics

1. Accuracy of the placement readiness ML model
2. Precision, recall, and F1-score of readiness classification
3. Relevance of Groq-extracted resume skills
4. Relevance of Groq-extracted JD skills
5. Accuracy of matched and missing skills
6. Quality of the readiness score
7. Quality of generated feedback
8. Dashboard usability
9. Report readability
10. Processing time

---

## 🌟 Impact

- Helps students understand job-specific readiness before applying
- Helps students improve resumes with targeted, actionable suggestions
- Reduces manual resume screening effort for placement teams
- Helps placement officers shortlist suitable students faster
- Supports trainers in identifying common skill gaps across a batch
- Supports data-driven placement readiness evaluation

---

## 🚀 Future Scope

- Batch mode: analyze multiple student resumes against one JD for placement officers
- Resume category / role-fit recommendation across multiple job families
- Support for DOCX resumes in addition to PDF
- Deployment on Hugging Face Spaces / Streamlit Community Cloud with authentication

---

## 👤 Project Info

**Project Title:** Placement Readiness Intelligence System (PRIS)
**Domain:** EdTech / Placement Analytics / Resume Intelligence / Career Readiness
