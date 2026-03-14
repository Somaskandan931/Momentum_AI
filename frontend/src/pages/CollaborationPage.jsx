import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getMembers, addMember } from "../services/projectService";

const ROLES = ["Project Lead", "Backend Developer", "Frontend Developer", "ML Engineer", "Researcher", "Designer", "Tester"];

const roleColors = {
  "Project Lead": "#7c6dfa",
  "Backend Developer": "#34d399",
  "Frontend Developer": "#60a5fa",
  "ML Engineer": "#f472b6",
  "Researcher": "#fbbf24",
  "Designer": "#a78bfa",
  "Tester": "#fb923c",
};

export default function CollaborationPage() {
  const { projectId } = useParams();
  const [members, setMembers] = useState([]);
  const [roles, setRoles] = useState({});
  const [userId, setUserId] = useState("");
  const [role, setRole] = useState("Backend Developer");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getMembers(projectId).then(({ data }) => {
      setMembers(data.team_members || []);
      setRoles(data.roles || {});
    });
  }, [projectId]);

  const handleAddMember = async () => {
    if (!userId.trim()) return;
    setLoading(true);
    try {
      await addMember(projectId, userId.trim(), role);
      setMembers((prev) => [...prev, userId.trim()]);
      setRoles((prev) => ({ ...prev, [userId.trim()]: role }));
      setMessage(`Added ${userId} as ${role}`);
      setUserId("");
      setTimeout(() => setMessage(""), 3000);
    } catch {
      setMessage("Failed to add member.");
    } finally {
      setLoading(false);
    }
  };

  const initials = (uid) => uid.slice(0, 2).toUpperCase();

  return (
    <div className="page fade-up" style={{ maxWidth: "700px" }}>
      <h2 style={{ marginBottom: "0.5rem" }}>Team</h2>
      <p style={{ color: "var(--text-2)", marginBottom: "2rem", fontSize: "14px" }}>Manage collaborators and roles</p>

      {/* Add member card */}
      <div className="card" style={{ marginBottom: "1.5rem" }}>
        <h4 style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-2)", letterSpacing: "0.04em", textTransform: "uppercase", marginBottom: "1rem" }}>
          Add Member
        </h4>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", marginBottom: "10px" }}>
          <input
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="User ID or email"
            onKeyDown={(e) => e.key === "Enter" && handleAddMember()}
          />
          <select value={role} onChange={(e) => setRole(e.target.value)}
            style={{ background: "var(--bg-input)", border: "1px solid var(--border)", color: "var(--text)", borderRadius: "var(--radius)", padding: "10px 14px", fontSize: "14px" }}>
            {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
          </select>
        </div>
        <button className="btn-primary" onClick={handleAddMember} disabled={loading} style={{ padding: "10px 20px" }}>
          {loading ? "Adding..." : "Add Member"}
        </button>
        {message && (
          <p style={{ fontSize: "13px", color: "#34d399", marginTop: "8px" }}>{message}</p>
        )}
      </div>

      {/* Members list */}
      <div>
        <p style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-3)", letterSpacing: "0.04em", textTransform: "uppercase", marginBottom: "12px" }}>
          Team Members ({members.length})
        </p>
        {members.length === 0 ? (
          <div style={{
            border: "1px dashed var(--border)", borderRadius: "var(--radius-lg)",
            padding: "2rem", textAlign: "center", color: "var(--text-3)", fontSize: "13px",
          }}>
            No team members yet. Add someone above.
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {members.map((uid) => {
              const r = roles[uid] || "Member";
              const color = roleColors[r] || "var(--accent)";
              return (
                <div key={uid} className="card" style={{ padding: "12px 16px", display: "flex", alignItems: "center", gap: "12px" }}>
                  <div style={{
                    width: "36px", height: "36px", borderRadius: "50%",
                    background: `${color}20`, border: `1px solid ${color}40`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: "12px", fontWeight: 600, color, flexShrink: 0,
                  }}>
                    {initials(uid)}
                  </div>
                  <span style={{ fontWeight: 500, fontSize: "14px", flex: 1 }}>{uid}</span>
                  <span style={{
                    fontSize: "11px", fontWeight: 600, padding: "3px 10px",
                    borderRadius: "20px", background: `${color}18`,
                    color, letterSpacing: "0.03em",
                  }}>
                    {r}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}