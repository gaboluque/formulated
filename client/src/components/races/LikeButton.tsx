import { useState, useEffect } from 'react';
import { Button } from '../Button';
import { racesApi } from '../../lib/api/races';
import { useAuth } from '../../lib/contexts/AuthContext';

export interface RaceLikeButtonProps {
    raceId: string;
    className?: string;
}

export const RaceLikeButton = ({ raceId, className }: RaceLikeButtonProps) => {
    const { user } = useAuth();
    const [isLiked, setIsLiked] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const checkLikeStatus = async () => {
            if (!user) return;
            
            try {
                const response = await racesApi.checkLike(raceId);
                setIsLiked(response.liked);
            } catch (err) {
                console.error('Error checking like status:', err);
            }
        };

        checkLikeStatus();
    }, [raceId, user]);

    const handleLikeToggle = async () => {
        if (!user) {
            setError('Please log in to like races');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            if (isLiked) {
                await racesApi.unlikeRace(raceId);
                setIsLiked(false);
            } else {
                await racesApi.likeRace(raceId);
                setIsLiked(true);
            }
        } catch (err) {
            setError('Failed to update like status');
            console.error('Error toggling like:', err);
        } finally {
            setIsLoading(false);
        }
    };

    if (!user) {
        return null;
    }

    return (
        <div className={className}>
            <Button
                onClick={handleLikeToggle}
                variant={isLiked ? "primary" : "outline"}
                size="sm"
                isLoading={isLoading}
                className="flex items-center space-x-2"
            >
                <svg
                    className="w-4 h-4"
                    fill={isLiked ? "currentColor" : "none"}
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                    />
                </svg>
                <span>{isLiked ? 'Liked' : 'Like'}</span>
            </Button>
            {error && (
                <p className="text-red-600 dark:text-red-400 text-sm mt-2">{error}</p>
            )}
        </div>
    );
}; 