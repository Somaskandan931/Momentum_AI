import React, { useState } from "react";
import { getSurvivalScore } from "../services/projectService";
import { survivalScoreLabel } from "../utils/helpers";

export default function SurvivalScore({ projectId }) {
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchScore = async () => {
    setLoading(true);
    setError(null);
    try {
      const { data } = await getSurvivalScore(projectId);
      setScore(data.idea_survival_score);
    } catch (err) {
      setError("Could not compute score.");
    } finally {
      setLoading(false);
    }
  };

  const label = score !== null ? survivalScoreLabel(score) : null;
  const filled = score !== null ? Math.round(score) : 0;

  return (
    <div style={{ padding: "1rem", background: "#f8f9fa", borderRadius: "8px", maxWidth: "320px" }}>
      <h4 style={{ margin: "0 0 12px", color: "#2c3e50" }}>Idea Survival Score</h4>

      {score === null ? (
        <button
          onClick={fetchScore}
          disabled={loading}
          style={{
            background: "#1a1a2e",
            color: "#fff",
            border: "none",
            padding: "8px 16px",
            borderRadius: "6px",
            cursor: "pointer",
            fontSize: "0.9rem",
          }}
        >
          {loading ? "Computing..." : "Compute Score"}
        </button>
      ) : (
        <div>
          <div style={{ fontSize: "2.5rem", fontWeight: 700, color: label.color }}>
            {filled}
            <span style={{ fontSize: "1rem", fontWeight: 400, color: "#95a5a6" }}>/100</span>
          </div>

          {/* Progress bar */}
          <div style={{ background: "#dde1e7", borderRadius: "4px", height: "8px", margin: "8px 0" }}>
            <div
              style={{
                width: `${filled}%`,
                height: "100%",
                background: label.color,
                borderRadius: "4px",
                transition: "width 0.5s ease",
              }}
            />
          </div>

          <span
            style={{
              fontSize: "0.85rem",
              fontWeight: 600,
              color: label.color,
              background: label.color + "18",
              padding: "3px 10px",
              borderRadius: "12px",
            }}
          >
            {label.label}
          </span>

          {score < 50 && (
            <p style={{ fontSize: "0.8rem", color: "#7f8c8d", marginTop: "10px" }}>
              Consider reducing project scope or adding more collaborators to improve your score.
            </p>
          )}

          <button
            onClick={fetchScore}
            style={{
              marginTop: "10px",
              background: "transparent",
              border: "1px solid #dde1e7",
              padding: "5px 10px",
              borderRadius: "4px",
              cursor: "pointer",
              fontSize: "0.8rem",
              color: "#555",
            }}
          >
            Refresh
          </button>
        </div>
      )}

      {error && <p style={{ color: "#e74c3c", fontSize: "0.85rem" }}>{error}</p>}
    </div>
  );
}
