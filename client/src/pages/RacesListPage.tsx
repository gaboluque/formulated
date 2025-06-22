import { useState, useEffect } from 'react';
import { RaceCard } from '../components/races';
import { Error } from '../components/Error';
import { racesApi } from '../lib/api/races';
import type { Race } from '../lib/types/races';

export const RacesListPage = () => {
    const [races, setRaces] = useState<Race[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadRaces = async () => {
            try {
                setLoading(true);
                const response = await racesApi.getRaces();
                setRaces(response.results || []);
            } catch (err) {
                console.error('Error loading races:', err);
                setError('Failed to load races. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        loadRaces();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center min-h-64">
                <div className="text-lg text-gray-600 dark:text-gray-400">Loading races...</div>
            </div>
        );
    }

    if (error) {
        return <Error message={error} />;
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Races</h1>
                    <p className="mt-2 text-gray-600 dark:text-gray-400">
                        Explore all Formula 1 races and their results
                    </p>
                </div>
            </div>

            {races.length === 0 ? (
                <div className="text-center py-12">
                    <div className="text-gray-500 dark:text-gray-400">
                        <svg className="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
                        </svg>
                        <h3 className="text-lg font-medium mb-2">No races found</h3>
                        <p>There are currently no races available.</p>
                    </div>
                </div>
            ) : (
                <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {races.map((race) => (
                        <RaceCard key={race.id} race={race} />
                    ))}
                </div>
            )}
        </div>
    );
}; 