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
            minute: '2-digit'
        });
    };

    return (
        <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                        {race.name}
                    </h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(race.status)}`}>
                        {race.status}
                    </span>
                </div>
            </div>

            <div className="mb-4">
                <div className="h-10 flex items-center text-sm text-gray-600 dark:text-gray-400 mb-2">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    {race.circuit.name}, {race.circuit.location}
                </div>
                <div className="h-10 flex items-center text-sm text-gray-600 dark:text-gray-400 mb-2">
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {formatDate(race.start_at)}
                </div>
            </div>

            <p className="h-20 text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                {race.description}
            </p>

            <div className="h-22 mb-4">
                <div className="block h-full">
                    {[1, 2, 3].map((position) => {
                        const color = position === 1 ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400' : 'bg-gray-100 text-gray-600 dark:bg-gray-900/20 dark:text-gray-400';
                        const driver = race.positions[position - 1]?.driver;

                        return (
                            <p key={position} className={`mb-1 block items-center px-2 py-1 rounded-md text-xs font-medium ${color}`}  >
                                P{position} {driver?.name || '?'}
                            </p>
                        )
                    })}
                </div>
            </div>

            <div className="flex justify-between items-center">
                <Link to={`/races/${race.id}`}>
                    <Button variant="outline" size="sm">
                        View Details
                    </Button>
                </Link>
            </div>
        </Card>
    );
}; 