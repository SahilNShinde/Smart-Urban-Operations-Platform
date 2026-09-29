import { MapSection } from '@/components/dashboard/MapSection';
import { LiveCityStatus } from '@/components/dashboard/LiveCityStatus';
import { RecentAlerts } from '@/components/dashboard/RecentAlerts';
import { QuickActions } from '@/components/dashboard/QuickActions';
import { BottomWidgets } from '@/components/dashboard/BottomWidgets';
import styles from './page.module.css';

export default function Home() {
  return (
    <div className={styles.dashboard}>
      <div className={styles.topSection}>
        <div className={styles.mainCol}>
          <MapSection />
        </div>
        <div className={styles.sideCol}>
          <LiveCityStatus />
          <RecentAlerts />
          <QuickActions />
        </div>
      </div>
      <BottomWidgets />
    </div>
  );
}
