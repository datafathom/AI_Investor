import React, { useState, useEffect, useRef } from 'react';
import apiClient from '../services/apiClient';
import { Network, Activity, Cpu, ShieldAlert, Zap, Layers, Box, Clock, Search } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import * as d3 from 'd3';
import { StatCard } from '../components/DataViz';
import useTimelineStore from '../stores/timelineStore';
import RegimeLight from '../components/Charts/RegimeLight';
import DeepDive from '../components/Research/DeepDive';
import MasterView from '../components/Dashboard/MasterView';

import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const MasterOrchestrator = () => {
    // This page acts as the entry point for the "Master View" of the entire AI Investment System.
    // We render the consolidated MasterView component which handles the sub-layouting.
    
    return (
        <div className="full-bleed-page system-dashboard-page bg-[#0a0e14] overflow-y-auto">
             <MasterView />
        </div>
    );
};

export default MasterOrchestrator;
