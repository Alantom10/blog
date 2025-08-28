import axios from "axios";

const API_URL = "http://127.0.0.1:8000/blogs"; // FastAPI backend URL

export const getBlogs = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        if (error.response) {
            throw new Error(error.response.data.detail || "Error fetching blogs");
        }
        throw error;
    }
}
// export const getBlogBySlug = (slug) => axios.get(`${API_URL}/${slug}`);
// export const createBlog = (blog) => axios.post(API_URL, blog);
// export const updateBlog = (slug, blog) => axios.put(`${API_URL}/${slug}`, blog);
// export const deleteBlog = (slug) => axios.delete(`${API_URL}/${slug}`);