import React from 'react';
import { Calendar, CloudRain, MapPin, User, ChevronDown } from 'lucide-react';
import styles from './Header.module.css';

export function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <div className={styles.logoIcon}>
          {/* Using a simple placeholder for the city skyline icon */}
          <div className={styles.buildings}>
            <div className={styles.building} style={{ height: '24px' }}></div>
            <div className={styles.building} style={{ height: '32px' }}></div>
            <div className={styles.building} style={{ height: '28px' }}></div>
          </div>
        </div>
        <div className={styles.titleContainer}>
          <h1 className={styles.title}>Smart Urban Operations Platform</h1>
          <p className={styles.subtitle}>Bandra - Borivali | Mumbai</p>
        </div>
      </div>

      <div className={styles.right}>
        <div className={styles.infoItem}>
          <Calendar size={18} className={styles.icon} />
          <div className={styles.infoText}>
            <span>Sep 21, 2025</span>
            <span className={styles.time}>17:24</span>
          </div>
        </div>

        <div className={styles.divider}></div>

        <div className={styles.infoItem}>
          <CloudRain size={24} className={styles.iconBlue} />
          <div className={styles.infoText}>
            <span className={styles.temp}>28°C</span>
            <span>Light Rain</span>
          </div>
        </div>

        <div className={styles.divider}></div>

        <div className={styles.infoItem}>
          <MapPin size={18} className={styles.iconBlue} />
          <span>Mumbai</span>
        </div>

        <div className={styles.divider}></div>

        <div className={styles.profile}>
          <div className={styles.avatar}>
            <User size={16} />
          </div>
          <span>Sahil Shinde</span>
          <ChevronDown size={14} className={styles.chevron} />
        </div>
      </div>
    </header>
  );
}
