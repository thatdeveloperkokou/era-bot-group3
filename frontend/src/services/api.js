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
      const status = error.response.status;
      const data = error.response.data;
      console.error(`API Error ${status}:`, data);
      
      // Attach error message to error object for easier access
      if (data && data.error) {
        error.message = data.error;
      } else if (data && typeof data === 'string') {
        error.message = data;
      } else if (data && data.message) {
        error.message = data.message;
      } else {
        error.message = `Server error (${status})`;
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error: No response from server. Is the backend running?');
      const apiUrl = getApiUrl();
      const envVar = process.env.REACT_APP_API_URL;
      console.error('Attempted to connect to:', apiUrl);
      console.error('REACT_APP_API_URL env var:', envVar || 'NOT SET - This is the problem!');
      if (!envVar) {
        console.error('⚠️ SOLUTION: Set REACT_APP_API_URL in Vercel Environment Variables');
        console.error('   Go to: Vercel Dashboard → Settings → Environment Variables');
        console.error('   Add: REACT_APP_API_URL = https://era-bot-group3-production.up.railway.app/api');
      }
      error.message = `Cannot connect to backend server. Please check if the backend is running at ${apiUrl}.`;
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;

