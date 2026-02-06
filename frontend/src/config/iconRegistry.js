import { 
  Cpu, Layout, Brain, Target, TrendingUp, Atom, Crosshair, Shield, 
  Home, ShieldCheck, Scale, Search, Users, Briefcase, Clock, Zap, 
  Landmark, Grid, Terminal, Power, Activity, Sliders, PlayCircle,
  Eye, EyeOff, RefreshCcw, LogOut, Maximize, Key, Package, Heart,
  CreditCard, Navigation, Scissors, AlertTriangle, Globe, Phone,
  Calendar, Book, Layers, Swords, Shuffle, ShieldAlert, FileText,
  PieChart, Settings
} from "lucide-react";

/**
 * DEPT_ICON_MAP - Centralized mapping for all department icons.
 */
export const DEPT_ICON_MAP = {
  'cpu': Cpu,
  'drafting-compass': Layout,
  'brain': Brain,
  'target': Target,
  'trending-up': TrendingUp,
  'atom': Atom,
  'crosshair': Crosshair,
  'shield': Shield,
  'home': Home,
  'shield-check': ShieldCheck,
  'scale': Scale,
  'search': Search,
  'users': Users,
  'briefcase': Briefcase,
  'clock': Clock,
  'zap': Zap,
  'settings': Settings,
  'landmark': Landmark,
  'terminal': Terminal,
  'grid': Grid,
  'power': Power,
  'activity': Activity,
  'sliders': Sliders,
  'play-circle': PlayCircle,
  'eye': Eye,
  'eye-off': EyeOff,
  'refresh-ccw': RefreshCcw,
  'log-out': LogOut,
  'maximize': Maximize,
  'key': Key,
  'package': Package,
  'heart': Heart,
  'credit-card': CreditCard,
  'navigation': Navigation,
  'scissors': Scissors,
  'alert-triangle': AlertTriangle,
  'globe': Globe,
  'phone': Phone,
  'calendar': Calendar,
  'book': Book,
  'layers': Layers,
  'swords': Swords,
  'shuffle': Shuffle,
  'shield-alert': ShieldAlert,
  'file-text': FileText,
  'pie-chart': PieChart
};

/**
 * Returns the Lucide icon component associated with the given name.
 * @param {string} iconName 
 * @returns {React.Component}
 */
export const getIcon = (iconName) => {
  return DEPT_ICON_MAP[iconName] || Grid;
};

export default DEPT_ICON_MAP;
