import axios from "axios";

const API_URL = "http://localhost:8000";

export const uploadVideo = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await axios.post(`${API_URL}/detect/`, formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response.data;
    } catch (error) {
        console.error("Error uploading video:", error.response?.data || error.message);
        return { error: "Failed to process video." };
    }
};
