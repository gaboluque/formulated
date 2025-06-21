import React, { useState } from 'react';
import { Link } from 'react-router';
import { Form } from '../Form';
import { Card } from '../Card';
import { useAuth } from '../../lib/contexts/AuthContext';
import type { FormConfig, FormFieldValue } from '../../lib/types/form';
import type { RegisterCredentials } from '../../lib/types/auth';

export interface RegisterFormProps {
  onSuccess?: () => void;
  className?: string;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ 
  onSuccess, 
  className = '' 
}) => {
  const { register, isLoading, error, clearError } = useAuth();
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
        name: 'username',
        type: 'text',
        label: 'Username (Optional)',
        placeholder: 'Choose a username',
        validation: {
          minLength: 3,
          maxLength: 30,
        },
      },
      {
        name: 'password',
        type: 'password',
        label: 'Password',
        placeholder: 'Create a password',
        validation: {
          required: true,
          minLength: 6,
        },
      },
    ],
    submitText: 'Create Account',
  };

  const handleSubmit = async (data: Record<string, FormFieldValue>) => {
    setIsSubmitting(true);
    clearError();

    try {
      const credentials: RegisterCredentials = {
        email: data.email as string,
        password: data.password as string,
        username: data.username ? (data.username as string) : undefined,
      };

      await register(credentials);
      onSuccess?.();
    } catch (error) {
      // Error is handled by the auth context
      console.error('Registration error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className={`w-full max-w-md mx-auto ${className}`}>
      <div className="p-6">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Create Account
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Join Formulated to track your favorite F1 teams and races.
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
            Already have an account?{' '}
            <Link
              to="/login"
              className="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </Card>
  );
}; 