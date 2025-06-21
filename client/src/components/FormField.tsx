import React from 'react';
import { cn } from '../lib/utils';
import type { FormFieldProps, SelectOption } from '../lib/types/form';

export type { FormFieldProps };

const baseInputStyles = 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-200 dark:bg-gray-800 dark:border-gray-600 dark:text-white dark:placeholder-gray-400';

const errorInputStyles = 'border-red-300 focus:ring-red-500 dark:border-red-600';

const labelStyles = 'block text-sm font-medium text-gray-700 mb-1 dark:text-gray-300';

const errorStyles = 'mt-1 text-sm text-red-600 dark:text-red-400';

const TextInput: React.FC<FormFieldProps> = ({ config, value, error, onChange, onBlur }) => {
  return (
    <input
      type={config.type}
      id={config.name}
      name={config.name}
      value={String(value || '')}
      placeholder={config.placeholder}
      disabled={config.disabled}
      className={cn(
        baseInputStyles,
        error && errorInputStyles,
        config.disabled && 'opacity-50 cursor-not-allowed'
      )}
      onChange={(e) => onChange(config.name, e.target.value)}
      onBlur={() => onBlur(config.name)}
    />
  );
};

const NumberInput: React.FC<FormFieldProps> = ({ config, value, error, onChange, onBlur }) => {
  return (
    <input
      type="number"
      id={config.name}
      name={config.name}
      value={String(value || '')}
      placeholder={config.placeholder}
      disabled={config.disabled}
      className={cn(
        baseInputStyles,
        error && errorInputStyles,
        config.disabled && 'opacity-50 cursor-not-allowed'
      )}
      onChange={(e) => {
        const numValue = e.target.valueAsNumber;
        onChange(config.name, isNaN(numValue) ? e.target.value : numValue);
      }}
      onBlur={() => onBlur(config.name)}
    />
  );
};

const SelectInput: React.FC<FormFieldProps> = ({ config, value, error, onChange, onBlur }) => {
  return (
    <select
      id={config.name}
      name={config.name}
      value={String(value || '')}
      disabled={config.disabled}
      className={cn(
        baseInputStyles,
        'cursor-pointer',
        error && errorInputStyles,
        config.disabled && 'opacity-50 cursor-not-allowed'
      )}
      onChange={(e) => onChange(config.name, e.target.value)}
      onBlur={() => onBlur(config.name)}
    >
      <option value="">{config.placeholder || 'Select an option'}</option>
      {config.options?.map((option: SelectOption) => (
        <option
          key={option.value}
          value={option.value}
          disabled={option.disabled}
        >
          {option.label}
        </option>
      ))}
    </select>
  );
};

const TextAreaInput: React.FC<FormFieldProps> = ({ config, value, error, onChange, onBlur }) => {
  return (
    <textarea
      id={config.name}
      name={config.name}
      value={String(value || '')}
      placeholder={config.placeholder}
      disabled={config.disabled}
      rows={4}
      className={cn(
        baseInputStyles,
        'resize-vertical min-h-[100px]',
        error && errorInputStyles,
        config.disabled && 'opacity-50 cursor-not-allowed'
      )}
      onChange={(e) => onChange(config.name, e.target.value)}
      onBlur={() => onBlur(config.name)}
    />
  );
};

const fieldComponents = {
  text: TextInput,
  email: TextInput,
  password: TextInput,
  number: NumberInput,
  select: SelectInput,
  textarea: TextAreaInput,
};

export const FormField: React.FC<FormFieldProps> = (props) => {
  const { config, error } = props;
  const FieldComponent = fieldComponents[config.type];

  if (!FieldComponent) {
    console.warn(`Unknown field type: ${config.type}`);
    return null;
  }

  const isRequired = config.validation?.required;

  return (
    <div className="mb-4">
      <label htmlFor={config.name} className={labelStyles}>
        {config.label}
        {isRequired && (
          <span className="text-red-500 ml-1">*</span>
        )}
      </label>
      <FieldComponent {...props} />
      {error && (
        <p className={errorStyles}>
          {error}
        </p>
      )}
    </div>
  );
}; 