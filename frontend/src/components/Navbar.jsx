import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav
      style={{
        background: "#1a1a2e",
        color: "#fff",
        padding: "0 2rem",
        height: "56px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
        position: "sticky",
        top: 0,
        zIndex: 100,
      }}
    >
      <Link to="/dashboard" style={{ color: "#fff", textDecoration: "none", fontWeight: 700, fontSize: "1.1rem" }}>
        Momentum AI
      </Link>

      <div style={{ display: "flex", gap: "1.5rem", alignItems: "center" }}>
        <Link to="/dashboard" style={{ color: "#ccc", textDecoration: "none", fontSize: "0.9rem" }}>Dashboard</Link>
        <Link to="/schedule" style={{ color: "#ccc", textDecoration: "none", fontSize: "0.9rem" }}>Schedule</Link>
        <Link to="/analytics" style={{ color: "#ccc", textDecoration: "none", fontSize: "0.9rem" }}>Analytics</Link>
        <button
          onClick={handleLogout}
          style={{
            background: "transparent",
            border: "1px solid #555",
            color: "#ccc",
            padding: "5px 12px",
            borderRadius: "4px",
            cursor: "pointer",
            fontSize: "0.85rem",
          }}
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
