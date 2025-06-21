import { Link } from 'react-router';
import { Card } from '../Card';
import { Button } from '../Button';
import type { Team } from '../../lib/types/teams';

export interface TeamCardProps {
    team: Team;
}

export const TeamCard = ({ team }: TeamCardProps) => {
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
        <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                        {team.name}
                    </h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(team.status)}`}>
                        {team.status}
                    </span>
                </div>
            </div>
            
            <p className="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                {team.description}
            </p>
            
            {team.members && team.members.length > 0 && (
                <div className="mb-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">
                        {team.members.length} member{team.members.length !== 1 ? 's' : ''}
                    </p>
                    <div className="flex flex-wrap gap-1">
                        {team.members.slice(0, 3).map((member) => (
                            <span
                                key={member.id}
                                className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400"
                            >
                                {member.name}
                            </span>
                        ))}
                        {team.members.length > 3 && (
                            <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-600 dark:bg-gray-900/20 dark:text-gray-400">
                                +{team.members.length - 3} more
                            </span>
                        )}
                    </div>
                </div>
            )}
            
            <div className="flex justify-between items-center">
                <Link to={`/teams/${team.id}`}>
                    <Button variant="outline" size="sm">
                        View Details
                    </Button>
                </Link>
            </div>
        </Card>
    );
}; 