import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const uploadAndPredict = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await axios.post(`${API_URL}/predict-model`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'An error occurred during prediction.');
  }
};

export const fetchHistory = async (brand = '') => {
  try {
    const params = brand ? { brand } : {};
    const response = await axios.get(`${API_URL}/history`, { params });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch history.');
  }
};
