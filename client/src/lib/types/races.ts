export type RaceStatus = 'scheduled' | 'ongoing' | 'completed' | 'cancelled';

export type CircuitRace = {
    url: string;
    id: string;
    name: string;
    description: string;
    start_at: string;
    status: RaceStatus;
    created_at: string;
    updated_at: string;
};

export type Circuit = {
    url: string;
    id: string;
    name: string;
    location: string;
    races: CircuitRace[];
    races_count: number;
    upcoming_races_count: number;
    completed_races_count: number;
    created_at: string;
    updated_at: string;
};

export type RacePosition = {
    url: string;
    id: string;
    position: number;
    points: number;
    driver_url: string;
    driver_name: string;
    driver_number: string;
    driver_acronym: string;
    team_name: string;
    team_url: string;
    created_at: string;
    updated_at: string;
};

export type Race = {
    url: string;
    id: string;
    name: string;
    description: string;
    start_at: string;
    status: RaceStatus;
    is_finished: boolean;
    circuit: Circuit;
    circuit_url: string;
    positions: RacePosition[];
    positions_count: number;
    created_at: string;
    updated_at: string;
};

export type Position = {
    url: string;
    id: string;
    position: number;
    points: number;
    race: Race;
    race_url: string;
    driver_url: string;
    driver_name: string;
    driver_number: string;
    driver_acronym: string;
    team_name: string;
    team_url: string;
    created_at: string;
    updated_at: string;
}; 