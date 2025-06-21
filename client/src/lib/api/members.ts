import { api, type PaginatedResponse } from "./client";
import type { Member } from "../types/teams";
import type { Like, Review, ReviewFormData, LikeResponse } from "../types/interactions";

export const membersApi = {
    // Member operations
    getMembers: async (): Promise<PaginatedResponse<Member>> => {
        const response = await api.get<PaginatedResponse<Member>>('/members/');
        return response.data;
    },

    getMember: async (id: string): Promise<Member> => {
        const response = await api.get<Member>(`/members/${id}/`);
        return response.data;
    },

    // Like operations
    checkLike: async (memberId: string): Promise<LikeResponse> => {
        const response = await api.get<LikeResponse>(`/members/${memberId}/likes/`);
        return response.data;
    },

    likeMember: async (memberId: string): Promise<Like> => {
        const response = await api.post<Like>(`/members/${memberId}/likes/`, {});
        return response.data;
    },

    unlikeMember: async (memberId: string): Promise<void> => {
        await api.delete(`/members/${memberId}/likes/`);
    },

    // Review operations
    getReviews: async (memberId: string): Promise<Review[]> => {
        const response = await api.get<Review[]>(`/members/${memberId}/reviews/`);
        return response.data;
    },

    createReview: async (memberId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.post<Review>(`/members/${memberId}/reviews/`, reviewData);
        return response.data;
    },

    updateReview: async (memberId: string, reviewData: ReviewFormData): Promise<Review> => {
        const response = await api.put<Review>(`/members/${memberId}/reviews/`, reviewData);
        return response.data;
    },

    deleteReview: async (memberId: string): Promise<void> => {
        await api.delete(`/members/${memberId}/reviews/`);
    }
}; 