import React from 'react';
import QuotaHealthMeter from './QuotaHealthMeter';
import LatencyGlobalMap from './LatencyGlobalMap';
import SearchHistorySpotlight from './SearchHistorySpotlight';
import SystemLoadRibbon from './SystemLoadRibbon';
import CliHistoryWizard from './CliHistoryWizard';
import AuthSessionTimer from './AuthSessionTimer';
import './Widgets.css';

const WidgetShowcase = () => {
    return (
        <div className="widget-showcase">
            <h1 className="showcase-title">Sprint 1: Telemetry & Status Widgets</h1>
            <div className="widget-grid">
                <div className="widget-column">
                    <QuotaHealthMeter />
                    <AuthSessionTimer />
                    <SearchHistorySpotlight />
                </div>
                <div className="widget-column">
                    <LatencyGlobalMap />
                    <SystemLoadRibbon />
                    <CliHistoryWizard />
                </div>
            </div>
        </div>
    );
};

export default WidgetShowcase;
