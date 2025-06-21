import { createBrowserRouter } from "react-router";
import App from "../App";
import { teamsApi } from "../lib/api/teams";
import { DesignSystemDemo } from "../components";
import { LoginPage } from "../pages/LoginPage";
import { RegisterPage } from "../pages/RegisterPage";


export const routes = {
    home: {
        path: "/",  
        loader: async () => {
            const teams = await teamsApi.getTeams();
            return { teams: teams.results };
        },
        Component: App,
    },
    login: {
        path: "/login",
        Component: LoginPage,
    },
    register: {
        path: "/register", 
        Component: RegisterPage,
    },
    designSystem: {
        path: "/design-system",
        Component: DesignSystemDemo,
    },
}

export const router = createBrowserRouter(Object.values(routes));