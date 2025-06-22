import { ReviewForm } from '../ReviewForm';
import type { ReviewFormData, Review } from '../../lib/types/interactions';
import type { Race } from '../../lib/types/races';

export interface RaceReviewFormProps {
    race: Race;
    onSubmit: (data: ReviewFormData) => Promise<void>;
    initialData?: Review;
    isEditing?: boolean;
    loading?: boolean;
}

export const RaceReviewForm = ({ race, onSubmit, initialData, isEditing = false, loading = false }: RaceReviewFormProps) => {
    const isRaceFinished = () => {
        const raceDate = new Date(race.start_at);
        const now = new Date();
        return race.status === 'completed' || raceDate < now;
    };

    const raceFinished = isRaceFinished();

    return (
        <ReviewForm
            onSubmit={onSubmit}
            initialData={initialData}
            isEditing={isEditing}
            loading={loading}
            placeholder="Share your thoughts about this race..."
            defaultRating={5}
            disabled={!raceFinished}
            disabledMessage="You can only review races that have finished"
        />
    );
}; 