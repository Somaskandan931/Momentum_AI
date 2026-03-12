import { useState, useEffect } from "react";
import { listProjects, createProject, deleteProject } from "../services/projectService";

export function useProjects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const { data } = await listProjects();
      setProjects(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const addProject = async (title, description) => {
    const { data } = await createProject({ title, description });
    setProjects((prev) => [...prev, data]);
    return data;
  };

  const removeProject = async (id) => {
    await deleteProject(id);
    setProjects((prev) => prev.filter((p) => p.id !== id));
  };

  useEffect(() => { fetchProjects(); }, []);

  return { projects, loading, error, addProject, removeProject, refetch: fetchProjects };
}
