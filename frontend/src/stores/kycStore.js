/**
 * KYC Store - Zustand State Management for KYC & Document Vault
 * 
 * : Manages identity verification status, document uploads,
 * and regulatory filing deadlines.
 * 
 * State slices:
 * - verificationStatus: Current user verification level
 * - documents: Uploaded document list
 * - filingDeadlines: Upcoming regulatory deadlines
 * - uploadProgress: Active upload progress tracking
 * 
 * Usage:
 *   const { verificationStatus, uploadDocument } = useKYCStore();
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

/**
 * @typedef {'pending'|'verified'|'rejected'|'expired'} DocumentStatus
 */

/**
 * @typedef {Object} Document
 * @property {string} id
 * @property {string} type
 * @property {string} filename
 * @property {DocumentStatus} status
 * @property {string} uploadedAt
 * @property {string|null} expiresAt
 */

/**
 * @typedef {Object} VerificationResult
 * @property {boolean} isVerified
 * @property {'basic'|'enhanced'|'accredited'} level
 * @property {string[]} missingDocuments
 * @property {string|null} expiresAt
 */

/**
 * @typedef {Object} FilingDeadline
 * @property {string} filingType
 * @property {string} dueDate
 * @property {string} description
 * @property {'upcoming'|'due_soon'|'overdue'} status
 * @property {number} daysRemaining
 */

const useKYCStore = create((set, get) => ({
    // ─────────────────────────────────────────────────────────────────────────
    // State
    // ─────────────────────────────────────────────────────────────────────────
    
    /** @type {VerificationResult|null} */
    verificationStatus: null,
    
    /** @type {Document[]} */
    documents: [],
    
    /** @type {FilingDeadline[]} */
    filingDeadlines: [],
    
    /** @type {Object.<string, number>} */
    uploadProgress: {},
    
    /** @type {boolean} */
    isLoading: false,
    
    /** @type {string|null} */
    error: null,
    
    /** @type {boolean} */
    isUploading: false,
    
    // ─────────────────────────────────────────────────────────────────────────
    // Actions
    // ─────────────────────────────────────────────────────────────────────────
    
    /**
     * Sets the verification status
     * @param {VerificationResult} status 
     */
    setVerificationStatus: (status) => set({ verificationStatus: status }),
    
    /**
     * Sets the documents list
     * @param {Document[]} docs 
     */
    setDocuments: (docs) => set({ documents: docs }),
    
    /**
     * Adds a document to the list
     * @param {Document} doc 
     */
    addDocument: (doc) => set((state) => ({
        documents: [...state.documents, doc]
    })),
    
    /**
     * Updates a document's status
     * @param {string} docId 
     * @param {DocumentStatus} status 
     */
    updateDocumentStatus: (docId, status) => set((state) => ({
        documents: state.documents.map(d => 
            d.id === docId ? { ...d, status } : d
        )
    })),
    
    /**
     * Removes a document
     * @param {string} docId 
     */
    removeDocument: (docId) => set((state) => ({
        documents: state.documents.filter(d => d.id !== docId)
    })),
    
    /**
     * Sets filing deadlines
     * @param {FilingDeadline[]} deadlines 
     */
    setFilingDeadlines: (deadlines) => set({ filingDeadlines: deadlines }),
    
    /**
     * Updates upload progress for a file
     * @param {string} filename 
     * @param {number} progress 
     */
    setUploadProgress: (filename, progress) => set((state) => ({
        uploadProgress: { ...state.uploadProgress, [filename]: progress }
    })),
    
    /**
     * Clears upload progress for a file
     * @param {string} filename 
     */
    clearUploadProgress: (filename) => set((state) => {
        const { [filename]: removed, ...rest } = state.uploadProgress;
        return { uploadProgress: rest };
    }),
    
    /**
     * Sets loading state
     * @param {boolean} loading 
     */
    setLoading: (loading) => set({ isLoading: loading }),
    
    /**
     * Sets uploading state
     * @param {boolean} uploading 
     */
    setUploading: (uploading) => set({ isUploading: uploading }),
    
    /**
     * Sets error message
     * @param {string|null} error 
     */
    setError: (error) => set({ error: error }),
    
    /**
     * Clears error state
     */
    clearError: () => set({ error: null }),
    
    // ─────────────────────────────────────────────────────────────────────────
    // Computed / Selectors
    // ─────────────────────────────────────────────────────────────────────────
    
    /**
     * Gets verified documents count
     * @returns {number}
     */
    getVerifiedCount: () => {
        const state = get();
        return state.documents.filter(d => d.status === 'verified').length;
    },
    
    /**
     * Gets pending documents count
     * @returns {number}
     */
    getPendingCount: () => {
        const state = get();
        return state.documents.filter(d => d.status === 'pending').length;
    },
    
    /**
     * Gets urgent filing deadlines (due within 7 days)
     * @returns {FilingDeadline[]}
     */
    getUrgentDeadlines: () => {
        const state = get();
        return state.filingDeadlines.filter(d => d.daysRemaining <= 7);
    },
    
    /**
     * Checks if user is fully verified
     * @returns {boolean}
     */
    isFullyVerified: () => {
        const state = get();
        return state.verificationStatus?.isVerified === true;
    },
    
    /**
     * Gets verification level
     * @returns {string|null}
     */
    getVerificationLevel: () => {
        const state = get();
        return state.verificationStatus?.level || null;
    },
    
    // ─────────────────────────────────────────────────────────────────────────
    // Async Actions (API Integration)
    // ─────────────────────────────────────────────────────────────────────────
    
    /**
     * Fetches verification status from API
     */
    fetchVerificationStatus: async () => {
        const { setLoading, setError, setVerificationStatus } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await apiClient.get('/kyc/status');
            setVerificationStatus(response.data);
        } catch (error) {
            console.error('Error fetching verification status:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Fetches user documents from API
     */
    fetchDocuments: async () => {
        const { setLoading, setError, setDocuments } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await apiClient.get('/kyc/documents');
            setDocuments(response.data.documents || []);
        } catch (error) {
            console.error('Error fetching documents:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Fetches filing deadlines from API
     */
    fetchFilingDeadlines: async () => {
        const { setLoading, setError, setFilingDeadlines } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await apiClient.get('/kyc/filings/calendar');
            setFilingDeadlines(response.data.deadlines || []);
        } catch (error) {
            console.error('Error fetching filing deadlines:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Uploads a document
     * @param {File} file 
     * @param {string} documentType 
     */
    uploadDocument: async (file, documentType) => {
        const { setUploading, setError, addDocument, setUploadProgress, clearUploadProgress } = get();
        
        setUploading(true);
        setError(null);
        setUploadProgress(file.name, 0);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('document_type', documentType);
            
            const response = await apiClient.post('/kyc/documents/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            addDocument(response.data.document);
            setUploadProgress(file.name, 100);
            
            // Clear progress after delay
            setTimeout(() => clearUploadProgress(file.name), 2000);
            
        } catch (error) {
            console.error('Error uploading document:', error);
            setError(error.message);
            clearUploadProgress(file.name);
        } finally {
            setUploading(false);
        }
    },
    
    /**
     * Triggers 13F XML export
     * @param {string} portfolioId 
     */
    export13F: async (portfolioId) => {
        const { setLoading, setError } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await apiClient.get(`/kyc/filings/13f/${portfolioId}/export`, {
                responseType: 'blob'
            });
            
            // Trigger download
            const url = window.URL.createObjectURL(response.data);
            const a = document.createElement('a');
            a.href = url;
            a.download = `13F_${portfolioId}_${new Date().toISOString().split('T')[0]}.xml`;
            a.click();
            window.URL.revokeObjectURL(url);
            
        } catch (error) {
            console.error('Error exporting 13F:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Resets store to initial state
     */
    reset: () => set({
        verificationStatus: null,
        documents: [],
        filingDeadlines: [],
        uploadProgress: {},
        isLoading: false,
        error: null,
        isUploading: false
    })
}));

export default useKYCStore;
