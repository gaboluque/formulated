import React, { useState } from 'react';
import { Link } from 'react-router';
import { Form } from '../Form';
import { Card } from '../Card';
import { useAuth } from '../../lib/contexts/AuthContext';
import type { FormConfig, FormFieldValue } from '../../lib/types/form';
import type { LoginCredentials } from '../../lib/types/auth';

export interface LoginFormProps {
  onSuccess?: () => void;
  className?: string;
}

export const LoginForm: React.FC<LoginFormProps> = ({ 
  onSuccess, 
  className = '' 
}) => {
  const { login, isLoading, error, clearError } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const formConfig: FormConfig = {
    fields: [
      {
        name: 'email',
        type: 'email',
        label: 'Email Address',
        placeholder: 'Enter your email',
        validation: {
          required: true,
          email: true,
        },
      },
      {
        name: 'password',
        type: 'password',
        label: 'Password',
        placeholder: 'Enter your password',
        validation: {
          required: true,
          minLength: 6,
        },
      },
    ],
    submitText: 'Sign In',
  };

  const handleSubmit = async (data: Record<string, FormFieldValue>) => {
    setIsSubmitting(true);
    clearError();

    try {
      const credentials: LoginCredentials = {
        email: data.email as string,
        password: data.password as string,
      };

      await login(credentials);
      onSuccess?.();
    } catch (error) {
      // Error is handled by the auth context
      console.error('Login error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className={`w-full max-w-md mx-auto ${className}`}>
      <div className="p-6">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Sign In
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Welcome back! Please sign in to your account.
          </p>
        </div>

        {/* Display error message */}
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md dark:bg-red-900/50 dark:border-red-700 dark:text-red-400">
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        <Form
          config={formConfig}
          onSubmit={handleSubmit}
          isLoading={isLoading || isSubmitting}
          className="space-y-4"
        />

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </Card>
  );
}; 