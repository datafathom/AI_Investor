import React from 'react';
import { Home, Palette, Briefcase, Car, Gem, Landmark } from 'lucide-react';
import './ManualEntry.css'; // Shared styles

export const ASSET_CATEGORIES = [
  { id: 'real_estate', label: 'Real Estate', icon: Home, color: 'var(--neon-cyan)' },
  { id: 'art', label: 'Art & Collectibles', icon: Palette, color: 'var(--neon-purple)' },
  { id: 'pe', label: 'Private Equity', icon: Briefcase, color: 'var(--neon-green)' },
  { id: 'vehicles', label: 'Vehicles', icon: Car, color: 'var(--neon-yellow)' },
  { id: 'jewelry', label: 'Jewelry', icon: Gem, color: 'var(--neon-red)' },
  { id: 'other', label: 'Other Illiquid', icon: Landmark, color: 'var(--text-secondary)' },
];

export default function AssetCategories({ selectedCategory, onSelect }) {
  return (
    <div className="asset-categories-grid">
      {ASSET_CATEGORIES.map((cat) => {
        const Icon = cat.icon;
        const isSelected = selectedCategory === cat.label; // Using label as key for simplicity in store
        
        return (
          <button
            key={cat.id}
            className={`category-card ${isSelected ? 'selected' : ''}`}
            onClick={() => onSelect(cat.label)}
            style={{ '--cat-color': cat.color }}
          >
            <div className="cat-icon-wrapper">
              <Icon size={24} />
            </div>
            <span className="cat-label">{cat.label}</span>
            {isSelected && <div className="cat-glow" />}
          </button>
        );
      })}
    </div>
  );
}
