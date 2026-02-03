import React, { useState } from 'react';
import { ChevronUp, ChevronDown, ChevronsUpDown } from 'lucide-react';
import './DataTable.css';

/**
 * Enhanced data table with sorting and hover effects.
 * 
 * @param {Array} columns - Column definitions { key, label, sortable, align, width }
 * @param {Array} data - Row data objects
 * @param {function} onRowClick - Row click handler
 * @param {string} emptyMessage - Message when no data
 */
const DataTable = ({
  columns = [],
  data = [],
  onRowClick,
  emptyMessage = 'No data available',
  className = ''
}) => {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const sortedData = React.useMemo(() => {
    if (!Array.isArray(data)) return [];
    if (!sortConfig.key) return data;
    
    return [...data].sort((a, b) => {
      const aVal = a[sortConfig.key];
      const bVal = b[sortConfig.key];
      
      if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, [data, sortConfig]);

  const getSortIcon = (key) => {
    if (sortConfig.key !== key) {
      return <ChevronsUpDown size={14} className="data-table__sort-icon" />;
    }
    return sortConfig.direction === 'asc' 
      ? <ChevronUp size={14} className="data-table__sort-icon data-table__sort-icon--active" />
      : <ChevronDown size={14} className="data-table__sort-icon data-table__sort-icon--active" />;
  };

  return (
    <div className={`data-table-container ${className}`}>
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th 
                key={col.key}
                className={`data-table__th ${col.sortable ? 'data-table__th--sortable' : ''}`}
                style={{ width: col.width, textAlign: col.align || 'left' }}
                onClick={() => col.sortable && handleSort(col.key)}
              >
                <div className="data-table__th-content">
                  <span>{col.label}</span>
                  {col.sortable && getSortIcon(col.key)}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedData.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="data-table__empty">
                {emptyMessage}
              </td>
            </tr>
          ) : (
            sortedData.map((row, idx) => (
              <tr 
                key={row.id || idx}
                className={`data-table__row ${onRowClick ? 'data-table__row--clickable' : ''}`}
                onClick={() => onRowClick?.(row)}
              >
                {columns.map((col) => (
                  <td 
                    key={col.key}
                    className="data-table__td"
                    style={{ textAlign: col.align || 'left' }}
                  >
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
