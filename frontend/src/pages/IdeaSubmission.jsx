import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createProject } from "../services/projectService";
import API from "../services/api";

export default function IdeaSubmission() {
  const navigate = useNavigate();
  const [idea, setIdea] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!idea.trim() || !title.trim()) {
      setError("Please fill in both the project title and your idea.");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      // 1. Create project
      const { data: project } = await createProject({ title, description: idea });

      // 2. Generate tasks from idea
      await API.post("/ideas/generate-tasks", {
        idea,
        project_id: project.id,
      });

      navigate(`/dashboard/${project.id}`);
    } catch (err) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "640px", margin: "3rem auto", padding: "0 1rem" }}>
      <h1 style={{ color: "#1a1a2e", marginBottom: "0.5rem" }}>Submit Your Idea</h1>
      <p style={{ color: "#7f8c8d", marginBottom: "2rem" }}>
        Describe your project idea and Momentum AI will generate a full execution roadmap and Kanban board automatically.
      </p>

      <label style={labelStyle}>Project Title</label>
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="e.g. AI Resume Analyzer"
        style={inputStyle}
      />

      <label style={labelStyle}>Describe Your Idea</label>
      <textarea
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        placeholder="e.g. A tool that uses NLP to analyze resumes, score them against job descriptions, and suggest improvements..."
        rows={5}
        style={{ ...inputStyle, resize: "vertical" }}
      />

      {error && <p style={{ color: "#e74c3c", fontSize: "0.9rem" }}>{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          background: loading ? "#95a5a6" : "#1a1a2e",
          color: "#fff",
          border: "none",
          padding: "12px 28px",
          borderRadius: "6px",
          cursor: loading ? "not-allowed" : "pointer",
          fontWeight: 600,
          fontSize: "1rem",
          marginTop: "0.5rem",
        }}
      >
        {loading ? "Generating plan..." : "Generate Execution Plan"}
      </button>
    </div>
  );
}

const labelStyle = {
  display: "block",
  fontWeight: 600,
  fontSize: "0.9rem",
  color: "#2c3e50",
  marginBottom: "6px",
  marginTop: "1.2rem",
};

const inputStyle = {
  width: "100%",
  padding: "10px 12px",
  border: "1px solid #dde1e7",
  borderRadius: "6px",
  fontSize: "0.95rem",
  outline: "none",
  boxSizing: "border-box",
};
