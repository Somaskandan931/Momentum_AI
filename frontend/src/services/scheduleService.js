import API from "./api";

export const generateSchedule = (projectId, taskIds) =>
  API.post("/schedules/generate", { project_id: projectId, task_ids: taskIds });

export const getSchedule = (projectId) =>
  API.get(`/schedules/${projectId}`);
