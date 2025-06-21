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
  withCredentials: true, // Include cookies for session-based auth
});

// Store CSRF token in memory
let csrfToken: string | null = null;

// Function to get CSRF token from Django
async function getCsrfToken(): Promise<string | null> {
  if (csrfToken) {
    return csrfToken;
  }
  
  try {
    const response = await axios.get(`${BASE_URL}/auth/csrf/`, {
      withCredentials: true,
    });
    csrfToken = response.data.csrfToken;
    return csrfToken;
  } catch (error) {
    console.error('Failed to get CSRF token:', error);
    return null;
  }
}

// Request interceptor to add CSRF token to non-safe requests
apiClient.interceptors.request.use(
  async (config) => {
    // Add CSRF token to non-safe HTTP methods
    const unsafeMethods = ['post', 'put', 'patch', 'delete'];
    if (config.method && unsafeMethods.includes(config.method.toLowerCase())) {
      const token = await getCsrfToken();
      if (token && config.headers) {
        // Set the CSRF token header
        config.headers['X-CSRFToken'] = token;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle common error scenarios
    const status = error.response?.status;
    if (status === 401) {
      // Unauthorized - handle authentication failure
      console.warn('Authentication expired. Please log in again.');
      // You might want to trigger a logout or redirect to login page here
      // This will be handled by the auth context
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
