import { TeamCard } from '../components/teams/TeamCard';
import type { Team } from '../lib/types/teams';
import { useLoaderData } from 'react-router';

interface LoaderData {
    teams: Team[]
}

export const TeamsListPage = () => {
    const { teams } = useLoaderData() as LoaderData;

    return (
        <>
            {/* Page Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                    F1 Teams
                </h1>
                <p className="text-gray-600 dark:text-gray-300">
                    Explore all Formula 1 teams, their members, and what fans are saying about them.
                </p>
            </div>

            {/* Teams grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {teams.map((team) => (
                    <TeamCard key={team.id} team={team} />
                ))}
            </div>
        </>
    );
}; 