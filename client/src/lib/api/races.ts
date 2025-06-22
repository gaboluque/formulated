import { api, type PaginatedResponse } from "./client";
import type { Race, Circuit } from "../types/races";
import type { Like, Review, ReviewFormData, LikeResponse } from "../types/interactions";

export const racesApi = {
    // Race operations
    getRaces: async (): Promise<PaginatedResponse<Race>> => {
        const response = await api.get<PaginatedResponse<Race>>('/races/');
        return response.data;
    },

    getRace: async (id: string): Promise<Race> => {
        const response = await api.get<Race>(`/races/${id}/`);
        return response.data;
    },

    // Circuit operations
    getCircuits: async (): Promise<PaginatedResponse<Circuit>> => {
        const response = await api.get<PaginatedResponse<Circuit>>('/circuits/');
        return response.data;
    },

    getCircuit: async (id: string): Promise<Circuit> => {
        const response = await api.get<Circuit>(`/circuits/${id}/`);
        return response.data;
    },

    // Like operations for races
    checkLike: async (raceId: string): Promise<LikeResponse> => {
        const response = await api.get<LikeResponse>(`/races/${raceId}/likes/`);
        return response.data;
    },

    likeRace: async (raceId: string): Promise<Like> => {
        const response = await api.post<Like>(`/races/${raceId}/likes/`, {});
        return response.data;
    },

    unlikeRace: async (raceId: string): Promise<void> => {
        await api.delete(`/races/${raceId}/likes/`);
    },

    // Review operations for races
    getReviews: async (raceId: string): Promise<Review[]> => {
        const response = await api.get<Review[]>(`/races/${raceId}/reviews/`);
        return response.data;
    },

    createReview: async (raceId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.post<Review>(`/races/${raceId}/reviews/`, reviewData);
        return response.data;
    },

    updateReview: async (raceId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.put<Review>(`/races/${raceId}/reviews/`, reviewData);
        return response.data;
    },

    deleteReview: async (raceId: string): Promise<void> => {
        await api.delete(`/races/${raceId}/reviews/`);
    }
}; 