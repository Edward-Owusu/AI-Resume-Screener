import streamlit as st
import os
from resume_parser import extract_text_from_pdf as extract_resume_pdf, extract_text_from_docx as extract_resume_docx
from job_parser import extract_text_from_pdf as extract_job_pdf, extract_text_from_docx as extract_job_docx, extract_text_from_txt
from similarity import calculate_similarity, find_missing_keywords

UPLOAD_FOLDER = "uploads"

def save_uploaded_file(uploaded_file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Set page configuration
st.set_page_config(page_title="AI Resume Screener", layout="centered")

# Apply custom background and style
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        height: 100%;
    }

    /* Makes the form container readable */
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }

    h1, h2, h3, label {
        color: #002b5c;
        font-family: 'Segoe UI', sans-serif;
    }

    .stButton > button {
        background-color: #004080;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6em 1.2em;
    }

    .stButton > button:hover {
        background-color: #0066cc;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("📄 AI-Based Resume Screener")

# Upload Section
st.header("Step 1: Upload Resume")
resume_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

st.header("Step 2: Upload Job Description")
job_file = st.file_uploader("Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

# Main Logic
if st.button("Extract and Display Text"):
    if resume_file and job_file:
        resume_path = save_uploaded_file(resume_file)
        job_path = save_uploaded_file(job_file)

        # Extract resume text
        resume_text = extract_resume_pdf(resume_path) if resume_file.name.endswith(".pdf") else extract_resume_docx(resume_path)

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

        # Score & Feedback
        score = calculate_similarity(resume_text, job_text)
        missing_keywords = find_missing_keywords(resume_text, job_text)

        st.subheader("📊 Resume Match Score")
        st.success(f"Overall Resume Match Score: {score:.2f}%")

        st.subheader("🔍 Missing Keywords")
        st.warning(f"Your resume is missing {len(missing_keywords)} important keyword(s):")
        st.write(", ".join(missing_keywords))

        feedback = (
            f"AI Resume Screener Feedback Report\n\n"
            f"✅ Resume Match Score: {score:.2f}%\n\n"
            f"🔍 Missing Keywords ({len(missing_keywords)}):\n"
            f"{', '.join(missing_keywords)}\n\n"
            f"💡 Suggestion: Consider updating your resume to include some of the key terms found in the job description."
        )

        st.download_button(
            label="📥 Download Feedback as TXT",
            data=feedback,
            file_name="resume_feedback.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please upload both a resume and a job description.")
