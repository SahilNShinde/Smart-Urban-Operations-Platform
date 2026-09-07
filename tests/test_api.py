import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_health_check():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["city"] == "Mumbai"


def test_metadata():
    res = client.get("/api/v1/metadata")
    assert res.status_code == 200
    data = res.json()
    assert data["city"] == "Mumbai"
    assert "supported_scenarios" in data


def test_traffic_current():
    res = client.get("/api/v1/traffic/current")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "predicted_travel_time_min" in data[0]
    assert "predicted_congestion_level" in data[0]


def test_traffic_predict():
    payload = {
        "hour": 8,
        "dow": 1,
        "Traffic_Volume": 3100,
        "Average_Speed": 42.5,
        "Road_Length": 7.0,
        "segment_id": "ROAD_WEH_01"
    }
    res = client.post("/api/v1/traffic/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "predicted_travel_time_min" in data
    assert "predicted_congestion_level" in data
    assert data["predicted_travel_time_min"] > 0
    assert data["predicted_congestion_level"] in ["Low", "Medium", "High"]


def test_flood_current():
    res = client.get("/api/v1/flood/current")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "predicted_inundation_depth_cm" in data[0]


def test_hospitals_status():
    res = client.get("/api/v1/hospitals/status")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0
    kem = [h for h in data if h["hospital_id"] == "HOSP_KEM"][0]
    assert kem["total_beds"] > 0


def test_simulation_increased_rainfall():
    payload = {
        "scenario_type": "increased_rainfall",
        "rainfall_delta_pct": 50.0,
        "tide_height_m": 4.4
    }
    res = client.post("/api/v1/simulation/predict-impact", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["scenario_type"] == "increased_rainfall"
    assert len(data["affected_flood_zones"]) > 0
