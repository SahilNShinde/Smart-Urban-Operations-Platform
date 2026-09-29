import React from 'react';
import { Card } from '@/components/ui/Card';
import { Car } from 'lucide-react';
import styles from '../page.module.css';

export default function TrafficPage() {
  return (
    <div className={styles.dashboard}>
      <Card title="Traffic Analytics" action={<Car size={20} />}>
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <p>Traffic details and congestion models will be displayed here.</p>
        </div>
      </Card>
    </div>
  );
}
