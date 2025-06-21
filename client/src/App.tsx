import './App.css'
import { useLoaderData } from 'react-router';
import type { Team } from './lib/types/team';

function App() {
  const data = useLoaderData() as { teams: Team[] };
  console.log(data);

  return (
    <>
      <div>
        {data.teams.map((team: Team) => {
          return (
            <div key={team.id}>{team.name}</div>
          )
        })}
      </div>
    </>
  )
}

export default App
