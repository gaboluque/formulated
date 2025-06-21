export type TeamStatus = 'active' | 'inactive';

export type MemberRole = 'driver' | 'engineer' | 'manager' | 'other';

export type Member = {
    id: string;
    name: string;
    role: MemberRole;
    description: string;
    team: string;
    team_url: string;
    created_at: string;
    updated_at: string;
};

export type Team = {
    id: string;
    name: string;
    description: string;
    status: TeamStatus;
    members?: Member[];
    created_at: string;
    updated_at: string;
}; 