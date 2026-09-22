import React from 'react';
import { Card } from '@/components/ui/Card';
import { Settings2, Navigation, MessageSquare } from 'lucide-react';
import styles from './QuickActions.module.css';

export function QuickActions() {
  return (
    <Card title="Quick Actions">
      <div className={styles.grid}>
        <button className={styles.actionButton}>
          <Settings2 size={24} />
          <span>Run Simulation</span>
        </button>
        <button className={styles.actionButton}>
          <MessageSquare size={24} />
          <span>Find Nearest Hospital</span>
        </button>
        <button className={styles.actionButton}>
          <Navigation size={24} />
          <span>Plan Emergency Route</span>
        </button>
      </div>
    </Card>
  );
}
