/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Documents/DocumentLibrary.jsx
 * ROLE: Document Library Widget
 * PURPOSE: Displays and manages user documents stored in AWS S3. Supports
 *          upload, download, and deletion with drag-and-drop support.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/documents: Backend API endpoints
 *     - S3Service: AWS S3 storage backend
 *     
 * FEATURES:
 *     - Document listing with pagination
 *     - Drag-and-drop file upload
 *     - Presigned URL downloads
 *     - Delete with confirmation
 *     - Upload progress tracking
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect, useRef } from 'react';
import './DocumentLibrary.css';

const API_BASE = '/api/v1/documents';

/**
 * Format file size for display
 */
const formatFileSize = (bytes) => {
    if (!bytes) return '0 B';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
};

/**
 * Format date for display
 */
const formatDate = (dateStr) => {
    if (!dateStr) return 'Unknown';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};

/**
 * Get file icon based on content type
 */
const getFileIcon = (contentType) => {
    if (contentType?.includes('pdf')) return '📄';
    if (contentType?.includes('image')) return '🖼️';
    if (contentType?.includes('spreadsheet') || contentType?.includes('excel')) return '📊';
    if (contentType?.includes('word') || contentType?.includes('document')) return '📝';
    return '📎';
};

/**
 * DocumentLibrary Component
 */
const DocumentLibrary = () => {
    const [documents, setDocuments] = useState([]);
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [error, setError] = useState(null);
    const [category, setCategory] = useState('all');
    const [page, setPage] = useState(1);
    const [pagination, setPagination] = useState({ page: 1, per_page: 20, total: 0, pages: 0 });
    const [deleteConfirm, setDeleteConfirm] = useState(null);
    
    const fileInputRef = useRef(null);
    const dropZoneRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);

    // Load documents on mount and when filters change
    useEffect(() => {
        fetchDocuments();
    }, [category, page]);

    const fetchDocuments = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const params = new URLSearchParams({
                page: page.toString(),
                per_page: '20'
            });
            if (category !== 'all') {
                params.set('category', category);
            }
            
            const response = await fetch(`${API_BASE}?${params}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch documents: ${response.statusText}`);
            }
            
            const data = await response.json();
            setDocuments(data.data.documents || []);
            setPagination(data.data.pagination || {});
        } catch (err) {
            console.error('Failed to fetch documents:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleFileSelect = async (files) => {
        if (!files || files.length === 0) return;
        
        const file = files[0];
        
        // Validate file size (10MB limit)
        const maxSize = 10 * 1024 * 1024;
        if (file.size > maxSize) {
            setError(`File too large. Maximum size is ${formatFileSize(maxSize)}`);
            return;
        }
        
        setUploading(true);
        setUploadProgress(0);
        setError(null);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('category', category === 'all' ? 'general' : category);
            formData.append('description', '');
            
            // Simulate upload progress (in real app, use XMLHttpRequest for progress)
            const progressInterval = setInterval(() => {
                setUploadProgress(prev => Math.min(prev + 10, 90));
            }, 100);
            
            const response = await fetch(`${API_BASE}`, {
                method: 'POST',
                body: formData
            });
            
            clearInterval(progressInterval);
            setUploadProgress(100);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.errors?.[0]?.message || 'Upload failed');
            }
            
            // Refresh document list
            await fetchDocuments();
            setUploadProgress(0);
            
        } catch (err) {
            console.error('Upload failed:', err);
            setError(err.message);
        } finally {
            setUploading(false);
            setTimeout(() => setUploadProgress(0), 1000);
        }
    };

    const handleDownload = async (documentId, filename) => {
        try {
            const response = await fetch(`${API_BASE}/${documentId}?expires_in=3600`);
            if (!response.ok) {
                throw new Error('Failed to get download URL');
            }
            
            const data = await response.json();
            const downloadUrl = data.data.download_url;
            
            // Open in new tab
            window.open(downloadUrl, '_blank');
        } catch (err) {
            console.error('Download failed:', err);
            setError(err.message);
        }
    };

    const handleDelete = async (documentId) => {
        try {
            const response = await fetch(`${API_BASE}/${documentId}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                throw new Error('Delete failed');
            }
            
            // Refresh document list
            await fetchDocuments();
            setDeleteConfirm(null);
        } catch (err) {
            console.error('Delete failed:', err);
            setError(err.message);
        }
    };

    // Drag and drop handlers
    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files);
        }
    };

    return (
        <div className="document-library">
            <div className="document-library__header">
                <h3 className="document-library__title">📁 Document Library</h3>
                <div className="document-library__controls">
                    <select
                        className="document-library__category-select"
                        value={category}
                        onChange={(e) => {
                            setCategory(e.target.value);
                            setPage(1);
                        }}
                    >
                        <option value="all">All Categories</option>
                        <option value="tax">Tax Documents</option>
                        <option value="kyc">KYC Documents</option>
                        <option value="report">Reports</option>
                        <option value="user_upload">User Uploads</option>
                        <option value="general">General</option>
                    </select>
                    <button
                        className="document-library__upload-btn"
                        onClick={() => fileInputRef.current?.click()}
                        disabled={uploading}
                    >
                        {uploading ? '⏳ Uploading...' : '📤 Upload'}
                    </button>
                </div>
            </div>

            {/* Drag and Drop Zone */}
            <div
                ref={dropZoneRef}
                className={`document-library__drop-zone ${isDragging ? 'dragging' : ''}`}
                onDragEnter={handleDragEnter}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <input
                    ref={fileInputRef}
                    type="file"
                    style={{ display: 'none' }}
                    onChange={(e) => handleFileSelect(e.target.files)}
                />
                {uploading ? (
                    <div className="document-library__upload-progress">
                        <div className="document-library__progress-bar">
                            <div
                                className="document-library__progress-fill"
                                style={{ width: `${uploadProgress}%` }}
                            />
                        </div>
                        <span>{uploadProgress}%</span>
                    </div>
                ) : (
                    <p className="document-library__drop-text">
                        Drag and drop files here or click Upload
                    </p>
                )}
            </div>

            {/* Error Display */}
            {error && (
                <div className="document-library__error">
                    ⚠️ {error}
                    <button onClick={() => setError(null)}>✕</button>
                </div>
            )}

            {/* Document List */}
            <div className="document-library__list">
                {loading ? (
                    <div className="document-library__loading">
                        <div className="document-library__skeleton"></div>
                        <div className="document-library__skeleton"></div>
                        <div className="document-library__skeleton"></div>
                    </div>
                ) : documents.length === 0 ? (
                    <div className="document-library__empty">
                        <p>No documents found</p>
                        <p className="document-library__empty-hint">
                            Upload your first document using the Upload button above
                        </p>
                    </div>
                ) : (
                    documents.map((doc) => (
                        <div key={doc.document_id} className="document-library__item">
                            <div className="document-library__item-icon">
                                {getFileIcon(doc.content_type)}
                            </div>
                            <div className="document-library__item-info">
                                <div className="document-library__item-name">
                                    {doc.filename}
                                </div>
                                <div className="document-library__item-meta">
                                    <span>{formatFileSize(doc.size_bytes)}</span>
                                    <span>•</span>
                                    <span>{formatDate(doc.uploaded_at)}</span>
                                    {doc.category && (
                                        <>
                                            <span>•</span>
                                            <span className="document-library__category-badge">
                                                {doc.category}
                                            </span>
                                        </>
                                    )}
                                </div>
                            </div>
                            <div className="document-library__item-actions">
                                <button
                                    className="document-library__action-btn document-library__action-btn--download"
                                    onClick={() => handleDownload(doc.document_id, doc.filename)}
                                    title="Download"
                                >
                                    ⬇️
                                </button>
                                <button
                                    className="document-library__action-btn document-library__action-btn--delete"
                                    onClick={() => setDeleteConfirm(doc.document_id)}
                                    title="Delete"
                                >
                                    🗑️
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>

            {/* Pagination */}
            {pagination.pages > 1 && (
                <div className="document-library__pagination">
                    <button
                        className="document-library__page-btn"
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        disabled={page === 1}
                    >
                        ← Previous
                    </button>
                    <span className="document-library__page-info">
                        Page {pagination.page} of {pagination.pages}
                    </span>
                    <button
                        className="document-library__page-btn"
                        onClick={() => setPage(p => Math.min(pagination.pages, p + 1))}
                        disabled={page === pagination.pages}
                    >
                        Next →
                    </button>
                </div>
            )}

            {/* Delete Confirmation Modal */}
            {deleteConfirm && (
                <div className="document-library__modal-overlay" onClick={() => setDeleteConfirm(null)}>
                    <div className="document-library__modal" onClick={(e) => e.stopPropagation()}>
                        <h4>Confirm Delete</h4>
                        <p>Are you sure you want to delete this document? This action cannot be undone.</p>
                        <div className="document-library__modal-actions">
                            <button
                                className="document-library__modal-btn document-library__modal-btn--cancel"
                                onClick={() => setDeleteConfirm(null)}
                            >
                                Cancel
                            </button>
                            <button
                                className="document-library__modal-btn document-library__modal-btn--confirm"
                                onClick={() => handleDelete(deleteConfirm)}
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default DocumentLibrary;
