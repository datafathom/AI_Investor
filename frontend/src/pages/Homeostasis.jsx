import React, { Suspense, lazy } from 'react';
import DepartmentViz from '../components/Departments/DepartmentViz/DepartmentViz';
import { D3_TYPES } from '../config/departmentRegistry';
import { Shield, ArrowRightLeft, Info } from 'lucide-react';
import './Homeostasis.css';

const HomeostasisWidget = lazy(() => import('../components/AI_Investor/Views/HomeostasisWidget'));

const Homeostasis = () => {
    return (
        <div className="homeostasis-page">
            <header className="homeostasis-header">
                <div className="flex items-center gap-4">
                    <Shield className="w-10 h-10 text-cyan-400" />
                    <div>
                        <h1>Total Homeostasis</h1>
                        <p>Real-time equilibrium monitoring: Liquidity vs. Institutional Debt</p>
                    </div>
                </div>
            </header>

            <div className="homeostasis-grid">
                {/* Main Visualization Center */}
                <section className="viz-section glass">
                    <h2>
                        <ArrowRightLeft className="w-5 h-5 text-cyan-400" />
                        Liquidity Flow Architecture (Sankey Projection)
                    </h2>
                    <div className="flex-1 min-h-[500px]">
                        <DepartmentViz 
                            type={D3_TYPES.SANKEY} 
                            color="#00f2ff" 
                            deptId={1} 
                        />
                    </div>
                </section>

                {/* Status Sidebar */}
                <aside className="info-sidebar">
                    <Suspense fallback={<div className="p-8 text-cyan-500">Connecting to Homeostasis Stream...</div>}>
                        <HomeostasisWidget />
                    </Suspense>

                    <div className="homeostasis-summary-card glass">
                        <h3>
                            <Info className="w-4 h-4 inline mr-2" />
                            System Protocol
                        </h3>
                        <p>
                            Homeostasis represents the point of total financial independence where 
                            risk-free yields cover all institutional burn rates. The system 
                            automatically shifts from **Aggressive Growth** to **Defensive Preservation** 
                            once the 100% threshold is sustained.
                        </p>
                    </div>

                    <div className="homeostasis-summary-card glass">
                        <h3>Institutional Health</h3>
                        <div className="space-y-4 mt-2">
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-400">Solvency Buffer</span>
                            <span className="text-green-400 font-mono">STABLE</span>
                          </div>
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-400">Yield/Debt Ratio</span>
                            <span className="text-cyan-400 font-mono">142.4%</span>
                          </div>
                          <div className="flex justify-between items-center text-sm">
                            <span className="text-gray-400">Burn Coverage</span>
                            <span className="text-cyan-400 font-mono">YES</span>
                          </div>
                        </div>
                    </div>
                </aside>
            </div>

            {/* Force Scroll Buffer */}
            <div style={{ height: '150px', width: '100%', flexShrink: 0 }} />
        </div>
    );
};

export default Homeostasis;
