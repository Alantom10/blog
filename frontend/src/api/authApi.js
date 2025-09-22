import axios from "axios";

const AUTH_URL = "http://localhost:8000/auth"; // Your FastAPI auth endpoint


const handleError = (error, defaultMessage) => {
  if (error.response) {
    throw new Error(error.response.data.detail || defaultMessage);
  }
  throw error;
};

export const login = async (credentials) => {
    try {
        const response = await axios.post(`${AUTH_URL}/login-json`, credentials, {
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        handleError(error, "Login failed");
    }
};

export const getCurrentUser = async () => {
    try {
        const response = await axios.get(`${AUTH_URL}/me`, {
            withCredentials: true
        });
        return response.data;
    } catch (error) {
        handleError(error, "Failed to get user information");
    }
};

export const logout = async () => {
    try {
        await axios.post(`${AUTH_URL}/logout`, {}, {
            withCredentials: true
        });
        
        // Remove any user data from localStorage
        localStorage.removeItem('user');
    } catch (error) {
        console.error("Logout error:", error);
    }
};