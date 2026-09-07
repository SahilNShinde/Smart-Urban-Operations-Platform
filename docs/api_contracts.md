# Smart Urban Operations Platform (Mumbai City)
## API Contract & Team Integration Handbook
**Author**: Member 1 (Data Engineering & Machine Learning — 25%)  
**Stakeholders**:
- **Member 2**: AI Agents & Decision Engine (LangGraph / Ollama)
- **Member 3**: Backend, Digital Twin & Simulation
- **Member 4**: Frontend Dashboard & GIS Map (React + Mapbox/Leaflet)

---

## 1. Overview & Service Base URL
- **Local Dev Server**: `http://localhost:8000`
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`
- **CORS**: Enabled for all origins (`*`), supporting React on port 3000, 5173, etc.
- **Dataset Grounding**: Models are trained exclusively on real telemetry (`flood_dataset.csv` and `all_features_traffic_dataset.csv`).

---

## 2. Endpoints Specification

### A. Traffic Prediction (`/api/v1/traffic`)

#### `GET /api/v1/traffic/current`
Returns real-time predicted traffic status across road segments.
- **Response Sample**:
```json
[
  {
    "segment_id": "ROAD_WEH_01",
    "road_name": "Western Express Highway (Bandra to Santacruz)",
    "predicted_travel_time_min": 10.29,
    "predicted_congestion_level": "Medium",
    "confidence_probabilities": {
      "HIGH": 0.20,
      "LOW": 0.40,
      "MEDIUM": 0.40
    },
    "speed_limit_kmh": 70,
    "is_closed": false
  }
]
```

#### `POST /api/v1/traffic/predict`
Predicts travel time and congestion level using the 5 core features:
- **Request Body**:
```json
{
  "segment_id": "ROAD_WEH_01",
  "hour": 9,
  "dow": 1,
  "Traffic_Volume": 3200,
  "Average_Speed": 45.0,
  "Road_Length": 5.4
}
```

---

### B. Flood Risk & Inundation (`/api/v1/flood`)

#### `GET /api/v1/flood/current`
Returns predicted inundation depth and risk levels across monitored flood zones.
- **Query Params**: `rainfall` (float, mm)
- **Response Sample**:
```json
[
  {
    "zone_id": "FLOOD_HINDMATA",
    "zone_name": "Hindmata Junction & Dadar TT",
    "predicted_inundation_depth_cm": 35.8,
    "predicted_flood_risk_score": 0.475,
    "predicted_risk_category": "LOW",
    "confidence_probabilities": {
      "SAFE": 0.05,
      "LOW": 0.85,
      "MODERATE": 0.08,
      "HIGH": 0.02,
      "CRITICAL": 0.00
    },
    "drainage_strain": 0.60,
    "is_marine_locked": false
  }
]
```

#### `POST /api/v1/flood/predict`
- **Request Body**:
```json
{
  "zone_id": "FLOOD_HINDMATA",
  "rainfall": 82.5,
  "rainfall_rolling_3d": 145.0,
  "rainfall_rolling_7d": 210.0,
  "air_pressure": 1001.0,
  "wind_speed": 24.0,
  "elevation": 2.8
}
```

---

### C. What-If Simulation Engine (`/api/v1/simulation`)

#### Scenario 1: Rainfall Surge (`"scenario_type": "increased_rainfall"`)
```json
POST /api/v1/simulation/predict-impact
{
  "scenario_type": "increased_rainfall",
  "rainfall_delta_pct": 50.0,
  "absolute_rainfall_mm": 90.0
}
```

#### Scenario 2: Road Closure (`"scenario_type": "road_closure"`)
```json
POST /api/v1/simulation/predict-impact
{
  "scenario_type": "road_closure",
  "closed_segment_ids": ["ROAD_WEH_01"]
}
```

#### Scenario 3: Hospital Unavailability (`"scenario_type": "hospital_unavailable"`)
```json
POST /api/v1/simulation/predict-impact
{
  "scenario_type": "hospital_unavailable",
  "unavailable_hospital_ids": ["HOSP_SION"]
}
```

---

### D. Emergency Hospitals (`/api/v1/hospitals`)

#### `GET /api/v1/hospitals/status`
Returns real-time capacity and flood isolation risk for all Mumbai hospitals.

---

### E. GIS & Spatial Infrastructure (`/api/v1/gis`)

Designed specifically for **Member 4 (Frontend / GIS Map)**:

#### `GET /api/v1/gis/layers`
Returns the metadata catalog of available GeoJSON layers.

#### `GET /api/v1/gis/roads`
Returns GeoJSON `FeatureCollection` of 15 major Mumbai highway and arterial road corridors with coordinates and attributes.

#### `GET /api/v1/gis/flood-zones`
Returns GeoJSON `FeatureCollection` of 8 chronic flood vulnerability hotspot polygons (Hindmata, Milan Subway, Kurla, Dharavi, etc.).

#### `GET /api/v1/gis/hospitals`
Returns GeoJSON `FeatureCollection` of 8 designated trauma & municipal emergency hospital points with coordinates and capacity.

#### `GET /api/v1/gis/unified-view`
Returns a unified JSON bundle containing all three spatial layers in a single request for fast map rendering.

---

## 3. How to Run Locally

```bash
# 1. Run Data Pipeline & Training on User Datasets
python main.py pipeline

# 2. Run Test Suite
python -m pytest -v tests/

# 3. Launch FastAPI Server
python main.py serve --port 8000
```
