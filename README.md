# Smart Urban Operations Platform

> **Status:** 🚧 **Active Development**

An intelligent decision-support dashboard for emergency dispatchers and city planners to monitor urban disruptions, dynamically reroute emergency vehicles, and test disaster scenarios.

---

## 🚀 Key Features

* **🗺️ Interactive City Map:** Multi-layer GIS showing roads, traffic conditions, flood-risk zones, and hospitals.
* **🚦 Live & Predicted Traffic:** Real-time speeds, congestion bottlenecks, and flow forecasting.
* **🌧️ Flood Risk & Weather:** Real-time rainfall telemetry and topography-based inundation predictions.
* **🏥 Hospital Status:** Real-time tracking of triage delays, operational capacity, and ICU/bed availability.
* **🚑 Smart Emergency Routing:** Dynamic pathfinding balancing travel time, flood safety, and hospital intake readiness.
* **🔮 What-If Simulator:** Run urban impact experiments across 3 initial scenarios:
  * **Rainfall Shift:** Increase/decrease rain levels to evaluate waterlogged roads.
  * **Road Closure:** Manually sever routes to observe secondary traffic choke points.
  * **Hospital Offline:** Mark a medical center as unavailable to re-route inbound emergency vehicles.
* **💬 AI Copilot:** Natural language assistant to query route safety, hospital availability, and scenario impacts.

---

## 🛠️ Tech Stack

* **Frontend:** React, TypeScript, Mapbox GL / Leaflet
* **Backend:** FastAPI (Python), NetworkX / OSRM (Dynamic Graph Routing)
* **AI & Data:** LLM Agent (LangChain/LlamaIndex), PostGIS, Redis

