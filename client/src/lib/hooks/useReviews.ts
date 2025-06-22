import { useState, useEffect } from 'react';
import type { Review, ReviewFormData } from '../types/interactions';

interface ReviewsApi {
  getReviews: (id: string) => Promise<Review[]>;
  createReview: (id: string, reviewData: ReviewFormData) => Promise<Review | void>;
  updateReview?: (id: string, reviewData: ReviewFormData) => Promise<Review | void>;
  deleteReview: (id: string) => Promise<void>;
}

interface UseReviewsOptions {
  entityId: string;
  api: ReviewsApi;
}

export const useReviews = ({ entityId, api }: UseReviewsOptions) => {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadReviews = async () => {
    try {
      setLoading(true);
      setError(null);
      const reviewsData = await api.getReviews(entityId);
      setReviews(reviewsData);
    } catch (err) {
      setError('Failed to load reviews');
      console.error('Error loading reviews:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (entityId) {
      loadReviews();
    }
  }, [entityId]);

  const handleCreateReview = async (reviewData: ReviewFormData) => {
    await api.createReview(entityId, reviewData);
    await loadReviews(); // Refresh reviews
  };

  const handleEditReview = api.updateReview ? async (reviewData: ReviewFormData) => {
    await api.updateReview!(entityId, reviewData);
    await loadReviews(); // Refresh reviews
  } : undefined;

  const handleDeleteReview = async () => {
    await api.deleteReview(entityId);
    await loadReviews(); // Refresh reviews
  };

  return {
    reviews,
    loading,
    error,
    handleCreateReview,
    handleEditReview,
    handleDeleteReview,
    refetchReviews: loadReviews
  };
}; 