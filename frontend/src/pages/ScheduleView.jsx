import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getSchedule } from "../services/scheduleService";
import { formatTime, formatDate } from "../utils/helpers";

export default function ScheduleView() {
  const { projectId } = useParams();
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSchedule(projectId)
      .then(({ data }) => setSchedule(data))
      .catch(() => setSchedule(null))
      .finally(() => setLoading(false));
  }, [projectId]);

  if (loading) return <p style={{ padding: "2rem" }}>Loading schedule...</p>;
  if (!schedule || !schedule.schedule_slots?.length)
    return (
      <div style={{ padding: "2rem" }}>
        <h2>Schedule</h2>
        <p style={{ color: "#7f8c8d" }}>No schedule generated yet. Go to the Dashboard and click "Generate RL Schedule".</p>
      </div>
    );

  return (
    <div style={{ padding: "2rem", maxWidth: "800px" }}>
      <h2 style={{ color: "#1a1a2e", marginBottom: "1.5rem" }}>
        AI-Generated Schedule
        {schedule.generated_by_rl && (
          <span style={{ fontSize: "0.75rem", background: "#8e44ad22", color: "#8e44ad", padding: "3px 10px", borderRadius: "12px", marginLeft: "12px", fontWeight: 500 }}>
            RL Optimized
          </span>
        )}
      </h2>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {schedule.schedule_slots.map((slot, i) => (
          <div
            key={i}
            style={{
              background: "#fff",
              border: "1px solid #dde1e7",
              borderRadius: "8px",
              padding: "1rem 1.25rem",
              display: "grid",
              gridTemplateColumns: "2fr 1fr 1fr",
              alignItems: "center",
              gap: "1rem",
            }}
          >
            <div>
              <div style={{ fontWeight: 600, color: "#2c3e50", fontSize: "0.9rem" }}>
                Task {i + 1}
              </div>
              <div style={{ fontSize: "0.78rem", color: "#95a5a6" }}>ID: {slot.task_id.slice(-8)}</div>
            </div>
            <div style={{ fontSize: "0.85rem", color: "#2c3e50" }}>
              <div>{formatDate(slot.start_time)}</div>
              <div style={{ color: "#7f8c8d" }}>{formatTime(slot.start_time)} – {formatTime(slot.end_time)}</div>
            </div>
            <div style={{ fontSize: "0.8rem", color: "#27ae60", fontWeight: 500 }}>
              {Math.round((new Date(slot.end_time) - new Date(slot.start_time)) / 60000)} min
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
