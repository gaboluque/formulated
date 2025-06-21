import './App.css'
import { useLoaderData, Link } from 'react-router';
import { Card, Button } from './components';
import type { Team } from './lib/types/team';

function App() {
  const data = useLoaderData() as { teams: Team[] };
  console.log(data);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card title="Welcome to Formulated" className="mb-6">
        <p className="text-gray-600 dark:text-gray-400 mb-4">
          Explore our components and features:
        </p>
        <div className="flex gap-4 flex-wrap">
          <Link to="/design-system">
            <Button variant="primary">Design System & Components</Button>
          </Link>
        </div>
      </Card>

      <Card title="Teams" className="mb-6">
        <div className="grid gap-2">
          {data.teams.map((team: Team) => (
            <div key={team.id} className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <h3 className="font-medium">{team.name}</h3>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}

export default App
