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
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            {team.name}
                        </h1>
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(team.status)}`}>
                            {team.status}
                        </span>
                    </div>
                    <LikeButton teamId={team.id} />
                </div>
                <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                    {team.description}
                </p>
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
                    {/* Team Info */}
                    <Card className="p-6">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                            Team Information
                        </h3>
                        <div className="space-y-3">
                            <div>
                                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">Status</span>
                                <p className="text-gray-900 dark:text-white capitalize">{team.status}</p>
                            </div>
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

                    {/* Members */}
                    {team.members && team.members.length > 0 && (
                        <Card className="p-6">
                            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                                Team Members ({team.members.length})
                            </h3>
                            <div className="space-y-3">
                                {team.members.map((member) => (
                                    <div key={member.id} className="border-b border-gray-200 dark:border-gray-700 last:border-b-0 pb-3 last:pb-0">
                                        <Link to={`/members/${member.id}`} className="flex justify-between items-start">
                                            <div>
                                                <h4 className="font-medium text-gray-900 dark:text-white">
                                                    {member.name}
                                                </h4>
                                                <span className="text-sm text-blue-600 dark:text-blue-400 capitalize">
                                                    {member.role}
                                                </span>
                                            </div>
                                        </Link>
                                    </div>
                                ))}
                            </div>
                        </Card>
                    )}
                </div>
            </div>
        </>
    );
}; 