import axios from "axios";

const BASE_URL = "http://localhost:8000";


export const authApi = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
});


// Add this response interceptor
authApi.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('user');
            
            // Redirect to login
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const handleError = (error, defaultMessage) => {
    if (error.response) {
        // For 422 errors, show detailed validation info
        if (error.response.status === 422 && error.response.data.errors) {
            const errorMessages = error.response.data.errors.join(', ');
            throw new Error(`Validation failed: ${errorMessages}`);
        }
        throw new Error(error.response.data.detail || defaultMessage);
    }
    throw error;
};