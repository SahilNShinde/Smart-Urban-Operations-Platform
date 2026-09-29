'use client';

import React from 'react';
import { Search, Map as MapIcon } from 'lucide-react';
import styles from './MapSection.module.css';

export function MapSection() {
  return (
    <div className={styles.mapContainer}>
      <div className={styles.searchBar}>
        <Search size={18} className={styles.searchIcon} />
        <input 
          type="text" 
          placeholder="Search places, roads, hospitals..." 
          className={styles.searchInput} 
        />
      </div>

      <div className={styles.placeholderMap}>
        <div className={styles.mapGrid}>
          {/* Simulated map grid lines */}
        </div>
        <MapIcon size={64} className={styles.placeholderIcon} />
        <h3>Interactive City Map</h3>
        <p className={styles.mapSubtitle}>Bandra - Borivali Region</p>
      </div>

      {/* Legend Overlay */}
      <div className={styles.legend}>
        <h4 className={styles.legendTitle}>Traffic</h4>
        <div className={styles.legendItem}>
          <span className={styles.line} style={{ backgroundColor: '#22c55e' }}></span> Free Flow
        </div>
        <div className={styles.legendItem}>
          <span className={styles.line} style={{ backgroundColor: '#f59e0b' }}></span> Moderate
        </div>
        <div className={styles.legendItem}>
          <span className={styles.line} style={{ backgroundColor: '#f97316' }}></span> Heavy
        </div>
        <div className={styles.legendItem}>
          <span className={styles.line} style={{ backgroundColor: '#ef4444' }}></span> Severe
        </div>
        
        <h4 className={styles.legendTitle} style={{ marginTop: '12px' }}>Flood Risk Zone</h4>
        <div className={styles.legendItem}>
          <span className={styles.circle} style={{ backgroundColor: '#3b82f6' }}></span> Low
        </div>
        <div className={styles.legendItem}>
          <span className={styles.circle} style={{ backgroundColor: '#8b5cf6' }}></span> Medium
        </div>
        <div className={styles.legendItem}>
          <span className={styles.circle} style={{ backgroundColor: '#ec4899' }}></span> High
        </div>
      </div>
    </div>
  );
}
