import { useState, useEffect } from 'react';
import { racesApi } from '../lib/api/races';
import { type Circuit } from '../lib/types/races';
import { CircuitCard } from '../components/circuits';

export const CircuitsListPage = () => {
    const [circuits, setCircuits] = useState<Circuit[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchCircuits = async () => {
            try {
                setLoading(true);
                const response = await racesApi.getCircuits();
                setCircuits(response.results);
            } catch (err) {
                setError('Failed to load circuits');
                console.error('Error fetching circuits:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchCircuits();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center py-12">
                <div className="text-red-500 dark:text-red-400">
                    <svg className="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                    </svg>
                    <h3 className="text-lg font-medium mb-2">Error loading circuits</h3>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Circuits</h1>
                    <p className="mt-2 text-gray-600 dark:text-gray-400">
                        Explore all Formula 1 circuits and racing venues
                    </p>
                </div>
            </div>

            {circuits.length === 0 ? (
                <div className="text-center py-12">
                    <div className="text-gray-500 dark:text-gray-400">
                        <svg className="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                        <h3 className="text-lg font-medium mb-2">No circuits found</h3>
                        <p>There are currently no circuits available.</p>
                    </div>
                </div>
            ) : (
                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {circuits.map((circuit) => (
                        <CircuitCard key={circuit.id} circuit={circuit} />
                    ))}
                </div>
            )}
        </div>
    );
}; 