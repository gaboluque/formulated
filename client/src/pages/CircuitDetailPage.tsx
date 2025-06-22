import { Link, useLoaderData } from 'react-router';
import { racesApi } from '../lib/api/races';
import { type Circuit, type Race } from '../lib/types/races';
import { Card } from '../components/Card';
import { ReviewsList } from '../components/ReviewsList';
import { CircuitLikeButton } from '../components/circuits';
import { useReviews } from '../lib/hooks/useReviews';
import type { PaginatedResponse } from '../lib/api/client';

interface LoaderData {
    circuit: Circuit
    races: PaginatedResponse<Race>
}

export const CircuitDetailPage = () => {
    const { circuit, races } = useLoaderData() as LoaderData;

    // Use the reviews hook
    const {
        reviews,
        loading: reviewsLoading,
        error: reviewsError,
        handleCreateReview,
        handleDeleteReview
    } = useReviews({
        entityId: circuit.id,
        api: {
            getReviews: racesApi.getCircuitReviews,
            createReview: racesApi.createCircuitReview,
            deleteReview: racesApi.deleteCircuitReview
        }
    });

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    };

    return (
        <div className="space-y-8">
            {/* Circuit Header */}
            <div className="bg-white dark:bg-gray-800 shadow-sm border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                            {circuit.name}
                        </h1>
                        <p className="text-lg text-gray-600 dark:text-gray-400 mt-2">
                            {circuit.location}
                        </p>
                    </div>
                    
                    <CircuitLikeButton circuitId={circuit.id} className="ml-4" />
                </div>
            </div>

            {/* Circuit Information */}
            <Card className="p-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Circuit Information</h2>
                
                <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-3">
                        <div className="flex items-center text-gray-600 dark:text-gray-400">
                            <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <span className="font-medium mr-2">Location:</span>
                            {circuit.location}
                        </div>
                        
                        <div className="flex items-center text-gray-600 dark:text-gray-400">
                            <svg className="w-5 h-5 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            <span className="font-medium mr-2">Added:</span>
                            {formatDate(circuit.created_at)}
                        </div>
                    </div>
                </div>
            </Card>

            {/* Race History */}
            {races.results.length > 0 && (
                <Card className="p-6">
                    <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                        Race History ({races.results.length})
                    </h2>
                    
                    <div className="space-y-3">
                        {races.results.map((race) => (
                            <div key={race.id} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-md">
                                <div>
                                    <h3 className="font-medium text-gray-900 dark:text-white">
                                        {race.name}
                                    </h3>
                                    <p className="text-sm text-gray-600 dark:text-gray-400">
                                        {formatDate(race.start_at)} • Status: {race.status}
                                    </p>
                                </div>
                                <Link
                                    to={`/races/${race.id}`}
                                    className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium text-sm"
                                >
                                    View Details →
                                </Link>
                            </div>
                        ))}
                    </div>
                </Card>
            )}

            {/* Reviews Section */}
            <ReviewsList
                reviews={reviews}
                loading={reviewsLoading}
                error={reviewsError}
                entityName="circuit"
                onCreateReview={handleCreateReview}
                onDeleteReview={handleDeleteReview}
                emptyStateMessage="Be the first to share your thoughts about this circuit!"
            />
        </div>
    );
}; 