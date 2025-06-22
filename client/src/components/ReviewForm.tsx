import { useState } from 'react';
import { Button } from './Button';
import type { ReviewFormData, Review } from '../lib/types/interactions';

export interface ReviewFormProps {
    onSubmit: (data: ReviewFormData) => Promise<void>;
    initialData?: Review;
    isEditing?: boolean;
    loading?: boolean;
    placeholder?: string;
    defaultRating?: number;
    disabled?: boolean;
    disabledMessage?: string;
}

export const ReviewForm = ({ 
    onSubmit, 
    initialData, 
    isEditing = false, 
    loading = false,
    placeholder = "Share your thoughts...",
    defaultRating = 5,
    disabled = false,
    disabledMessage
}: ReviewFormProps) => {
    const [formData, setFormData] = useState<ReviewFormData>({
        rating: initialData?.rating || defaultRating,
        description: initialData?.description || '',
    });
    const [errors, setErrors] = useState<Partial<ReviewFormData>>({});

    const validateForm = (): boolean => {
        const newErrors: Partial<ReviewFormData> = {};

        if (formData.rating < 1 || formData.rating > 5) {
            newErrors.rating = 1; // Reset to minimum valid rating
        }

        if (!formData.description.trim()) {
            newErrors.description = 'Description is required';
        } else if (formData.description.length < 10) {
            newErrors.description = 'Description must be at least 10 characters';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        try {
            await onSubmit(formData);
        } catch (error) {
            console.error('Error submitting review:', error);
        }
    };

    const handleRatingChange = (rating: number) => {
        setFormData(prev => ({ ...prev, rating }));
        if (errors.rating) {
            setErrors(prev => ({ ...prev, rating: undefined }));
        }
    };

    if (disabled && disabledMessage) {
        return (
            <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                <p className="text-center text-yellow-800 dark:text-yellow-400">
                    {disabledMessage}
                </p>
            </div>
        );
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Rating
                </label>
                <div className="flex gap-1">
                    {[1, 2, 3, 4, 5].map((star) => (
                        <button
                            key={star}
                            type="button"
                            onClick={() => handleRatingChange(star)}
                            disabled={disabled}
                            className={`text-2xl transition-colors ${
                                star <= formData.rating
                                    ? 'text-yellow-400 hover:text-yellow-500'
                                    : 'opacity-30 hover:text-gray-400 dark:text-gray-600 dark:hover:text-gray-500'
                            } ${disabled ? 'cursor-not-allowed opacity-50' : ''}`}
                        >
                            ⭐
                        </button>
                    ))}
                </div>
                {errors.rating && (
                    <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                        {errors.rating}
                    </p>
                )}
            </div>

            <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Review *
                </label>
                <textarea
                    id="description"
                    value={formData.description}
                    onChange={(e) => {
                        setFormData(prev => ({ ...prev, description: e.target.value }));
                        if (errors.description) {
                            setErrors(prev => ({ ...prev, description: undefined }));
                        }
                    }}
                    placeholder={placeholder}
                    rows={4}
                    disabled={disabled}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white disabled:cursor-not-allowed disabled:opacity-50"
                />
                {errors.description && (
                    <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                        {errors.description}
                    </p>
                )}
            </div>

            <div className="flex gap-3">
                <Button
                    type="submit"
                    disabled={loading || disabled}
                    variant="primary"
                >
                    {loading ? 'Submitting...' : isEditing ? 'Update Review' : 'Submit Review'}
                </Button>
            </div>
        </form>
    );
}; 