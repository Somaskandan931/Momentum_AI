import React from "react";
import { priorityColor, formatDate } from "../utils/helpers";

const STATUS_OPTIONS = ["To Do", "In Progress", "Completed"];

export default function TaskCard({ task, onStatusChange, onDelete }) {
  return (
    <div
      style={{
        background: "#fff",
        borderRadius: "6px",
        padding: "0.75rem 1rem",
        boxShadow: "0 1px 3px rgba(0,0,0,0.08)",
        borderLeft: `4px solid ${priorityColor(task.priority)}`,
      }}
    >
      <div style={{ fontWeight: 600, fontSize: "0.9rem", color: "#2c3e50", marginBottom: "4px" }}>
        {task.title}
      </div>

      {task.description && (
        <p style={{ fontSize: "0.8rem", color: "#7f8c8d", margin: "0 0 8px" }}>
          {task.description}
        </p>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "6px" }}>
        <span
          style={{
            fontSize: "0.75rem",
            background: priorityColor(task.priority) + "22",
            color: priorityColor(task.priority),
            padding: "2px 8px",
            borderRadius: "12px",
            fontWeight: 500,
          }}
        >
          {task.priority}
        </span>

        {task.deadline && (
          <span style={{ fontSize: "0.75rem", color: "#95a5a6" }}>
            Due: {formatDate(task.deadline)}
          </span>
        )}

        {task.created_by_ai && (
          <span style={{ fontSize: "0.7rem", color: "#8e44ad", background: "#f5eef8", padding: "2px 6px", borderRadius: "8px" }}>
            AI
          </span>
        )}
      </div>

      <div style={{ marginTop: "10px", display: "flex", gap: "6px", flexWrap: "wrap" }}>
        {STATUS_OPTIONS.filter((s) => s !== task.status).map((s) => (
          <button
            key={s}
            onClick={() => onStatusChange(task.id, s)}
            style={{
              fontSize: "0.72rem",
              padding: "3px 8px",
              border: "1px solid #dde1e7",
              borderRadius: "4px",
              cursor: "pointer",
              background: "#fff",
              color: "#2c3e50",
            }}
          >
            Move to {s}
          </button>
        ))}
        <button
          onClick={() => onDelete(task.id)}
          style={{
            fontSize: "0.72rem",
            padding: "3px 8px",
            border: "1px solid #e74c3c33",
            borderRadius: "4px",
            cursor: "pointer",
            background: "#fff",
            color: "#e74c3c",
          }}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
