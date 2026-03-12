import React from "react";
import TaskCard from "./TaskCard";
import { groupTasksByStatus } from "../utils/helpers";

const COLUMNS = ["To Do", "In Progress", "Completed"];

export default function KanbanBoard({ tasks, onStatusChange, onDelete }) {
  const grouped = groupTasksByStatus(tasks);

  return (
    <div style={{ display: "flex", gap: "1.5rem", alignItems: "flex-start" }}>
      {COLUMNS.map((col) => (
        <div
          key={col}
          style={{
            flex: 1,
            background: "#f4f6f8",
            borderRadius: "8px",
            padding: "1rem",
            minHeight: "400px",
          }}
        >
          <h3 style={{ marginTop: 0, color: "#2c3e50", fontSize: "0.95rem", fontWeight: 600 }}>
            {col}
            <span
              style={{
                marginLeft: "8px",
                background: "#dde1e7",
                borderRadius: "12px",
                padding: "2px 8px",
                fontSize: "0.8rem",
              }}
            >
              {grouped[col]?.length || 0}
            </span>
          </h3>

          <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
            {(grouped[col] || []).map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onStatusChange={onStatusChange}
                onDelete={onDelete}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
