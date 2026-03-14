import React from "react";
import TaskCard from "./TaskCard";
import { groupTasksByStatus } from "../utils/helpers";

const COLUMNS = [
  { key: "To Do",       accent: "rgba(148,144,168,0.5)", dot: "#5c586e" },
  { key: "In Progress", accent: "rgba(251,191,36,0.4)",  dot: "#fbbf24" },
  { key: "Completed",   accent: "rgba(52,211,153,0.4)",  dot: "#34d399" },
];

export default function KanbanBoard({ tasks, onStatusChange, onDelete }) {
  const grouped = groupTasksByStatus(tasks);

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem", alignItems: "flex-start" }}>
      {COLUMNS.map(({ key, accent, dot }) => (
        <div key={key} style={{
          background: "var(--bg-card)",
          border: "1px solid var(--border)",
          borderRadius: "var(--radius-lg)",
          padding: "1rem",
          minHeight: "420px",
        }}>
          {/* Column header */}
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "1rem" }}>
            <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: dot, flexShrink: 0 }} />
            <span style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-2)", letterSpacing: "0.04em", textTransform: "uppercase", flex: 1 }}>
              {key}
            </span>
            <span style={{
              fontSize: "11px", fontWeight: 600,
              background: "var(--bg-input)", border: "1px solid var(--border)",
              color: "var(--text-3)", borderRadius: "20px", padding: "1px 8px",
            }}>
              {grouped[key]?.length || 0}
            </span>
          </div>

          {/* Drop zone line */}
          <div style={{ height: "1px", background: `linear-gradient(to right, ${accent}, transparent)`, marginBottom: "1rem" }} />

          <div style={{ display: "flex", flexDirection: "column", gap: "0.6rem" }}>
            {(grouped[key] || []).length === 0 ? (
              <div style={{
                border: "1px dashed var(--border)",
                borderRadius: "10px", padding: "2rem",
                textAlign: "center", color: "var(--text-3)", fontSize: "12px",
              }}>
                No tasks
              </div>
            ) : (
              (grouped[key] || []).map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onStatusChange={onStatusChange}
                  onDelete={onDelete}
                />
              ))
            )}
          </div>
        </div>
      ))}
    </div>
  );
}