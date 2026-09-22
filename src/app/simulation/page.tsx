import React from 'react';
import { Card } from '@/components/ui/Card';
import { Settings2 } from 'lucide-react';
import styles from '../page.module.css';

export default function SimulationPage() {
  return (
    <div className={styles.dashboard}>
      <Card title="Scenario Simulation" action={<Settings2 size={20} />}>
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <p>Disaster scenario modeling and outcome predictions will be displayed here.</p>
        </div>
      </Card>
    </div>
  );
}
