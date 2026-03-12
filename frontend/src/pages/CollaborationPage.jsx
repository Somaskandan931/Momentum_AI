import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getMembers, addMember } from "../services/projectService";

const ROLES = ["Project Lead", "Backend Developer", "Frontend Developer", "ML Engineer", "Researcher", "Designer", "Tester"];

export default function CollaborationPage() {
  const { projectId } = useParams();
  const [members, setMembers] = useState([]);
  const [roles, setRoles] = useState({});
  const [userId, setUserId] = useState("");
  const [role, setRole] = useState("Developer");
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
    } catch {
      setMessage("Failed to add member.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px" }}>
      <h2 style={{ color: "#1a1a2e" }}>Collaboration</h2>

      <div style={{ background: "#f8f9fa", borderRadius: "8px", padding: "1.25rem", marginBottom: "2rem" }}>
        <h4 style={{ margin: "0 0 12px" }}>Add Team Member</h4>
        <input
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="User ID"
          style={inputStyle}
        />
        <select value={role} onChange={(e) => setRole(e.target.value)} style={{ ...inputStyle, marginTop: "8px" }}>
          {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
        </select>
        <button onClick={handleAddMember} disabled={loading} style={btnStyle}>
          {loading ? "Adding..." : "Add Member"}
        </button>
        {message && <p style={{ fontSize: "0.85rem", color: "#27ae60", marginTop: "8px" }}>{message}</p>}
      </div>

      <h4 style={{ color: "#2c3e50" }}>Team Members ({members.length})</h4>
      {members.length === 0 ? (
        <p style={{ color: "#95a5a6" }}>No team members added yet.</p>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {members.map((uid) => (
            <div key={uid} style={{ background: "#fff", border: "1px solid #dde1e7", borderRadius: "6px", padding: "10px 14px", display: "flex", justifyContent: "space-between" }}>
              <span style={{ fontWeight: 500, fontSize: "0.9rem" }}>{uid}</span>
              <span style={{ fontSize: "0.8rem", color: "#8e44ad", background: "#f5eef8", padding: "2px 10px", borderRadius: "12px" }}>
                {roles[uid] || "Member"}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

const inputStyle = {
  width: "100%", padding: "9px 12px", border: "1px solid #dde1e7",
  borderRadius: "6px", fontSize: "0.9rem", boxSizing: "border-box", outline: "none",
};
const btnStyle = {
  marginTop: "10px", background: "#1a1a2e", color: "#fff", border: "none",
  padding: "9px 20px", borderRadius: "6px", cursor: "pointer", fontWeight: 600, fontSize: "0.9rem",
};
