export type Circuit = {
    id: string;
    name: string;
    location: string;
    country: string;
    length: number;
    created_at: string;
    updated_at: string;
};

export type Race = {
    id: string;
    name: string;
    circuit: string;
    circuit_url: string;
    date: string;
    status: 'scheduled' | 'ongoing' | 'completed' | 'cancelled';
    created_at: string;
    updated_at: string;
};

export type Position = {
    id: string;
    race: string;
    race_url: string;
    team: string;
    team_url: string;
    position: number;
    points: number;
    created_at: string;
    updated_at: string;
}; 