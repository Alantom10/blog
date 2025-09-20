import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";


export const authApi = axios.create({
    baseURL: BASE_URL,
});

authApi.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Add this response interceptor
authApi.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            
            // Redirect to login
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const handleError = (error, defaultMessage) => {
    if (error.response) {
        throw new Error(error.response.data.detail || defaultMessage);
    }
    throw error;
};