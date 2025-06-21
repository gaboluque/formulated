import { createBrowserRouter } from "react-router";
import App from "../App";
import { teamsApi } from "../lib/api/teams";

export const router = createBrowserRouter([
    {
        path: "/",  
        loader: async () => {
            const teams = await teamsApi.getTeams();
            return { teams: teams.results };
        },
        Component: App,
    },
]);