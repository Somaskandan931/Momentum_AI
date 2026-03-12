import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";
import { useTasks } from "../hooks/useTasks";

const COLORS = ["#3498db", "#f39c12", "#27ae60"];

export default function AnalyticsPage() {
  const { projectId } = useParams();
  const { tasks } = useTasks(projectId);

  const statusData = [
    { name: "To Do",       value: tasks.filter(t => t.status === "To Do").length },
    { name: "In Progress", value: tasks.filter(t => t.status === "In Progress").length },
    { name: "Completed",   value: tasks.filter(t => t.status === "Completed").length },
  ];

  const priorityData = [
    { name: "High",   count: tasks.filter(t => t.priority === "high").length },
    { name: "Medium", count: tasks.filter(t => t.priority === "medium").length },
    { name: "Low",    count: tasks.filter(t => t.priority === "low").length },
  ];

  const completionRate = tasks.length > 0
    ? Math.round((tasks.filter(t => t.status === "Completed").length / tasks.length) * 100)
    : 0;

  return (
    <div style={{ padding: "2rem" }}>
      <h2 style={{ color: "#1a1a2e", marginBottom: "2rem" }}>Project Analytics</h2>

      {/* Summary cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem", marginBottom: "2.5rem" }}>
        {[
          { label: "Total Tasks", value: tasks.length, color: "#3498db" },
          { label: "Completion Rate", value: `${completionRate}%`, color: "#27ae60" },
          { label: "In Progress", value: tasks.filter(t => t.status === "In Progress").length, color: "#f39c12" },
        ].map(({ label, value, color }) => (
          <div key={label} style={{ background: "#fff", border: "1px solid #dde1e7", borderRadius: "8px", padding: "1.25rem" }}>
            <div style={{ fontSize: "0.85rem", color: "#7f8c8d", marginBottom: "6px" }}>{label}</div>
            <div style={{ fontSize: "2rem", fontWeight: 700, color }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "2rem" }}>
        <div style={{ background: "#fff", border: "1px solid #dde1e7", borderRadius: "8px", padding: "1.25rem" }}>
          <h4 style={{ margin: "0 0 1rem", color: "#2c3e50" }}>Tasks by Priority</h4>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={priorityData}>
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#1a1a2e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ background: "#fff", border: "1px solid #dde1e7", borderRadius: "8px", padding: "1.25rem" }}>
          <h4 style={{ margin: "0 0 1rem", color: "#2c3e50" }}>Tasks by Status</h4>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={statusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {statusData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Legend />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
