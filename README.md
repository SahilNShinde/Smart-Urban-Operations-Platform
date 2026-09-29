# Smart Urban Operations Platform

An intelligent decision-support dashboard for emergency dispatchers and city planners to monitor urban disruptions, dynamically reroute emergency vehicles, and test disaster scenarios.

This repository currently includes a modern, responsive Next.js dashboard for city management, monitoring traffic, flood risks, hospital capacities, and emergency route planning.

---

## Key Features

* **Interactive City Map:** Multi-layer GIS showing roads, traffic conditions, flood-risk zones, and hospitals.
* **Live & Predicted Traffic:** Real-time speeds, congestion bottlenecks, and flow forecasting.
* **Flood Risk & Weather:** Real-time rainfall telemetry and topography-based inundation predictions.
* **Hospital Status:** Real-time tracking of triage delays, operational capacity, and ICU/bed availability.
* **Smart Emergency Routing:** Dynamic pathfinding balancing travel time, flood safety, and hospital intake readiness.
* **What-If Simulator:** Run urban impact experiments across 3 initial scenarios:
  * **Rainfall Shift:** Increase/decrease rain levels to evaluate waterlogged roads.
  * **Road Closure:** Manually sever routes to observe secondary traffic choke points.
  * **Hospital Offline:** Mark a medical center as unavailable to re-route inbound emergency vehicles.
* **AI Copilot:** Natural language assistant to query route safety, hospital availability, and scenario impacts.

---

## Tech Stack

* **Frontend:** Next.js, React, TypeScript, CSS Modules
* **Backend:** FastAPI (Python), NetworkX / OSRM (Dynamic Graph Routing)
* **AI & Data:** LLM Agent (LangChain/LlamaIndex), PostGIS, Redis

> **Status:** Under Development

---

## Dashboard (Next.js)

### Prerequisites

- [Node.js](https://nodejs.org/en/) (Version 18+ recommended)
- `npm` (comes with Node.js)

### Getting Started

1. Clone the repository and open the project folder.

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000). The dashboard should load automatically.

### Project Structure

- `src/app/`: Contains the Next.js routes (`/traffic`, `/hospitals`, etc.) and the root layout.
- `src/components/dashboard/`: Contains the core dashboard widgets (MapSection, LiveCityStatus, BottomWidgets).
- `src/components/layout/`: Contains the Sidebar and Header components.
- `src/components/ui/`: Reusable UI elements (Cards, Badges, Progress Bars).
- `src/lib/mockData.ts`: The central data store. Replace exports here with `fetch` calls to your API.

### Map Configuration (Optional)

Currently, the map section uses a styled placeholder so the app builds without third-party accounts.

To integrate a real interactive map:

1. Obtain an API token from [Mapbox](https://www.mapbox.com/).
2. Re-install `react-map-gl` if it was removed (`npm install react-map-gl mapbox-gl`).
3. Add your token to a `.env.local` file at the root of the project:

   ```env
   NEXT_PUBLIC_MAPBOX_TOKEN=your_token_here
   ```

4. Update `src/components/dashboard/MapSection.tsx` to use the `react-map-gl` `Map` component.

---

## License

MIT License
