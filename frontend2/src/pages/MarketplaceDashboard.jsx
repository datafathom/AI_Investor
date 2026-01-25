/**
 * ==============================================================================
 * FILE: frontend2/src/pages/MarketplaceDashboard.jsx
 * ROLE: Marketplace & Extensions Dashboard
 * PURPOSE: Phase 30 - Marketplace & Extensions
 *          Displays extension marketplace, installation management, and reviews.
 * 
 * INTEGRATION POINTS:
 *    - MarketplaceAPI: /api/v1/marketplace endpoints
 * 
 * FEATURES:
 *    - Extension browsing
 *    - Installation management
 *    - Reviews and ratings
 *    - Extension management
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MarketplaceDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const MarketplaceDashboard = () => {
  const [extensions, setExtensions] = useState([]);
  const [installedExtensions, setInstalledExtensions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userId] = useState('user_1');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadExtensions();
    loadInstalledExtensions();
  }, []);

  const loadExtensions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/marketplace/extensions`, {
        params: { search: searchQuery }
      });
      setExtensions(res.data.data || []);
    } catch (error) {
      console.error('Error loading extensions:', error);
    }
  };

  const loadInstalledExtensions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/v1/marketplace/installed`, {
        params: { user_id: userId }
      });
      setInstalledExtensions(res.data.data || []);
    } catch (error) {
      console.error('Error loading installed extensions:', error);
    }
  };

  const installExtension = async (extensionId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/marketplace/install`, {
        user_id: userId,
        extension_id: extensionId
      });
      loadInstalledExtensions();
    } catch (error) {
      console.error('Error installing extension:', error);
    } finally {
      setLoading(false);
    }
  };

  const uninstallExtension = async (extensionId) => {
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/api/v1/marketplace/uninstall`, {
        extension_id: extensionId
      });
      loadInstalledExtensions();
    } catch (error) {
      console.error('Error uninstalling extension:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    for (let i = 0; i < 5; i++) {
      stars.push(
        <span key={i} className={i < rating ? 'star filled' : 'star'}>
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <div className="marketplace-dashboard">
      <div className="dashboard-header">
        <h1>Extension Marketplace</h1>
        <p className="subtitle">Phase 30: Marketplace & Extensions</p>
      </div>

      <div className="search-bar">
        <input
          type="text"
          placeholder="Search extensions..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && loadExtensions()}
          className="search-input"
        />
        <button onClick={loadExtensions} className="search-button">
          Search
        </button>
      </div>

      <div className="dashboard-content">
        {/* Available Extensions */}
        <div className="extensions-panel">
          <h2>Available Extensions</h2>
          {extensions.length > 0 ? (
            <div className="extensions-grid">
              {extensions.map((extension) => {
                const isInstalled = installedExtensions.some(
                  inst => inst.extension_id === extension.extension_id
                );
                return (
                  <div key={extension.extension_id} className="extension-card">
                    <div className="extension-header">
                      <h3>{extension.extension_name}</h3>
                      <div className="extension-rating">
                        {renderStars(Math.round(extension.average_rating || 0))}
                        <span className="rating-value">({extension.review_count || 0})</span>
                      </div>
                    </div>
                    <p className="extension-description">{extension.description}</p>
                    <div className="extension-meta">
                      <span className="extension-author">By: {extension.author_name}</span>
                      <span className="extension-category">{extension.category}</span>
                    </div>
                    <div className="extension-stats">
                      <span>Downloads: {extension.download_count || 0}</span>
                      <span>Version: {extension.version}</span>
                    </div>
                    {isInstalled ? (
                      <button className="installed-button" disabled>
                        Installed
                      </button>
                    ) : (
                      <button
                        onClick={() => installExtension(extension.extension_id)}
                        disabled={loading}
                        className="install-button"
                      >
                        Install
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="no-data">No extensions found</div>
          )}
        </div>

        {/* Installed Extensions */}
        <div className="installed-panel">
          <h2>Installed Extensions</h2>
          {installedExtensions.length > 0 ? (
            <div className="installed-list">
              {installedExtensions.map((extension) => (
                <div key={extension.extension_id} className="installed-card">
                  <div className="installed-header">
                    <h3>{extension.extension_name}</h3>
                    <span className="installed-version">v{extension.version}</span>
                  </div>
                  <p className="installed-description">{extension.description}</p>
                  <div className="installed-actions">
                    <button className="update-button">Update</button>
                    <button
                      onClick={() => uninstallExtension(extension.extension_id)}
                      disabled={loading}
                      className="uninstall-button"
                    >
                      Uninstall
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No extensions installed</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MarketplaceDashboard;
