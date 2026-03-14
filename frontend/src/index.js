import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

/* ── Global Design Tokens ─────────────────────────────────── */
const style = document.createElement("style");
style.textContent = `
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:           #0d0d12;
    --bg-card:      #13131a;
    --bg-hover:     #1a1a24;
    --bg-input:     #1e1e2a;
    --border:       rgba(255,255,255,0.07);
    --border-hover: rgba(255,255,255,0.14);
    --accent:       #7c6dfa;
    --accent-glow:  rgba(124,109,250,0.25);
    --accent-dim:   rgba(124,109,250,0.12);
    --text:         #e8e6f0;
    --text-2:       #9490a8;
    --text-3:       #5c586e;
    --success:      #34d399;
    --warning:      #fbbf24;
    --danger:       #f87171;
    --radius:       10px;
    --radius-lg:    16px;
    --font:         'DM Sans', sans-serif;
    --font-mono:    'DM Mono', monospace;
    --transition:   0.18s ease;
  }

  html, body, #root { height: 100%; }

  body {
    font-family: var(--font);
    background: var(--bg);
    color: var(--text);
    font-size: 15px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  h1, h2, h3, h4, h5 {
    font-weight: 500;
    line-height: 1.25;
    letter-spacing: -0.02em;
  }

  a { color: var(--accent); text-decoration: none; }
  a:hover { opacity: 0.8; }

  input, textarea, select {
    font-family: var(--font);
    font-size: 14px;
    background: var(--bg-input);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: var(--radius);
    padding: 10px 14px;
    outline: none;
    transition: border-color var(--transition), box-shadow var(--transition);
    width: 100%;
  }

  input:focus, textarea:focus, select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-glow);
  }

  input::placeholder, textarea::placeholder { color: var(--text-3); }

  button {
    font-family: var(--font);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    border-radius: var(--radius);
    transition: all var(--transition);
  }

  button:disabled { opacity: 0.4; cursor: not-allowed; }

  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 3px; }

  /* Utility classes */
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
  }

  .btn-primary {
    background: var(--accent);
    color: #fff;
    padding: 10px 20px;
    box-shadow: 0 0 20px var(--accent-glow);
  }
  .btn-primary:hover:not(:disabled) {
    background: #9080fb;
    box-shadow: 0 0 28px var(--accent-glow);
    transform: translateY(-1px);
  }

  .btn-ghost {
    background: transparent;
    color: var(--text-2);
    border: 1px solid var(--border);
    padding: 8px 16px;
  }
  .btn-ghost:hover:not(:disabled) {
    background: var(--bg-hover);
    color: var(--text);
    border-color: var(--border-hover);
  }

  .tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 20px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
  }

  .page { padding: 2rem 2.5rem; max-width: 1200px; margin: 0 auto; }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .fade-up { animation: fadeUp 0.4s ease both; }
`;
document.head.appendChild(style);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);