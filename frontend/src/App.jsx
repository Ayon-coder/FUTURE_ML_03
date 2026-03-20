import React, { useState, useRef } from 'react';
import './index.css';

function App() {
  const [jobDescription, setJobDescription] = useState('');
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => {
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleSubmit = async () => {
    if (!jobDescription || files.length === 0) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('job_description', jobDescription);
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const apiUrl = import.meta.env.PROD ? '/api/screen' : 'http://localhost:8000/api/screen';
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error('Error uploading files:', error);
      alert('Error connecting to backend API. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>AI Resume Screener</h1>
        <p>Automated skills extraction & candidate ranking system</p>
      </header>

      <main className="main-content">
        <section className="glass-panel" style={{ animationDelay: '0.1s' }}>
          <div className="input-group">
            <label htmlFor="jd">Job Description</label>
            <textarea
              id="jd"
              placeholder="Paste the target job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Candidate Resumes (PDF or TXT)</label>
            <div 
              className={`file-drop-area ${dragOver ? 'drag-over' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input 
                type="file" 
                multiple 
                accept=".pdf,.txt" 
                ref={fileInputRef}
                onChange={handleFileChange}
              />
              <p>Drag & drop resumes here or click to browse</p>
              <span style={{ fontSize: '2rem', marginTop: '1rem', display: 'block' }}>📄</span>
            </div>
          </div>

          {files.length > 0 && (
            <div className="file-list">
              <label>Selected Files ({files.length}):</label>
              {files.map((file, idx) => (
                <div className="file-item" key={idx} style={{ animationDelay: `${idx * 0.05}s` }}>
                  <span>{file.name}</span>
                  <span style={{ color: 'var(--text-muted)' }}>{(file.size / 1024).toFixed(1)} KB</span>
                </div>
              ))}
            </div>
          )}

          <button 
            className="btn-primary" 
            onClick={handleSubmit}
            disabled={loading || !jobDescription || files.length === 0}
          >
            {loading ? (
              <><span className="loading-spinner"></span> Analyzing Candidates...</>
            ) : 'Screen Resumes'}
          </button>
        </section>

        {results && (
          <section className="glass-panel" style={{ animationDelay: '0.3s' }}>
            <h2>Candidate Rankings</h2>
            <div style={{ overflowX: 'auto' }}>
              <table className="results-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Candidate</th>
                    <th>Match Score</th>
                    <th>Matching Skills</th>
                    <th>Missing Skills</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((res, idx) => (
                    <tr key={idx} style={{ animation: `slideIn 0.3s ease-out ${idx * 0.1}s both` }}>
                      <td>#{idx + 1}</td>
                      <td style={{ fontWeight: 500, color: '#fff' }}>{res.filename}</td>
                      <td>
                        <div className="score-cell">
                          <span style={{ fontWeight: 'bold', color: 'var(--accent-color)' }}>{res.similarity_score}%</span>
                          <div className="score-bar-bg">
                            <div className="score-bar-fill" style={{ width: `${res.similarity_score}%` }}></div>
                          </div>
                        </div>
                      </td>
                      <td>
                        {res.matching_skills.length > 0 ? res.matching_skills.map((skill, i) => (
                          <span key={i} className="badge badge-success">{skill}</span>
                        )) : <span style={{ color: 'var(--text-muted)' }}>None</span>}
                      </td>
                      <td>
                        {res.missing_skills.length > 0 ? res.missing_skills.map((skill, i) => (
                          <span key={i} className="badge badge-danger">{skill}</span>
                        )) : <span style={{ color: 'var(--text-muted)' }}>None</span>}
                      </td>
                    </tr>
                  ))}
                  {results.length === 0 && (
                    <tr>
                      <td colSpan="5" style={{ textAlign: 'center', padding: '2rem' }}>No resumes matched.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
