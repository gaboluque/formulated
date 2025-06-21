import { Link } from 'react-router';
import { Card } from '../Card';
import { Button } from '../Button';
import type { Member } from '../../lib/types/teams';

export interface MemberCardProps {
    member: Member;
}

export const MemberCard = ({ member }: MemberCardProps) => {
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
        <Card className="p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
                <div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                        {member.name}
                    </h3>
                    <div className="flex items-center gap-2 mb-2">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRoleColor(member.role)}`}>
                            {getRoleIcon(member.role)} {member.role}
                        </span>
                    </div>
                </div>
            </div>
            
            <p className="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
                {member.description}
            </p>
            
            {member.team && (
                <div className="mb-4">
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                        Team: <span className="font-medium text-gray-700 dark:text-gray-300">
                            {member.team.name}
                        </span>
                    </p>
                </div>
            )}
            
            <div className="flex justify-between items-center">
                <Link to={`/members/${member.id}`}>
                    <Button variant="outline" size="sm">
                        View Details
                    </Button>
                </Link>
            </div>
        </Card>
    );
}; 