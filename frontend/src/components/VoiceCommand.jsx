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
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      mediaRecorder.onstop = handleStop;
      mediaRecorder.start();
      setRecording(true);
    } catch (err) {
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
    } catch (err) {
      setError("Failed to process voice command.");
    }
  };

  return (
    <div style={{ padding: "1rem", background: "#f8f9fa", borderRadius: "8px", maxWidth: "400px" }}>
      <h4 style={{ margin: "0 0 12px", color: "#2c3e50" }}>Voice Commands</h4>

      <button
        onClick={recording ? stopRecording : startRecording}
        style={{
          background: recording ? "#e74c3c" : "#2c3e50",
          color: "#fff",
          border: "none",
          padding: "10px 20px",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: 600,
          fontSize: "0.9rem",
          display: "flex",
          alignItems: "center",
          gap: "8px",
        }}
      >
        <span style={{ fontSize: "1rem" }}>{recording ? "■" : "●"}</span>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {recording && (
        <p style={{ color: "#e74c3c", fontSize: "0.85rem", marginTop: "8px" }}>
          Listening...
        </p>
      )}

      {transcript && (
        <div style={{ marginTop: "12px", fontSize: "0.85rem" }}>
          <strong>You said:</strong> {transcript}
        </div>
      )}

      {result && (
        <div style={{ marginTop: "8px", fontSize: "0.85rem", color: "#27ae60" }}>
          <strong>Action:</strong> {result.action} {result.title ? `— "${result.title}"` : ""}
        </div>
      )}

      {error && (
        <div style={{ marginTop: "8px", fontSize: "0.85rem", color: "#e74c3c" }}>
          {error}
        </div>
      )}

      <p style={{ fontSize: "0.75rem", color: "#95a5a6", marginTop: "12px", marginBottom: 0 }}>
        Try: "Add task write tests due tomorrow" · "Show today's schedule"
      </p>
    </div>
  );
}
