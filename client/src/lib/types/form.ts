export type FormFieldValue = string | number | boolean;

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  min?: number;
  max?: number;
  pattern?: RegExp;
  email?: boolean;
  custom?: {
    validator: (value: FormFieldValue) => boolean;
    message: string;
  };
}

export interface SelectOption {
  value: string | number;
  label: string;
  disabled?: boolean;
}

export interface FormFieldConfig {
  name: string;
  type: 'text' | 'email' | 'password' | 'number' | 'select' | 'textarea';
  label: string;
  placeholder?: string;
  defaultValue?: FormFieldValue;
  validation?: ValidationRule;
  options?: SelectOption[]; // For select fields
  disabled?: boolean;
}

export interface FormConfig {
  fields: FormFieldConfig[];
  submitText?: string;
}

export interface FormFieldProps {
  config: FormFieldConfig;
  value: FormFieldValue;
  error?: string;
  onChange: (name: string, value: FormFieldValue) => void;
  onBlur: (name: string) => void;
}

export interface FormProps {
  config: FormConfig;
  onSubmit: (data: Record<string, FormFieldValue>) => void | Promise<void>;
  initialData?: Record<string, FormFieldValue>;
  className?: string;
  isLoading?: boolean;
}

export interface FormErrors {
  [fieldName: string]: string;
}

export interface FormState {
  data: Record<string, FormFieldValue>;
  errors: FormErrors;
  touched: Record<string, boolean>;
  isSubmitting: boolean;
} 