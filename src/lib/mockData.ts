export const hospitals = [
  { id: '1', name: 'Lilavati Hospital (Bandra)', capacity: 68, status: 'Available' },
  { id: '2', name: 'KEM Hospital (Parel)', capacity: 82, status: 'Limited' },
  { id: '3', name: 'Cooper Hospital (Juhu)', capacity: 74, status: 'Available' },
  { id: '4', name: 'Sion Hospital (Sion)', capacity: 56, status: 'Available' },
  { id: '5', name: 'ESIC Hospital (Andheri)', capacity: 76, status: 'Available' },
];

export const alerts = [
  { id: '1', time: '17:12', message: 'Heavy traffic on SV Road (Bandra)', type: 'traffic', severity: 'high' },
  { id: '2', time: '16:45', message: 'High flood risk near Oshiwara (low lying area)', type: 'weather', severity: 'high' },
  { id: '3', time: '16:20', message: 'Khar Hospital - 3 beds available (ICU)', type: 'hospital', severity: 'medium' },
  { id: '4', time: '15:50', message: 'Road work on Link Road (Andheri)', type: 'incident', severity: 'low' },
];

export const trafficRoutes = [
  { id: '1', route: 'Bandra - Khar Road', status: 'Moderate', speed: [30, 28, 25, 27, 26, 32, 28] },
  { id: '2', route: 'Khar - Santacruz', status: 'Heavy', speed: [20, 18, 15, 12, 10, 14, 18] },
  { id: '3', route: 'Santacruz - Andheri', status: 'Moderate', speed: [35, 32, 30, 31, 28, 25, 30] },
  { id: '4', route: 'Andheri - Goregaon', status: 'Low', speed: [45, 48, 42, 50, 46, 44, 45] },
  { id: '5', route: 'Goregaon - Kandivali', status: 'Moderate', speed: [35, 34, 30, 32, 31, 29, 30] },
  { id: '6', route: 'Kandivali - Borivali', status: 'Low', speed: [50, 52, 48, 55, 51, 49, 50] },
];

export const floodRisk = {
  high: 2,
  medium: 5,
  low: 11,
};
