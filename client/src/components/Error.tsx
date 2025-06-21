import React from 'react';
import { Button } from './Button';

export interface ErrorProps {
  title?: string;
  message?: string;
  error?: Error;
  onRetry?: () => void;
  showRetry?: boolean;
  variant?: 'default' | 'minimal' | 'page';
}

export const Error: React.FC<ErrorProps> = ({
  title = 'Something went wrong',
  message,
  error,
  onRetry,
  showRetry = true,
  variant = 'default'
}) => {
  const displayMessage = message || error?.message || 'An unexpected error occurred. Please try again.';

  const variants = {
    default: 'bg-red-50 border border-red-200 rounded-lg p-6',
    minimal: 'text-red-600',
    page: 'min-h-[50vh] flex items-center justify-center'
  };

  const content = (
    <div className={`${variants[variant]} ${variant === 'page' ? '' : 'max-w-md'}`}>
      <div className={variant === 'page' ? 'text-center' : ''}>
        <div className="flex items-center gap-3 mb-2">
          <div className="flex-shrink-0">
            <svg 
              className="h-5 w-5 text-red-400" 
              viewBox="0 0 20 20" 
              fill="currentColor"
              aria-hidden="true"
            >
              <path 
                fillRule="evenodd" 
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z" 
                clipRule="evenodd" 
              />
            </svg>
          </div>
          <h3 className={`font-medium ${variant === 'minimal' ? 'text-red-800' : 'text-red-800'}`}>
            {title}
          </h3>
        </div>
        
        <div className={`${variant === 'minimal' ? 'text-red-700' : 'text-red-700'} mb-4`}>
          <p>{displayMessage}</p>
        </div>

        {showRetry && onRetry && (
          <div className={variant === 'page' ? 'flex justify-center' : ''}>
            <Button
              variant="outline"
              size="sm"
              onClick={onRetry}
              className="text-red-700 border-red-300 hover:bg-red-50"
            >
              Try Again
            </Button>
          </div>
        )}
      </div>
    </div>
  );

  if (variant === 'page') {
    return <div className={variants.page}>{content}</div>;
  }

  return content;
}; 