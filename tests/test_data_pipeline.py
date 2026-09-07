"""
Unit tests for data pipeline and processed user datasets.
Member 1: Data Engineering & Machine Learning
"""

import os
import json
import pandas as pd
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
GEOJSON_DIR = os.path.join(BASE_DIR, "data", "geojson")


def test_geojson_layers():
    for name in ["mumbai_roads.geojson", "mumbai_flood_zones.geojson", "mumbai_hospitals.geojson"]:
        p = os.path.join(GEOJSON_DIR, name)
        assert os.path.exists(p), f"Missing GeoJSON layer {name}"
        with open(p, "r") as f:
            data = json.load(f)
            assert data["type"] == "FeatureCollection"
            assert len(data["features"]) > 0


def test_user_flood_processed_data():
    p = os.path.join(PROCESSED_DIR, "flood_processed.csv")
    assert os.path.exists(p), f"Missing {p}"
    df = pd.read_csv(p)
    assert len(df) == 3120
    assert "rainfall" in df.columns
    assert "rainfall_rolling_3d" in df.columns
    assert "flood_risk_score" in df.columns
    assert "risk_category" in df.columns
    assert df["rainfall"].isnull().sum() == 0
    assert (df["flood_risk_score"] >= 0.0).all() and (df["flood_risk_score"] <= 1.0).all()


def test_user_traffic_processed_data():
    p = os.path.join(PROCESSED_DIR, "traffic_processed.csv")
    assert os.path.exists(p), f"Missing {p}"
    df = pd.read_csv(p)
    assert len(df) == 61368
    assert "Traffic_Volume" in df.columns
    assert "Traffic_Speed" in df.columns
    assert "Congestion_Level" in df.columns
    assert "Volume_per_Lane" in df.columns
    assert df["Incidents_or_Events"].isnull().sum() == 0
