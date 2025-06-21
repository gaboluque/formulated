import React from 'react';
import { useNavigate, useLocation } from 'react-router';
import { LoginForm } from '../components';
import { useAuth } from '../lib/contexts/AuthContext';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated } = useAuth();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      const from = (location.state as { from?: { pathname: string } })?.from?.pathname || '/';
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const handleLoginSuccess = () => {
    const from = (location.state as { from?: { pathname: string } })?.from?.pathname || '/';
    navigate(from, { replace: true });
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <LoginForm 
          onSuccess={handleLoginSuccess}
          className="shadow-xl"
        />
      </div>
    </div>
  );
}; 