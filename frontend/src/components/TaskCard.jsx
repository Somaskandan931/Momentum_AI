import React from "react";
import { priorityColor, formatDate } from "../utils/helpers";

const STATUS_OPTIONS = ["To Do", "In Progress", "Completed"];

const priorityDot = (priority) => {
  const colors = { high: "#f87171", medium: "#fbbf24", low: "#34d399" };
  return colors[priority] || "#9490a8";
};

export default function TaskCard({ task, onStatusChange, onDelete }) {
  const dot = priorityDot(task.priority);

  return (
    <div style={{
      background: "var(--bg)",
      border: "1px solid var(--border)",
      borderRadius: "10px",
      padding: "0.875rem 1rem",
      transition: "border-color var(--transition), transform var(--transition)",
      cursor: "default",
      borderLeft: `3px solid ${dot}`,
    }}
    onMouseEnter={e => e.currentTarget.style.borderColor = "var(--border-hover)"}
    onMouseLeave={e => e.currentTarget.style.borderLeft = `3px solid ${dot}`}
    >
      {/* Title row */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "8px", marginBottom: "6px" }}>
        <span style={{ fontWeight: 500, fontSize: "13px", color: "var(--text)", lineHeight: 1.4 }}>
          {task.title}
        </span>
        {task.created_by_ai && (
          <span style={{
            fontSize: "10px", fontWeight: 600, padding: "2px 7px",
            borderRadius: "20px", background: "rgba(124,109,250,0.15)",
            color: "var(--accent)", letterSpacing: "0.04em", textTransform: "uppercase",
            whiteSpace: "nowrap", flexShrink: 0,
          }}>
            AI
          </span>
        )}
      </div>

      {task.description && (
        <p style={{ fontSize: "12px", color: "var(--text-2)", marginBottom: "10px", lineHeight: 1.5 }}>
          {task.description}
        </p>
      )}

      {/* Meta row */}
      <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "10px", flexWrap: "wrap" }}>
        <span style={{ display: "flex", alignItems: "center", gap: "4px", fontSize: "11px", color: "var(--text-2)" }}>
          <span style={{ width: "6px", height: "6px", borderRadius: "50%", background: dot, display: "inline-block" }} />
          {task.priority}
        </span>
        {task.deadline && (
          <span style={{ fontSize: "11px", color: "var(--text-3)" }}>
            Due {formatDate(task.deadline)}
          </span>
        )}
        {task.estimated_time && (
          <span style={{ fontSize: "11px", color: "var(--text-3)" }}>
            ~{task.estimated_time}m
          </span>
        )}
      </div>

      {/* Actions */}
      <div style={{ display: "flex", gap: "5px", flexWrap: "wrap" }}>
        {STATUS_OPTIONS.filter((s) => s !== task.status).map((s) => (
          <button
            key={s}
            onClick={() => onStatusChange(task.id, s)}
            style={{
              fontSize: "11px", padding: "3px 9px",
              border: "1px solid var(--border)",
              borderRadius: "6px", cursor: "pointer",
              background: "var(--bg-input)", color: "var(--text-2)",
              transition: "all var(--transition)",
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = "var(--accent)"; e.currentTarget.style.color = "var(--accent)"; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = "var(--border)"; e.currentTarget.style.color = "var(--text-2)"; }}
          >
            → {s}
          </button>
        ))}
        <button
          onClick={() => onDelete(task.id)}
          style={{
            fontSize: "11px", padding: "3px 9px",
            border: "1px solid transparent",
            borderRadius: "6px", cursor: "pointer",
            background: "transparent", color: "var(--text-3)",
            marginLeft: "auto", transition: "all var(--transition)",
          }}
          onMouseEnter={e => { e.currentTarget.style.color = "var(--danger)"; e.currentTarget.style.borderColor = "rgba(248,113,113,0.3)"; }}
          onMouseLeave={e => { e.currentTarget.style.color = "var(--text-3)"; e.currentTarget.style.borderColor = "transparent"; }}
        >
          Delete
        </button>
      </div>
    </div>
  );
}