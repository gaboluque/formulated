import React from 'react';
import { useNavigate } from 'react-router';
import { RegisterForm } from '../components';
import { useAuth } from '../lib/contexts/AuthContext';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleRegisterSuccess = () => {
    navigate('/', { replace: true });
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <RegisterForm 
          onSuccess={handleRegisterSuccess}
          className="shadow-xl"
        />
      </div>
    </div>
  );
}; 