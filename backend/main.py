from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.parser import extract_text_from_file
from utils.skill_extractor import extract_skills
from ml.scoring import calculate_similarity

app = FastAPI(title="Resume Screening API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/screen")
async def screen_resumes(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    results = []
    jd_skills = extract_skills(job_description, is_jd=True)
    
    for file in files:
        file_content = await file.read()
        filename = file.filename
        text = extract_text_from_file(file_content, filename)
        
        if not text.strip():
            continue
            
        resume_skills = extract_skills(text)
        
        raw_matching = list(set(jd_skills) & set(resume_skills))
        raw_missing = list(set(jd_skills) - set(resume_skills))
        
        # Remove standalone words if part of a larger matched phrase
        matching_skills = []
        for match in raw_matching:
            if not any(match != other and match in other.split() for other in raw_matching):
                matching_skills.append(match)
                
        # Remove missing words if part of a successfully matched phrase
        missing_skills = []
        for m in raw_missing:
            if not any(m in match.split() for match in matching_skills):
                missing_skills.append(m)
        
        score = calculate_similarity(job_description, text)
        
        results.append({
            "filename": filename,
            "similarity_score": round(score * 100, 2),
            "matching_skills": sorted(matching_skills),
            "missing_skills": sorted(missing_skills)
        })
    
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)
    return {"results": results}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
