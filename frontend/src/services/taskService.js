import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const getProjects = async () => {
    try {
        const response = await axios.get(`${API_URL}/projects`);
        return response.data;
    } catch (error) {
        console.error("Error fetching projects:", error);
        throw error;
    }
};

export const getProjectDashboard = async (projectId) => {
    try {
        const response = await axios.get(`${API_URL}/projects/${projectId}/dashboard`);
        return response.data;
    } catch (error) {
        console.error("Error fetching project dashboard:", error);
        throw error;
    }
};

export const getCeoDashboard = async () => {
    try {
        const response = await axios.get(`${API_URL}/dashboard/ceo`);
        return response.data;
    } catch (error) {
        console.error("Error fetching CEO dashboard:", error);
        throw error;
    }
};

export const getWeeklySummary = async () => {
    try {
        const response = await axios.get(`${API_URL}/weekly-summary`);
        return response.data;
    } catch (error) {
        console.error("Error fetching weekly summary:", error);
        throw error;
    }
};
