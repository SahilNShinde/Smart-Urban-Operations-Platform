# Mumbai Smart Urban Operations Platform

An AI platform for Mumbai city administration to monitor **traffic**, **monsoon flooding**, and **emergency hospital access** in real time.

---

## Key Features

- **Traffic Prediction**: Estimates travel times (in minutes) and congestion levels (Low, Medium, High).
- **Flood Monitoring**: Predicts waterlogging depth (cm) and alert levels at chronic flood hotspots (Hindmata, Milan Subway, Kurla).
- **Hospital Bed Telemetry**: Tracks live ICU and general bed availability across major trauma centers.
- **What-If Simulations**: Tests crisis scenarios (e.g., +50% heavier rainfall or major highway closures).
- **GIS Map Layers**: Provides GeoJSON spatial data for interactive map dashboards.

---

## AI Performance

Trained on real Mumbai traffic telemetry and historical monsoon weather records:
- **Traffic Model**: **~80% to 84% accuracy** (travel time estimates within 2–3 minutes).
- **Flood Model**: **~81% to 83% accuracy** (reliable waterlogging hazard detection).

---

## Quick Start

### 1. Install & Run
```bash
pip install -r requirements.txt
python main.py serve
```

### 2. Open API Docs
Visit: **[http://localhost:8000/docs](http://localhost:8000/docs)** to test live predictions directly in your browser.

---

## Testing & Docker (Optional)

```bash
# Run automated tests (17/17 passing)
python -m pytest

# Run with Docker
docker compose up --build
```
