import { Link, useLoaderData } from 'react-router';
import { Card } from '../components/Card';
import { ReviewsList } from '../components/ReviewsList';
import { RaceLikeButton } from '../components/races';
import { racesApi } from '../lib/api/races';
import { useReviews } from '../lib/hooks/useReviews';
import type { Race } from '../lib/types/races';

interface LoaderData {
    race: Race
}

export const RaceDetailPage = () => {
    const { race } = useLoaderData() as LoaderData;

    // Use the reviews hook
    const {
        reviews,
        loading: reviewsLoading,
        error: reviewsError,
        handleCreateReview,
        handleDeleteReview
    } = useReviews({
        entityId: race.id,
        api: {
            getReviews: racesApi.getReviews,
            createReview: racesApi.createReview,
            updateReview: racesApi.updateReview,
            deleteReview: racesApi.deleteReview
        }
    });

    const isRaceFinished = () => {
        if (!race) return false;
        const raceDate = new Date(race.start_at);
        const now = new Date();
        return race.status === 'completed' || raceDate < now;
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'scheduled':
                return 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/20';
            case 'ongoing':
                return 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20';
            case 'completed':
                return 'text-green-600 bg-green-100 dark:text-green-400 dark:bg-green-900/20';
            case 'cancelled':
                return 'text-red-600 bg-red-100 dark:text-red-400 dark:bg-red-900/20';
            default:
                return 'text-gray-600 bg-gray-100 dark:text-gray-400 dark:bg-gray-900/20';
        }
    };

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex justify-between items-start">
                <div className="flex-1">
                    <div className="flex items-center gap-4 mb-4">
                        <Link 
                            to="/races"
                            className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 flex items-center gap-2"
                        >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 18l-6-6 6-6" />
                            </svg>
                            Back to Races
                        </Link>
                    </div>
                    
                    <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
                        {race.name}
                    </h1>
                    
                    <div className="flex items-center gap-4 mb-4">
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(race.status)}`}>
                            {race.status}
                        </span>
                    </div>
                </div>
                
                <RaceLikeButton raceId={race.id} className="ml-4" />
            </div>

            {/* Race Info */}
            <Card className="p-6">
                <div className="grid md:grid-cols-2 gap-6">
                    <div>
                        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Race Information</h2>
                        
                        <div className="space-y-3">
                            <div className="flex items-center text-gray-600 dark:text-gray-400">
                                <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                <span className="font-medium mr-2">Circuit:</span>
                                {race.circuit.name}, {race.circuit.location}
                            </div>
                            
                            <div className="flex items-center text-gray-600 dark:text-gray-400">
                                <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                </svg>
                                <span className="font-medium mr-2">Date:</span>
                                {formatDate(race.start_at)}
                            </div>
                        </div>
                    </div>
                    
                    <div>
                        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">Description</h3>
                        <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                            {race.description}
                        </p>
                    </div>
                </div>
            </Card>

            {/* Race Results */}
            {race.positions && race.positions.length > 0 && (
                <Card className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                        Race Results
                    </h2>
                    
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                            <thead className="bg-gray-50 dark:bg-gray-800">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        Position
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        Driver
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                                        Points
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
                                {race.positions.map((position) => (
                                    <tr key={position.id}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                                            {position.position}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {position.driver_acronym}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                                            {position.points}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </Card>
            )}

            {/* Reviews */}
            <ReviewsList
                reviews={reviews}
                loading={reviewsLoading}
                error={reviewsError}
                entityName="race"
                canUserReview={isRaceFinished()}
                onCreateReview={handleCreateReview}
                onDeleteReview={handleDeleteReview}
                emptyStateMessage="Reviews will be available after the race is completed."
            />
        </div>
    );
}; 