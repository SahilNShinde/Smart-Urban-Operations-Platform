# Smart Urban Operations Platform 🏙️🌧️🚦

An AI-powered urban operations platform designed to support smart city administration, disaster management, emergency healthcare routing, and real-time What-If scenario simulations for **Mumbai City**.

---

## 👥 Team Distribution (Member 1 Contribution)
- **Member 1 (Current)**: **Data Engineering + Machine Learning (25%)**
  - Data ingestion, cleaning, transformation, and feature extraction for real flood and traffic datasets.
  - PostgreSQL / PostGIS schema (`database/postgis_schema.sql`) & SQLite local database.
  - Traffic Speed & Congestion Prediction Models (`ml/models/traffic_model.py`).
  - Flood Inundation & Risk Assessment Models (`ml/models/flood_model.py`).
  - Comprehensive model evaluation suite (`reports/model_evaluation_report.md`).
  - FastAPI serving engine (`api/app.py`) with Swagger docs & What-If simulation support.
- **Member 2**: AI Agents + Decision Engine (LangGraph / Ollama)
- **Member 3**: Backend + Digital Twin + Simulation (FastAPI, Docker)
- **Member 4**: Frontend + GIS Dashboard (React, Mapbox / Leaflet)

---

## 📁 Real Datasets Used

The platform operates exclusively on real datasets located in `data/raw/`:

### 1. Flood Dataset (`data/raw/flood_dataset.csv`)
- **Size**: 3,120 records (daily meteorological observations from 2015 to 2024 across Mumbai weather stations: Bombay/Juhu, Bombay/Santacruz, Bombay/Colaba, T.B.I.A).
- **Features**: `date_of_record`, `month`, `season`, `station_name`, `avg_temp`, `min_temp`, `max_temp`, `wind_speed`, `air_pressure`, `elevation`, `latitude`, `longitude`, `rainfall`.
- **Extracted Features**: Rolling 3-day and 7-day rainfall accumulation, daily rainfall delta, barometric pressure drop, elevation vulnerability index, cyclical day-of-year and month encodings.
- **Target Variables**:
  - `inundation_depth_cm`: Predicted waterlogging depth (cm).
  - `flood_risk_score`: Continuous risk score ($0.0 - 1.0$).
  - `risk_category`: IMD alert classification (`SAFE`, `LOW`, `MODERATE`, `HIGH`, `CRITICAL`).

### 2. Traffic Dataset (`data/raw/all_features_traffic_dataset.csv`)
- **Size**: 61,368 records spanning 500 road segments with real timestamps.
- **Features Used (5 Core Features)**:
  1. `Timestamp / Hour` (`hour` / `Time_of_Day`, with cyclical `hour_sin`, `hour_cos`)
  2. `Day of Week` (`dow` / `Day_of_Week`, with cyclical `dow_sin`, `dow_cos`)
  3. `Traffic Volume` (`Traffic_Volume`)
  4. `Average Speed` (`Average_Speed` / `Traffic_Speed` in km/h)
  5. `Road Distance/Length` (`Road_Length` / `Road_Distance` in km)
- **Target Variables**:
  - `Travel_Time`: Predicted travel time in minutes (`predicted_travel_time_min`).
  - `Congestion_Level`: Traffic congestion classification (`Low`, `Medium`, `High`).

---

## 📊 Model Evaluation Summary

### 1. Flood Risk & Inundation Model (Trained on `flood_dataset.csv`)
- **Inundation Depth Regression**: $\text{MAE} = \mathbf{5.14 \text{ cm}}$, $\mathbf{R^2 = 0.8079}$
- **Flood Risk Score Regression**: $\text{MAE} = \mathbf{0.0782}$, $\mathbf{R^2 = 0.8311}$
- **Risk Category Classification**: Accuracy = $\mathbf{81.73\%}$ ($\text{Macro F1} = 0.8569$, $\text{Weighted F1} = 0.8167$)

### 2. Traffic Prediction Model (Trained on `all_features_traffic_dataset.csv`)
- **Travel Time Regression**: $\text{MAE} = \mathbf{2.39 \text{ min}}$, $\mathbf{R^2 = 0.8013}$
- **Congestion Level Classification**: Accuracy = $\mathbf{84.12\%}$ (Train: $\mathbf{86.36\%}$, $\text{F1} = 0.8418$)

---

## 🚀 Quickstart Guide

### 1. Run Data Cleaning, Feature Extraction & Training Pipeline
Executes the authoritative ETL on raw datasets, trains both ML models, and exports evaluation reports:
```bash
python main.py pipeline
```

### 2. Run Test Suite
Runs all 12 automated unit and integration tests:
```bash
python -m pytest -v tests/
```

### 3. Run Live Prediction Demo
```bash
python main.py demo
```

### 4. Start the FastAPI Prediction Server
```bash
python main.py serve --port 8000
```
Open your browser and navigate to:
- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔌 API Integration Contracts for Members 2, 3, and 4
Refer to [`docs/api_contracts.md`](docs/api_contracts.md) for full JSON payload schemas for:
- `GET /api/v1/traffic/current` — Current road network traffic status
- `POST /api/v1/traffic/predict` — Dynamic speed & congestion prediction
- `GET /api/v1/flood/current` — Current flood risk across monitored hotspots
- `POST /api/v1/flood/predict` — Inundation depth & risk score prediction
- `POST /api/v1/simulation/predict-impact` — What-If scenario simulations:
  - 🌧️ Increased/decreased rainfall
  - 🚧 Road closure
  - 🏥 Hospital unavailability
- `GET /api/v1/hospitals/status` — Hospital ICU & emergency bed availability
