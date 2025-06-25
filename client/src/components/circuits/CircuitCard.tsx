import { Link } from "react-router";
import type { Circuit } from "../../lib/types/races";
import { Card } from "../Card";
import { Button } from "../Button";

export interface CircuitCardProps {
    circuit: Circuit;
}

export const CircuitCard: React.FC<CircuitCardProps> = ({ circuit }) => {
    const upcomingRaces = circuit.races.filter(race => race.status === 'scheduled' || race.status === 'ongoing');
    const nextRace = upcomingRaces.sort((a, b) => new Date(a.start_at).getTime() - new Date(b.start_at).getTime())[0];

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    };

    return (
        <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                        {circuit.name}
                    </h3>
                    <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                        <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        {circuit.location}
                    </div>
                </div>
            </div>

            <div className="mb-4 space-y-2">
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
                        <div className="text-lg font-semibold text-blue-600 dark:text-blue-400">
                            {circuit.races_count}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">
                            Total Races
                        </div>
                    </div>
                    <div className="bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
                        <div className="text-lg font-semibold text-green-600 dark:text-green-400">
                            {circuit.completed_races_count}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">
                            Completed
                        </div>
                    </div>
                    <div className="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg">
                        <div className="text-lg font-semibold text-yellow-600 dark:text-yellow-400">
                            {circuit.upcoming_races_count}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">
                            Upcoming
                        </div>
                    </div>
                </div>

                {nextRace && (
                    <div className="bg-gray-50 dark:bg-gray-800 p-3 rounded-lg">
                        <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                            Next Race:
                        </div>
                        <div className="flex justify-between items-center">
                            <div>
                                <div className="font-semibold text-gray-900 dark:text-white">
                                    {nextRace.name}
                                </div>
                                <div className="text-sm text-gray-600 dark:text-gray-400">
                                    {formatDate(nextRace.start_at)}
                                </div>
                            </div>
                            <div className="text-right">
                                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                                    nextRace.status === 'scheduled' 
                                        ? 'text-blue-600 bg-blue-100 dark:text-blue-400 dark:bg-blue-900/20'
                                        : 'text-yellow-600 bg-yellow-100 dark:text-yellow-400 dark:bg-yellow-900/20'
                                }`}>
                                    {nextRace.status === 'scheduled' ? '📅' : '🏁'} {nextRace.status}
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>

            <div className="flex items-center justify-between">
                <Link to={`/circuits/${circuit.id}`}>
                    <Button variant="outline" size="sm">
                        View Details
                    </Button>
                </Link>
                {circuit.races_count > 0 && (
                    <Link to={`/races?circuit_id=${circuit.id}`}>
                        <Button variant="outline" size="sm">
                            View Races ({circuit.races_count})
                        </Button>
                    </Link>
                )}
            </div>
        </Card>
    );
}; 