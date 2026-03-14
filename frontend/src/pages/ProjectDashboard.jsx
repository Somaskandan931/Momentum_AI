import React from "react";
import { useParams, Link } from "react-router-dom";
import KanbanBoard from "../components/KanbanBoard";
import SurvivalScore from "../components/SurvivalScore";
import VoiceCommand from "../components/VoiceCommand";
import { useTasks } from "../hooks/useTasks";
import { generateSchedule } from "../services/scheduleService";

export default function ProjectDashboard() {
  const { projectId } = useParams();
  const { tasks, loading, updateTaskStatus, deleteTask } = useTasks(projectId);

  const handleGenerateSchedule = async () => {
    const taskIds = tasks.map((t) => t.id);
    try {
      await generateSchedule(projectId, taskIds);
      alert("Schedule generated. View in the Schedule tab.");
    } catch {
      alert("Failed to generate schedule.");
    }
  };

  const done = tasks.filter(t => t.status === "Completed").length;
  const pct = tasks.length > 0 ? Math.round((done / tasks.length) * 100) : 0;

  if (loading) return (
    <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-2)", fontSize: "14px" }}>
      <div style={{ marginBottom: "8px" }}>Loading tasks...</div>
    </div>
  );

  return (
    <div className="page fade-up">
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "2rem", gap: "1rem", flexWrap: "wrap" }}>
        <div>
          <h1 style={{ fontSize: "1.7rem", marginBottom: "4px" }}>Project Dashboard</h1>
          <p style={{ color: "var(--text-2)", fontSize: "14px" }}>
            {tasks.length} task{tasks.length !== 1 ? "s" : ""} · {pct}% complete
          </p>
        </div>

        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          <Link
            to={`/analytics/${projectId}`}
            style={{
              fontSize: "13px", fontWeight: 500,
              background: "var(--bg-card)", border: "1px solid var(--border)",
              color: "var(--text-2)", padding: "8px 16px",
              borderRadius: "8px", textDecoration: "none",
              transition: "all var(--transition)",
            }}
          >
            Analytics
          </Link>
          <Link
            to={`/collab/${projectId}`}
            style={{
              fontSize: "13px", fontWeight: 500,
              background: "var(--bg-card)", border: "1px solid var(--border)",
              color: "var(--text-2)", padding: "8px 16px",
              borderRadius: "8px", textDecoration: "none",
              transition: "all var(--transition)",
            }}
          >
            Team
          </Link>
          <button
            className="btn-primary"
            onClick={handleGenerateSchedule}
            style={{ padding: "8px 16px", fontSize: "13px" }}
          >
            Generate RL Schedule
          </button>
        </div>
      </div>

      {/* Progress bar */}
      <div style={{ marginBottom: "2rem" }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "11px", color: "var(--text-3)", marginBottom: "6px" }}>
          <span>PROGRESS</span>
          <span>{pct}%</span>
        </div>
        <div style={{ height: "4px", background: "var(--bg-card)", borderRadius: "2px", overflow: "hidden" }}>
          <div style={{
            width: `${pct}%`, height: "100%",
            background: "linear-gradient(90deg, var(--accent), #34d399)",
            borderRadius: "2px", transition: "width 0.5s ease",
          }} />
        </div>
      </div>

      {/* Main grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "1.5rem", alignItems: "start" }}>
        <KanbanBoard tasks={tasks} onStatusChange={updateTaskStatus} onDelete={deleteTask} />
        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <SurvivalScore projectId={projectId} />
          <VoiceCommand projectId={projectId} />
        </div>
      </div>
    </div>
  );
}