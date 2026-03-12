export const formatDate = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short", day: "numeric", year: "numeric"
  });
};

export const formatTime = (dateStr) => {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleTimeString("en-US", {
    hour: "2-digit", minute: "2-digit"
  });
};

export const priorityColor = (priority) => {
  const map = { high: "#e74c3c", medium: "#f39c12", low: "#27ae60" };
  return map[priority] || "#95a5a6";
};

export const statusColor = (status) => {
  const map = {
    "To Do": "#3498db",
    "In Progress": "#f39c12",
    "Completed": "#27ae60"
  };
  return map[status] || "#95a5a6";
};

export const survivalScoreLabel = (score) => {
  if (score >= 75) return { label: "Strong", color: "#27ae60" };
  if (score >= 50) return { label: "Moderate", color: "#f39c12" };
  return { label: "At Risk", color: "#e74c3c" };
};

export const groupTasksByStatus = (tasks) => {
  return {
    "To Do":       tasks.filter((t) => t.status === "To Do"),
    "In Progress": tasks.filter((t) => t.status === "In Progress"),
    "Completed":   tasks.filter((t) => t.status === "Completed"),
  };
};
