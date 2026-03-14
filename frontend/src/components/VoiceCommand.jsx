import React, { useState, useRef } from "react";
import API from "../services/api";

export default function VoiceCommand({ projectId, onCommandExecuted }) {
  const [recording, setRecording] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const startRecording = async () => {
    setError(null);
    setResult(null);
    setTranscript("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];
      mediaRecorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      mediaRecorder.onstop = handleStop;
      mediaRecorder.start();
      setRecording(true);
    } catch {
      setError("Microphone access denied.");
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  };

  const handleStop = async () => {
    const blob = new Blob(chunksRef.current, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", blob, "command.webm");
    formData.append("project_id", projectId);
    try {
      const { data } = await API.post("/voice/command", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setTranscript(data.transcript);
      setResult(data.action);
      if (onCommandExecuted) onCommandExecuted(data);
    } catch {
      setError("Failed to process voice command.");
    }
  };

  return (
    <div className="card">
      <h4 style={{ fontSize: "12px", fontWeight: 600, color: "var(--text-2)", letterSpacing: "0.04em", textTransform: "uppercase", marginBottom: "1rem" }}>
        Voice Commands
      </h4>

      <button
        onClick={recording ? stopRecording : startRecording}
        style={{
          width: "100%", padding: "10px",
          background: recording ? "rgba(248,113,113,0.15)" : "var(--bg-input)",
          color: recording ? "var(--danger)" : "var(--text-2)",
          border: `1px solid ${recording ? "rgba(248,113,113,0.4)" : "var(--border)"}`,
          borderRadius: "8px", cursor: "pointer", fontSize: "13px", fontWeight: 500,
          display: "flex", alignItems: "center", justifyContent: "center", gap: "8px",
          transition: "all var(--transition)",
        }}
      >
        <span style={{
          width: "8px", height: "8px", borderRadius: "50%",
          background: recording ? "var(--danger)" : "var(--text-3)",
          animation: recording ? "pulse 1s ease infinite" : "none",
        }} />
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {recording && (
        <p style={{ color: "var(--danger)", fontSize: "12px", marginTop: "8px", textAlign: "center" }}>
          Listening...
        </p>
      )}

      {transcript && (
        <div style={{ marginTop: "10px", background: "var(--bg-input)", borderRadius: "8px", padding: "8px 12px" }}>
          <p style={{ fontSize: "11px", color: "var(--text-3)", marginBottom: "3px" }}>YOU SAID</p>
          <p style={{ fontSize: "13px", color: "var(--text)" }}>{transcript}</p>
        </div>
      )}

      {result && (
        <div style={{ marginTop: "8px", background: "rgba(52,211,153,0.1)", border: "1px solid rgba(52,211,153,0.2)", borderRadius: "8px", padding: "8px 12px" }}>
          <p style={{ fontSize: "11px", color: "#34d399", marginBottom: "3px" }}>ACTION</p>
          <p style={{ fontSize: "13px", color: "var(--text)" }}>
            {result.action}{result.title ? ` — "${result.title}"` : ""}
          </p>
        </div>
      )}

      {error && <p style={{ color: "var(--danger)", fontSize: "12px", marginTop: "8px" }}>{error}</p>}

      <p style={{ fontSize: "11px", color: "var(--text-3)", marginTop: "10px", lineHeight: 1.5 }}>
        Try: "Add task write tests" · "Show today's schedule"
      </p>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </div>
  );
}