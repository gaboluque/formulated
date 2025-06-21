import React, { createContext, useContext, useReducer, useEffect, type ReactNode } from 'react';
import { authApi } from '../api/auth';
import type { AuthState, User, LoginCredentials, RegisterCredentials } from '../types/auth';

// Auth Actions
type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: User }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' };

// Auth Reducer
const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'AUTH_SUCCESS':
      return {
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'AUTH_FAILURE':
      return {
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    default:
      return state;
  }
};

// Initial state
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true, // Start with loading to check auth status
  error: null,
};

// Auth Context
interface AuthContextType extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (credentials: RegisterCredentials) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth Provider Component
interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check authentication status on app load
  const checkAuth = async () => {
    try {
      dispatch({ type: 'AUTH_START' });
      const user = await authApi.checkAuth();
      if (user) {
        dispatch({ type: 'AUTH_SUCCESS', payload: user });
      } else {
        dispatch({ type: 'AUTH_FAILURE', payload: 'Not authenticated' });
      }
    } catch {
      dispatch({ type: 'AUTH_FAILURE', payload: 'Authentication check failed' });
    }
  };

  // Login function
  const login = async (credentials: LoginCredentials) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const response = await authApi.login(credentials);
      dispatch({ type: 'AUTH_SUCCESS', payload: response.user });
    } catch (error: unknown) {
      const errorMessage = (error as any)?.response?.data?.error || 'Login failed. Please try again.';
      dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  // Register function
  const register = async (credentials: RegisterCredentials) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const response = await authApi.register(credentials);
      dispatch({ type: 'AUTH_SUCCESS', payload: response.user });
    } catch (error: unknown) {
      const errorMessage = (error as any)?.response?.data?.error || 'Registration failed. Please try again.';
      dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authApi.logout();
    } catch (error) {
      // Even if logout fails, clear local state
      console.error('Logout error:', error);
    } finally {
      dispatch({ type: 'LOGOUT' });
    }
  };

  // Clear error function
  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  // Check auth on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    clearError,
    checkAuth,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 