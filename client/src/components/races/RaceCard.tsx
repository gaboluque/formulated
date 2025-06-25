import { Link } from 'react-router';
import { Card } from '../Card';
import { Button } from '../Button';
import type { Race } from '../../lib/types/races';

export interface RaceCardProps {
    race: Race;
}

export const RaceCard = ({ race }: RaceCardProps) => {
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
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            timeZone: 'UTC'
        }) + ' UTC';
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'scheduled':
                return '📅';
            case 'ongoing':
                return '🏁';
            case 'completed':
                return '✅';
            case 'cancelled':
                return '❌';
            default:
                return '❓';
        }
    };

    return (
        <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2 h-8">
                        {race.name}
                    </h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(race.status)}`}>
                        {getStatusIcon(race.status)} {race.status.charAt(0).toUpperCase() + race.status.slice(1)}
                    </span>
                </div>
            </div>

            <div className="mb-4 h-24">
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-2 h-10">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {race.circuit.name}, {race.circuit.location}
                </div>
                <div className="flex items-center text-sm text-gray-600 dark:text-gray-400 mb-2 h-10">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {formatDate(race.start_at)}
                </div>
            </div>

            <div className="mb-4">
                <div className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Top 3 Results:
                </div>
                <div className="space-y-2 h-32">
                    {race.positions.length > 0 ? race.positions.slice(0, 3).map((position) => {
                        const podiumColor = position.position === 1
                            ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
                            : position.position === 2
                                ? 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
                                : 'bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-400';

                        const medal = position.position === 1 ? '🥇' : position.position === 2 ? '🥈' : '🥉';

                        return (
                            <div key={position.id} className={`flex items-center px-3 py-2 rounded-md text-sm font-medium ${podiumColor} relative`}>
                                <span className="mr-2">{medal}</span>
                                <span className="font-semibold">P{position.position}</span>
                                <span className="ml-2">{position.driver_acronym}</span>
                                <span className="ml-1 text-xs opacity-75 absolute right-2">#{position?.driver_number ?? ''}</span>
                            </div>
                        );
                    }) : <div className="text-sm text-gray-500 dark:text-gray-400 border-2 border-gray-200 dark:border-gray-700 rounded-md p-2">No results yet</div>}
                </div>
            </div>

            <div className="flex justify-between items-center">
                <Link to={`/races/${race.id}`}>
                    <Button variant="outline" size="sm">
                        View Details
                    </Button>
                </Link>
                <Link to={`/circuits/${race.circuit.id}`}>
                    <Button variant="outline" size="sm">
                        View Circuit
                    </Button>
                </Link>
            </div>
        </Card>
    );
}; 