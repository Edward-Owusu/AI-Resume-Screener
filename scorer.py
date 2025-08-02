# scorer.py

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [chunk.text.strip() for chunk in doc.noun_chunks if len(chunk.text.strip()) > 1]
    return list(set(keywords))  # remove duplicates

def score_resume(resume_text, job_text):
    documents = [job_text, resume_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity_score * 100, 2)  # percentage score
