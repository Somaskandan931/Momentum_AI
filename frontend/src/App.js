import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import IdeaSubmission from "./pages/IdeaSubmission";
import ProjectDashboard from "./pages/ProjectDashboard";
import ScheduleView from "./pages/ScheduleView";
import CollaborationPage from "./pages/CollaborationPage";
import AnalyticsPage from "./pages/AnalyticsPage";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: "100vh", background: "var(--bg)", color: "var(--text)" }}>
        <Navbar />
        <Routes>
          <Route path="/" element={<Navigate to="/submit" />} />
          <Route path="/submit" element={<IdeaSubmission />} />
          <Route path="/dashboard/:projectId" element={<ProjectDashboard />} />
          <Route path="/schedule/:projectId" element={<ScheduleView />} />
          <Route path="/collab/:projectId" element={<CollaborationPage />} />
          <Route path="/analytics/:projectId" element={<AnalyticsPage />} />
          <Route path="*" element={<Navigate to="/submit" />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}