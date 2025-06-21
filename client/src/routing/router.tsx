import { createBrowserRouter, type RouteObject } from "react-router";
import App from "../App";
import { teamsApi } from "../lib/api/teams";
import { membersApi } from "../lib/api/members";
import { Layout } from "../components/Layout";
import { Error as ErrorComponent } from "../components/Error";
import { DesignSystemDemo } from "../components";
import { LoginPage } from "../pages/LoginPage";
import { RegisterPage } from "../pages/RegisterPage";
import { TeamsListPage } from "../pages/TeamsListPage";
import { TeamDetailPage } from "../pages/TeamDetailPage";
import { MembersListPage } from "../pages/MembersListPage";
import { MemberDetailPage } from "../pages/MemberDetailPage";

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
            {
                path: "members",
                loader: async () => {
                    const members = await membersApi.getMembers();
                    return { members: members.results };
                },
                Component: MembersListPage,
                errorElement: <ErrorComponent variant="page" title="Application Error" />,
            },
            {
                path: "members/:id",
                loader: async ({ params }) => {
                    const { id } = params;
                    if (!id) throw new Error('Member ID is required');

                    const member = await membersApi.getMember(id);
                    return { member };
                },
                errorElement: <ErrorComponent variant="page" title="Error loading member" />,
                Component: MemberDetailPage,
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
    members: {
        path: "members",
        loader: async () => {
            const members = await membersApi.getMembers();
            return { members: members.results };
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