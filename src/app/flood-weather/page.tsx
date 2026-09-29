import React from 'react';
import { Card } from '@/components/ui/Card';
import { CloudRain } from 'lucide-react';
import styles from '../page.module.css';

export default function FloodWeatherPage() {
  return (
    <div className={styles.dashboard}>
      <Card title="Flood & Weather Analytics" action={<CloudRain size={20} />}>
        <div style={{ padding: '24px', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <p>Detailed weather forecasts and flood risk models will be displayed here.</p>
        </div>
      </Card>
    </div>
  );
}
