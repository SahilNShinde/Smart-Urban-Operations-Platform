import React from 'react';
import { Card } from '@/components/ui/Card';
import { alerts } from '@/lib/mockData';
import { TriangleAlert, CloudRain, PlusSquare, AlertCircle } from 'lucide-react';
import styles from './RecentAlerts.module.css';

const iconMap: Record<string, React.ReactNode> = {
  traffic: <TriangleAlert size={16} color="var(--status-red)" />,
  weather: <CloudRain size={16} color="var(--accent-blue)" />,
  hospital: <PlusSquare size={16} color="var(--status-red)" />,
  incident: <AlertCircle size={16} color="var(--status-yellow)" />
};

export function RecentAlerts() {
  return (
    <Card 
      title="Recent Alerts" 
      action={<a href="#" className={styles.viewAll}>View All →</a>}
    >
      <div className={styles.alertList}>
        {alerts.map(alert => (
          <div key={alert.id} className={styles.alertItem}>
            <div className={styles.iconWrapper}>
              {iconMap[alert.type]}
            </div>
            <span className={styles.time}>{alert.time}</span>
            <span className={styles.message}>{alert.message}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
