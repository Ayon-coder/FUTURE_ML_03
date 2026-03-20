import re

# Comprehensive skill catalog - covers major tech domains
SKILL_CATALOG = {
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "golang",
    "rust", "php", "swift", "kotlin", "scala", "perl", "r", "matlab", "dart", "lua",
    "objective-c", "shell", "bash", "powershell", "sql", "nosql", "html", "css", "sass",
    
    # Frameworks & Libraries
    "react", "angular", "vue", "next.js", "nextjs", "nuxt", "svelte", "django", "flask",
    "fastapi", "spring", "express", "node.js", "nodejs", ".net", "dotnet", "rails",
    "laravel", "bootstrap", "tailwind", "jquery", "redux", "graphql", "rest", "restful",
    
    # Data Science & ML
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "opencv", "spacy",
    "data science", "data analysis", "data engineering", "data mining",
    "neural network", "regression", "classification", "clustering",
    "random forest", "xgboost", "lightgbm", "reinforcement learning",
    "generative ai", "llm", "large language model", "transformer",
    "bert", "gpt", "prompt engineering", "rag",
    
    # AI/ML General
    "artificial intelligence", "ai", "ml", "aiml", "ai/ml",
    
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s",
    "terraform", "ansible", "jenkins", "ci/cd", "cicd", "devops", "mlops",
    "linux", "unix", "nginx", "apache", "serverless", "lambda", "cloudformation",
    "ec2", "s3", "rds", "dynamodb", "redis", "kafka", "rabbitmq",
    
    # Databases
    "mysql", "postgresql", "postgres", "mongodb", "sqlite", "oracle",
    "cassandra", "elasticsearch", "firebase", "supabase",
    
    # Tools & Practices
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "agile", "scrum", "kanban", "tdd", "bdd", "microservices",
    "api", "sdk", "oauth", "jwt", "websocket",
    
    # Specializations
    "blockchain", "web3", "solidity", "cybersecurity", "penetration testing",
    "embedded systems", "iot", "robotics", "ar", "vr",
    "figma", "photoshop", "ui/ux", "ux", "ui", "wireframing",
    
    # Soft Skills
    "leadership", "communication", "teamwork", "problem solving",
    "critical thinking", "project management", "time management",
}

def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text.lower().strip())

def extract_skills(text: str, is_jd: bool = False) -> list:
    normalized = _normalize(text)
    found = set()
    
    # 1. Match multi-word skills first (longest match priority)
    sorted_skills = sorted(SKILL_CATALOG, key=len, reverse=True)
    for skill in sorted_skills:
        if skill in normalized:
            found.add(skill)
    
    # 2. If JD is very short (1-3 words), grab each word as a skill
    words = text.split()
    if len(words) <= 5:
        for w in words:
            clean = re.sub(r'[^a-zA-Z0-9/#+.]', '', w).lower()
            if len(clean) >= 2:
                found.add(clean)
    
    return list(found)
