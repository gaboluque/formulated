import { api, type PaginatedResponse } from "./client";
import type { Team } from "../types/teams";
import type { Like, Review, ReviewFormData, LikeResponse } from "../types/interactions";

export const teamsApi = {
    // Team operations
    getTeams: async (): Promise<PaginatedResponse<Team>> => {
        const response = await api.get<PaginatedResponse<Team>>('/teams/');
        return response.data;
    },

    getTeam: async (id: string): Promise<Team> => {
        const response = await api.get<Team>(`/teams/${id}/`);
        return response.data;
    },

    // Like operations
    checkLike: async (teamId: string): Promise<LikeResponse> => {
        const response = await api.get<LikeResponse>(`/teams/${teamId}/likes/`);
        return response.data;
    },

    likeTeam: async (teamId: string): Promise<Like> => {
        const response = await api.post<Like>(`/teams/${teamId}/likes/`, {});
        return response.data;
    },

    unlikeTeam: async (teamId: string): Promise<void> => {
        await api.delete(`/teams/${teamId}/likes/`);
    },

    // Review operations
    getReviews: async (teamId: string): Promise<Review[]> => {
        const response = await api.get<Review[]>(`/teams/${teamId}/reviews/`);
        return response.data;
    },

    createReview: async (teamId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.post<Review>(`/teams/${teamId}/reviews/`, reviewData);
        return response.data;
    },

    updateReview: async (teamId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.put<Review>(`/teams/${teamId}/reviews/`, reviewData);
        return response.data;
    },

    deleteReview: async (teamId: string): Promise<void> => {
        await api.delete(`/teams/${teamId}/reviews/`);
    }
};