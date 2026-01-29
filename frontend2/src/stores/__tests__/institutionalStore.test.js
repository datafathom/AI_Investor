import { describe, it, expect, beforeEach, vi } from 'vitest';
import useInstitutionalStore from '../institutionalStore';
import apiClient from '../../services/apiClient';

vi.mock('../../services/apiClient', () => ({
    default: {
        get: vi.fn(),
        post: vi.fn(),
    }
}));

describe('institutionalStore', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useInstitutionalStore.setState({
            clients: [],
            analytics: {},
            revenueForecast: null,
            riskLevels: {},
            signatures: {},
            assetAllocation: {},
            loading: false,
            error: null,
            onboardingStep: 1,
        });
    });

    it('should initialize with default state', () => {
        const state = useInstitutionalStore.getState();
        expect(state.clients).toEqual([]);
        expect(state.loading).toBe(false);
        expect(state.onboardingStep).toBe(1);
    });

    it('should fetch clients successfully', async () => {
        const mockClients = [{ client_id: '1', client_name: 'Test Client' }];
        apiClient.get.mockResolvedValueOnce({ data: mockClients });

        await useInstitutionalStore.getState().fetchClients();

        expect(apiClient.get).toHaveBeenCalledWith('/institutional/clients');
        expect(useInstitutionalStore.getState().clients).toEqual(mockClients);
        expect(useInstitutionalStore.getState().loading).toBe(false);
    });

    it('should handle fetch clients error', async () => {
        apiClient.get.mockRejectedValueOnce(new Error('Network Error'));

        await useInstitutionalStore.getState().fetchClients();

        expect(useInstitutionalStore.getState().error).toBe('Network Error');
        expect(useInstitutionalStore.getState().loading).toBe(false);
    });

    it('should fetch client analytics', async () => {
        const mockAnalytics = { fee_forecast: 1000 };
        apiClient.get.mockResolvedValueOnce({ data: mockAnalytics });

        await useInstitutionalStore.getState().fetchClientAnalytics('client123');

        expect(apiClient.get).toHaveBeenCalledWith('/institutional/analytics/client123');
        expect(useInstitutionalStore.getState().analytics['client123']).toEqual(mockAnalytics);
    });

    it('should fetch revenue forecast', async () => {
        const mockForecast = { current_fees: 5000 };
        apiClient.get.mockResolvedValueOnce({ data: mockForecast });

        await useInstitutionalStore.getState().fetchRevenueForecast();

        expect(apiClient.get).toHaveBeenCalledWith('/institutional/analytics/fees');
        expect(useInstitutionalStore.getState().revenueForecast).toEqual(mockForecast);
    });

    it('should fetch risk levels', async () => {
        const mockRisk = { volatility_score: 15 };
        apiClient.get.mockResolvedValueOnce({ data: mockRisk });

        await useInstitutionalStore.getState().fetchRiskLevels('client123');

        expect(apiClient.get).toHaveBeenCalledWith('/institutional/analytics/risk/client123');
        expect(useInstitutionalStore.getState().riskLevels['client123']).toEqual(mockRisk);
    });

    it('should fetch signatures', async () => {
        const mockSignatures = { completion_percentage: 75 };
        apiClient.get.mockResolvedValueOnce({ data: mockSignatures });

        await useInstitutionalStore.getState().fetchSignatures('client123');

        expect(apiClient.get).toHaveBeenCalledWith('/institutional/analytics/signatures/client123');
        expect(useInstitutionalStore.getState().signatures['client123']).toEqual(mockSignatures);
    });

    it('should fetch asset allocation', async () => {
        const mockAllocation = { total_aum: 1000000 };
        apiClient.get.mockResolvedValueOnce({ data: mockAllocation });

        await useInstitutionalStore.getState().fetchAssetAllocation('client123');

        expect(apiClient.get).toHaveBeenCalledWith('/institutional/analytics/allocation/client123');
        expect(useInstitutionalStore.getState().assetAllocation['client123']).toEqual(mockAllocation);
    });

    it('should create client successfully', async () => {
        const newClient = { client_name: 'New Client' };
        const mockResponse = { data: { client_id: 'new123', ...newClient } };
        apiClient.post.mockResolvedValueOnce(mockResponse);

        const result = await useInstitutionalStore.getState().createClient(newClient);

        expect(apiClient.post).toHaveBeenCalledWith('/institutional/client/create', newClient);
        expect(useInstitutionalStore.getState().clients).toContainEqual(mockResponse.data);
        expect(result).toEqual(mockResponse.data);
    });

    it('should handle create client error', async () => {
        apiClient.post.mockRejectedValueOnce(new Error('Post Error'));

        const result = await useInstitutionalStore.getState().createClient({ name: 'Fail' });

        expect(result).toBeNull();
        expect(useInstitutionalStore.getState().error).toBe('Post Error');
    });

    it('should set onboarding step', () => {
        useInstitutionalStore.getState().setOnboardingStep(3);
        expect(useInstitutionalStore.getState().onboardingStep).toBe(3);
    });

    it('should reset onboarding', () => {
        useInstitutionalStore.setState({ onboardingStep: 4 });
        useInstitutionalStore.getState().resetOnboarding();
        expect(useInstitutionalStore.getState().onboardingStep).toBe(1);
    });
});
