import axios from 'axios';
import type { AxiosInstance, AxiosResponse, AxiosError } from 'axios';

export type PaginatedResponse<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Base URL for the API - adjust this based on your backend configuration
const BASE_URL = import.meta.env.API_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle common error scenarios
    const status = error.response?.status;
    if (status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('authToken');
      // You might want to redirect to login page here
      console.warn('Authentication expired. Please log in again.');
    } else if (status === 403) {
      console.error('Access denied.');
    } else if (status && status >= 500) {
      console.error('Server error. Please try again later.');
    }
    
    return Promise.reject(error);
  }
);

// Utility functions for common HTTP methods
export const api = {
  get: <T = unknown>(url: string, config = {}) => 
    apiClient.get<T>(url, config),
  
  post: <T = unknown>(url: string, data = {}, config = {}) => 
    apiClient.post<T>(url, data, config),
  
  put: <T = unknown>(url: string, data = {}, config = {}) => 
    apiClient.put<T>(url, data, config),
  
  patch: <T = unknown>(url: string, data = {}, config = {}) => 
    apiClient.patch<T>(url, data, config),
  
  delete: <T = unknown>(url: string, config = {}) => 
    apiClient.delete<T>(url, config),
};

export default apiClient;
