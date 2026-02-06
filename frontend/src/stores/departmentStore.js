import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import apiClient from '../services/apiClient';
import presenceService from '../services/presenceService';


/**
 * Department Store - Central state for 18-department system
 * 
 * Structure:
 * - departments: Object keyed by dept ID (1-18)
 * - activeDepartment: Currently viewed dept
 * - vennIntersection: Multi-dept view state
 * - pulse: Cross-department health metrics
 */
export const useDepartmentStore = create(
  devtools(
    persist(
      (set, get) => ({
        // ═══════════════════════════════════════════════
        // STATE
        // ═══════════════════════════════════════════════
        
        departments: {
          1: { 
            id: 1, 
            name: 'Orchestrator', 
            slug: 'orchestrator',
            quadrant: 'META',
            status: 'active', 
            agents: [],
            metrics: {
              systemLatency: 0,
              kafkaHealth: 'green',
              activeConnections: 0
            },
            color: '#00f2ff',
            lastUpdate: null
          },
          2: { 
            id: 2, 
            name: 'Architect', 
            slug: 'architect',
            quadrant: 'META',
            status: 'active', 
            agents: [],
            metrics: {
              onTrackPercent: 0,
              netWorthMomentum: 0,
              goalProgress: {}
            },
            color: '#3b82f6',
            lastUpdate: null
          },
          3: { 
            id: 3, 
            name: 'Data Scientist', 
            slug: 'data-scientist',
            quadrant: 'ATTACK',
            status: 'active', 
            agents: [],
            metrics: {
              modelConfidence: 0,
              correlationStrength: 0,
              anomalyCount: 0
            },
            color: '#8b5cf6',
            lastUpdate: null
          },
          4: { 
            id: 4, 
            name: 'Strategist', 
            slug: 'strategist',
            quadrant: 'ATTACK',
            status: 'active', 
            agents: [],
            metrics: {
              strategySuccessRate: 0,
              activePlaybooks: 0,
              riskOfRuin: 0
            },
            color: '#06b6d4',
            lastUpdate: null
          },
          5: { 
            id: 5, 
            name: 'Trader', 
            slug: 'trader',
            quadrant: 'ATTACK',
            status: 'active', 
            agents: [],
            metrics: {
              executionLatency: 0,
              dailyPnL: 0,
              openPositions: 0
            },
            color: '#22c55e',
            lastUpdate: null
          },
          6: { 
            id: 6, 
            name: 'Physicist', 
            slug: 'physicist',
            quadrant: 'ATTACK',
            status: 'active', 
            agents: [],
            metrics: {
              thetaDecayPerHour: 0,
              portfolioDelta: 0,
              vegaSensitivity: 0
            },
            color: '#a855f7',
            lastUpdate: null
          },
          7: { 
            id: 7, 
            name: 'Hunter', 
            slug: 'hunter',
            quadrant: 'ATTACK',
            status: 'active', 
            agents: [],
            metrics: {
              signalHitRate: 0,
              activeOpportunities: 0,
              sentimentScore: 0
            },
            color: '#f97316',
            lastUpdate: null
          },
          8: { 
            id: 8, 
            name: 'Sentry', 
            slug: 'sentry',
            quadrant: 'DEFENSE',
            status: 'active', 
            agents: [],
            metrics: {
              threatLevel: 'low',
              blockedAttempts24h: 0,
              credentialHealth: 100
            },
            color: '#ef4444',
            lastUpdate: null
          },
          9: { 
            id: 9, 
            name: 'Steward', 
            slug: 'steward',
            quadrant: 'HOUSEHOLD',
            status: 'active', 
            agents: [],
            metrics: {
              costOfLiving: 0,
              assetHealth: 100,
              maintenanceDue: 0
            },
            color: '#84cc16',
            lastUpdate: null
          },
          10: { 
            id: 10, 
            name: 'Guardian', 
            slug: 'guardian',
            quadrant: 'DEFENSE',
            status: 'active', 
            agents: [],
            metrics: {
              liquidityDays: 0,
              burnRate: 0,
              creditUtilization: 0
            },
            color: '#14b8a6',
            lastUpdate: null
          },
          11: { 
            id: 11, 
            name: 'Lawyer', 
            slug: 'lawyer',
            quadrant: 'DEFENSE',
            status: 'active', 
            agents: [],
            metrics: {
              taxLiability: 0,
              auditRiskScore: 0,
              complianceStatus: 'green'
            },
            color: '#6b7280',
            lastUpdate: null
          },
          12: { 
            id: 12, 
            name: 'Auditor', 
            slug: 'auditor',
            quadrant: 'DEFENSE',
            status: 'active', 
            agents: [],
            metrics: {
              feeLeakage: 0,
              slippageLoss: 0,
              performanceAlpha: 0
            },
            color: '#fbbf24',
            lastUpdate: null
          },
          13: { 
            id: 13, 
            name: 'Envoy', 
            slug: 'envoy',
            quadrant: 'HOUSEHOLD',
            status: 'active', 
            agents: [],
            metrics: {
              networkHealth: 0,
              philanthropyProgress: 0,
              pendingMeetings: 0
            },
            color: '#ec4899',
            lastUpdate: null
          },
          14: { 
            id: 14, 
            name: 'Front Office', 
            slug: 'front-office',
            quadrant: 'HOUSEHOLD',
            status: 'active', 
            agents: [],
            metrics: {
              pendingTasks: 0,
              voiceCallsActive: 0,
              inboxUnread: 0
            },
            color: '#0ea5e9',
            lastUpdate: null
          },
          15: { 
            id: 15, 
            name: 'Historian', 
            slug: 'historian',
            quadrant: 'META',
            status: 'active', 
            agents: [],
            metrics: {
              logicScore: 0,
              decisionQuality: 0,
              patternMatches: 0
            },
            color: '#78716c',
            lastUpdate: null
          },
          16: { 
            id: 16, 
            name: 'Stress-Tester', 
            slug: 'stress-tester',
            quadrant: 'META',
            status: 'active', 
            agents: [],
            metrics: {
              robustnessPercent: 0,
              worstCaseLoss: 0,
              survivalProbability: 0
            },
            color: '#dc2626',
            lastUpdate: null
          },
          17: { 
            id: 17, 
            name: 'Refiner', 
            slug: 'refiner',
            quadrant: 'META',
            status: 'active', 
            agents: [],
            metrics: {
              agentEfficiency: 0,
              tokenCost24h: 0,
              hallucinationRate: 0
            },
            color: '#7c3aed',
            lastUpdate: null
          },
          18: { 
            id: 18, 
            name: 'Banker', 
            slug: 'banker',
            quadrant: 'HOUSEHOLD',
            status: 'active', 
            agents: [],
            metrics: {
              burnRatePerDay: 0,
              pendingTransfers: 0,
              categoryBurn: {}
            },
            color: '#059669',
            lastUpdate: null
          }
        },
        
        departmentLogs: {}, // Keyed by deptId: { deptId: [log1, log2, ...] }
        
        activeDepartment: null,
        
        vennIntersection: null,
        
        pulse: {
          netWorth: 0,
          threatLevel: 'Low',
          dailyAlpha: 0,
          liquidityDays: 180,
          systemHealth: 'green',
          lastUpdate: null
        },
        
        isLoading: false,
        error: null,
        
        // ═══════════════════════════════════════════════
        // ACTIONS
        // ═══════════════════════════════════════════════
        
        initSocketListeners: () => {
          console.log("[DepartmentStore] Initializing Socket listeners...");
          
          // Agent Status Updates
          presenceService.on('agent:status-update', (data) => {
            const { agent_id, dept_id, status, details } = data;
            
            const departments = get().departments;
            const targetDeptId = dept_id || Object.keys(departments).find(id => 
              departments[id].agents?.some(a => (a.id === agent_id || a.agent_id === agent_id))
            );
            
            if (targetDeptId && departments[targetDeptId]) {
              const currentAgents = [...(departments[targetDeptId].agents || [])];
              const agentIdx = currentAgents.findIndex(a => (a.id === agent_id || a.agent_id === agent_id));
              
              if (agentIdx > -1) {
                currentAgents[agentIdx] = {
                  ...currentAgents[agentIdx],
                  status: status,
                  active: status === 'BUSY' || status === 'active',
                  last_result: details
                };
                
                get().updateDepartmentAgents(targetDeptId, currentAgents);
                get().addLogEntry(targetDeptId, {
                  type: 'agent_status_socket',
                  agent_id: agent_id,
                  message: `Status update: ${status}`
                });
              }
            }
          });

          // Metrics Updates
          presenceService.on('metrics:update', (data) => {
            const { dept_id, metrics } = data;
            if (dept_id && metrics) {
              get().updateDepartmentMetrics(dept_id, metrics);
            }
          });
          
          // Department Events (Generic)
          presenceService.on('dept_event', (data) => {
            const { dept_id, event_type, payload } = data;
            if (dept_id) {
              get().addLogEntry(dept_id, {
                type: 'event',
                event_type,
                message: payload.message || `Event: ${event_type}`,
                payload
              });
            }
          });
        },
        
        setActiveDepartment: (deptId) => {
          if (deptId !== null && !get().departments[deptId]) {
            console.warn(`Invalid department ID: ${deptId}`);
            return;
          }
          set({ activeDepartment: deptId, vennIntersection: null });
        },

        addLogEntry: (deptId, log) => {
          set((state) => {
            const currentLogs = state.departmentLogs[deptId] || [];
            // Keep only last 50 logs for performance
            const newLogs = [
              { id: Date.now() + Math.random(), timestamp: new Date().toLocaleTimeString(), ...log },
              ...currentLogs
            ].slice(0, 50);

            return {
              departmentLogs: {
                ...state.departmentLogs,
                [deptId]: newLogs
              }
            };
          });
        },
        
        clearLogs: (deptId) => {
          set((state) => ({
            departmentLogs: {
              ...state.departmentLogs,
              [deptId]: []
            }
          }));
        },
        
        triggerVennMode: (dept1Id, dept2Id) => {
          const depts = get().departments;
          if (!depts[dept1Id] || !depts[dept2Id]) {
            console.warn(`Invalid Venn department IDs: ${dept1Id}, ${dept2Id}`);
            return;
          }
          if (dept1Id === dept2Id) {
            console.warn('Cannot create Venn with same department');
            return;
          }
          set({ 
            vennIntersection: { 
              dept1: dept1Id, 
              dept2: dept2Id,
              blendColor: blendColors(depts[dept1Id].color, depts[dept2Id].color)
            },
            activeDepartment: null
          });
        },
        
        exitVennMode: () => set({ vennIntersection: null }),
        
        updateDepartmentMetrics: (deptId, metrics) => {
          set((state) => ({
            departments: {
              ...state.departments,
              [deptId]: {
                ...state.departments[deptId],
                metrics: { ...state.departments[deptId].metrics, ...metrics },
                lastUpdate: new Date().toISOString()
              }
            }
          }));
        },
        
        updateDepartmentAgents: (deptId, agents) => {
          set((state) => ({
            departments: {
              ...state.departments,
              [deptId]: {
                ...state.departments[deptId],
                agents
              }
            }
          }));
        },
        
        setDepartmentStatus: (deptId, status) => {
          set((state) => ({
            departments: {
              ...state.departments,
              [deptId]: {
                ...state.departments[deptId],
                status
              }
            }
          }));
        },
        
        updatePulse: (data) => {
          set((state) => ({
            pulse: { 
              ...state.pulse, 
              ...data,
              lastUpdate: new Date().toISOString()
            }
          }));
        },

        // --- API ACTIONS ---
        
        fetchDepartments: async () => {
          set({ isLoading: true, error: null });
          try {
            const data = await apiClient.get('/departments');
            // Transform data if needed or just replace
            // For now we use the ID-keyed object structure
            const departmentsMap = {};
            data.forEach(dept => {
              departmentsMap[dept.id] = {
                ...get().departments[dept.id], // Keep local static data (icons, etc)
                ...dept
              };
            });
            set({ departments: departmentsMap, isLoading: false });
          } catch (err) {
            set({ error: err.message, isLoading: false });
            console.error('Failed to fetch departments:', err);
          }
        },

        invokeAgent: async (deptId, agentId, payload) => {
          try {
            get().addLogEntry(deptId, {
              type: 'agent_call',
              agent_id: agentId,
              message: `Invoking agent...`
            });
            
            const result = await apiClient.post(`/departments/${deptId}/agents/${agentId}/invoke`, payload);
            
            get().addLogEntry(deptId, {
              type: 'agent_response',
              agent_id: agentId,
              message: result.response || 'Success (No response text)'
            });
            
            return result;
          } catch (err) {
            get().addLogEntry(deptId, {
              type: 'error',
              agent_id: agentId,
              message: `Error: ${err.message}`
            });
            throw err;
          }
        },
        
        setLoading: (isLoading) => set({ isLoading }),
        setError: (error) => set({ error }),
        
        // ═══════════════════════════════════════════════
        // SELECTORS (via get())
        // ═══════════════════════════════════════════════
        
        getDepartment: (deptId) => get().departments[deptId],
        
        getDepartmentsByQuadrant: (quadrant) => {
          return Object.values(get().departments)
            .filter(d => d.quadrant === quadrant);
        },
        
        getActiveDepartmentData: () => {
          const activeId = get().activeDepartment;
          return activeId ? get().departments[activeId] : null;
        },
        
        getVennDepartments: () => {
          const venn = get().vennIntersection;
          if (!venn) return null;
          return {
            dept1: get().departments[venn.dept1],
            dept2: get().departments[venn.dept2],
            blendColor: venn.blendColor
          };
        }
      }),
      {
        name: 'department-storage',
        partialize: (state) => ({
          activeDepartment: state.activeDepartment,
          // Don't persist real-time metrics
        })
      }
    ),
    { name: 'DepartmentStore' }
  )
);

// Utility: Blend two hex colors for Venn mode
function blendColors(color1, color2) {
  const hex = (c) => parseInt(c.slice(1), 16);
  const r1 = (hex(color1) >> 16) & 255;
  const g1 = (hex(color1) >> 8) & 255;
  const b1 = hex(color1) & 255;
  const r2 = (hex(color2) >> 16) & 255;
  const g2 = (hex(color2) >> 8) & 255;
  const b2 = hex(color2) & 255;
  const r = Math.round((r1 + r2) / 2);
  const g = Math.round((g1 + g2) / 2);
  const b = Math.round((b1 + b2) / 2);
  return `#${((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1)}`;
}

export default useDepartmentStore;
