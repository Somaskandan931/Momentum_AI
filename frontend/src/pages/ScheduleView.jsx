import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { getSchedule } from "../services/scheduleService";
import { formatTime, formatDate } from "../utils/helpers";
import API from "../services/api";

export default function ScheduleView() {
  const { projectId } = useParams();
  const [schedule, setSchedule] = useState(null);
  const [tasks, setTasks]       = useState({});   // map of id → task
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        // Fetch schedule and tasks in parallel
        const [schedRes, taskRes] = await Promise.all([
          getSchedule(projectId),
          API.get(`/tasks/project/${projectId}`),
        ]);

        const scheduleData = schedRes.data;
        const tasksData    = taskRes.data;

        // Build a quick lookup map: task id → task object
        const taskMap = {};
        (tasksData || []).forEach((t) => { taskMap[t.id] = t; });

        setSchedule(scheduleData && Object.keys(scheduleData).length ? scheduleData : null);
        setTasks(taskMap);
      } catch (err) {
        setError("Failed to load schedule.");
        setSchedule(null);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [projectId]);

  // ── Loading ────────────────────────────────────────────────────────────────
  if (loading) return (
    <div style={{ padding: "3rem", textAlign: "center", color: "var(--text-2)", fontSize: "14px" }}>
      Loading schedule...
    </div>
  );

  // ── Error ──────────────────────────────────────────────────────────────────
  if (error) return (
    <div className="page fade-up" style={{ maxWidth: "600px" }}>
      <h2 style={{ marginBottom: "0.5rem" }}>Schedule</h2>
      <div className="card" style={{ marginTop: "2rem", textAlign: "center", padding: "3rem" }}>
        <div style={{ fontSize: "2rem", marginBottom: "1rem" }}>⚠️</div>
        <p style={{ color: "var(--danger)", marginBottom: "1.5rem" }}>{error}</p>
        <Link to={`/dashboard/${projectId}`} className="btn-primary"
          style={{ display: "inline-block", padding: "10px 20px", textDecoration: "none" }}>
          Back to Dashboard
        </Link>
      </div>
    </div>
  );

  // ── Empty state ────────────────────────────────────────────────────────────
  if (!schedule || !schedule.schedule_slots?.length) return (
    <div className="page fade-up" style={{ maxWidth: "600px" }}>
      <h2 style={{ marginBottom: "0.5rem" }}>Schedule</h2>
      <div className="card" style={{ marginTop: "2rem", textAlign: "center", padding: "3rem" }}>
        <div style={{ fontSize: "2rem", marginBottom: "1rem" }}>📅</div>
        <p style={{ color: "var(--text-2)", marginBottom: "1.5rem", lineHeight: 1.6 }}>
          No schedule generated yet.<br />
          Go to the Dashboard and click <strong>"Generate RL Schedule"</strong>.
        </p>
        <Link to={`/dashboard/${projectId}`} className="btn-primary"
          style={{ display: "inline-block", padding: "10px 20px", textDecoration: "none" }}>
          Go to Dashboard
        </Link>
      </div>
    </div>
  );

  // ── Schedule view ──────────────────────────────────────────────────────────
  return (
    <div className="page fade-up" style={{ maxWidth: "800px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "0.5rem" }}>
        <h2>AI-Generated Schedule</h2>
        {schedule.generated_by_rl && (
          <span style={{
            fontSize: "10px", fontWeight: 700, padding: "3px 10px",
            borderRadius: "20px", background: "rgba(124,109,250,0.15)",
            color: "var(--accent)", letterSpacing: "0.06em", textTransform: "uppercase",
          }}>
            RL Optimised
          </span>
        )}
      </div>
      <p style={{ color: "var(--text-2)", marginBottom: "2rem", fontSize: "14px" }}>
        {schedule.schedule_slots.length} task{schedule.schedule_slots.length !== 1 ? "s" : ""} scheduled
      </p>

      {/* Slot list */}
      <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
        {schedule.schedule_slots.map((slot, i) => {
          const durationMin = Math.round(
            (new Date(slot.end_time) - new Date(slot.start_time)) / 60000
          );
          const task = tasks[slot.task_id];
          const priorityColors = { high: "#f87171", medium: "#fbbf24", low: "#34d399" };
          const priorityColor  = task ? (priorityColors[task.priority] || "var(--text-3)") : "var(--text-3)";

          return (
            <div
              key={i}
              className="card"
              style={{
                padding: "1rem 1.25rem",
                display: "grid",
                gridTemplateColumns: "auto 1fr auto auto",
                alignItems: "center",
                gap: "1rem",
                borderLeft: `3px solid ${priorityColor}`,
              }}
            >
              {/* Index badge */}
              <div style={{
                width: "32px", height: "32px", borderRadius: "8px",
                background: "var(--accent-dim)", border: "1px solid rgba(124,109,250,0.3)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: "13px", fontWeight: 600, color: "var(--accent)", flexShrink: 0,
              }}>
                {i + 1}
              </div>

              {/* Task info */}
              <div>
                <p style={{ fontWeight: 500, fontSize: "13px", marginBottom: "2px" }}>
                  {task ? task.title : "Task"}
                </p>
                <p style={{ fontSize: "11px", color: "var(--text-3)", fontFamily: "var(--font-mono)" }}>
                  {task?.priority && (
                    <span style={{ color: priorityColor, marginRight: "8px", textTransform: "uppercase" }}>
                      {task.priority}
                    </span>
                  )}
                  ID: {slot.task_id.slice(-8)}
                </p>
              </div>

              {/* Date / time */}
              <div style={{ textAlign: "right" }}>
                <p style={{ fontSize: "13px", color: "var(--text-2)" }}>
                  {formatDate(slot.start_time)}
                </p>
                <p style={{ fontSize: "11px", color: "var(--text-3)" }}>
                  {formatTime(slot.start_time)} – {formatTime(slot.end_time)}
                </p>
              </div>

              {/* Duration pill */}
              <div style={{
                fontSize: "12px", fontWeight: 600, color: "#34d399",
                background: "rgba(52,211,153,0.1)", border: "1px solid rgba(52,211,153,0.2)",
                padding: "4px 10px", borderRadius: "20px", whiteSpace: "nowrap",
              }}>
                {durationMin}m
              </div>
            </div>
          );
        })}
      </div>

      {/* Back link */}
      <div style={{ marginTop: "2rem" }}>
        <Link
          to={`/dashboard/${projectId}`}
          style={{ fontSize: "13px", color: "var(--text-2)" }}
        >
          ← Back to Dashboard
        </Link>
      </div>
    </div>
  );
}