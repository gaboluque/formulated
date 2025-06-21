import { api, type PaginatedResponse } from "./client";
import type { Team } from "../types/team";

export const teamsApi = {
    getTeams: async (): Promise<PaginatedResponse<Team>> => {
        const response = await api.get<PaginatedResponse<Team>>('/teams');
        return response.data;
    },
    getTeam: async (id: string): Promise<Team> => {
        const response = await api.get<Team>(`/teams/${id}`);
        return response.data;
    }
}