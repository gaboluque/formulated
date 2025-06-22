import { ReviewForm } from '../ReviewForm';
import type { ReviewFormData, Review } from '../../lib/types/interactions';

export interface MemberReviewFormProps {
    onSubmit: (data: ReviewFormData) => Promise<void>;
    initialData?: Review;
    isEditing?: boolean;
    loading?: boolean;
}

export const MemberReviewForm = ({ onSubmit, initialData, isEditing = false, loading = false }: MemberReviewFormProps) => {
    return (
        <ReviewForm
            onSubmit={onSubmit}
            initialData={initialData}
            isEditing={isEditing}
            loading={loading}
            placeholder="Share your thoughts about this member's performance, skills, or contribution..."
            defaultRating={5}
        />
    );
}; 