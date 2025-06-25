import { api, type PaginatedResponse } from "./client";
import type { Race, Circuit, Position, RaceStatus } from "../types/races";
import type { Like, Review, ReviewFormData, LikeResponse } from "../types/interactions";

export interface RaceFilters {
    circuit_id?: string;
    status?: RaceStatus;
    year?: number;
    season?: number;
    upcoming?: boolean;
    completed?: boolean;
}

export interface CircuitFilters {
    location?: string;
}

export interface PositionFilters {
    race_id?: string;
    driver_id?: string;
    team_id?: string;
    position?: number;
    year?: number;
    season?: number;
    min_points?: number;
}

export const racesApi = {
    // Race operations
    getRaces: async (filters?: RaceFilters): Promise<PaginatedResponse<Race>> => {
        const params: Record<string, string> = {};
        
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined) {
                    params[key] = String(value);
                }
            });
        }
        
        const response = await api.get<PaginatedResponse<Race>>('/races/', { params });
        return response.data;
    },

    getRace: async (id: string): Promise<Race> => {
        const response = await api.get<Race>(`/races/${id}/`);
        return response.data;
    },

    // Convenience methods for common race queries
    getUpcomingRaces: async (): Promise<PaginatedResponse<Race>> => {
        return racesApi.getRaces({ upcoming: true });
    },

    getCompletedRaces: async (year?: number): Promise<PaginatedResponse<Race>> => {
        return racesApi.getRaces({ completed: true, year });
    },

    getRacesByCircuit: async (circuitId: string): Promise<PaginatedResponse<Race>> => {
        return racesApi.getRaces({ circuit_id: circuitId });
    },

    getRacesBySeason: async (season: number): Promise<PaginatedResponse<Race>> => {
        return racesApi.getRaces({ season });
    },

    // Circuit operations
    getCircuits: async (filters?: CircuitFilters): Promise<PaginatedResponse<Circuit>> => {
        const params: Record<string, string> = {};
        
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined) {
                    params[key] = String(value);
                }
            });
        }
        
        const response = await api.get<PaginatedResponse<Circuit>>('/circuits/', { params });
        return response.data;
    },

    getCircuit: async (id: string): Promise<Circuit> => {
        const response = await api.get<Circuit>(`/circuits/${id}/`);
        return response.data;
    },

    // Position operations
    getPositions: async (filters?: PositionFilters): Promise<PaginatedResponse<Position>> => {
        const params: Record<string, string> = {};
        
        if (filters) {
            Object.entries(filters).forEach(([key, value]) => {
                if (value !== undefined) {
                    params[key] = String(value);
                }
            });
        }
        
        const response = await api.get<PaginatedResponse<Position>>('/positions/', { params });
        return response.data;
    },

    // Convenience methods for positions
    getRaceResults: async (raceId: string): Promise<PaginatedResponse<Position>> => {
        return racesApi.getPositions({ race_id: raceId });
    },

    getDriverResults: async (driverId: string, season?: number): Promise<PaginatedResponse<Position>> => {
        return racesApi.getPositions({ driver_id: driverId, season });
    },

    getTeamResults: async (teamId: string, season?: number): Promise<PaginatedResponse<Position>> => {
        return racesApi.getPositions({ team_id: teamId, season });
    },

    getRaceWinners: async (season?: number): Promise<PaginatedResponse<Position>> => {
        return racesApi.getPositions({ position: 1, season });
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