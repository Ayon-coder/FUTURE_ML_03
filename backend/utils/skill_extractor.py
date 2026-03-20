import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    pass

# Fallback common tech skills
COMMON_SKILLS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "react", "node.js",
    "fastapi", "html", "css", "sql", "aws", "docker", "kubernetes", "git",
    "machine learning", "deep learning", "nlp", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "data science", "agile", "linux", "aiml", "artificial intelligence"
}

def extract_skills(text: str, is_jd: bool = False) -> list:
    """
    If is_jd=True, we aggressively extract all proper nouns/noun chunks as 'required skills'.
    Otherwise, we just extract predefined tech skills and obvious entities to avoid noise.
    """
    doc = nlp(text.lower())
    found_skills = set()
    
    # 1. Look for known heavy-hitters
    lower_text = text.lower()
    for skill in COMMON_SKILLS:
        if skill in lower_text:
            found_skills.add(skill)
            
    # 2. Add dynamic extraction
    for chunk in doc.noun_chunks:
        word = chunk.text.strip().lower()
        if len(word) > 2 and word not in ["we", "you", "they", "this", "that", "the role", "candidate", "experience", "years", "job", "description"]:
            # If it's a JD, we assume all technical terms/nouns are required skills 
            if is_jd or word in COMMON_SKILLS:
                found_skills.add(word)
                
    # If the user literally just typed one word (like "AIML"), ensure we grab it!
    words = text.split()
    if len(words) <= 3:
        for w in words:
            if len(w) > 2:
                found_skills.add(w.lower())
                
    return list(found_skills)
