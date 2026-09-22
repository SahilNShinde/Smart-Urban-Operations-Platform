import React from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { trafficRoutes, floodRisk, hospitals } from '@/lib/mockData';
import { Droplet, Thermometer, CloudRain, ShieldAlert, Send } from 'lucide-react';
import styles from './BottomWidgets.module.css';

function getTrafficBadgeColor(status: string) {
  if (status === 'Low') return 'green';
  if (status === 'Moderate') return 'yellow';
  if (status === 'Heavy') return 'orange';
  return 'red';
}

function getHospitalBadgeColor(status: string) {
  if (status === 'Available') return 'green';
  if (status === 'Limited') return 'yellow';
  return 'red';
}

export function BottomWidgets() {
  return (
    <div className={styles.widgetsGrid}>
      {/* Traffic Overview */}
      <Card title="Traffic Overview" action={<a href="#" className={styles.link}>View Details →</a>}>
        <div className={styles.list}>
          {trafficRoutes.slice(0, 5).map(route => (
            <div key={route.id} className={styles.listItem}>
              <div className={styles.routeItem}>
                <span className={styles.dot} style={{ backgroundColor: `var(--status-${getTrafficBadgeColor(route.status)})` }}></span>
                <span className={styles.routeName}>{route.route}</span>
              </div>
              <Badge variant={getTrafficBadgeColor(route.status)}>{route.status}</Badge>
            </div>
          ))}
        </div>
        <div className={styles.summaryBox}>
          <div>
            <div className={styles.summaryLabel}>Avg. Speed (City)</div>
            <div className={styles.summaryValue}>28 km/h</div>
            <div className={styles.trendDown}>↓ 12%</div>
          </div>
          {/* Mock speed chart line */}
          <div className={styles.mockChartLine}>
            <svg viewBox="0 0 100 30" className={styles.svgLine}>
              <path d="M0,25 Q10,20 20,25 T40,15 T60,20 T80,10 T100,5" fill="none" stroke="var(--accent-blue)" strokeWidth="2" />
            </svg>
          </div>
        </div>
      </Card>

      {/* Flood & Weather */}
      <Card title="Flood & Weather" action={<a href="#" className={styles.link}>View Details →</a>}>
        <div className={styles.weatherTop}>
          <div className={styles.weatherIconBox}>
             <CloudRain size={32} className={styles.iconBlue} />
          </div>
          <div>
            <div className={styles.weatherLabel}>Current Rainfall</div>
            <div className={styles.weatherValue}>12 mm/hr</div>
            <div className={styles.weatherSub}>(Next 3 hrs: 20 mm/hr)</div>
          </div>
        </div>
        
        <div className={styles.floodZones}>
          <div className={styles.zoneTitle}>Flood Risk Zone <br/><span className={styles.sub}>(Bandra - Borivali)</span></div>
          <div className={styles.zoneList}>
            <div className={styles.zoneItem}>
              <span><span className={styles.dot} style={{ backgroundColor: 'var(--status-red)' }}></span> High</span>
              <span>{floodRisk.high}</span>
            </div>
            <div className={styles.zoneItem}>
              <span><span className={styles.dot} style={{ backgroundColor: 'var(--status-yellow)' }}></span> Medium</span>
              <span>{floodRisk.medium}</span>
            </div>
            <div className={styles.zoneItem}>
              <span><span className={styles.dot} style={{ backgroundColor: 'var(--status-green)' }}></span> Low</span>
              <span>{floodRisk.low}</span>
            </div>
          </div>
        </div>

        <div className={styles.weatherBottom}>
          <div className={styles.weatherStat}>
            <Thermometer size={16} />
            <div>
              <div className={styles.statLabel}>Temperature</div>
              <div className={styles.statValue}>28°C</div>
            </div>
          </div>
          <div className={styles.weatherStat}>
            <Droplet size={16} className={styles.iconBlue} />
            <div>
              <div className={styles.statLabel}>Humidity</div>
              <div className={styles.statValue}>86%</div>
            </div>
          </div>
        </div>
      </Card>

      {/* Hospital Status */}
      <Card title="Hospital Status" action={<a href="#" className={styles.link}>View Details →</a>}>
        <div className={styles.list}>
          {hospitals.map(hospital => (
            <div key={hospital.id} className={styles.hospitalItem}>
              <div className={styles.hospitalIcon}>+</div>
              <div className={styles.hospitalInfo}>
                <div className={styles.hospitalName} title={hospital.name}>{hospital.name}</div>
                <div className={styles.hospitalCap}>{hospital.capacity}% capacity</div>
              </div>
              <Badge variant={getHospitalBadgeColor(hospital.status)}>{hospital.status}</Badge>
            </div>
          ))}
        </div>
      </Card>

      {/* Emergency Route */}
      <Card title="Emergency Route" action={<a href="#" className={styles.link}>Run Scenario →</a>}>
        <div className={styles.routeHeader}>
          <div className={styles.routeCol}>
            <small>From</small>
            <div>Bandra</div>
            <small>To</small>
            <div>Lilavati Hospital</div>
          </div>
          <div className={styles.routeCol}>
            <small>Rainfall Increase</small>
            <div>+50% (to 18 mm/hr)</div>
          </div>
        </div>
        
        <div className={styles.routeMetrics}>
          <div className={styles.routeCol}>
            <small>Distance</small>
            <div>3.2 km</div>
          </div>
          <div className={styles.routeCol}>
            <small>Est. Time</small>
            <div>10 min</div>
          </div>
          <button className={styles.runSimBtn}>Run Simulation</button>
        </div>

        <button className={styles.viewRouteBtn}>View Best Route →</button>

        <div className={styles.altRoutes}>
          <div className={styles.altTitle}>Alternative Routes <button className={styles.viewAltBtn}>View</button></div>
          <ul className={styles.altList}>
            <li>Flood risk increases in 3 zones</li>
            <li>Traffic may slow down by 15-25%</li>
            <li>1 hospital may face high load</li>
          </ul>
        </div>
      </Card>


    </div>
  );
}
