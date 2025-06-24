import { Link } from 'react-router';
import { Card } from '../Card';
import { Button } from '../Button';
import type { Team } from '../../lib/types/teams';

export interface TeamCardProps {
    team: Team;
}

export const TeamCard = ({ team }: TeamCardProps) => {
    const getStatusColor = (status: string) => {
        switch (status) {
            case 'active':
                return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20';
            case 'inactive':
                return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
            default:
                return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
        }
    };

    return (
        <Card className="p-6 hover:shadow-lg transition-all duration-200 hover:scale-[1.02] h-full flex flex-col">
            {/* Header with logo and team name - Fixed height */}
            <div className="flex items-start gap-4 mb-4 min-h-[60px]">
                {team.logo_url ? (
                    <img
                        src={team.logo_url}
                        alt={`${team.name} logo`}
                        className="w-12 h-12 object-contain rounded-full p-1 bg-white flex-shrink-0"
                    />
                ) : (
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0">
                        <span className="text-white font-bold text-lg">
                            {team.name.charAt(0)}
                        </span>
                    </div>
                )}
                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1 line-clamp-1">
                                {team.name}
                            </h3>
                            <div className="min-h-[20px]">
                                {team.base ? (
                                    <p className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
                                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                        </svg>
                                        {team.base}
                                    </p>
                                ) : (
                                    <p className="text-sm text-transparent select-none">-</p>
                                )}
                            </div>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(team.status)} flex-shrink-0 ml-2`}>
                            {team.status}
                        </span>
                    </div>
                </div>
            </div>

            {/* Description - Fixed height */}
            <div className="mb-4 h-[40px] flex items-start">
                <p className="text-gray-600 dark:text-gray-300 line-clamp-2 text-sm leading-relaxed">
                    {team.description || 'No description available.'}
                </p>
            </div>

            {/* Key Stats - Always present */}
            <div className="grid grid-cols-2 gap-4 mb-4">
                {/* Championships */}
                <div className={`rounded-lg p-3 border ${
                    team.world_championships !== undefined && team.world_championships > 0
                        ? 'bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 border-yellow-200 dark:border-yellow-800'
                        : 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700'
                }`}>
                    <div className="flex items-center gap-2 min-h-[20px]">
                        <svg className={`w-4 h-4 ${
                            team.world_championships !== undefined && team.world_championships > 0
                                ? 'text-yellow-600 dark:text-yellow-400'
                                : 'text-gray-400 dark:text-gray-500'
                        }`} fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        <span className={`text-sm font-medium ${
                            team.world_championships !== undefined && team.world_championships > 0
                                ? 'text-yellow-800 dark:text-yellow-200'
                                : 'text-gray-600 dark:text-gray-400'
                        }`}>
                            {team.world_championships !== undefined && team.world_championships > 0
                                ? `${team.world_championships} Championship${team.world_championships !== 1 ? 's' : ''}`
                                : '0 Championships'
                            }
                        </span>
                    </div>
                </div>

                {/* First Team Entry */}
                <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                    <div className="flex items-center gap-2 min-h-[20px]">
                        <svg className="w-4 h-4 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {team.first_team_entry ? `Since ${team.first_team_entry}` : 'Entry date unknown'}
                        </span>
                    </div>
                </div>
            </div>

            {/* Technical Info - Always present */}
            <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 min-h-[72px]">
                <div className="grid grid-cols-1 gap-2 text-sm">
                    <div className="flex justify-between">
                        <span className="text-blue-600 dark:text-blue-400 font-medium">Engine:</span>
                        <span className="text-blue-800 dark:text-blue-200">
                            {team.engine || 'Not specified'}
                        </span>
                    </div>
                    <div className="flex justify-between">
                        <span className="text-blue-600 dark:text-blue-400 font-medium">Chassis:</span>
                        <span className="text-blue-800 dark:text-blue-200">
                            {team.chassis || 'Not specified'}
                        </span>
                    </div>
                </div>
            </div>

            {/* Members - Always present with fixed height */}
            <div className="mb-4 min-h-[60px]">
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                    {team.members && team.members.length > 0 
                        ? `${team.members.length} member${team.members.length !== 1 ? 's' : ''}`
                        : '0 members'
                    }
                </p>
                <div className="flex flex-wrap gap-1 min-h-[28px] items-start">
                    {team.members && team.members.length > 0 ? (
                        <>
                            {team.members.slice(0, 3).map((member) => (
                                <span
                                    key={member.id}
                                    className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400"
                                >
                                    {member.name_acronym || member.name.split(' ').map(n => n[0]).join('')}
                                </span>
                            ))}
                            {team.members.length > 3 && (
                                <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600 dark:bg-gray-900/20 dark:text-gray-400">
                                    +{team.members.length - 3} more
                                </span>
                            )}
                        </>
                    ) : (
                        <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-500 dark:bg-gray-900/20 dark:text-gray-500">
                            No members
                        </span>
                    )}
                </div>
            </div>

            {/* Bottom section - Pushed to bottom */}
            <div className="flex justify-between items-center mt-auto">
                <Link to={`/teams/${team.id}`}>
                    <Button variant="outline" size="sm" className="hover:bg-blue-50 hover:border-blue-300 dark:hover:bg-blue-900/20">
                        View Details
                    </Button>
                </Link>
            </div>
        </Card>
    );
}; 