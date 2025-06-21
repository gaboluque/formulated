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
};

export type TeamMember = {
    url: string;
    id: string;
    name: string;
    role: MemberRole;
    description: string;
    created_at: string;
    updated_at: string;
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
}; 