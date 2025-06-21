import './App.css'
import { useLoaderData, Link } from 'react-router';
import { Card, Button, UserMenu } from './components';
import { useAuth } from './lib/contexts/AuthContext';
import type { Team } from './lib/types/team';
import { routes } from './routing/router';

function App() {
  const data = useLoaderData() as { teams: Team[] };
  const { user, isAuthenticated, isLoading } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to={routes.home.path} className="text-xl font-bold text-gray-900 dark:text-white">
                🏁 Formulated
              </Link>
              <nav className="hidden sm:flex space-x-6">
                <Link to={routes.home.path} className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                  Teams
                </Link>
              </nav>
            </div>
            
            <div className="flex items-center space-x-4">
              {isLoading ? (
                <div className="animate-pulse">
                  <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
                </div>
              ) : isAuthenticated && user ? (
                <UserMenu />
              ) : (
                <div className="flex items-center space-x-3">
                  <Link to={routes.login.path}>
                    <Button variant="outline" size="sm">Sign In</Button>
                  </Link>
                  <Link to={routes.register.path}>
                    <Button variant="primary" size="sm">Sign Up</Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto p-6">
        <Card title="Welcome to Formulated" className="mb-6">
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            {isAuthenticated && user ? (
              <>Welcome back, <strong>{user.username}</strong>! Explore F1 teams and races.</>
            ) : (
              <>Welcome to Formulated! Sign in to track your favorite F1 teams and races.</>
            )}
          </p>
          {!isAuthenticated && (
            <div className="flex gap-4 flex-wrap">
              <Link to={routes.login.path}>
                <Button variant="primary">Get Started</Button>
              </Link>
              <Link to={routes.designSystem.path}>
                <Button variant="outline">View Components</Button>
              </Link>
            </div>
          )}
        </Card>

        <Card title="Teams" className="mb-6">
          <div className="grid gap-2">
            {data.teams.map((team: Team) => (
              <div key={team.id} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <h3 className="font-medium">{team.name}</h3>
                {team.description && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {team.description}
                  </p>
                )}
              </div>
            ))}
          </div>
        </Card>
      </main>
    </div>
  )
}

export default App
