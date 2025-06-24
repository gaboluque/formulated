export type TeamStatus = 'active' | 'inactive';

export type MemberRole = 'driver' | 'engineer' | 'manager' | 'other';

export type Member = {
    url: string;
    id: string;
    name: string;
    role: MemberRole;
    description: string;
    team: Team;
    created_at: string;
    updated_at: string;
    // Driver-specific fields
    driver_number?: number;
    name_acronym?: string;
    country_code?: string;
    headshot_url?: string;
};

export type TeamMember = {
    url: string;
    id: string;
    name: string;
    role: MemberRole;
    description: string;
    created_at: string;
    updated_at: string;
    // Driver-specific fields
    driver_number?: number;
    name_acronym?: string;
    country_code?: string;
    headshot_url?: string;
};

export type Team = {
    url: string;
    id: string;
    name: string;
    description: string;
    status: TeamStatus;
    members?: TeamMember[];
    created_at: string;
    updated_at: string;
    logo_url?: string;
    base?: string;
    first_team_entry?: number;
    world_championships?: number;
    highest_race_finish?: number;
    pole_positions?: number;
    fastest_laps?: number;
    president?: string;
    director?: string;
    technical_manager?: string;
    chassis?: string;
    engine?: string;
    tyres?: string;
}; 