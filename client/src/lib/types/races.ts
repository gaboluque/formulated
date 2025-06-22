import type { Member } from "./teams";

export type Circuit = {
    url: string;
    id: string;
    name: string;
    location: string;
    created_at: string;
    updated_at: string;
};

export type Position = {
    url: string;
    id: string;
    race: string;
    race_url: string;
    driver: Member;
    driver_url: string;
    position: number;
    points: number;
    created_at: string;
    updated_at: string;
};

export type Race = {
    url: string;
    id: string;
    name: string;
    description: string;
    circuit: Circuit;
    circuit_url: string;
    start_at: string;
    status: 'scheduled' | 'ongoing' | 'completed' | 'cancelled';
    positions: Position[];
    created_at: string;
    updated_at: string;
}; 