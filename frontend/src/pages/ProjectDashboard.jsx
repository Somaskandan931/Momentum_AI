import React from "react";
import { useParams } from "react-router-dom";
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

  if (loading) return <p style={{ padding: "2rem" }}>Loading tasks...</p>;

  return (
    <div style={{ padding: "2rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "2rem", flexWrap: "wrap", gap: "1rem" }}>
        <div>
          <h1 style={{ margin: 0, color: "#1a1a2e" }}>Project Dashboard</h1>
          <p style={{ color: "#7f8c8d", marginTop: "4px" }}>
            {tasks.length} task{tasks.length !== 1 ? "s" : ""} total
          </p>
        </div>

        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <button
            onClick={handleGenerateSchedule}
            style={btnStyle}
          >
            Generate RL Schedule
          </button>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: "2rem", alignItems: "start" }}>
        <KanbanBoard
          tasks={tasks}
          onStatusChange={updateTaskStatus}
          onDelete={deleteTask}
        />

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          <SurvivalScore projectId={projectId} />
          <VoiceCommand projectId={projectId} />
        </div>
      </div>
    </div>
  );
}

const btnStyle = {
  background: "#1a1a2e",
  color: "#fff",
  border: "none",
  padding: "10px 18px",
  borderRadius: "6px",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.9rem",
};
