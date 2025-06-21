import { useState, useEffect } from 'react';
import { Button } from '../Button';
import { teamsApi } from '../../lib/api/teams';
import { useAuth } from '../../lib/contexts/AuthContext';

export interface LikeButtonProps {
    teamId: string;
    onLikeChange?: (liked: boolean) => void;
}

export const LikeButton = ({ teamId, onLikeChange }: LikeButtonProps) => {
    const { user } = useAuth();
    const [liked, setLiked] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const checkLikeStatus = async () => {
            if (!user) return;
            
            try {
                const response = await teamsApi.checkLike(teamId);
                setLiked(response.liked);
            } catch (err) {
                console.error('Error checking like status:', err);
            }
        };

        checkLikeStatus();
    }, [teamId, user]);

    const handleLikeToggle = async () => {
        if (!user) {
            setError('You must be logged in to like teams');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            if (liked) {
                await teamsApi.unlikeTeam(teamId);
                setLiked(false);
                onLikeChange?.(false);
            } else {
                await teamsApi.likeTeam(teamId);
                setLiked(true);
                onLikeChange?.(true);
            }
        } catch (err) {
            console.error('Error toggling like:', err);
            setError('Failed to update like status');
        } finally {
            setLoading(false);
        }
    };

    if (!user) {
        return null;
    }

    return (
        <div className="flex flex-col items-center gap-2">
            <Button
                onClick={handleLikeToggle}
                disabled={loading}
                variant={liked ? 'primary' : 'outline'}
                size="sm"
                className="flex items-center gap-2"
            >
                <span className="text-lg">
                    {liked ? '❤️' : '🤍'}
                </span>
                {loading ? 'Loading...' : liked ? 'Liked' : 'Like'}
            </Button>
            {error && (
                <span className="text-xs text-red-600 dark:text-red-400">
                    {error}
                </span>
            )}
        </div>
    );
}; 