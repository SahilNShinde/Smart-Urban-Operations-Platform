import React from 'react';
import styles from './ProgressBar.module.css';

interface ProgressBarProps {
  progress: number; // 0-100
  color?: string;
  height?: string;
}

export function ProgressBar({ progress, color = 'var(--accent-blue)', height = '4px' }: ProgressBarProps) {
  return (
    <div className={styles.container} style={{ height }}>
      <div 
        className={styles.bar} 
        style={{ width: `${progress}%`, backgroundColor: color }}
      ></div>
    </div>
  );
}
