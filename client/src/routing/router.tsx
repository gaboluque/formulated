import { createBrowserRouter, type RouteObject } from "react-router";
import App from "../App";
import { teamsApi } from "../lib/api/teams";
import { Layout } from "../components/Layout";
import { Error as ErrorComponent } from "../components/Error";
import { DesignSystemDemo } from "../components";
import { LoginPage } from "../pages/LoginPage";
import { RegisterPage } from "../pages/RegisterPage";
import { TeamsListPage } from "../pages/TeamsListPage";
import { TeamDetailPage } from "../pages/TeamDetailPage";

export const routes: Record<string, RouteObject> = {
    root: {
        path: "/",
        element: <Layout />,
        errorElement: <ErrorComponent variant="page" title="Application Error" />,
        children: [
            {
                index: true,
                loader: async () => {
                    const teams = await teamsApi.getTeams();
                    return { teams: teams.results };
                },
                Component: App,
            },
            {
                path: "teams",
                loader: async () => {
                    const teams = await teamsApi.getTeams();
                    return { teams: teams.results };
                },
                Component: TeamsListPage,
                errorElement: <ErrorComponent variant="page" title="Application Error" />,
            },
            {
                path: "teams/:id",
                loader: async ({ params }) => {
                    const { id } = params;
                    if (!id) throw new Error('Team ID is required');

                    const team = await teamsApi.getTeam(id);
                    return { team };
                },
                errorElement: <ErrorComponent variant="page" title="Error loading team" />,
                Component: TeamDetailPage,
            },
        ]
    },
    teams: {
        path: "teams",
        loader: async () => {
            const teams = await teamsApi.getTeams();
            return { teams: teams.results };
        },
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
};

export const router = createBrowserRouter(Object.values(routes));