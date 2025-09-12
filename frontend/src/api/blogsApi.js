import axios from "axios";

const API_URL = "http://127.0.0.1:8000/blogs"; // FastAPI backend URL


const handleError = (error, defaultMessage) => {
  if (error.response) {
    throw new Error(error.response.data.detail || defaultMessage);
  }
  throw error;
};

export const getBlogs = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        handleError(error, "Error fetching blogs");
    }
}

export const getBlogBySlug = async (slug) => {
    try {
        const response = await axios.get(`${API_URL}/${slug}`);
        return response.data;
    } catch (error) {
        handleError(error, "Error fetching blog");
    }
}

export const createBlog = async (blog) => {
    try {
        const response = await axios.post(API_URL, blog);
        return response.data;
    } catch (error) {
        handleError(error, "Error creating blog");
    }
}

export const updateBlog = async (slug, blog) => {
    try {
        const response = await axios.put(`${API_URL}/${slug}`, blog);
        return response.data;
    } catch (error) {
        handleError(error, "Error updating blog");
    }
}

export const deleteBlog = async (slug) => {
    try {
        const response = await axios.delete(`${API_URL}/${slug}`);
        return response.data;
    } catch (error) {
        handleError(error, "Error deleting blog");
    }
}
