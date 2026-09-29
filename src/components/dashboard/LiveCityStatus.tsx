'use client';

import React from 'react';
import { Card } from '@/components/ui/Card';
import { Car, CloudRain, Waves, PlusSquare } from 'lucide-react';
import { LineChart, Line, ResponsiveContainer, YAxis } from 'recharts';
import styles from './LiveCityStatus.module.css';

const trafficData = Array.from({ length: 10 }).map((_, i) => ({ value: 20 + Math.random() * 20 }));
const rainData = Array.from({ length: 10 }).map((_, i) => ({ value: 5 + Math.random() * 15 }));
const floodData = Array.from({ length: 10 }).map((_, i) => ({ value: 10 + Math.random() * 30 }));
const hospitalData = Array.from({ length: 10 }).map((_, i) => ({ value: 50 + Math.random() * 40 }));

export function LiveCityStatus() {
  return (
    <Card 
      title="Live City Status" 
      action={<span className={styles.liveIndicator}>● Live</span>}
    >
      <div className={styles.grid}>
        <div className={styles.statusItem}>
          <div className={styles.itemHeader}>
            <Car size={20} className={styles.iconGreen} />
            <div className={styles.itemInfo}>
              <h4>Traffic</h4>
              <p>Moderate</p>
              <small>Avg. speed 28 km/h</small>
            </div>
          </div>
          <div className={styles.sparkline}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trafficData}>
                <YAxis domain={['auto', 'auto']} hide />
                <Line type="monotone" dataKey="value" stroke="#f59e0b" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className={styles.statusItem}>
          <div className={styles.itemHeader}>
            <CloudRain size={20} className={styles.iconBlue} />
            <div className={styles.itemInfo}>
              <h4>Rainfall</h4>
              <p>12 mm/hr</p>
              <small>(Next 3 hrs: 20 mm/hr)</small>
            </div>
          </div>
          <div className={styles.sparkline}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={rainData}>
                <YAxis domain={['auto', 'auto']} hide />
                <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className={styles.statusItem}>
          <div className={styles.itemHeader}>
            <Waves size={20} className={styles.iconPurple} />
            <div className={styles.itemInfo}>
              <h4>Flood Risk</h4>
              <p>Low - Moderate</p>
              <small>(Higher near creek areas)</small>
            </div>
          </div>
          <div className={styles.sparkline}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={floodData}>
                <YAxis domain={['auto', 'auto']} hide />
                <Line type="monotone" dataKey="value" stroke="#8b5cf6" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className={styles.statusItem}>
          <div className={styles.itemHeader}>
            <PlusSquare size={20} className={styles.iconRed} />
            <div className={styles.itemInfo}>
              <h4>Hospitals</h4>
              <p>Normal</p>
              <small>(Avg. 68% capacity)</small>
            </div>
          </div>
          <div className={styles.sparkline}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={hospitalData}>
                <YAxis domain={['auto', 'auto']} hide />
                <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </Card>
  );
}
