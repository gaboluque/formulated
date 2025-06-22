import { Link, Outlet } from 'react-router';
import { AuthProvider } from '../lib/contexts/AuthContext';
import { UserMenu } from './auth/UserMenu';

export const Layout = () => {
    return (
        <AuthProvider>
            <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
                {/* Navigation */}
                <nav className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between h-16">
                            <div className="flex items-center">
                                <Link to="/" className="text-xl font-bold text-gray-900 dark:text-white">
                                    🏎️ Formulated
                                </Link>
                                <div className="ml-10 flex items-baseline space-x-4">
                                    <Link
                                        to="/"
                                        className="text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Home
                                    </Link>
                                    <Link
                                        to="/teams"
                                        className="text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Teams
                                    </Link>
                                    <Link
                                        to="/members"
                                        className="text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Members
                                    </Link>
                                    <Link
                                        to="/races"
                                        className="text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Races
                                    </Link>
                                    <Link
                                        to="/circuits"
                                        className="text-gray-500 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                                    >
                                        Circuits
                                    </Link>
                                </div>
                            </div>
                            <div className="flex items-center">
                                <UserMenu />
                            </div>
                        </div>
                    </div>
                </nav>

                {/* Main Content */}
                <main className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
                    <Outlet />
                </main>
            </div>
        </AuthProvider>
    );
}; 