import React from 'react';
import { useLocation } from 'react-router-dom';
import { getOverviewForPath } from '../data/overviewContent';
import { 
  Layout, 
  Cpu, 
  Search, 
  PieChart, 
  Shield, 
  Activity, 
  HardDrive, 
  Globe,
  Zap,
  Lock
} from 'lucide-react';

import CategoryDashboardTemplate from '../components/Navigation/CategoryDashboardTemplate';

const ICON_MAP = {
  Layout,
  Cpu,
  Search,
  PieChart,
  Shield,
  Activity,
  HardDrive,
  Globe,
  Zap,
  Lock
};

const RoleOverview = () => {
  const location = useLocation();
  const content = getOverviewForPath(location.pathname);

  if (!content) {
    return (
      <div className="flex items-center justify-center h-full text-zinc-500">
        <div className="text-center">
            <h2 className="text-2xl font-bold mb-2">Namespace Not Found</h2>
            <p>We couldn't find a mapping for this breadcrumb segment.</p>
        </div>
      </div>
    );
  }

  const IconComponent = ICON_MAP[content.icon] || Layout;

  return (
    <CategoryDashboardTemplate
      title={content.title}
      subtitle="V3.2.0-STABLE ROLE AUTH: VERIFIED"
      description={content.description}
      metrics={content.glimpses}
      capabilities={content.children}
      accentColor={content.accentColor}
      icon={IconComponent}
    />
  );
};

export default RoleOverview;
