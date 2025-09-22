import axios from "axios";
import { authApi, handleError } from './apiClient';

const BASE_URL = "http://localhost:8000"; // FastAPI backend URL


export const getBlogs = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/blogs`);
        return response.data;
    } catch (error) {
        handleError(error, "Error fetching blogs");
    }
};

export const getBlogBySlug = async (slug) => {
    try {
        const response = await axios.get(`${BASE_URL}/blogs/${slug}`);
        return response.data;
    } catch (error) {
        handleError(error, "Error fetching blog");
    }
};

export const createBlog = async (blog) => {
    try {
        const response = await authApi.post('/blogs', blog);
        return response.data;
    } catch (error) {
        handleError(error, "Error creating blog");
    }
};

export const updateBlog = async (slug, blog) => {
    try {
        const response = await authApi.put(`/blogs/${slug}`, blog);
        return response.data;
    } catch (error) {
        handleError(error, "Error updating blog");
    }
};

export const deleteBlog = async (slug) => {
    try {
        const response = await authApi.delete(`/blogs/${slug}`);
        return response.data;
    } catch (error) {
        handleError(error, "Error deleting blog");
    }
};