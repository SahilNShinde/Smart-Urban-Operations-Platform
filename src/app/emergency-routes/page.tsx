import React from 'react';
import { Card } from '@/components/ui/Card';
import { Navigation } from 'lucide-react';
import styles from '../page.module.css';

export default function EmergencyRoutesPage() {
  return (
    <div className={styles.dashboard}>
      <Card title="Emergency Route Planning" action={<Navigation size={20} />}>
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <p>Real-time ambulance dispatching and route optimizations will be displayed here.</p>
        </div>
      </Card>
    </div>
  );
}
