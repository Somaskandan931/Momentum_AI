import React from "react";
import { useParams } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";
import { useTasks } from "../hooks/useTasks";

const COLORS = ["#9490a8", "#7c6dfa", "#34d399"];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: "var(--bg-card)", border: "1px solid var(--border)",
        borderRadius: "8px", padding: "8px 12px", fontSize: "13px",
      }}>
        <p style={{ color: "var(--text-2)", marginBottom: "2px" }}>{label}</p>
        <p style={{ color: "var(--text)", fontWeight: 500 }}>{payload[0].value} tasks</p>
      </div>
    );
  }
  return null;
};

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

  const stats = [
    { label: "Total Tasks", value: tasks.length, color: "var(--text)" },
    { label: "Completed", value: tasks.filter(t => t.status === "Completed").length, color: "#34d399" },
    { label: "In Progress", value: tasks.filter(t => t.status === "In Progress").length, color: "#fbbf24" },
    { label: "Completion Rate", value: `${completionRate}%`, color: "var(--accent)" },
  ];

  return (
    <div className="page fade-up">
      <h2 style={{ marginBottom: "0.5rem" }}>Analytics</h2>
      <p style={{ color: "var(--text-2)", marginBottom: "2rem", fontSize: "14px" }}>Project performance overview</p>

      {/* Stats */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "1rem", marginBottom: "2rem" }}>
        {stats.map(({ label, value, color }) => (
          <div key={label} className="card" style={{ padding: "1.25rem" }}>
            <p style={{ fontSize: "11px", fontWeight: 600, color: "var(--text-3)", letterSpacing: "0.05em", textTransform: "uppercase", marginBottom: "8px" }}>{label}</p>
            <p style={{ fontSize: "2rem", fontWeight: 600, color, letterSpacing: "-0.03em" }}>{value}</p>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
        <div className="card">
          <h4 style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-2)", marginBottom: "1.25rem", letterSpacing: "0.03em", textTransform: "uppercase" }}>
            Tasks by Priority
          </h4>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={priorityData} barCategoryGap="35%">
              <XAxis dataKey="name" tick={{ fill: "var(--text-3)", fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis allowDecimals={false} tick={{ fill: "var(--text-3)", fontSize: 12 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: "rgba(124,109,250,0.05)" }} />
              <Bar dataKey="count" fill="var(--accent)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h4 style={{ fontSize: "13px", fontWeight: 600, color: "var(--text-2)", marginBottom: "1.25rem", letterSpacing: "0.03em", textTransform: "uppercase" }}>
            Tasks by Status
          </h4>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={statusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={75} innerRadius={35} paddingAngle={3}>
                {statusData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Legend wrapperStyle={{ fontSize: "12px", color: "var(--text-2)" }} />
              <Tooltip
                contentStyle={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: "8px", fontSize: "13px" }}
                itemStyle={{ color: "var(--text)" }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}