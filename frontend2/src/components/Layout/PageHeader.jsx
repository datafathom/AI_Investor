/**
 * Page Header Component
 * 
 * Dynamic breadcrumbs and page title based on current route.
 */

import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useColorPalette } from '../../hooks/useColorPalette';

const routeMap = {
  '/dashboard': { title: 'Dashboard', breadcrumbs: ['Home', 'Dashboard'] },
  '/chat': { title: 'Chat', breadcrumbs: ['Home', 'Chat'] },
  '/telemetry': { title: 'Telemetry', breadcrumbs: ['Home', 'Telemetry'] },
  '/design-system': { title: 'Design System', breadcrumbs: ['Home', 'Design System'] },
  '/settings': { title: 'Settings', breadcrumbs: ['Home', 'Settings'] },
};

function PageHeader() {
  const location = useLocation();
  const { palette } = useColorPalette();
  const routeInfo = routeMap[location.pathname] || { title: 'Page', breadcrumbs: ['Home'] };

  return (
    <header
      style={{
        padding: '1.5rem 2rem',
        borderBottom: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`,
        backgroundColor: palette?.backgrounds?.card || '#fefae8',
        backdropFilter: 'blur(24px)',
      }}
    >
      {/* Breadcrumbs */}
      <nav
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          marginBottom: '0.5rem',
          fontSize: '0.875rem',
        }}
      >
        {routeInfo.breadcrumbs.map((crumb, index) => {
          const isLast = index === routeInfo.breadcrumbs.length - 1;
          return (
            <React.Fragment key={crumb}>
              {isLast ? (
                <span
                  style={{
                    color: palette?.burgundy?.primary || '#5a1520',
                    fontWeight: 600,
                  }}
                >
                  {crumb}
                </span>
              ) : (
                <>
                  <Link
                    to={index === 0 ? '/dashboard' : '#'}
                    style={{
                      color: palette?.text?.secondary || '#5a4a3a',
                      textDecoration: 'none',
                      transition: 'color 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.color = palette?.burgundy?.primary || '#5a1520';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.color = palette?.text?.secondary || '#5a4a3a';
                    }}
                  >
                    {crumb}
                  </Link>
                  <span
                    style={{
                      color: palette?.text?.secondary || '#5a4a3a',
                      opacity: 0.5,
                    }}
                  >
                    /
                  </span>
                </>
              )}
            </React.Fragment>
          );
        })}
      </nav>

      {/* Page Title */}
      <h1
        style={{
          margin: 0,
          fontSize: '1.75rem',
          fontWeight: 700,
          color: palette?.burgundy?.primary || '#5a1520',
        }}
      >
        {routeInfo.title}
      </h1>
    </header>
  );
}

export default PageHeader;

