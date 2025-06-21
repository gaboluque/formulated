import { api } from './client';
import type { 
  LoginCredentials, 
  RegisterCredentials, 
  AuthResponse, 
  User,
  PasswordResetData 
} from '../types/auth';

export const authApi = {
  /**
   * Register a new user
   */
  register: async (credentials: RegisterCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/register/', credentials);
    return response.data;
  },

  /**
   * Login user
   */
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login/', credentials);
    return response.data;
  },

  /**
   * Logout current user
   */
  logout: async (): Promise<{ message: string }> => {
    const response = await api.post<{ message: string }>('/auth/logout/');
    return response.data;
  },

  /**
   * Get current authenticated user
   */
  getCurrentUser: async (): Promise<{ user: User }> => {
    const response = await api.get<{ user: User }>('/auth/me/');
    return response.data;
  },

  /**
   * Request password reset (future implementation)
   */
  requestPasswordReset: async (data: PasswordResetData): Promise<{ message: string }> => {
    // Placeholder for future implementation
    console.log('Password reset requested for:', data.email);
    throw new Error('Password reset not yet implemented');
  },

  /**
   * Check if user is authenticated by trying to get current user
   */
  checkAuth: async (): Promise<User | null> => {
    try {
      const response = await authApi.getCurrentUser();
      return response.user;
    } catch (error) {
      // Expected error when not authenticated
      console.debug('Auth check failed:', error);
      return null;
    }
  },
}; 