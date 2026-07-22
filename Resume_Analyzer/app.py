import os
import time
import datetime

import pandas as pd
import altair as alt
import streamlit as st

from resume_parser import extract_resume_text
from resume_analyzer import analyze_resume
from jd_analyzer import analyze_job_description
from skill_gap_analyzer import analyze_skill_gap
from improvement_plan import generate_improvement_plan
from feature_builder import build_feature_dataframe
from predictor import predict_readiness
from report_generator import generate_pdf_report

# =============================================================
# PAGE CONFIG
# =============================================================
st.set_page_config(
    page_title="Placement Readiness Intelligence System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================
# STYLES
# =============================================================
st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}

    .pris-hero {
        padding: 1.6rem 1.8rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #4338CA 0%, #6D28D9 55%, #7C3AED 100%);
        color: #fff;
        margin-bottom: 1.4rem;
    }
    .pris-hero h1 {margin: 0; font-size: 1.9rem;}
    .pris-hero p {margin: 0.35rem 0 0 0; opacity: 0.9; font-size: 0.98rem;}

    .score-card {
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        color: #fff;
        text-align: center;
    }
    .score-card .score-value {font-size: 3rem; font-weight: 800; line-height: 1;}
    .score-card .score-label {font-size: 1.05rem; font-weight: 600; margin-top: 0.35rem;}
    .score-card .score-sub {font-size: 0.82rem; opacity: 0.85; margin-top: 0.3rem;}

    .chip-container {display: flex; flex-wrap: wrap; gap: 8px; margin: 0.4rem 0 0.8rem 0;}
    .chip {
        padding: 5px 13px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .chip-matched  {background:#DCFCE7; color:#166534; border:1px solid #86EFAC;}
    .chip-missing  {background:#FEE2E2; color:#991B1B; border:1px solid #FCA5A5;}
    .chip-critical {background:#FEF3C7; color:#92400E; border:1px solid #FCD34D;}
    .chip-optional {background:#F3F4F6; color:#374151; border:1px solid #D1D5DB;}
    .chip-neutral  {background:#E0E7FF; color:#3730A3; border:1px solid #A5B4FC;}
    .chip-empty {color:#9CA3AF; font-size:0.85rem; font-style: italic;}

    .section-card {
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1rem;
        background: #FFFFFF;
        color: #111827;
    }
    .section-card h4 {margin-top: 0; color: #111827;}
    .section-card p {color: #111827;}
    .section-card b {color: #111827;}
    </style>
    """,
    unsafe_allow_html=True,
)

READINESS_STYLE = {
    "Highly Ready": {"color": "#16A34A", "emoji": "🟢"},
    "Moderately Ready": {"color": "#2563EB", "emoji": "🔵"},
    "Needs Improvement": {"color": "#D97706", "emoji": "🟠"},
    "Not Ready Yet": {"color": "#DC2626", "emoji": "🔴"},
}
DEFAULT_STYLE = {"color": "#6B7280", "emoji": "⚪"}

SAMPLE_JD = """We are hiring a Data Scientist.

Skills Required:
Python, SQL, Machine Learning, Deep Learning, TensorFlow, Scikit-learn, NLP, Git, Docker

Good to Have:
AWS, Spark

Responsibilities:
- Build and deploy ML models
- Perform data cleaning and feature engineering
- Collaborate with cross-functional teams

Qualification:
B.Tech / M.Tech in Computer Science or related field
"""

# =============================================================
# HELPERS
# =============================================================
def render_chips(items, css_class):
    items = [i for i in (items or []) if str(i).strip()]
    if not items:
        return "<p class='chip-empty'>None 🎉</p>"
    chips = "".join(f"<span class='chip {css_class}'>{str(i).title()}</span>" for i in items)
    return f"<div class='chip-container'>{chips}</div>"


def readiness_style(label):
    return READINESS_STYLE.get(label, DEFAULT_STYLE)


def reset_analysis():
    for key in ("result", "jd_textarea"):
        st.session_state.pop(key, None)


def run_pipeline(pdf_path, job_description):
    steps = [
        "📄 Extracting text from resume PDF",
        "🧠 Analyzing resume with AI",
        "📋 Analyzing job description with AI",
        "🔍 Computing skill gap & features",
        "📊 Predicting placement readiness (ML model)",
        "🗺️ Generating personalized improvement plan",
        "📥 Building downloadable PDF report",
    ]
    result = {}
    with st.status("Running analysis pipeline…", expanded=True) as status:
        st.write(steps[0])
        resume_text = extract_resume_text(pdf_path)
        if not resume_text:
            status.update(label="Failed to read the resume PDF.", state="error")
            st.error("Could not extract any text from the uploaded PDF. Please try a different file.")
            st.stop()

        st.write(steps[1])
        resume_json = analyze_resume(resume_text)

        st.write(steps[2])
        jd_json = analyze_job_description(job_description)

        st.write(steps[3])
        gap = analyze_skill_gap(resume_json, jd_json)
        feature_df = build_feature_dataframe(gap["features"])

        st.write(steps[4])
        prediction, confidence = predict_readiness(feature_df)

        st.write(steps[5])
        improvement_plan = generate_improvement_plan(gap)

        st.write(steps[6])
        report_name = f"Placement_Readiness_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path_out = generate_pdf_report(
            report_name, prediction, confidence, feature_df, gap, improvement_plan
        )

        status.update(label="✅ Analysis complete!", state="complete")

    result.update(
        resume_json=resume_json,
        jd_json=jd_json,
        gap=gap,
        feature_df=feature_df,
        prediction=prediction,
        confidence=confidence,
        improvement_plan=improvement_plan,
        pdf_path=pdf_path_out,
    )
    return result


# =============================================================
# SIDEBAR
# =============================================================
with st.sidebar:
    st.markdown("## 🎯 PRIS")
    st.caption("Placement Readiness Intelligence System")

    api_key_present = bool(os.getenv("GROQ_API_KEY"))
    if api_key_present:
        st.success("Groq API key detected", icon="✅")
    else:
        st.error("GROQ_API_KEY not found in environment (.env)", icon="⚠️")

    st.markdown("---")
    st.markdown(
        """
        **How it works**
        1. Upload a student resume (PDF)
        2. Paste the target job description
        3. Click **Analyze Resume**
        4. Review skill gaps & readiness score
        5. Download the full PDF report
        """
    )

    st.markdown("---")
    if st.button("📋 Load Sample Job Description", use_container_width=True):
        st.session_state["jd_textarea"] = SAMPLE_JD
        st.rerun()

    if st.button("🔄 Start New Analysis", use_container_width=True):
        reset_analysis()
        st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit · Groq LLM · Scikit-learn")

# =============================================================
# HERO
# =============================================================
st.markdown(
    """
    <div class="pris-hero">
        <h1>🎯 Placement Readiness Intelligence System</h1>
        <p>Upload a resume, paste a job description, and get an AI + ML powered readiness score,
        skill gap analysis, and a personalized improvement roadmap.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =============================================================
# INPUT SECTION
# =============================================================
col_left, col_right = st.columns([1, 1.4], gap="large")

with col_left:
    st.markdown("#### 📄 Student Resume")
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF only)", type=["pdf"], label_visibility="collapsed"
    )
    if uploaded_file:
        st.caption(f"Selected file: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")

with col_right:
    st.markdown("#### 📋 Job Description")
    st.session_state.setdefault("jd_textarea", "")
    job_description = st.text_area(
        "Paste Job Description",
        height=220,
        placeholder="Paste the full job description here…",
        label_visibility="collapsed",
        key="jd_textarea",
    )

analyze_clicked = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

st.markdown("---")

# =============================================================
# RUN PIPELINE
# =============================================================
if analyze_clicked:
    if not uploaded_file:
        st.error("Please upload a resume PDF before analyzing.")
        st.stop()
    if not job_description.strip():
        st.error("Please paste a job description before analyzing.")
        st.stop()
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY is missing. Add it to your .env file before analyzing.")
        st.stop()

    os.makedirs("uploads", exist_ok=True)
    safe_name = f"{int(time.time())}_{uploaded_file.name}"
    pdf_path = os.path.join("uploads", safe_name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        st.session_state["result"] = run_pipeline(pdf_path, job_description)
    except Exception as e:
        st.error(f"Something went wrong during analysis: {e}")
        st.stop()

# =============================================================
# RESULTS
# =============================================================
result = st.session_state.get("result")

if not result:
    st.info("👆 Upload a resume and paste a job description, then click **Analyze Resume** to get started.")
else:
    resume_json = result["resume_json"]
    jd_json = result["jd_json"]
    gap = result["gap"]
    feature_df = result["feature_df"]
    prediction = result["prediction"]
    confidence = result["confidence"]
    improvement_plan = result["improvement_plan"]
    pdf_path = result["pdf_path"]

    style = readiness_style(prediction)
    top_score = round(confidence.get(prediction, 0), 1)

    tab_overview, tab_resume, tab_jd, tab_gap, tab_plan, tab_report = st.tabs(
        ["🏁 Overview", "🧑‍💼 Resume Analysis", "📋 JD Analysis", "🔍 Skill Gap", "🗺️ Improvement Plan", "📥 Report"]
    )

    # ---------------- OVERVIEW ----------------
    with tab_overview:
        c1, c2 = st.columns([1, 1.6], gap="large")

        with c1:
            st.markdown(
                f"""
                <div class="score-card" style="background:{style['color']};">
                    <div class="score-value">{top_score}<span style="font-size:1.3rem;">/100</span></div>
                    <div class="score-label">{style['emoji']} {prediction}</div>
                    <div class="score-sub">Placement Readiness Score</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            m1.metric("Skill Match", f"{gap['features']['skill_match_percentage']}%")
            m2.metric("Critical Skill Match", f"{gap['features']['critical_skill_match_percentage']}%")
            m3.metric("Resume Completeness", f"{gap['features']['resume_completeness_score']}%")

        with c2:
            st.markdown("##### Confidence by Category")
            conf_df = pd.DataFrame(
                {"Category": list(confidence.keys()), "Confidence": list(confidence.values())}
            )
            bar_colors = [readiness_style(cat)["color"] for cat in conf_df["Category"]]
            conf_df["Color"] = bar_colors

            chart = (
                alt.Chart(conf_df)
                .mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, height=28)
                .encode(
                    x=alt.X("Confidence:Q", title="Confidence (%)", scale=alt.Scale(domain=[0, 100])),
                    y=alt.Y("Category:N", sort="-x", title=None),
                    color=alt.Color("Color:N", scale=None, legend=None),
                    tooltip=[alt.Tooltip("Category:N"), alt.Tooltip("Confidence:Q", format=".1f")],
                )
            )
            labels = (
                alt.Chart(conf_df)
                .mark_text(align="left", dx=6, fontWeight="bold")
                .encode(
                    x="Confidence:Q",
                    y=alt.Y("Category:N", sort="-x"),
                    text=alt.Text("Confidence:Q", format=".1f"),
                )
            )
            st.altair_chart(
                (chart + labels).properties(height=200).configure_axis(labelFontSize=13, titleFontSize=12),
                use_container_width=True,
            )

        st.markdown("##### 📝 Quick Summary")
        st.markdown(
            f"""
            <div class="section-card">
                <p><b>Resume Summary:</b> {resume_json.get("summary") or "Not available."}</p>
                <p><b>Target Role:</b> {jd_json.get("job_title") or "Not specified"} ({jd_json.get("role_category") or "N/A"})</p>
                <p><b>Resume Category:</b> {resume_json.get("resume_category") or "Not detected"}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------- RESUME ANALYSIS ----------------
    with tab_resume:
        r1, r2 = st.columns(2, gap="large")
        with r1:
            st.markdown("##### Resume Snapshot")
            st.write(f"**Category:** {resume_json.get('resume_category', 'N/A')}")
            st.write(f"**Education:** {resume_json.get('education', 'N/A')}")
            st.write("**Resume Completeness**")
            st.progress(min(100, int(resume_json.get("resume_completeness", 0))) / 100)

            st.markdown("##### Skills")
            st.markdown(render_chips(resume_json.get("skills"), "chip-neutral"), unsafe_allow_html=True)

            st.markdown("##### Tools & Technologies")
            st.markdown(render_chips(resume_json.get("tools"), "chip-neutral"), unsafe_allow_html=True)

        with r2:
            st.markdown("##### ✅ Strengths")
            for s in resume_json.get("strengths", []) or ["Not available"]:
                st.markdown(f"- {s}")
            st.markdown("##### ⚠️ Weaknesses")
            for w in resume_json.get("weaknesses", []) or ["Not available"]:
                st.markdown(f"- {w}")

        st.markdown("---")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown("##### 💼 Projects")
            for x in resume_json.get("projects", []) or ["None listed"]:
                st.markdown(f"- {x}")
        with p2:
            st.markdown("##### 🎓 Certifications")
            for x in resume_json.get("certifications", []) or ["None listed"]:
                st.markdown(f"- {x}")
        with p3:
            st.markdown("##### 🏢 Internships")
            for x in resume_json.get("internships", []) or ["None listed"]:
                st.markdown(f"- {x}")

    # ---------------- JD ANALYSIS ----------------
    with tab_jd:
        j1, j2 = st.columns(2, gap="large")
        with j1:
            st.write(f"**Job Title:** {jd_json.get('job_title', 'N/A')}")
            st.write(f"**Role Category:** {jd_json.get('role_category', 'N/A')}")
            st.write(f"**Minimum Education:** {jd_json.get('minimum_education', 'N/A')}")
            st.write(f"**Minimum Experience:** {jd_json.get('minimum_experience', 'N/A')}")

            st.markdown("##### Required Skills")
            st.markdown(render_chips(jd_json.get("required_skills"), "chip-neutral"), unsafe_allow_html=True)
            st.markdown("##### Critical Skills")
            st.markdown(render_chips(jd_json.get("critical_skills"), "chip-critical"), unsafe_allow_html=True)
            st.markdown("##### Optional / Good-to-have Skills")
            st.markdown(render_chips(jd_json.get("optional_skills"), "chip-optional"), unsafe_allow_html=True)

        with j2:
            st.markdown("##### Tools & Frameworks")
            st.markdown(render_chips(jd_json.get("tools_and_frameworks"), "chip-neutral"), unsafe_allow_html=True)
            st.markdown("##### Soft Skills")
            st.markdown(render_chips(jd_json.get("soft_skills"), "chip-neutral"), unsafe_allow_html=True)
            st.markdown("##### ATS Keywords")
            st.markdown(render_chips(jd_json.get("keywords"), "chip-optional"), unsafe_allow_html=True)

            st.markdown("##### Responsibilities")
            for r in jd_json.get("responsibilities", []) or ["Not specified"]:
                st.markdown(f"- {r}")

    # ---------------- SKILL GAP ----------------
    with tab_gap:
        g1, g2 = st.columns(2, gap="large")
        with g1:
            st.markdown("##### ✅ Matched Skills")
            st.markdown(render_chips(gap["matched_skills"], "chip-matched"), unsafe_allow_html=True)
            st.markdown("##### ❌ Missing Skills")
            st.markdown(render_chips(gap["missing_skills"], "chip-missing"), unsafe_allow_html=True)
        with g2:
            st.markdown("##### 🔴 Critical Missing Skills")
            st.markdown(render_chips(gap["critical_missing_skills"], "chip-critical"), unsafe_allow_html=True)
            st.markdown("##### 🟡 Optional Missing Skills")
            st.markdown(render_chips(gap["optional_missing_skills"], "chip-optional"), unsafe_allow_html=True)

        st.markdown("##### 🎯 Skills To Learn First")
        for i, s in enumerate(gap["skills_to_learn_first"], start=1):
            st.markdown(f"{i}. {s.title()}")
        if not gap["skills_to_learn_first"]:
            st.markdown("_No priority skill gaps found — great job!_")

        with st.expander("📊 View Raw ML Feature Table"):
            st.dataframe(feature_df, use_container_width=True)

    # ---------------- IMPROVEMENT PLAN ----------------
    with tab_plan:
        i1, i2 = st.columns(2, gap="large")
        with i1:
            st.markdown("##### 📝 Resume Improvement Suggestions")
            for x in improvement_plan["resume_improvement_suggestions"]:
                st.markdown(f"- ✅ {x}")
        with i2:
            st.markdown("##### 📘 Job Preparation Suggestions")
            for x in improvement_plan["job_preparation_suggestions"]:
                st.markdown(f"- 📘 {x}")

        st.markdown("---")
        st.markdown("##### 🗓️ 7-Day Improvement Plan")
        day_cols = st.columns(len(improvement_plan["seven_day_plan"]))
        for col, (day, tasks) in zip(day_cols, improvement_plan["seven_day_plan"].items()):
            with col:
                st.markdown(f"**{day}**")
                for t in tasks:
                    st.markdown(f"- {t}")

        st.markdown("##### 📆 30-Day Improvement Plan")
        for week, tasks in improvement_plan["thirty_day_plan"].items():
            with st.expander(week, expanded=False):
                for t in tasks:
                    st.markdown(f"- {t}")

    # ---------------- REPORT ----------------
    with tab_report:
        st.markdown("##### 📥 Download Full Report")
        st.write(
            "This PDF includes the readiness score, confidence breakdown, extracted features, "
            "skill gap analysis, and the full 7-day / 30-day improvement plan."
        )
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📥 Download PDF Report",
                    f,
                    file_name=os.path.basename(pdf_path),
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )
        else:
            st.warning("Report file not found. Please re-run the analysis.")

    st.markdown("---")
    if st.button("🔄 Analyze Another Resume"):
        reset_analysis()
        st.rerun()
