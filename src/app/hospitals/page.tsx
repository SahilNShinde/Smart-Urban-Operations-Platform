import React from 'react';
import { Card } from '@/components/ui/Card';
import { PlusSquare } from 'lucide-react';
import styles from '../page.module.css';

export default function HospitalsPage() {
  return (
    <div className={styles.dashboard}>
      <Card title="Hospital Status & Capacity" action={<PlusSquare size={20} color="#ef4444" />}>
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <p>Real-time hospital bed availability and resource tracking will be displayed here.</p>
        </div>
      </Card>
    </div>
  );
}
