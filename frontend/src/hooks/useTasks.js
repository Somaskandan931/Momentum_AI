import { useState, useEffect, useCallback } from "react";
import API from "../services/api";

export function useTasks(projectId) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTasks = useCallback(async () => {
    if (!projectId) return;
    try {
      setLoading(true);
      const { data } = await API.get(`/tasks/project/${projectId}`);
      setTasks(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  const updateTaskStatus = async (taskId, status) => {
    await API.patch(`/tasks/${taskId}`, { status });
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, status } : t))
    );
  };

  const deleteTask = async (taskId) => {
    await API.delete(`/tasks/${taskId}`);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  useEffect(() => { fetchTasks(); }, [fetchTasks]);

  return { tasks, loading, error, updateTaskStatus, deleteTask, refetch: fetchTasks };
}
