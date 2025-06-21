import './App.css'
import { useLoaderData, Link } from 'react-router';
import { TeamCard } from './components/teams/TeamCard'
import type { Team } from './lib/types/teams';

interface LoaderData {
  teams: Team[]
}

function App() {
  const { teams } = useLoaderData() as LoaderData;

  return (
    <>
      {/* Hero Section */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Welcome to Formulated
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          Your ultimate destination for Formula 1 team information, reviews, and social interaction.
        </p>
      </div>

      {/* Featured Teams */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
            Featured Teams
          </h2>
          <Link
            to="/teams"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            View All Teams
          </Link>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {teams.slice(0, 6).map((team) => (
            <TeamCard key={team.id} team={team} />
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
          Features
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl mb-2">👥</div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">Team Profiles</h4>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Explore detailed information about F1 teams and their members
            </p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">❤️</div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">Like & Follow</h4>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Show support for your favorite teams with likes
            </p>
          </div>
          <div className="text-center">
            <div className="text-2xl mb-2">⭐</div>
            <h4 className="font-medium text-gray-900 dark:text-white mb-2">Reviews</h4>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Share your thoughts and read what other fans are saying
            </p>
          </div>
        </div>
      </div>
    </>
  )
}

export default App
