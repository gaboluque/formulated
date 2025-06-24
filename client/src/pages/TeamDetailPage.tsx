import { Link, useLoaderData } from 'react-router';
import { Card } from '../components/Card';
import { ReviewsList } from '../components/ReviewsList';
import { LikeButton } from '../components/teams/LikeButton';
import { teamsApi } from '../lib/api/teams';
import { useReviews } from '../lib/hooks/useReviews';
import type { Team } from '../lib/types/teams';

interface LoaderData {
    team: Team
}

export const TeamDetailPage = () => {
    const { team } = useLoaderData() as LoaderData;

    // Use the reviews hook
    const {
        reviews,
        loading: reviewsLoading,
        error: reviewsError,
        handleCreateReview,
        handleEditReview,
        handleDeleteReview
    } = useReviews({
        entityId: team.id,
        api: {
            getReviews: teamsApi.getReviews,
            createReview: teamsApi.createReview,
            updateReview: teamsApi.updateReview,
            deleteReview: teamsApi.deleteReview
        }
    });

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
        <>
            {/* Hero Header */}
            <div className="mb-8">
                <div className="flex items-start gap-6 mb-6">
                    {/* Team Logo */}
                    <div className="flex-shrink-0">
                        {team.logo_url ? (
                            <img
                                src={team.logo_url}
                                alt={`${team.name} logo`}
                                className="w-20 h-20 object-contain rounded-xl bg-white dark:bg-gray-800 p-2 shadow-lg border border-gray-200 dark:border-gray-700"
                            />
                        ) : (
                            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                                <span className="text-white font-bold text-2xl">
                                    {team.name.charAt(0)}
                                </span>
                            </div>
                        )}
                    </div>

                    {/* Team Info */}
                    <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
                                    {team.name}
                                </h1>
                                <div className="flex items-center gap-4 mb-2">
                                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(team.status)}`}>
                                        {team.status}
                                    </span>
                                    {team.base && (
                                        <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                            </svg>
                                            <span className="text-sm font-medium">{team.base}</span>
                                        </div>
                                    )}
                                    {team.first_team_entry && (
                                        <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                            </svg>
                                            <span className="text-sm font-medium">Since {team.first_team_entry}</span>
                                        </div>
                                    )}
                                </div>
                            </div>
                            <LikeButton teamId={team.id} />
                        </div>
                        <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                            {team.description}
                        </p>
                    </div>
                </div>

                {/* Championships and Key Stats */}
                {(team.world_championships || team.pole_positions || team.fastest_laps) && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                        {team.world_championships !== undefined && team.world_championships > 0 && (
                            <Card className="p-4 bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 border-yellow-200 dark:border-yellow-800">
                                <div className="flex items-center gap-3">
                                    <svg className="w-8 h-8 text-yellow-600 dark:text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                    <div>
                                        <p className="text-2xl font-bold text-yellow-800 dark:text-yellow-200">
                                            {team.world_championships}
                                        </p>
                                        <p className="text-sm font-medium text-yellow-700 dark:text-yellow-300">
                                            World Championship{team.world_championships !== 1 ? 's' : ''}
                                        </p>
                                    </div>
                                </div>
                            </Card>
                        )}

                        {team.pole_positions !== undefined && team.pole_positions > 0 && (
                            <Card className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-200 dark:border-blue-800">
                                <div className="flex items-center gap-3">
                                    <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                    <div>
                                        <p className="text-2xl font-bold text-blue-800 dark:text-blue-200">
                                            {team.pole_positions}
                                        </p>
                                        <p className="text-sm font-medium text-blue-700 dark:text-blue-300">
                                            Pole Position{team.pole_positions !== 1 ? 's' : ''}
                                        </p>
                                    </div>
                                </div>
                            </Card>
                        )}

                        {team.fastest_laps !== undefined && team.fastest_laps > 0 && (
                            <Card className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-green-200 dark:border-green-800">
                                <div className="flex items-center gap-3">
                                    <svg className="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                    </svg>
                                    <div>
                                        <p className="text-2xl font-bold text-green-800 dark:text-green-200">
                                            {team.fastest_laps}
                                        </p>
                                        <p className="text-sm font-medium text-green-700 dark:text-green-300">
                                            Fastest Lap{team.fastest_laps !== 1 ? 's' : ''}
                                        </p>
                                    </div>
                                </div>
                            </Card>
                        )}
                    </div>
                )}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main content */}
                <div className="lg:col-span-2">
                    <ReviewsList
                        reviews={reviews}
                        loading={reviewsLoading}
                        error={reviewsError}
                        entityName="team"
                        onCreateReview={handleCreateReview}
                        onEditReview={handleEditReview}
                        onDeleteReview={handleDeleteReview}
                        emptyStateMessage="Be the first to review this team!"
                    />
                </div>

                {/* Sidebar */}
                <div className="space-y-6">
                    {/* Team Statistics */}
                    <Card className="p-6">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Team Statistics
                        </h3>
                        <div className="space-y-4">
                            {team.highest_race_finish && (
                                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Highest Finish</span>
                                    <span className="text-sm font-bold text-gray-900 dark:text-white">P{team.highest_race_finish}</span>
                                </div>
                            )}
                            {team.world_championships !== undefined && (
                                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Championships</span>
                                    <span className="text-sm font-bold text-gray-900 dark:text-white">{team.world_championships}</span>
                                </div>
                            )}
                            {team.pole_positions !== undefined && (
                                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Pole Positions</span>
                                    <span className="text-sm font-bold text-gray-900 dark:text-white">{team.pole_positions}</span>
                                </div>
                            )}
                            {team.fastest_laps !== undefined && (
                                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Fastest Laps</span>
                                    <span className="text-sm font-bold text-gray-900 dark:text-white">{team.fastest_laps}</span>
                                </div>
                            )}
                            <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Status</span>
                                <span className="text-sm font-bold text-gray-900 dark:text-white capitalize">{team.status}</span>
                            </div>
                            {team.first_team_entry && (
                                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">First Entry</span>
                                    <span className="text-sm font-bold text-gray-900 dark:text-white">{team.first_team_entry}</span>
                                </div>
                            )}
                        </div>
                    </Card>

                    {/* Technical Specifications */}
                    {(team.chassis || team.engine || team.tyres) && (
                        <Card className="p-6">
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                Technical Specifications
                            </h3>
                            <div className="space-y-3">
                                {team.chassis && (
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Chassis</span>
                                        <p className="text-gray-900 dark:text-white font-medium">{team.chassis}</p>
                                    </div>
                                )}
                                {team.engine && (
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Engine</span>
                                        <p className="text-gray-900 dark:text-white font-medium">{team.engine}</p>
                                    </div>
                                )}
                                {team.tyres && (
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Tyres</span>
                                        <p className="text-gray-900 dark:text-white font-medium">{team.tyres}</p>
                                    </div>
                                )}
                            </div>
                        </Card>
                    )}

                    {/* Team Management */}
                    {(team.president || team.director || team.technical_manager) && (
                        <Card className="p-6">
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                Team Management
                            </h3>
                            <div className="space-y-3">
                                {team.president && (
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">President</span>
                                        <p className="text-gray-900 dark:text-white font-medium">{team.president}</p>
                                    </div>
                                )}
                                {team.director && (
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Director</span>
                                        <p className="text-gray-900 dark:text-white font-medium">{team.director}</p>
                                    </div>
                                )}
                                {team.technical_manager && (
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Technical Manager</span>
                                        <p className="text-gray-900 dark:text-white font-medium">{team.technical_manager}</p>
                                    </div>
                                )}
                            </div>
                        </Card>
                    )}

                    {/* Team Members */}
                    {team.members && team.members.length > 0 && (
                        <Card className="p-6">
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                Team Members ({team.members.length})
                            </h3>
                            <div className="space-y-3">
                                {team.members.map((member) => (
                                    <div key={member.id} className="border-b border-gray-200 dark:border-gray-700 last:border-b-0 pb-3 last:pb-0">
                                        <Link to={`/members/${member.id}`} className="block hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg p-2 -m-2 transition-colors">
                                            <div className="flex items-center gap-3">
                                                {member.headshot_url ? (
                                                    <img
                                                        src={member.headshot_url}
                                                        alt={member.name}
                                                        className="w-10 h-10 rounded-full object-cover"
                                                    />
                                                ) : (
                                                    <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                                                        <span className="text-blue-600 dark:text-blue-400 font-medium text-sm">
                                                            {member.name_acronym || member.name.split(' ').map(n => n[0]).join('')}
                                                        </span>
                                                    </div>
                                                )}
                                                <div className="flex-1 min-w-0">
                                                    <div className="flex items-center justify-between">
                                                        <div>
                                                            <h4 className="font-medium text-gray-900 dark:text-white">
                                                                {member.name}
                                                            </h4>
                                                            <div className="flex items-center gap-2">
                                                                <span className="text-sm text-blue-600 dark:text-blue-400 capitalize">
                                                                    {member.role}
                                                                </span>
                                                                {member.driver_number && (
                                                                    <span className="text-xs bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 px-2 py-0.5 rounded">
                                                                        #{member.driver_number}
                                                                    </span>
                                                                )}
                                                                {member.country_code && (
                                                                    <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 px-2 py-0.5 rounded">
                                                                        {member.country_code}
                                                                    </span>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </Link>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    )}

                    {/* Meta Information */}
                    <Card className="p-6">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Information
                        </h3>
                        <div className="space-y-3">
                            <div>
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Created</span>
                                <p className="text-gray-900 dark:text-white">
                                    {new Date(team.created_at).toLocaleDateString()}
                                </p>
                            </div>
                            {team.updated_at !== team.created_at && (
                                <div>
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Last Updated</span>
                                    <p className="text-gray-900 dark:text-white">
                                        {new Date(team.updated_at).toLocaleDateString()}
                                    </p>
                                </div>
                            )}
                        </div>
                    </Card>
                </div>
            </div>
        </>
    );
}; 