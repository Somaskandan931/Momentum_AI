import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createProject } from "../services/projectService";
import API from "../services/api";

const examples = [
  "An AI tool that reads your calendar and automatically drafts agenda items for every meeting",
  "A browser extension that summarizes any article in 3 bullet points using NLP",
  "A habit tracker that uses reinforcement learning to adapt reminders to your schedule",
];

export default function IdeaSubmission() {
  const navigate = useNavigate();
  const [idea, setIdea] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState(0);

  const handleSubmit = async () => {
    if (!idea.trim() || !title.trim()) {
      setError("Please fill in both fields.");
      return;
    }
    setLoading(true);
    setError(null);
    setStep(1);

    try {
      const { data: project } = await createProject({ title, description: idea });
      setStep(2);
      await API.post("/ideas/generate-tasks", { idea, project_id: project.id });
      setStep(3);
      navigate(`/dashboard/${project.id}`);
    } catch (err) {
      setError("Something went wrong. Is the backend running?");
      setStep(0);
    } finally {
      setLoading(false);
    }
  };

  const steps = ["Analyzing idea", "Creating project", "Generating tasks"];

  return (
    <div style={{ minHeight: "calc(100vh - 56px)", display: "flex", alignItems: "center", justifyContent: "center", padding: "2rem" }}>
      {/* Background glow */}
      <div style={{
        position: "fixed", top: "20%", left: "50%", transform: "translateX(-50%)",
        width: "600px", height: "400px",
        background: "radial-gradient(ellipse, rgba(124,109,250,0.08) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />

      <div className="fade-up" style={{ width: "100%", maxWidth: "620px", position: "relative" }}>
        {/* Header */}
        <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
          <div style={{
            display: "inline-flex", alignItems: "center", gap: "6px",
            background: "var(--accent-dim)", border: "1px solid rgba(124,109,250,0.3)",
            borderRadius: "20px", padding: "4px 12px", marginBottom: "1.25rem",
            fontSize: "11px", fontWeight: 600, color: "var(--accent)",
            letterSpacing: "0.06em", textTransform: "uppercase",
          }}>
            <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: "var(--accent)", display: "inline-block" }} />
            AI-Powered Project Planning
          </div>
          <h1 style={{ fontSize: "2.6rem", fontWeight: 600, letterSpacing: "-0.04em", lineHeight: 1.1, marginBottom: "0.75rem" }}>
            What are you<br />
            <span style={{ color: "var(--accent)" }}>building?</span>
          </h1>
          <p style={{ color: "var(--text-2)", fontSize: "15px", lineHeight: 1.6 }}>
            Describe your idea and Momentum AI generates a full Kanban board,<br />
            task breakdown, and RL-optimised schedule automatically.
          </p>
        </div>

        {/* Form card */}
        <div className="card" style={{ padding: "2rem" }}>
          <div style={{ marginBottom: "1.25rem" }}>
            <label style={{ display: "block", fontSize: "12px", fontWeight: 600, color: "var(--text-2)", marginBottom: "8px", letterSpacing: "0.04em", textTransform: "uppercase" }}>
              Project Name
            </label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. AI Resume Analyzer"
              style={{ fontSize: "15px" }}
            />
          </div>

          <div style={{ marginBottom: "1.5rem" }}>
            <label style={{ display: "block", fontSize: "12px", fontWeight: 600, color: "var(--text-2)", marginBottom: "8px", letterSpacing: "0.04em", textTransform: "uppercase" }}>
              Describe Your Idea
            </label>
            <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Describe what you want to build, the problem it solves, and any technical ideas you have..."
              rows={5}
              style={{ resize: "vertical", lineHeight: 1.6, fontSize: "14px" }}
            />
          </div>

          {/* Example chips */}
          <div style={{ marginBottom: "1.5rem" }}>
            <p style={{ fontSize: "11px", color: "var(--text-3)", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.04em", fontWeight: 600 }}>
              Try an example
            </p>
            <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
              {examples.map((ex, i) => (
                <button
                  key={i}
                  onClick={() => {
                    setIdea(ex);
                    if (!title) setTitle(ex.split(" ").slice(0, 4).join(" "));
                  }}
                  style={{
                    background: "var(--bg-input)",
                    border: "1px solid var(--border)",
                    color: "var(--text-2)",
                    padding: "8px 12px",
                    borderRadius: "8px",
                    textAlign: "left",
                    fontSize: "12px",
                    lineHeight: 1.4,
                    cursor: "pointer",
                    transition: "all var(--transition)",
                  }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = "var(--accent)"; e.currentTarget.style.color = "var(--text)"; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = "var(--border)"; e.currentTarget.style.color = "var(--text-2)"; }}
                >
                  {ex}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div style={{
              background: "rgba(248,113,113,0.1)", border: "1px solid rgba(248,113,113,0.25)",
              borderRadius: "8px", padding: "10px 14px", marginBottom: "1rem",
              fontSize: "13px", color: "var(--danger)",
            }}>
              {error}
            </div>
          )}

          {/* Loading progress */}
          {loading && (
            <div style={{ marginBottom: "1rem" }}>
              {steps.map((s, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: "10px", padding: "6px 0" }}>
                  <div style={{
                    width: "18px", height: "18px", borderRadius: "50%",
                    background: i < step ? "var(--accent)" : i === step - 1 ? "var(--accent-dim)" : "var(--bg-input)",
                    border: `1px solid ${i < step ? "var(--accent)" : "var(--border)"}`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: "10px", flexShrink: 0,
                    transition: "all 0.3s ease",
                  }}>
                    {i < step ? "✓" : ""}
                  </div>
                  <span style={{ fontSize: "13px", color: i < step ? "var(--text)" : "var(--text-3)" }}>{s}</span>
                </div>
              ))}
            </div>
          )}

          <button
            className="btn-primary"
            onClick={handleSubmit}
            disabled={loading}
            style={{ width: "100%", padding: "13px", fontSize: "15px" }}
          >
            {loading ? "Generating plan..." : "Generate Execution Plan →"}
          </button>
        </div>
      </div>
    </div>
  );
}