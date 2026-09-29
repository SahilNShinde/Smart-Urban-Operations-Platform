'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Home, 
  Car, 
  CloudRain, 
  PlusSquare, 
  Navigation, 
  Settings2, 
  Bot 
} from 'lucide-react';
import styles from './Sidebar.module.css';

const menuItems = [
  { icon: Home, label: 'City Overview', href: '/' },
  { icon: Car, label: 'Traffic', href: '/traffic' },
  { icon: CloudRain, label: 'Flood & Weather', href: '/flood-weather' },
  { icon: PlusSquare, label: 'Hospitals', color: '#ef4444', href: '/hospitals' },
  { icon: Navigation, label: 'Emergency Routes', href: '/emergency-routes' },
  { icon: Settings2, label: 'Simulation', href: '/simulation' },
  { icon: Bot, label: 'AI Assistant', iconColor: '#3b82f6', href: '/ai-assistant' },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className={styles.sidebar}>
      <nav className={styles.nav}>
        <ul className={styles.menu}>
          {menuItems.map((item, index) => {
            const isActive = pathname === item.href;
            return (
              <li key={index} className={`${styles.menuItem} ${isActive ? styles.active : ''}`}>
                <Link href={item.href} className={styles.linkWrapper}>
                  <item.icon 
                    size={20} 
                    className={styles.icon} 
                    color={item.color || (isActive ? 'white' : 'var(--text-secondary)')}
                  />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className={styles.footer}>
        <p>Safer Cities.</p>
        <p>Smarter Decisions.</p>
        <p>A Better Tomorrow.</p>
      </div>
    </aside>
  );
}
