import React from "react";
import { Link, useLocation, useParams } from "react-router-dom";

const Logo = () => (
  <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
    <rect width="22" height="22" rx="6" fill="#7c6dfa"/>
    <path d="M6 16L11 6L16 16" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M8 13h6" stroke="white" strokeWidth="1.8" strokeLinecap="round"/>
  </svg>
);

export default function Navbar() {
  const location = useLocation();

  // Extract projectId from any route that contains one
  // e.g. /dashboard/:id  /schedule/:id  /collab/:id  /analytics/:id
  const projectIdMatch = location.pathname.match(
    /\/(dashboard|schedule|collab|analytics)\/([^/]+)/
  );
  const projectId = projectIdMatch ? projectIdMatch[2] : null;

  // Build nav links — only include project-scoped links when we have an id
  const navLinks = [
    { to: "/submit",                                    label: "New Idea",  always: true  },
    { to: projectId ? `/dashboard/${projectId}` : null, label: "Dashboard", always: false },
    { to: projectId ? `/schedule/${projectId}`  : null, label: "Schedule",  always: false },
    { to: projectId ? `/analytics/${projectId}` : null, label: "Analytics", always: false },
  ].filter((l) => l.always || l.to !== null);

  return (
    <nav style={{
      background: "rgba(13,13,18,0.85)",
      backdropFilter: "blur(20px)",
      WebkitBackdropFilter: "blur(20px)",
      borderBottom: "1px solid var(--border)",
      height: "56px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 2rem",
      position: "sticky",
      top: 0,
      zIndex: 100,
    }}>
      <Link to="/submit" style={{
        display: "flex",
        alignItems: "center",
        gap: "10px",
        color: "var(--text)",
        textDecoration: "none",
      }}>
        <Logo />
        <span style={{ fontWeight: 600, fontSize: "15px", letterSpacing: "-0.02em" }}>
          Momentum <span style={{ color: "var(--accent)" }}>AI</span>
        </span>
      </Link>

      <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
        {navLinks.map(({ to, label }) => {
          const active = location.pathname.startsWith(
            to.replace(/\/[^/]+$/, (m) =>
              m.match(/^\/[a-f0-9]{24}$/) ? "" : m          // strip ObjectId so startsWith works
            )
          );
          const isActive = (() => {
            if (label === "New Idea")   return location.pathname === "/submit";
            if (label === "Dashboard")  return location.pathname.startsWith("/dashboard");
            if (label === "Schedule")   return location.pathname.startsWith("/schedule");
            if (label === "Analytics")  return location.pathname.startsWith("/analytics");
            return false;
          })();

          return (
            <Link
              key={label}
              to={to}
              style={{
                fontSize: "13px",
                fontWeight: 500,
                color: isActive ? "var(--text)" : "var(--text-2)",
                background: isActive ? "var(--bg-hover)" : "transparent",
                padding: "6px 12px",
                borderRadius: "8px",
                transition: "all var(--transition)",
                textDecoration: "none",
                border: isActive ? "1px solid var(--border)" : "1px solid transparent",
              }}
              onMouseEnter={e => { if (!isActive) e.currentTarget.style.color = "var(--text)"; }}
              onMouseLeave={e => { if (!isActive) e.currentTarget.style.color = "var(--text-2)"; }}
            >
              {label}
            </Link>
          );
        })}
      </div>

      <div style={{
        width: "32px",
        height: "32px",
        borderRadius: "50%",
        background: "var(--accent-dim)",
        border: "1px solid var(--accent)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: "13px",
        fontWeight: 600,
        color: "var(--accent)",
      }}>
        U
      </div>
    </nav>
  );
}