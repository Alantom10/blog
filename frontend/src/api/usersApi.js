import axios from "axios";
import { authApi, handleError } from './apiClient';

const BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend URL


export const createUser = async (userData) => {
    try {
        const response = await axios.post(`${BASE_URL}/users`, userData);
        return response.data;
    } catch (error) {
        handleError(error, "Error creating user");
    }
};

export const getUsers = async () => {
    try {
        const response = await authApi.get('/users');
        return response.data;
    } catch (error) {
        handleError(error, "Error fetching users");
    }
};

export const getUserById = async (userId) => {
    try {
        const response = await authApi.get(`/users/${userId}`);
        return response.data;
    } catch (error) {
        handleError(error, "Error fetching user");
    }
};

export const updateUser = async (userId, userData) => {
    try {
        const response = await authApi.put(`/users/${userId}`, userData);
        return response.data;
    } catch (error) {
        handleError(error, "Error updating user");
    }
};

export const deleteUser = async (userId) => {
    try {
        const response = await authApi.delete(`/users/${userId}`);
        return response.data;
    } catch (error) {
        handleError(error, "Error deleting user");
    }
};