# AI-Powered Resume Screening System 🚀

An advanced, machine learning-driven Resume Screening and Ranking system built to automate the recruitment pipeline. This application critically evaluates candidate resumes against custom job descriptions, dynamically extracts required technical skills using Natural Language Processing (NLP), and assigns a percentile match score based on semantic vector similarity.

## 🌟 Key Features
- **Dynamic Skill Extraction**: Automatically leverages the `spaCy` NLP pipeline to dynamically recognize and extract required terminology directly from custom Job Descriptions.
- **Smart Resume Parsing**: Native extraction of structured raw text directly from PDF (`pypdf`) and TXT files.
- **AI Scoring Engine**: Combines baseline Keyword Intersection with Semantic `scikit-learn` TF-IDF Cosine Similarity for a robust, resilient match ranking.
- **Premium User Interface**: Features a beautiful React layout built with Vanilla CSS glassmorphism and smooth micro-animations for an interactive dragged-and-drop recruiter experience.
- **Vercel Optimized**: Fully configured via `vercel.json` monorepo routing to deploy the frontend statically while hosting the FastAPI backend purely on Python Serverless Functions.

## 🏗️ Architecture Stack
- **Backend API**: Python 3, FastAPI, Uvicorn, scikit-learn, spaCy
- **Frontend Panel**: React 18, Vite, JS, CSS

## 💻 Local Quickstart

### 1. Start the Backend
From the root folder, simply double-click or run:
```bash
.\start_backend.bat
```
*(This script automatically hooks into the secure Python virtual environment and boots the Uvicorn server on `http://0.0.0.0:8000`)*

### 2. Start the Frontend
In a separate terminal, run:
```bash
.\start_frontend.bat
```
*(The Dashboard will be live locally at `http://localhost:5173`)*

## ☁️ Vercel Deployment
This repository is 100% production-ready for **Vercel Serverless Hosting**.
1. Import the repository into your Vercel Dashboard from GitHub.
2. Ensure the "Root Directory" is set to the base directory.
3. Vercel will explicitly read the `vercel.json` controller configuration to seamlessly build both the frontend and Serverless backend API entirely in one pipeline!
