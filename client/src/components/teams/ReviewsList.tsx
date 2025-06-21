import { useState, useEffect } from 'react';
import { Button } from '../Button';
import { Card } from '../Card';
import { ReviewForm } from './ReviewForm';
import { teamsApi } from '../../lib/api/teams';
import { useAuth } from '../../lib/contexts/AuthContext';
import type { Review, ReviewFormData } from '../../lib/types/interactions';

export interface ReviewsListProps {
    teamId: string;
}

export const ReviewsList = ({ teamId }: ReviewsListProps) => {
    const { user } = useAuth();
    const [reviews, setReviews] = useState<Review[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showForm, setShowForm] = useState(false);
    const [editingReview, setEditingReview] = useState<Review | null>(null);
    const [submitting, setSubmitting] = useState(false);

    const userReview = reviews.find(review => review.user === user?.username);

    useEffect(() => {
        loadReviews();
    }, [teamId]);

    const loadReviews = async () => {
        try {
            setLoading(true);
            const reviewsData = await teamsApi.getReviews(teamId);
            setReviews(reviewsData);
        } catch (err) {
            console.error('Error loading reviews:', err);
            setError('Failed to load reviews');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitReview = async (data: ReviewFormData) => {
        if (!user) return;

        try {
            setSubmitting(true);
            if (editingReview) {
                await teamsApi.updateReview(teamId, data);
            } else {
                await teamsApi.createReview(teamId, data);
            }
            await loadReviews();
            setShowForm(false);
            setEditingReview(null);
        } catch (err) {
            console.error('Error submitting review:', err);
            setError('Failed to submit review');
        } finally {
            setSubmitting(false);
        }
    };

    const handleDeleteReview = async () => {
        if (!user || !userReview) return;

        if (!confirm('Are you sure you want to delete your review?')) {
            return;
        }

        try {
            await teamsApi.deleteReview(teamId);
            await loadReviews();
        } catch (err) {
            console.error('Error deleting review:', err);
            setError('Failed to delete review');
        }
    };

    const handleEdit = (review: Review) => {
        setEditingReview(review);
        setShowForm(true);
    };

    const renderStars = (rating: number) => {
        return (
            <div className="flex">
                {[1, 2, 3, 4, 5].map((star) => (
                    <span
                        key={star}
                        className={`text-lg ${
                            star <= rating ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'
                        }`}
                    >
                        ⭐
                    </span>
                ))}
            </div>
        );
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center py-8">
                <div className="text-gray-500 dark:text-gray-400">Loading reviews...</div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Reviews ({reviews.length})
                </h3>
                {user && !userReview && !showForm && (
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

            {showForm && (
                <Card className="p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h4 className="text-md font-medium text-gray-900 dark:text-white">
                            {editingReview ? 'Edit Your Review' : 'Write a Review'}
                        </h4>
                        <Button
                            onClick={() => {
                                setShowForm(false);
                                setEditingReview(null);
                            }}
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
                    />
                </Card>
            )}

            <div className="space-y-4">
                {reviews.length === 0 ? (
                    <Card className="p-6 text-center">
                        <p className="text-gray-500 dark:text-gray-400">
                            No reviews yet. Be the first to review this team!
                        </p>
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
                                        {new Date(review.created_at).toLocaleDateString()}
                                        {review.updated_at !== review.created_at && (
                                            <span className="ml-2">(edited)</span>
                                        )}
                                    </span>
                                </div>
                                {user && review.user === user.username && (
                                    <div className="flex gap-2">
                                        <Button
                                            onClick={() => handleEdit(review)}
                                            variant="outline"
                                            size="sm"
                                        >
                                            Edit
                                        </Button>
                                        <Button
                                            onClick={handleDeleteReview}
                                            variant="outline"
                                            size="sm"
                                            className="text-red-600 hover:text-red-700 dark:text-red-400"
                                        >
                                            Delete
                                        </Button>
                                    </div>
                                )}
                            </div>
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                                {review.description}
                            </p>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}; 