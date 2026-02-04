import { create } from 'zustand';
import socialService from '../services/socialService';

const useSocialStore = create((set, get) => ({
    // Shared State
    isLoading: false,
    error: null,

    // Social Trading State (Phase 24)
    leaderboard: [],
    followedTraders: [],
    copyTrades: [],

    // Reddit Analysis State (Existing)
    posts: [],
    sentimentData: {}, // { "NVDA": { score, label, hype } }
    
    // Actions - Social Trading
    fetchLeaderboard: async () => {
        set({ isLoading: true, error: null });
        try {
            const data = await socialService.getLeaderboard();
            set({ leaderboard: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch leaderboard:', error);
        }
    },

    fetchFollowedTraders: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await socialService.getFollowedTraders(userId);
            set({ followedTraders: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch followed traders:', error);
        }
    },

    fetchCopyTrades: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await socialService.getCopyTrades(userId);
            set({ copyTrades: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch copy trades:', error);
        }
    },

    followTrader: async (userId, traderId) => {
        set({ isLoading: true, error: null });
        try {
            await socialService.followTrader({
                user_id: userId,
                trader_id: traderId
            });
            // Refresh list
            await get().fetchFollowedTraders(userId);
            await get().fetchLeaderboard(); // In case follower count updates
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to follow trader:', error);
            return false;
        }
    },

    startCopyTrading: async (userId, traderId, amount) => {
        set({ isLoading: true, error: null });
        try {
            await socialService.startCopyTrading({
                user_id: userId,
                trader_id: traderId,
                allocation_amount: amount
            });
            // Refresh list
            await get().fetchCopyTrades(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to start copy trading:', error);
            return false;
        }
    },

    // Actions - Reddit Analysis
    fetchPosts: async (subreddit = 'wallstreetbets', limit = 10, mock = true) => {
        set({ isLoading: true, error: null });
        try {
            const data = await socialService.fetchRedditPosts(subreddit, limit, mock);
            set({ posts: data || [], isLoading: false });
        } catch (error) {
            console.error('Fetch reddit posts failed:', error);
            set({ error: error.message, isLoading: false });
        }
    },

    analyzeSentiment: async (ticker, mock = true) => {
        set({ isLoading: true, error: null });
        try {
            const data = await socialService.analyzeRedditSentiment(ticker, mock);
            set((state) => ({
                sentimentData: { ...state.sentimentData, [ticker]: data },
                isLoading: false
            }));
        } catch (error) {
            console.error(`Analyze sentiment ${ticker} failed:`, error);
            set({ error: error.message, isLoading: false });
        }
    }
}));

export default useSocialStore;
