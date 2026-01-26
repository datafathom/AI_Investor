import { authService } from './authService';

class AssistantService {
    constructor() {
        this.baseUrl = '/api/ai-assistant';
    }

    /**
     * Creates a new conversation session.
     */
    async createConversation(userId = 'user_1', title = 'Investment Assistant Chat') {
        try {
            const response = await authService.authenticatedFetch(`${this.baseUrl}/conversation/create`, {
                method: 'POST',
                body: JSON.stringify({ user_id: userId, title })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Failed to create conversation');
            return data.data;
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
            const response = await authService.authenticatedFetch(`${this.baseUrl}/conversation/${conversationId}/message`, {
                method: 'POST',
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Failed to send message');
            return data.data;
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
            const response = await authService.authenticatedFetch(`${this.baseUrl}/recommendations/${userId}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Failed to load recommendations');
            return data.data || [];
        } catch (error) {
            console.error('Assistant Service Error [getRecommendations]:', error);
            throw error;
        }
    }
}

export const assistantService = new AssistantService();
export default assistantService;
