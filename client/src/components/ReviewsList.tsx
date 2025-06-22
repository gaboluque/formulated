import { useState } from 'react';
import { Button } from './Button';
import { Card } from './Card';
import { ReviewForm } from './ReviewForm';
import { useAuth } from '../lib/contexts/AuthContext';
import type { Review, ReviewFormData } from '../lib/types/interactions';

export interface ReviewsListProps {
    reviews: Review[];
    loading: boolean;
    error: string | null;
    entityName: string; // e.g., "team", "race", "circuit", "member"
    showWriteButton?: boolean;
    canUserReview?: boolean;      // Controls if user can review (e.g., race must be finished)
    onCreateReview?: (data: ReviewFormData) => Promise<void>;
    onEditReview?: (data: ReviewFormData) => Promise<void>;
    onDeleteReview?: () => Promise<void>;
    className?: string;
    emptyStateMessage?: string;
}

export const ReviewsList = ({ 
    reviews, 
    loading, 
    error, 
    entityName,
    showWriteButton = true,
    canUserReview = true,
    onCreateReview,
    onEditReview,
    onDeleteReview,
    className,
    emptyStateMessage
}: ReviewsListProps) => {
    const { user } = useAuth();
    const [showForm, setShowForm] = useState(false);
    const [editingReview, setEditingReview] = useState<Review | null>(null);
    const [submitting, setSubmitting] = useState(false);

    const userReview = reviews.find(review => review.user === user?.username);

    const handleSubmitReview = async (data: ReviewFormData) => {
        if (!user) return;

        try {
            setSubmitting(true);
            if (editingReview && onEditReview) {
                await onEditReview(data);
            } else if (onCreateReview) {
                await onCreateReview(data);
            }
            setShowForm(false);
            setEditingReview(null);
        } catch (err) {
            console.error('Error submitting review:', err);
        } finally {
            setSubmitting(false);
        }
    };

    const handleDeleteReview = async () => {
        if (!user || !userReview || !onDeleteReview) return;

        if (!confirm('Are you sure you want to delete your review?')) {
            return;
        }

        try {
            await onDeleteReview();
        } catch (err) {
            console.error('Error deleting review:', err);
        }
    };

    const handleEdit = (review: Review) => {
        setEditingReview(review);
        setShowForm(true);
    };

    const handleCancelForm = () => {
        setShowForm(false);
        setEditingReview(null);
    };

    const renderStars = (rating: number) => {
        return (
            <div className="flex">
                {[1, 2, 3, 4, 5].map((star) => (
                    <span
                        key={star}
                        className={`text-lg ${
                            star <= rating ? 'text-yellow-400' : 'opacity-30'
                        }`}
                    >
                        ⭐
                    </span>
                ))}
            </div>
        );
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    if (loading) {
        return (
            <div className={`flex justify-center items-center py-8 ${className || ''}`}>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    return (
        <div className={`space-y-6 ${className || ''}`}>
            <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Reviews ({reviews.length})
                </h3>
                {user && showWriteButton && canUserReview && !userReview && !showForm && onCreateReview && (
                    <Button
                        onClick={() => setShowForm(true)}
                        variant="primary"
                        size="sm"
                    >
                        Write Review
                    </Button>
                )}
            </div>

            {error && (
                <div className="p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
                    <p className="text-red-800 dark:text-red-200">{error}</p>
                </div>
            )}

            {!user && (
                <Card className="p-6 text-center">
                    <p className="text-gray-500 dark:text-gray-400 mb-3">
                        Please log in to write a review
                    </p>
                    <a
                        href="/login"
                        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 dark:bg-blue-900 dark:text-blue-100 dark:hover:bg-blue-800"
                    >
                        Log In
                    </a>
                </Card>
            )}

            {user && !canUserReview && !userReview && (
                <Card className="p-6 text-center">
                    <p className="text-gray-500 dark:text-gray-400">
                        Reviews will be available after the {entityName} is completed
                    </p>
                </Card>
            )}

            {showForm && user && (
                <Card className="p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h4 className="text-md font-medium text-gray-900 dark:text-white">
                            {editingReview ? 'Edit Your Review' : 'Write a Review'}
                        </h4>
                        <Button
                            onClick={handleCancelForm}
                            variant="outline"
                            size="sm"
                        >
                            Cancel
                        </Button>
                    </div>
                    <ReviewForm
                        onSubmit={handleSubmitReview}
                        initialData={editingReview || undefined}
                        isEditing={!!editingReview}
                        loading={submitting}
                        placeholder={`Share your thoughts about this ${entityName}...`}
                    />
                </Card>
            )}

            <div className="space-y-4">
                {reviews.length === 0 ? (
                    <Card className="p-6 text-center">
                        <div className="text-gray-500 dark:text-gray-400">
                            <svg className="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                            </svg>
                            <h3 className="text-lg font-medium mb-2">No reviews yet</h3>
                            <p>{emptyStateMessage || `Be the first to review this ${entityName}!`}</p>
                        </div>
                    </Card>
                ) : (
                    reviews.map((review) => (
                        <Card key={review.id} className="p-6">
                            <div className="flex justify-between items-start mb-3">
                                <div>
                                    <div className="flex items-center gap-3 mb-2">
                                        <span className="font-medium text-gray-900 dark:text-white">
                                            {review.user}
                                        </span>
                                        {renderStars(review.rating)}
                                    </div>
                                    <span className="text-sm text-gray-500 dark:text-gray-400">
                                        {formatDate(review.created_at)}
                                        {review.updated_at !== review.created_at && (
                                            <span className="ml-2">(edited)</span>
                                        )}
                                    </span>
                                </div>
                                {user && review.user === user.username && (
                                    <div className="flex gap-2">
                                        {onEditReview && (
                                            <Button
                                                onClick={() => handleEdit(review)}
                                                variant="outline"
                                                size="sm"
                                            >
                                                Edit
                                            </Button>
                                        )}
                                        {onDeleteReview && (
                                            <Button
                                                onClick={handleDeleteReview}
                                                variant="outline"
                                                size="sm"
                                                className="text-red-600 hover:text-red-700 dark:text-red-400"
                                            >
                                                Delete
                                            </Button>
                                        )}
                                    </div>
                                )}
                            </div>
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed whitespace-pre-wrap">
                                {review.description}
                            </p>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}; 