import apiClient from './apiClient';

export const exercisePlanAPI = {
  generatePlan: (profileData) =>
    apiClient.post('/exercise-plans/generate_plan/', profileData),
  getPlan: (id) =>
    apiClient.get(`/exercise-plans/${id}/`),
};

export const workoutScheduleAPI = {
  generateSchedule: (scheduleData) =>
    apiClient.post('/workout-schedules/generate_schedule/', scheduleData),
  getSchedule: (id) =>
    apiClient.get(`/workout-schedules/${id}/`),
};

export const workoutSessionAPI = {
  getUpcoming: () =>
    apiClient.get('/workout-sessions/upcoming/'),
  getHistory: () =>
    apiClient.get('/workout-sessions/history/'),
};

export const progressReportAPI = {
  generateReport: (reportData) =>
    apiClient.post('/progress-reports/generate_report/', reportData),
};

export const notificationAPI = {
  getUnread: () =>
    apiClient.get('/notifications/unread/'),
  markAllAsRead: () =>
    apiClient.post('/notifications/mark_all_as_read/'),
};