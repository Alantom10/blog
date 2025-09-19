import axios from "axios";

const AUTH_URL = "http://127.0.0.1:8000/auth"; // Your FastAPI auth endpoint

const handleError = (error, defaultMessage) => {
  if (error.response) {
    throw new Error(error.response.data.detail || defaultMessage);
  }
  throw error;
};

export const login = async (credentials) => {
    try {
        const response = await axios.post(`${AUTH_URL}/login-json`, credentials);
        return response.data;
    } catch (error) {
        handleError(error, "Login failed");
    }
};

export const getCurrentUser = async (token) => {
    try {
        const response = await axios.get(`${AUTH_URL}/me`, {
            headers: { 
                Authorization: `Bearer ${token}` 
            }
        });
        return response.data;
    } catch (error) {
        handleError(error, "Failed to get user information");
    }
};

export const logout = () => {
    // Remove token from localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
};