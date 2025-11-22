import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const getTasks = async () => {
    try {
        const response = await axios.get(`${API_URL}/tasks`);
        return response.data;
    } catch (error) {
        console.error("Error fetching tasks:", error);
        throw error;
    }
};

export const getStats = async () => {
    try {
        const response = await axios.get(`${API_URL}/stats`);
        return response.data;
    } catch (error) {
        console.error("Error fetching stats:", error);
        throw error;
    }
};

export const getInsights = async () => {
    try {
        const response = await axios.get(`${API_URL}/insights`);
        return response.data;
    } catch (error) {
        console.error("Error fetching insights:", error);
        throw error;
    }
};
