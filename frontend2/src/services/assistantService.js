import apiClient from './apiClient';

class AssistantService {
    constructor() {
        this.baseUrl = '/api/ai-assistant';
    }

    /**
     * Creates a new conversation session.
     */
    async createConversation(userId = 'user_1', title = 'Investment Assistant Chat') {
        try {
            const response = await apiClient.post(`${this.baseUrl}/conversation/create`, { user_id: userId, title });
            return response.data.data;
        } catch (error) {
            console.error('Assistant Service Error [createConversation]:', error);
            throw error;
        }
    }

    /**
     * Sends a message in a conversation and gets a response.
     */
    async sendMessage(conversationId, message) {
        try {
            const response = await apiClient.post(`${this.baseUrl}/conversation/${conversationId}/message`, { message });
            return response.data.data;
        } catch (error) {
            console.error('Assistant Service Error [sendMessage]:', error);
            throw error;
        }
    }

    /**
     * Loads personalized recommendations.
     */
    async getRecommendations(userId = 'user_1') {
        try {
            const response = await apiClient.get(`${this.baseUrl}/recommendations/${userId}`);
            return response.data.data || [];
        } catch (error) {
            console.error('Assistant Service Error [getRecommendations]:', error);
            throw error;
        }
    }
}

export const assistantService = new AssistantService();
export default assistantService;
