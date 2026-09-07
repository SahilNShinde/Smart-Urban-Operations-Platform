"""
Unit tests for Real Mumbai Traffic and Flood models.
Member 1: Data Engineering & Machine Learning
"""

import os
import pandas as pd
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from ml.models.traffic_model import MumbaiTrafficModel
from ml.models.flood_model import MumbaiFloodModel

SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")


def test_real_traffic_model_inference():
    model = MumbaiTrafficModel.load(SAVED_MODELS_DIR)
    assert model.is_fitted

    sample = pd.DataFrame([{
        "hour": 9,
        "dow": 1,
        "Traffic_Volume": 3200,
        "Average_Speed": 48.0,
        "Road_Length": 6.5
    }])

    res = model.predict(sample)
    assert "predicted_travel_time_min" in res.columns
    assert "predicted_congestion_level" in res.columns

    tt = res["predicted_travel_time_min"].iloc[0]
    lvl = res["predicted_congestion_level"].iloc[0]

    assert 0.5 <= tt <= 300.0
    assert lvl in ["Low", "Medium", "High"]


def test_real_flood_model_inference():
    model = MumbaiFloodModel.load(SAVED_MODELS_DIR)
    assert model.is_fitted

    sample = pd.DataFrame([{
        "rainfall": 65.0,
        "rainfall_rolling_3d": 110.0,
        "rainfall_rolling_7d": 180.0,
        "rainfall_delta_1d": 25.0,
        "air_pressure": 1002.5,
        "wind_speed": 22.0,
        "temp_range": 3.2,
        "barometric_depression": 10.75,
        "elevation": 4.0,
        "elevation_vulnerability": 11.0,
        "latitude": 19.1167,
        "longitude": 72.8333,
        "doy_sin": 0.25,
        "doy_cos": -0.96,
        "month_sin": -0.5,
        "month_cos": -0.86
    }])

    res = model.predict(sample)
    assert "predicted_inundation_depth_cm" in res.columns
    assert "predicted_flood_risk_score" in res.columns
    assert "predicted_risk_category" in res.columns

    depth = res["predicted_inundation_depth_cm"].iloc[0]
    score = res["predicted_flood_risk_score"].iloc[0]
    cat = res["predicted_risk_category"].iloc[0]

    assert depth >= 0.0
    assert 0.0 <= score <= 1.0
    assert cat in ["SAFE", "LOW", "MODERATE", "HIGH", "CRITICAL"]
