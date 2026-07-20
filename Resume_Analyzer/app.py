import os

import streamlit as st

from resume_parser import extract_resume_text
from llm_analyzer import analyze_resume
from feature_builder import build_feature_dataframe
from predictor import predict_readiness


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Analyze Resume against Job Description using Gemini + Machine Learning")


# ---------------------------------------------------
# Resume Upload
# ---------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


# ---------------------------------------------------
# Job Description
# ---------------------------------------------------

job_description = st.text_area(
    "Paste Job Description",
    height=250
)


# ---------------------------------------------------
# Analyze Button
# ---------------------------------------------------

if st.button("Analyze Resume"):

    if uploaded_file is None:

        st.error("Please upload a resume.")

    elif job_description.strip() == "":

        st.error("Please enter Job Description.")

    else:

        # Create uploads folder
        os.makedirs("uploads", exist_ok=True)

        pdf_path = os.path.join(
            "uploads",
            uploaded_file.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # -----------------------------------------

        with st.spinner("Extracting Resume..."):

            resume_text = extract_resume_text(pdf_path)

        st.success("Resume Extracted Successfully")

        # -----------------------------------------

        with st.spinner("Analyzing using Gemini..."):

            llm_features = analyze_resume(
                resume_text,
                job_description
            )

        st.success("Analysis Completed")

        # -----------------------------------------

        feature_df = build_feature_dataframe(
            llm_features
        )

        result = predict_readiness(
            feature_df
        )

        # -----------------------------------------

        st.header("Prediction")

        st.success(result["predicted_class"])

        # -----------------------------------------

        st.header("Confidence Scores")

        st.json(result["probabilities"])

        # -----------------------------------------

        st.header("Extracted Features")

        st.dataframe(feature_df)
