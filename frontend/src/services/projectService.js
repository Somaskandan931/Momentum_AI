import API from "./api";

export const createProject = (data) => API.post("/projects/", data);
export const listProjects = () => API.get("/projects/");
export const getProject = (id) => API.get(`/projects/${id}`);
export const deleteProject = (id) => API.delete(`/projects/${id}`);
export const getSurvivalScore = (id) => API.get(`/projects/${id}/survival-score`);

export const analyzeIdea = (idea, projectId) =>
  API.post("/ideas/analyze", { idea, project_id: projectId });

export const generateTasksFromIdea = (idea, projectId) =>
  API.post("/ideas/generate-tasks", { idea, project_id: projectId });

export const addMember = (projectId, userId, role) =>
  API.post("/collab/add-member", { project_id: projectId, user_id: userId, role });

export const getMembers = (projectId) =>
  API.get(`/collab/${projectId}/members`);
