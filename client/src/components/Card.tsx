import React from 'react';
import { cn } from '../lib/utils';

export interface CardProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'title'> {
  variant?: 'default' | 'outline' | 'elevated';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  title?: React.ReactNode;
  extra?: React.ReactNode;
  children: React.ReactNode;
}

const cardVariants = {
  default: 'bg-white border border-gray-200 dark:bg-gray-800 dark:border-gray-700',
  outline: 'border-2 border-gray-300 bg-transparent dark:border-gray-600',
  elevated: 'bg-white shadow-lg border border-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:shadow-gray-900/20',
};

const cardPadding = {
  none: 'p-0',
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
};

export const Card: React.FC<CardProps> = ({
  variant = 'default',
  padding = 'md',
  title,
  extra,
  className,
  children,
  ...props
}) => {
  const hasHeader = title || extra;

  return (
    <div
      className={cn(
        // Base styles
        'rounded-lg transition-shadow duration-200',
        // Variant styles
        cardVariants[variant],
        // Padding styles - only apply to cards without custom padding structure
        !hasHeader ? cardPadding[padding] : '',
        className
      )}
      {...props}
    >
      {hasHeader && (
        <div
          className={cn(
            'flex items-center justify-between border-b border-gray-200 dark:border-gray-700',
            // Apply padding to header
            padding === 'none' ? 'p-0' : 
            padding === 'sm' ? 'px-3 py-2' :
            padding === 'md' ? 'px-4 py-3' :
            'px-6 py-4'
          )}
        >
          {title && (
            <div className="flex-1">
              {typeof title === 'string' ? (
                <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                  {title}
                </h3>
              ) : (
                title
              )}
            </div>
          )}
          {extra && (
            <div className="flex-shrink-0 ml-4">
              {extra}
            </div>
          )}
        </div>
      )}
      <div
        className={cn(
          // Apply padding to body
          padding === 'none' ? 'p-0' : 
          padding === 'sm' ? 'p-3' :
          padding === 'md' ? 'p-4' :
          'p-6'
        )}
      >
        {children}
      </div>
    </div>
  );
}; 