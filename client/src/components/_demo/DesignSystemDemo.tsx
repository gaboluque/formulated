import React, { useState } from 'react';
import { Button, Card, Form } from '../index';
import type { FormConfig, FormFieldValue } from '../../lib/types/form';

// Contact Form Demo Component
const ContactFormDemo: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);

  const contactFormConfig: FormConfig = {
    fields: [
      {
        name: 'name',
        type: 'text',
        label: 'Name',
        placeholder: 'Your full name',
        validation: { required: true, minLength: 2 }
      },
      {
        name: 'email',
        type: 'email',
        label: 'Email',
        placeholder: 'your@email.com',
        validation: { required: true, email: true }
      },
      {
        name: 'message',
        type: 'textarea',
        label: 'Message',
        placeholder: 'How can we help you?',
        validation: { required: true, minLength: 10, maxLength: 500 }
      }
    ],
    submitText: 'Send Message'
  };

  const handleSubmit = async (data: Record<string, FormFieldValue>) => {
    console.log('Contact form submitted:', data);
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  if (submitted) {
    return (
      <div className="text-center py-4">
        <div className="text-green-600 mb-2">✓ Message sent successfully!</div>
        <p className="text-sm text-gray-600 dark:text-gray-400">We'll get back to you soon.</p>
      </div>
    );
  }

  return <Form config={contactFormConfig} onSubmit={handleSubmit} />;
};

// Registration Form Demo Component
const RegistrationFormDemo: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);

  const registrationFormConfig: FormConfig = {
    fields: [
      {
        name: 'username',
        type: 'text',
        label: 'Username',
        placeholder: 'Choose a username',
        validation: { required: true, minLength: 3, maxLength: 20 }
      },
      {
        name: 'email',
        type: 'email',
        label: 'Email',
        placeholder: 'your@email.com',
        validation: { required: true, email: true }
      },
      {
        name: 'age',
        type: 'number',
        label: 'Age',
        placeholder: 'Enter your age',
        validation: { required: true, min: 13, max: 120 }
      },
      {
        name: 'role',
        type: 'select',
        label: 'Role',
        placeholder: 'Select your role',
        validation: { required: true },
        options: [
          { value: 'developer', label: 'Developer' },
          { value: 'designer', label: 'Designer' },
          { value: 'manager', label: 'Manager' },
          { value: 'other', label: 'Other' }
        ]
      }
    ],
    submitText: 'Create Account'
  };

  const handleSubmit = async (data: Record<string, FormFieldValue>) => {
    console.log('Registration form submitted:', data);
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  if (submitted) {
    return (
      <div className="text-center py-4">
        <div className="text-green-600 mb-2">🎉 Account created!</div>
        <p className="text-sm text-gray-600 dark:text-gray-400">Welcome to the platform!</p>
      </div>
    );
  }

  return <Form config={registrationFormConfig} onSubmit={handleSubmit} />;
};

// Newsletter Form Demo Component
const NewsletterFormDemo: React.FC = () => {
  const [submitted, setSubmitted] = useState(false);

  const newsletterFormConfig: FormConfig = {
    fields: [
      {
        name: 'email',
        type: 'email',
        label: 'Email Address',
        placeholder: 'Enter your email',
        validation: { required: true, email: true }
      }
    ],
    submitText: 'Subscribe'
  };

  const handleSubmit = async (data: Record<string, FormFieldValue>) => {
    console.log('Newsletter signup:', data);
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 3000);
  };

  if (submitted) {
    return (
      <div className="flex items-center justify-center py-4">
        <div className="flex items-center space-x-2 text-green-600">
          <span>✓</span>
          <span>Successfully subscribed!</span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-end space-x-4">
      <div className="flex-1">
        <Form config={newsletterFormConfig} onSubmit={handleSubmit} />
      </div>
    </div>
  );
};

export const DesignSystemDemo: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleLoadingDemo = () => {
    setIsLoading(true);
    setTimeout(() => setIsLoading(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Design System Demo
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Showcase of our Button, Card, and Form components
          </p>
        </div>

        {/* Button Variants Section */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Button Components
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card title="Button Variants">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Different styles for different use cases
              </p>
              <div className="space-y-3">
                <Button variant="primary">Primary</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="destructive">Destructive</Button>
              </div>
            </Card>

            <Card title="Button Sizes">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Different sizes for different contexts
              </p>
              <div className="space-y-3">
                <Button size="sm">Small</Button>
                <Button size="md">Medium</Button>
                <Button size="lg">Large</Button>
              </div>
            </Card>

            <Card title="Button States">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Loading and disabled states
              </p>
              <div className="space-y-3">
                <Button 
                  onClick={handleLoadingDemo}
                  isLoading={isLoading}
                >
                  {isLoading ? 'Loading...' : 'Click me'}
                </Button>
                <Button disabled>Disabled</Button>
              </div>
            </Card>
          </div>
        </section>

        {/* Card Variants Section */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Card Components
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card 
              variant="default" 
              title="Default Card"
              extra={<Button size="sm">Primary</Button>}
            >
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                Standard card with border
              </p>
              <p className="text-gray-700 dark:text-gray-300">
                This is a default card with standard styling and border.
              </p>
            </Card>

            <Card 
              variant="outline" 
              title="Outline Card"
              extra={
                <div className="space-x-2">
                  <Button size="sm" variant="ghost">Cancel</Button>
                  <Button size="sm" variant="primary">Confirm</Button>
                </div>
              }
            >
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                Transparent with outline border
              </p>
              <p className="text-gray-700 dark:text-gray-300">
                This card has a transparent background with a prominent outline.
              </p>
            </Card>

            <Card 
              variant="elevated" 
              title="Elevated Card"
              extra={<Button size="sm">View Details</Button>}
            >
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                Card with shadow elevation
              </p>
              <p className="text-gray-700 dark:text-gray-300 mb-3">
                This card uses shadow to create depth and emphasis.
              </p>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                Last updated: Today
              </span>
            </Card>
          </div>
        </section>

        {/* Complex Card Examples */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Complex Card Examples
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card 
              variant="elevated" 
              padding="lg"
              title={
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold">JD</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                      John Doe
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      Software Engineer
                    </p>
                  </div>
                </div>
              }
              extra={
                <div className="space-x-2">
                  <Button size="sm" variant="outline">Share</Button>
                  <Button size="sm">Reply</Button>
                </div>
              }
            >
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                "This design system makes building consistent UI components incredibly easy. 
                The components are well-designed and highly customizable."
              </p>
              <div className="flex space-x-2 mb-4">
                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full dark:bg-blue-900 dark:text-blue-200">
                  React
                </span>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full dark:bg-green-900 dark:text-green-200">
                  TypeScript
                </span>
                <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full dark:bg-purple-900 dark:text-purple-200">
                  Tailwind
                </span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400">
                <span>⭐ 5.0</span>
                <span>•</span>
                <span>2 days ago</span>
              </div>
            </Card>

            <Card 
              padding="none"
              title="Project Dashboard"
              extra={
                <div className="space-x-2">
                  <Button variant="ghost" size="sm">View All</Button>
                  <Button size="sm">Generate Report</Button>
                </div>
              }
            >
              <div className="h-48 bg-gradient-to-r from-blue-500 to-purple-600 mb-4"></div>
              <div className="px-6 pb-6">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  Real-time analytics and insights
                </p>
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600">127</div>
                    <div className="text-xs text-gray-500">Active Users</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">98%</div>
                    <div className="text-xs text-gray-500">Uptime</div>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </section>

        {/* Form Components Section */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Form Components
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card title="Contact Form" variant="elevated">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Simple contact form with validation
              </p>
              <ContactFormDemo />
            </Card>

            <Card title="User Registration" variant="elevated">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Complex form with all field types
              </p>
              <RegistrationFormDemo />
            </Card>
          </div>

          <div className="mt-6">
            <Card title="Newsletter Signup" variant="outline">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                Inline form layout example
              </p>
              <NewsletterFormDemo />
            </Card>
          </div>
        </section>

        {/* Cards without headers */}
        <section>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Simple Cards (No Header)
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card variant="default">
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                Simple Card
              </h4>
              <p className="text-gray-600 dark:text-gray-400">
                Card without header, just content.
              </p>
            </Card>

            <Card variant="outline" padding="lg">
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                Large Padding
              </h4>
              <p className="text-gray-600 dark:text-gray-400">
                This card has large padding for more breathing room.
              </p>
            </Card>

            <Card variant="elevated" padding="sm">
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                Small Padding
              </h4>
              <p className="text-gray-600 dark:text-gray-400">
                Compact card with small padding.
              </p>
            </Card>
          </div>
        </section>
      </div>
    </div>
  );
}; 