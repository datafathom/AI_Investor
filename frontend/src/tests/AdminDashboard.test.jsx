import React from 'react';
import { render, screen } from '@testing-library/react';
import AdminDashboard from '../pages/AdminDashboard';

describe('AdminDashboard Component', () => {
    it('renders the admin control center header', () => {
        render(<AdminDashboard />);
        expect(screen.getByText(/Admin Control Center/i)).toBeTruthy();
        expect(screen.getByText(/Agent and Cloud Infrastructure Health Monitoring/i)).toBeTruthy();
    });

    it('renders the service status section', () => {
        render(<AdminDashboard />);
        expect(screen.getByText(/Service Status/i)).toBeTruthy();
        expect(screen.getByText(/Core API/i)).toBeTruthy();
        expect(screen.getByText(/Data Ingestion/i)).toBeTruthy();
    });

    it('renders the infrastructure quick stats', () => {
        render(<AdminDashboard />);
        expect(screen.getByText(/Infrastucture Quick Stats/i)).toBeTruthy();
        expect(screen.getByText(/Total Servers/i)).toBeTruthy();
        expect(screen.getByText(/Active Agents/i)).toBeTruthy();
    });
});
