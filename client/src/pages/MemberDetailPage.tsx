import { useLoaderData, Link } from 'react-router';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { ReviewsList } from '../components/ReviewsList';
import { MemberLikeButton } from '../components/members/MemberLikeButton';
import { membersApi } from '../lib/api/members';
import { useReviews } from '../lib/hooks/useReviews';
import type { Member } from '../lib/types/teams';

interface LoaderData {
    member: Member
}

export const MemberDetailPage = () => {
    const { member } = useLoaderData() as LoaderData;

    // Use the reviews hook
    const {
        reviews,
        loading: reviewsLoading,
        error: reviewsError,
        handleCreateReview,
        handleDeleteReview
    } = useReviews({
        entityId: member.id,
        api: {
            getReviews: membersApi.getReviews,
            createReview: membersApi.createReview,
            deleteReview: membersApi.deleteReview
        }
    });

    const getRoleColor = (role: string) => {
        switch (role) {
            case 'driver':
                return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/20';
            case 'engineer':
                return 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/20';
            case 'manager':
                return 'text-purple-600 bg-purple-100 dark:text-purple-400 dark:bg-purple-900/20';
            case 'other':
                return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
            default:
                return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
        }
    };

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
                return '👤';
        }
    };

    return (
        <>
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-6">
                        <div>
                            {/* Driver headshot */}
                            {member.role === 'driver' && member.headshot_url && (
                                <img
                                    src={member.headshot_url}
                                    alt={`${member.name} headshot`}
                                    className="w-24 h-24 rounded-full object-cover border-4 border-gray-200 dark:border-gray-700 mb-4"
                                />
                            )}
                            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                                {member.name}
                                {member.role === 'driver' && member.name_acronym && (
                                    <span className="text-xl text-gray-500 dark:text-gray-400 ml-2">
                                        ({member.name_acronym})
                                    </span>
                                )}
                            </h1>
                            <div className="flex items-center gap-3">
                                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getRoleColor(member.role)}`}>
                                    {getRoleIcon(member.role)} {member.role}
                                    {member.role === 'driver' && member.driver_number && (
                                        <span className="ml-1 font-bold">#{member.driver_number}</span>
                                    )}
                                </span>
                                {member.role === 'driver' && member.country_code && (
                                    <span className="text-sm text-gray-500 dark:text-gray-400 font-medium">
                                        🏁 {member.country_code}
                                    </span>
                                )}
                                {member.team && (
                                    <Link to={`/teams/${member.team.id}`}>
                                        <Button variant="outline" size="sm">
                                            View Team
                                        </Button>
                                    </Link>
                                )}
                            </div>
                        </div>
                    </div>
                    <MemberLikeButton memberId={member.id} />
                </div>
                <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                    {member.description}
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main content */}
                <div className="lg:col-span-2">
                    <ReviewsList
                        reviews={reviews}
                        loading={reviewsLoading}
                        error={reviewsError}
                        entityName="member"
                        onCreateReview={handleCreateReview}
                        onDeleteReview={handleDeleteReview}
                        emptyStateMessage="Be the first to review this team member!"
                    />
                </div>

                {/* Sidebar */}
                <div className="space-y-6">
                    {/* Member Info */}
                    <Card className="p-6">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Member Information
                        </h3>
                        <div className="space-y-3">
                            <div>
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Role</span>
                                <div className="flex items-center gap-2 mt-1">
                                    <span className="text-lg">{getRoleIcon(member.role)}</span>
                                    <span className="text-gray-900 dark:text-white capitalize">{member.role}</span>
                                </div>
                            </div>

                            {/* Driver-specific fields */}
                            {member.role === 'driver' && (
                                <>
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Driver Number</span>
                                        <p className="text-gray-900 dark:text-white font-bold">#{member.driver_number}</p>
                                    </div>

                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Name Acronym</span>
                                        <p className="text-gray-900 dark:text-white font-mono">{member.name_acronym}</p>
                                    </div>
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Country</span>
                                        <p className="text-gray-900 dark:text-white">🏁 {member.country_code}</p>
                                    </div>
                                    <div>
                                        <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Team</span>
                                        <p className="text-gray-900 dark:text-white">{member.team.name}</p>
                                    </div>
                                </>
                            )}

                            <div>
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Joined</span>
                                <p className="text-gray-900 dark:text-white">
                                    {new Date(member.created_at).toLocaleDateString()}
                                </p>
                            </div>

                            {member.updated_at !== member.created_at && (
                                <div>
                                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Last Updated</span>
                                    <p className="text-gray-900 dark:text-white">
                                        {new Date(member.updated_at).toLocaleDateString()}
                                    </p>
                                </div>
                            )}
                        </div>
                    </Card>

                    {/* Quick Actions */}
                    <Card className="p-6">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Quick Actions
                        </h3>
                        <div className="space-y-3">
                            <Link to="/members" className="block">
                                <Button variant="outline" className="w-full justify-start">
                                    ← Back to All Members
                                </Button>
                            </Link>

                            {member.team && (
                                <Link to={`/teams/${member.team.id}`} className="block">
                                    <Button variant="outline" className="w-full justify-start">
                                        🏆 View Team Profile
                                    </Button>
                                </Link>
                            )}

                            <Link to={`/members?role=${member.role}`} className="block">
                                <Button variant="outline" className="w-full justify-start">
                                    {getRoleIcon(member.role)} View Other {member.role}s
                                </Button>
                            </Link>
                        </div>
                    </Card>

                    {/* Role Information */}
                    <Card className="p-6">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            About {member.role}s
                        </h3>
                        <div className="text-sm text-gray-600 dark:text-gray-300">
                            {member.role === 'driver' && (
                                <p>Drivers are the heart of Formula 1, piloting the cars at incredible speeds and showcasing their racing skills on tracks around the world.</p>
                            )}
                            {member.role === 'engineer' && (
                                <p>Engineers are the technical minds behind F1 teams, working on car development, performance optimization, and strategic race planning.</p>
                            )}
                            {member.role === 'manager' && (
                                <p>Managers oversee team operations, make strategic decisions, and ensure smooth coordination between all team members and departments.</p>
                            )}
                            {member.role === 'other' && (
                                <p>Team members in various specialized roles contribute to the success of Formula 1 teams through their unique skills and expertise.</p>
                            )}
                        </div>
                    </Card>
                </div>
            </div>
        </>
    );
}; 