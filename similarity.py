from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(resume_text, job_text):
    vectorizer = TfidfVectorizer().fit_transform([resume_text, job_text])
    score = cosine_similarity(vectorizer[0:1], vectorizer[1:2])[0][0]
    return round(score * 100, 2)

def find_missing_keywords(resume_text, job_text):
    job_words = set(job_text.lower().split())
    resume_words = set(resume_text.lower().split())
    missing = job_words - resume_words
    return sorted(missing)
