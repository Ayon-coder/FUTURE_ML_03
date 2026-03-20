from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def clean_text(text: str) -> str:
    text = re.sub(r'\W+', ' ', text)
    return text.lower().strip()

def calculate_similarity(job_description: str, resume_text: str) -> float:
    jd_clean = clean_text(job_description)
    resume_clean = clean_text(resume_text)
    
    if not jd_clean or not resume_clean:
        return 0.0
        
    # Baseline overlap matching - highly sensitive to small job descriptions
    jd_words = set(jd_clean.split())
    resume_words = set(resume_clean.split())
    
    overlap = len(jd_words.intersection(resume_words))
    keyword_score = overlap / len(jd_words) if jd_words else 0.0
    
    # ML TF-IDF matching
    try:
        # We don't use stop_words='english' if the JD is tiny, it might drop everything.
        use_stop_words = 'english' if len(jd_words) > 5 else None
        vectorizer = TfidfVectorizer(stop_words=use_stop_words)
        
        tfidf_matrix = vectorizer.fit_transform([jd_clean, resume_clean])
        cosine_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        
        # Merge scores: 60% Semantic, 40% Keyword
        final_score = (cosine_sim * 0.6) + (keyword_score * 0.4)
        return min(final_score, 1.0)
    except ValueError:
        return float(keyword_score)
