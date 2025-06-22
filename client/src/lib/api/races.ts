import { api, type PaginatedResponse } from "./client";
import type { Race, Circuit } from "../types/races";
import type { Like, Review, ReviewFormData, LikeResponse } from "../types/interactions";

export const racesApi = {
    // Race operations
    getRaces: async (params?: Record<string, string>): Promise<PaginatedResponse<Race>> => {
        const response = await api.get<PaginatedResponse<Race>>('/races/', { params });
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
    },

    // Like operations for circuits
    checkCircuitLike: async (circuitId: string): Promise<LikeResponse> => {
        const response = await api.get<LikeResponse>(`/circuits/${circuitId}/likes/`);
        return response.data;
    },

    likeCircuit: async (circuitId: string): Promise<Like> => {
        const response = await api.post<Like>(`/circuits/${circuitId}/likes/`, {});
        return response.data;
    },

    unlikeCircuit: async (circuitId: string): Promise<void> => {
        await api.delete(`/circuits/${circuitId}/likes/`);
    },

    // Review operations for circuits
    getCircuitReviews: async (circuitId: string): Promise<Review[]> => {
        const response = await api.get<Review[]>(`/circuits/${circuitId}/reviews/`);
        return response.data;
    },

    createCircuitReview: async (circuitId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.post<Review>(`/circuits/${circuitId}/reviews/`, reviewData);
        return response.data;
    },

    updateCircuitReview: async (circuitId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.put<Review>(`/circuits/${circuitId}/reviews/`, reviewData);
        return response.data;
    },

    deleteCircuitReview: async (circuitId: string): Promise<void> => {
        await api.delete(`/circuits/${circuitId}/reviews/`);
    }
}; 