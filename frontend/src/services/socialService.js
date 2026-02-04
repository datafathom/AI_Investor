/**
 * Social Trading Service
 * : Social Trading & Leaderboards
 */
import apiClient from './apiClient';

const BASE_URL = '/social-trading';

export const socialService = {
    /**
     * Get trading leaderboard
     */
    getLeaderboard: async () => {
        const response = await apiClient.get(`${BASE_URL}/leaderboard`);
        return response.data;
    },

    /**
     * Get followed traders
     * @param {string} userId
     */
    getFollowedTraders: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/following`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get current copy trades
     * @param {string} userId
     */
    getCopyTrades: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/copy-trades`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Follow a trader
     * @param {Object} data { user_id, trader_id }
     */
    followTrader: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/follow`, data);
        return response.data;
    },

    /**
     * Start copy trading a trader
     * @param {Object} data { user_id, trader_id, allocation_amount }
     */
    startCopyTrading: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/copy-trading/start`, data);
        return response.data;
    },

    /**
     * Fetch Reddit posts (Legacy Support)
     * @param {string} subreddit
     * @param {number} limit
     * @param {boolean} mock
     */
    fetchRedditPosts: async (subreddit, limit, mock = true) => {
        // NOTE: The original store used /api/v1/social/reddit/posts.
        // We preserve this endpoint path but route through apiClient.
        const response = await apiClient.get(`/social/reddit/posts`, {
            params: { subreddit, limit, mock }
        });
        return response.data;
    },

    /**
     * Analyze Reddit sentiment for a ticker (Legacy Support)
     * @param {string} ticker
     * @param {boolean} mock
     */
    analyzeRedditSentiment: async (ticker, mock = true) => {
        const response = await apiClient.get(`/social/reddit/analyze/${ticker}`, {
            params: { mock }
        });
        return response.data;
    }
};

export default socialService;
