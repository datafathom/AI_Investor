import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './Legal.css';

const TermsOfService = () => {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [version, setVersion] = useState('');
  const [effectiveDate, setEffectiveDate] = useState('');

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        const response = await apiClient.get('/legal/documents/terms_of_service');
        if (response.data.success) {
          setContent(response.data.data.content);
          setVersion(response.data.data.version);
          setEffectiveDate(response.data.data.effective_date);
        }
      } catch (err) {
        setError('Failed to load Terms of Service');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, []);

  if (loading) {
    return <div className="legal-container">Loading...</div>;
  }

  if (error) {
    return <div className="legal-container error">{error}</div>;
  }

  return (
    <div className="legal-container">
      <div className="legal-header">
        <h1>Terms of Service</h1>
        <div className="legal-meta">
          <span>Version: {version}</span>
          <span>Effective Date: {effectiveDate}</span>
        </div>
      </div>
      <div className="legal-content">
        <div dangerouslySetInnerHTML={{ __html: content.replace(/\n/g, '<br />') }} />
      </div>
    </div>
  );
};

export default TermsOfService;
