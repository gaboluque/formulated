export type Like = {
    id: string;
    user: string;
    record_type: string;
    record_id: string;
    created_at: string;
};

export type Review = {
    id: string;
    user: string;
    rating: number;
    description: string;
    record_type: string;
    record_id: string;
    created_at: string;
    updated_at: string;
};

export type ReviewFormData = {
    rating: number;
    description: string;
};

export type LikeResponse = {
    liked: boolean;
};

export type ReviewsResponse = {
    reviews: Review[];
    count: number;
}; 