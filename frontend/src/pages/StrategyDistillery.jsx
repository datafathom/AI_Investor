import React, { useEffect, Suspense } from 'react';
import { FlaskConical, Dna, Zap, Play, Info, AlertTriangle } from 'lucide-react';
import useEvolutionStore from '../stores/evolutionStore';
import './StrategyDistillery.css';

// Error Boundary for widgets
class WidgetErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error(`Widget Error [${this.props.name}]:`, error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-4 bg-red-900/20 border border-red-500/30 rounded-xl">
          <div className="flex items-center gap-2 text-red-400 text-sm mb-2">
            <AlertTriangle size={16} />
            <span className="font-bold">{this.props.name} Widget Error</span>
          </div>
          <p className="text-red-300/70 text-xs font-mono">{this.state.error?.message || 'Unknown error'}</p>
        </div>
      );
    }
    return this.props.children;
  }
}

// Lazy load widgets to isolate crashes
const FitnessSurface3D = React.lazy(() => import('../widgets/Evolution/FitnessSurface3D'));
const GeneFrequencyPlot = React.lazy(() => import('../widgets/Evolution/GeneFrequencyPlot'));
const MutationRateSlider = React.lazy(() => import('../widgets/Evolution/MutationRateSlider'));
const SurvivalProbabilityMeter = React.lazy(() => import('../widgets/Evolution/SurvivalProbabilityMeter'));
const AncestorLineageMap = React.lazy(() => import('../widgets/Evolution/AncestorLineageMap'));
const SplicingConflictResolver = React.lazy(() => import('../widgets/Evolution/SplicingConflictResolver'));
const AgentHallOfFame = React.lazy(() => import('../widgets/Evolution/AgentHallOfFame'));
const GenomicPlaybackModal = React.lazy(() => import('../components/Modals/GenomicPlaybackModal'));
const ShadowStrategyPanel = React.lazy(() => import('../widgets/Strategy/ShadowStrategyPanel'));

const WidgetLoader = () => (
  <div className="p-4 animate-pulse bg-slate-800/30 rounded-xl">
    <div className="h-4 bg-slate-700/50 rounded w-24 mb-2"></div>
    <div className="h-32 bg-slate-700/30 rounded"></div>
  </div>
);

const StrategyDistillery = () => {
  const { 
    geneFrequencies,
    hallOfFame,
    spliceAgents,
    generation,
    isEvolving,
    startEvolution,
    fitnessSurface,
    initSocket
  } = useEvolutionStore();

  const [selectedAgent, setSelectedAgent] = React.useState(null);
  const [isPlaybackOpen, setIsPlaybackOpen] = React.useState(false);
  const [splicingParents, setSplicingParents] = React.useState({ p1: null, p2: null });

  useEffect(() => {
    initSocket();
  }, [initSocket]);

  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
    setIsPlaybackOpen(true);
  };

  const handleResolveSplicing = async (resolvedGenes) => {
      if (splicingParents.p1 && splicingParents.p2) {
          await spliceAgents(splicingParents.p1, splicingParents.p2, resolvedGenes);
          setSplicingParents({ p1: null, p2: null });
      }
  };

  const activeStrategy = {
    id: 'strat_gen_7',
    name: 'Quantum Momentum v7.2',
    status: 'active'
  };

  return (
    <div className="full-bleed-page strategy-distillery-page">
      <header className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-cyan-900/30 rounded-xl border border-cyan-500/30 interact-hover">
            <FlaskConical size={32} className="text-cyan-400" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-300 to-blue-300">
              Genomic Evolution Lab
            </h1>
            <p className="text-slate-400 text-sm">Synthetic Agent Breeding & Mutation Suite</p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <div className="flex items-center gap-2 px-4 py-2 bg-slate-800/50 rounded-lg border border-slate-700">
            <Dna size={18} className="text-cyan-400" />
            <span className="font-mono text-sm">GENERATION: <span className="text-white font-bold">{generation}</span></span>
          </div>
          <button
            onClick={startEvolution}
            className={`flex items-center gap-2 px-6 py-2 rounded-lg font-bold transition-all interact-hover ${
              isEvolving 
                ? 'bg-cyan-900/50 border border-cyan-500 text-cyan-300 shadow-[0_0_20px_rgba(0,242,255,0.4)]' 
                : 'bg-cyan-600 hover:bg-cyan-500 shadow-lg shadow-cyan-500/20'
            }`}
          >
            {isEvolving ? <Zap size={18} className="animate-pulse" /> : <Play size={18} />}
            {isEvolving ? "EVOLVING..." : "INITIATE SEEDING"}
          </button>
        </div>
      </header>

      <div className="scrollable-content-wrapper">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* TOP SECTION: 3D Visualization & Shadow Engine */}
          <div className="lg:col-span-8">
            <WidgetErrorBoundary name="FitnessSurface3D">
              <Suspense fallback={<WidgetLoader />}>
                <FitnessSurface3D data={fitnessSurface} />
              </Suspense>
            </WidgetErrorBoundary>
          </div>
          <div className="lg:col-span-4">
            <WidgetErrorBoundary name="ShadowStrategyPanel">
              <Suspense fallback={<WidgetLoader />}>
                <ShadowStrategyPanel strategy={activeStrategy} userId="user_1" />
              </Suspense>
            </WidgetErrorBoundary>
          </div>

          {/* MIDDLE SECTION: Gene Frequencies & Control */}
          <div className="lg:col-span-4">
            <WidgetErrorBoundary name="MutationRateSlider">
              <Suspense fallback={<WidgetLoader />}>
                <MutationRateSlider />
              </Suspense>
            </WidgetErrorBoundary>
            <div className="mt-6 glass-panel p-4 flex items-start gap-3 bg-cyan-900/10 border-cyan-500/20">
              <Info className="text-cyan-400 mt-1" size={20} />
              <p className="text-xs text-slate-400 leading-relaxed">
                Higher mutation rates increase exploration but may destabilize successful alpha traits. 
                Use <b>Turbo</b> mode to accelerate generation cycles.
              </p>
            </div>
          </div>
          <div className="lg:col-span-8">
            <WidgetErrorBoundary name="GeneFrequencyPlot">
              <Suspense fallback={<WidgetLoader />}>
                <GeneFrequencyPlot data={geneFrequencies} />
              </Suspense>
            </WidgetErrorBoundary>
          </div>

          {/* BOTTOM SECTION: Lineage & Splicing */}
          <div className="lg:col-span-8">
            <WidgetErrorBoundary name="AncestorLineageMap">
              <Suspense fallback={<WidgetLoader />}>
                <AncestorLineageMap onSelect={handleSelectAgent} />
              </Suspense>
            </WidgetErrorBoundary>
          </div>
          <div className="lg:col-span-4">
            <WidgetErrorBoundary name="AgentHallOfFame">
              <Suspense fallback={<WidgetLoader />}>
                <AgentHallOfFame onSelectAgent={handleSelectAgent} />
              </Suspense>
            </WidgetErrorBoundary>
          </div>

          <div className="lg:col-span-12">
            <div className="p-8 glass-premium rounded-3xl border border-cyan-500/10">
                <div className="flex items-center gap-2 mb-8">
                    <Zap className="text-cyan-400" />
                    <h2 className="text-xl font-bold text-white uppercase italic">Active Splicing Lab</h2>
                </div>
                <WidgetErrorBoundary name="SplicingConflictResolver">
                  <Suspense fallback={<WidgetLoader />}>
                    <SplicingConflictResolver 
                        parent1={splicingParents.p1} 
                        parent2={splicingParents.p2} 
                        onResolve={handleResolveSplicing} 
                    />
                  </Suspense>
                </WidgetErrorBoundary>
            </div>
          </div>

        </div>
        
        <div className="scroll-buffer-100" />
      </div>

      <Suspense fallback={null}>
        <GenomicPlaybackModal 
          isOpen={isPlaybackOpen} 
          onClose={() => setIsPlaybackOpen(false)} 
          agent={selectedAgent} 
        />
      </Suspense>
    </div>
  );
};

export default StrategyDistillery;

