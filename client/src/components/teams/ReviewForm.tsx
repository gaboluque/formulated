import { ReviewForm as GenericReviewForm } from '../ReviewForm';
import type { ReviewFormData, Review } from '../../lib/types/interactions';

export interface ReviewFormProps {
    onSubmit: (data: ReviewFormData) => Promise<void>;
    initialData?: Review;
    isEditing?: boolean;
    loading?: boolean;
}

export const ReviewForm = ({ onSubmit, initialData, isEditing = false, loading = false }: ReviewFormProps) => {
    return (
        <GenericReviewForm
            onSubmit={onSubmit}
            initialData={initialData}
            isEditing={isEditing}
            loading={loading}
            placeholder="Share your thoughts about this team..."
            defaultRating={1} // Teams start at 1 by default
        />
    );
}; 