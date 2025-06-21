import React, { useState, useCallback } from 'react';
import { cn } from '../lib/utils';
import { Button } from './Button';
import { FormField } from './FormField';
import type { FormProps, FormState, FormFieldConfig, FormFieldValue, ValidationRule } from '../lib/types/form';

export type { FormProps };

const validateField = (value: FormFieldValue, validation?: ValidationRule): string => {
  if (!validation) return '';

  // Required validation
  if (validation.required) {
    if (!value || (typeof value === 'string' && value.trim() === '')) {
      return 'This field is required';
    }
  }

  // Skip other validations if field is empty and not required
  if (!value && !validation.required) return '';

  // String validations
  if (typeof value === 'string') {
    if (validation.minLength && value.length < validation.minLength) {
      return `Must be at least ${validation.minLength} characters`;
    }
    if (validation.maxLength && value.length > validation.maxLength) {
      return `Must be no more than ${validation.maxLength} characters`;
    }
    if (validation.pattern && !validation.pattern.test(value)) {
      return 'Invalid format';
    }
    if (validation.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        return 'Please enter a valid email address';
      }
    }
  }

  // Number validations
  if (typeof value === 'number') {
    if (validation.min !== undefined && value < validation.min) {
      return `Must be at least ${validation.min}`;
    }
    if (validation.max !== undefined && value > validation.max) {
      return `Must be no more than ${validation.max}`;
    }
  }

  // Custom validation
  if (validation.custom) {
    if (!validation.custom.validator(value)) {
      return validation.custom.message;
    }
  }

  return '';
};

const validateForm = (data: Record<string, FormFieldValue>, fields: FormFieldConfig[]): Record<string, string> => {
  const errors: Record<string, string> = {};
  
  fields.forEach((field) => {
    const value = data[field.name] ?? '';
    const error = validateField(value, field.validation);
    if (error) {
      errors[field.name] = error;
    }
  });
  
  return errors;
};

export const Form: React.FC<FormProps> = ({
  config,
  onSubmit,
  initialData = {},
  className,
  isLoading = false
}) => {
  const [state, setState] = useState<FormState>(() => {
    const initialFormData: Record<string, FormFieldValue> = {};
    config.fields.forEach((field) => {
      initialFormData[field.name] = initialData[field.name] ?? field.defaultValue ?? '';
    });
    
    return {
      data: initialFormData,
      errors: {},
      touched: {},
      isSubmitting: false
    };
  });

  const handleFieldChange = useCallback((name: string, value: FormFieldValue) => {
    setState(prev => ({
      ...prev,
      data: {
        ...prev.data,
        [name]: value
      },
      // Clear error when field is changed
      errors: {
        ...prev.errors,
        [name]: ''
      }
    }));
  }, []);

  const handleFieldBlur = useCallback((name: string) => {
    setState(prev => {
      const field = config.fields.find(f => f.name === name);
      if (!field) return prev;

      const error = validateField(prev.data[name] ?? '', field.validation);
      
      return {
        ...prev,
        touched: {
          ...prev.touched,
          [name]: true
        },
        errors: {
          ...prev.errors,
          [name]: error
        }
      };
    });
  }, [config.fields]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate all fields
    const errors = validateForm(state.data, config.fields);
    const hasErrors = Object.values(errors).some(error => error !== '');
    
    // Mark all fields as touched
    const allTouched = config.fields.reduce((acc, field) => {
      acc[field.name] = true;
      return acc;
    }, {} as Record<string, boolean>);
    
    setState(prev => ({
      ...prev,
      errors,
      touched: allTouched,
      isSubmitting: !hasErrors
    }));
    
    if (hasErrors) {
      return;
    }
    
    try {
      await onSubmit(state.data);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setState(prev => ({
        ...prev,
        isSubmitting: false
      }));
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className={cn('space-y-4', className)}
      noValidate
    >
      {config.fields.map((field) => (
        <FormField
          key={field.name}
          config={field}
          value={state.data[field.name] ?? ''}
          error={state.touched[field.name] ? state.errors[field.name] : ''}
          onChange={handleFieldChange}
          onBlur={handleFieldBlur}
        />
      ))}
      
      <div className="flex justify-end pt-4">
        <Button
          type="submit"
          isLoading={state.isSubmitting || isLoading}
          disabled={state.isSubmitting || isLoading}
        >
          {config.submitText || 'Submit'}
        </Button>
      </div>
    </form>
  );
}; 