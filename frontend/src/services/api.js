import axios from 'axios';

// Get API URL - ensure it ends with /api if it doesn't already
const getApiUrl = () => {
  const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
  // If URL doesn't end with /api, add it
  if (!baseUrl.endsWith('/api')) {
    return baseUrl.endsWith('/') ? `${baseUrl}api` : `${baseUrl}/api`;
  }
  return baseUrl;
};

const api = axios.create({
  baseURL: getApiUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Add request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error: No response from server. Is the backend running?');
      const apiUrl = getApiUrl();
      console.error('Attempted to connect to:', apiUrl);
      console.error('REACT_APP_API_URL env var:', process.env.REACT_APP_API_URL || 'NOT SET');
      error.message = `Cannot connect to backend server. Please check if the backend is running at ${apiUrl}.`;
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;

