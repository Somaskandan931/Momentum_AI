import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import IdeaSubmission from "./pages/IdeaSubmission";
import ProjectDashboard from "./pages/ProjectDashboard";
import ScheduleView from "./pages/ScheduleView";
import CollaborationPage from "./pages/CollaborationPage";
import AnalyticsPage from "./pages/AnalyticsPage";

const isAuthenticated = () => !!localStorage.getItem("token");

function PrivateRoute({ children }) {
  return isAuthenticated() ? children : <Navigate to="/login" />;
}

function LoginPage() {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState("");

  const handleLogin = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
      });
      const data = await res.json();
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/submit";
      } else {
        setError("Invalid credentials");
      }
    } catch {
      setError("Login failed. Is the backend running?");
    }
  };

  return (
    <div style={{ maxWidth: "380px", margin: "5rem auto", padding: "2rem", border: "1px solid #dde1e7", borderRadius: "8px" }}>
      <h2 style={{ marginTop: 0, color: "#1a1a2e" }}>Momentum AI</h2>
      <input value={email} onChange={e => setEmail(e.target.value)} placeholder="Email" style={inp} />
      <input value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" type="password" style={{ ...inp, marginTop: "10px" }} />
      {error && <p style={{ color: "#e74c3c", fontSize: "0.85rem" }}>{error}</p>}
      <button onClick={handleLogin} style={{ background: "#1a1a2e", color: "#fff", border: "none", padding: "10px 24px", borderRadius: "6px", cursor: "pointer", marginTop: "12px", fontWeight: 600, width: "100%" }}>
        Login
      </button>
    </div>
  );
}

const inp = { width: "100%", padding: "9px 12px", border: "1px solid #dde1e7", borderRadius: "6px", fontSize: "0.95rem", boxSizing: "border-box" };

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/*" element={
          <PrivateRoute>
            <>
              <Navbar />
              <Routes>
                <Route path="/submit" element={<IdeaSubmission />} />
                <Route path="/dashboard/:projectId" element={<ProjectDashboard />} />
                <Route path="/schedule/:projectId" element={<ScheduleView />} />
                <Route path="/collab/:projectId" element={<CollaborationPage />} />
                <Route path="/analytics/:projectId" element={<AnalyticsPage />} />
                <Route path="*" element={<Navigate to="/submit" />} />
              </Routes>
            </>
          </PrivateRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}
