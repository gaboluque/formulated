import { useState } from 'react';
import { MemberCard } from '../components/members/MemberCard';
import { Button } from '../components/Button';
import type { Member, MemberRole } from '../lib/types/teams';
import { useLoaderData } from 'react-router';

interface LoaderData {
    members: Member[]
}

export const MembersListPage = () => {
    const { members } = useLoaderData() as LoaderData;
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedRole, setSelectedRole] = useState<MemberRole | 'all'>('all');

    const roles: (MemberRole | 'all')[] = ['all', 'driver', 'engineer', 'manager', 'other'];

    const filteredMembers = members.filter(member => {
        const matchesSearch = member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                            member.description.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesRole = selectedRole === 'all' || member.role === selectedRole;
        return matchesSearch && matchesRole;
    });

    const getRoleIcon = (role: string) => {
        switch (role) {
            case 'driver':
                return '🏎️';
            case 'engineer':
                return '🔧';
            case 'manager':
                return '👔';
            case 'other':
                return '👤';
            default:
                return '👥';
        }
    };

    return (
        <>
            {/* Page Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                    F1 Team Members
                </h1>
                <p className="text-gray-600 dark:text-gray-300">
                    Discover Formula 1 team members, from drivers to engineers, and see what the community thinks about their contributions.
                </p>
            </div>

            {/* Search and Filters */}
            <div className="mb-8 space-y-4">
                {/* Search */}
                <div>
                    <input
                        type="text"
                        placeholder="Search members by name or description..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                </div>

                {/* Role Filter */}
                <div className="flex flex-wrap gap-2">
                    {roles.map((role) => (
                        <Button
                            key={role}
                            onClick={() => setSelectedRole(role)}
                            variant={selectedRole === role ? 'primary' : 'outline'}
                            size="sm"
                            className="flex items-center gap-2"
                        >
                            <span>{getRoleIcon(role)}</span>
                            <span className="capitalize">{role === 'all' ? 'All Members' : role}</span>
                        </Button>
                    ))}
                </div>
            </div>

            {/* Results Summary */}
            <div className="mb-6">
                <p className="text-gray-600 dark:text-gray-300">
                    {filteredMembers.length === members.length
                        ? `Showing all ${members.length} member${members.length !== 1 ? 's' : ''}`
                        : `Showing ${filteredMembers.length} of ${members.length} member${members.length !== 1 ? 's' : ''}`
                    }
                </p>
            </div>

            {/* Members grid */}
            {filteredMembers.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {filteredMembers.map((member) => (
                        <MemberCard key={member.id} member={member} />
                    ))}
                </div>
            ) : (
                <div className="text-center py-12">
                    <div className="text-gray-400 dark:text-gray-500 text-6xl mb-4">👤</div>
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                        No members found
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300">
                        Try adjusting your search terms or filters to find what you're looking for.
                    </p>
                </div>
            )}
        </>
    );
}; 