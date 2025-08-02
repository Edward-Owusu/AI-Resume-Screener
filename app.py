import streamlit as st
import os
from resume_parser import extract_text_from_pdf as extract_resume_pdf, extract_text_from_docx as extract_resume_docx
from job_parser import extract_text_from_pdf as extract_job_pdf, extract_text_from_docx as extract_job_docx, extract_text_from_txt
from similarity import calculate_similarity, find_missing_keywords  # Ensure this is in your project

UPLOAD_FOLDER = "uploads"

def save_uploaded_file(uploaded_file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

st.set_page_config(page_title="AI Resume Screener", layout="centered")
st.title("📄 AI-Based Resume Screener")
# Inject custom CSS for background and styling
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1521791136064-7986c2920216"); /* Example image */
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Text container background */
    .block-container {
        background-color: rgba(255, 255, 255, 0.8); /* semi-transparent white */
        padding: 2rem;
        border-radius: 12px;
    }

    /* Header font */
    h1, h2, h3, .stTextInput label {
        color: #003366;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Step 1: Upload Resume")
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

st.header("Step 2: Upload Job Description")
job_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

if st.button("Extract and Display Text"):
    if resume_file and job_file:
        resume_path = save_uploaded_file(resume_file)
        job_path = save_uploaded_file(job_file)

        # Extract resume text
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_resume_pdf(resume_path)
        else:
            resume_text = extract_resume_docx(resume_path)

        # Extract job description text
        if job_file.name.endswith(".pdf"):
            job_text = extract_job_pdf(job_path)
        elif job_file.name.endswith(".docx"):
            job_text = extract_job_docx(job_path)
        else:
            job_text = extract_text_from_txt(job_path)

        st.subheader("📘 Resume Text")
        st.text_area("Extracted Resume Text", resume_text, height=200)

        st.subheader("📙 Job Description Text")
        st.text_area("Extracted Job Description Text", job_text, height=200)

        # Scoring
        score = calculate_similarity(resume_text, job_text)
        missing_keywords = find_missing_keywords(resume_text, job_text)

        st.subheader("📊 Resume Match Score")
        st.success(f"Overall Resume Match Score: {score:.2f}%")

        st.subheader("🔍 Missing Keywords")
        st.warning(f"Your resume is missing {len(missing_keywords)} important keyword(s):")
        st.write(", ".join(missing_keywords))

        # Create downloadable feedback content
        feedback = (
            f"AI Resume Screener Feedback Report\n\n"
            f"✅ Resume Match Score: {score:.2f}%\n\n"
            f"🔍 Missing Keywords ({len(missing_keywords)}):\n"
            f"{', '.join(missing_keywords)}\n\n"
            f"💡 Suggestion: Consider updating your resume to include some of the key terms found in the job description."
        )

        # Show download button
        st.download_button(
            label="📥 Download Feedback as TXT",
            data=feedback,
            file_name="resume_feedback.txt",
            mime="text/plain"
        )

    else:
        st.warning("Please upload both a resume and a job description.")
