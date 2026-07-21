import os
import streamlit as st
from resume_parser import extract_resume_text
from resume_analyzer import analyze_resume
from jd_analyzer import analyze_job_description
from skill_gap_analyzer import analyze_skill_gap
from improvement_plan import generate_improvement_plan
from feature_builder import build_feature_dataframe
from predictor import predict_readiness
from report_generator import generate_pdf_report

st.set_page_config(page_title='Placement Readiness Intelligence System',page_icon='🎯',layout='wide')
st.title('🎯 Placement Readiness Intelligence System')
uploaded_file=st.file_uploader('Upload Resume (PDF)',type=['pdf'])
job_description=st.text_area('Paste Job Description',height=250)
if st.button('Analyze Resume'):
    if not uploaded_file:
        st.error('Upload Resume'); st.stop()
    if not job_description.strip():
        st.error('Paste Job Description'); st.stop()
    os.makedirs('uploads',exist_ok=True)
    pdf_path=os.path.join('uploads',uploaded_file.name)
    with open(pdf_path,'wb') as f:f.write(uploaded_file.read())
    resume_text=extract_resume_text(pdf_path)
    resume_json=analyze_resume(resume_text)
    jd_json=analyze_job_description(job_description)
    gap=analyze_skill_gap(resume_json,jd_json)
    feature_df=build_feature_dataframe(gap['features'])
    prediction,confidence=predict_readiness(feature_df)
    improvement_plan=generate_improvement_plan(gap)
    st.success(prediction)
    st.subheader('Confidence'); st.json(confidence)
    st.dataframe(feature_df)
    for t,k in [('Matched Skills','matched_skills'),('Missing Skills','missing_skills'),('Critical Missing Skills','critical_missing_skills'),('Optional Missing Skills','optional_missing_skills')]:
        st.subheader(t); st.write(gap[k])
    st.subheader('Skills to Learn First'); st.write(gap['skills_to_learn_first'])
    st.header('Resume Improvement Suggestions')
    for x in improvement_plan['resume_improvement_suggestions']: st.write('✅',x)
    st.header('Job Preparation Suggestions')
    for x in improvement_plan['job_preparation_suggestions']: st.write('📘',x)
    st.header('7-Day Improvement Plan')
    for d,tasks in improvement_plan['seven_day_plan'].items():
        st.subheader(d)
        [st.write('-',i) for i in tasks]
    st.header('30-Day Improvement Plan')
    for d,tasks in improvement_plan['thirty_day_plan'].items():
        st.subheader(d)
        [st.write('-',i) for i in tasks]
    pdf=generate_pdf_report('Placement_Readiness_Report.pdf',prediction,confidence,feature_df,gap,improvement_plan)
    with open(pdf,'rb') as f:
        st.download_button('📥 Download PDF Report',f,file_name='Placement_Readiness_Report.pdf',mime='application/pdf')
