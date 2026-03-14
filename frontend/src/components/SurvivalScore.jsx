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
    } catch {
      setError("Could not compute score.");
    } finally {
      setLoading(false);
    }
  };

  const label = score !== null ? survivalScoreLabel(score) : null;
  const filled = score !== null ? Math.round(score) : 0;

  const arcColors = { Strong: "#34d399", Moderate: "#fbbf24", "At Risk": "#f87171" };
  const arcColor = label ? arcColors[label.label] : "var(--accent)";

  return (
    <div className="card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h4 style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-2)", letterSpacing: "0.04em", textTransform: "uppercase" }}>
          Survival Score
        </h4>
        {score !== null && (
          <button className="btn-ghost" onClick={fetchScore} style={{ padding: "4px 10px", fontSize: "11px" }}>
            Refresh
          </button>
        )}
      </div>

      {score === null ? (
        <div style={{ textAlign: "center", padding: "1rem 0" }}>
          <p style={{ fontSize: "12px", color: "var(--text-3)", marginBottom: "1rem" }}>
            AI analysis of your project's viability
          </p>
          <button
            className="btn-primary"
            onClick={fetchScore}
            disabled={loading}
            style={{ width: "100%", padding: "10px" }}
          >
            {loading ? "Analyzing..." : "Compute Score"}
          </button>
        </div>
      ) : (
        <div>
          {/* Score display */}
          <div style={{ display: "flex", alignItems: "baseline", gap: "6px", marginBottom: "10px" }}>
            <span style={{ fontSize: "3rem", fontWeight: 600, color: arcColor, letterSpacing: "-0.04em" }}>{filled}</span>
            <span style={{ fontSize: "14px", color: "var(--text-3)" }}>/100</span>
          </div>

          {/* Progress bar */}
          <div style={{ height: "4px", background: "var(--bg-input)", borderRadius: "2px", marginBottom: "10px", overflow: "hidden" }}>
            <div style={{
              width: `${filled}%`, height: "100%",
              background: arcColor, borderRadius: "2px",
              transition: "width 0.6s ease",
            }} />
          </div>

          <span style={{
            display: "inline-block", fontSize: "11px", fontWeight: 600,
            color: arcColor, background: `${arcColor}18`,
            padding: "3px 10px", borderRadius: "20px",
            textTransform: "uppercase", letterSpacing: "0.04em",
          }}>
            {label.label}
          </span>

          {score < 50 && (
            <p style={{ fontSize: "12px", color: "var(--text-3)", marginTop: "10px", lineHeight: 1.5 }}>
              Consider reducing scope or adding collaborators.
            </p>
          )}
        </div>
      )}

      {error && <p style={{ color: "var(--danger)", fontSize: "12px", marginTop: "8px" }}>{error}</p>}
    </div>
  );
}