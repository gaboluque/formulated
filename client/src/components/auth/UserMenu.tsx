import React, { useState } from 'react';
import { Button } from '../Button';
import { useAuth } from '../../lib/contexts/AuthContext';
import { routes } from '../../routing/router';
import { Link } from 'react-router';

export interface UserMenuProps {
  className?: string;
}

export const UserMenu: React.FC<UserMenuProps> = ({ className = '' }) => {
  const { user, logout, isLoading } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
      setIsDropdownOpen(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (!user) return <Link to={routes.login.path} className="text-sm font-medium text-gray-700 dark:text-gray-300">Login</Link>;

  return (
    <div className={`relative ${className}`}>
      {/* User Avatar/Button */}
      <button
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
        className="flex items-center space-x-2 p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        aria-expanded={isDropdownOpen}
        aria-haspopup="true"
      >
        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
          {user.username.charAt(0).toUpperCase()}
        </div>
        <span className="text-sm font-medium text-gray-700 dark:text-gray-300 hidden sm:block">
          {user.username}
        </span>
        <svg
          className={`w-4 h-4 text-gray-500 transition-transform ${
            isDropdownOpen ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isDropdownOpen && (
        <>
          {/* Overlay */}
          <div 
            className="fixed inset-0 z-10" 
            onClick={() => setIsDropdownOpen(false)}
          />
          
          {/* Dropdown Content */}
          <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-20">
            <div className="py-1">
              {/* User Info */}
              <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  {user.username}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
                  {user.email}
                </p>
              </div>

              {/* Menu Items */}
              <div className="py-2">
                <button
                  onClick={() => setIsDropdownOpen(false)}
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  Profile
                </button>
                <button
                  onClick={() => setIsDropdownOpen(false)}
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  Settings
                </button>
              </div>

              {/* Logout */}
              <div className="border-t border-gray-200 dark:border-gray-700 py-2">
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handleLogout}
                  isLoading={isLoading}
                >
                  Sign Out
                </Button>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}; 