/**
 * Budgeting Store - Phase 17
 * Manages budgets, expenses, and insights
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useBudgetingStore = create((set, get) => ({
    // State
    budgets: [],
    expenses: [],
    insights: [],
    loading: false,
    error: null,

    // Actions
    fetchBudgets: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/budgeting/budgets', {
                params: { user_id: userId }
            });
            set({ budgets: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchExpenses: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/budgeting/expenses', {
                params: { user_id: userId }
            });
            set({ expenses: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchInsights: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/budgeting/insights', {
                params: { user_id: userId }
            });
            set({ insights: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    addExpense: async (expenseData) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/budgeting/expenses/add', expenseData);
            await get().fetchExpenses(expenseData.user_id);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    }
}));

export default useBudgetingStore;
