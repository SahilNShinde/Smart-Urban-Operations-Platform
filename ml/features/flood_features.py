"""
Feature definitions and transformer for Real Mumbai Flood Dataset.
Member 1: Data Engineering & Machine Learning
"""

from typing import List
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

NUMERICAL_FEATURES: List[str] = [
    "rainfall",
    "rainfall_rolling_3d",
    "rainfall_rolling_7d",
    "rainfall_delta_1d",
    "air_pressure",
    "wind_speed",
    "temp_range",
    "barometric_depression",
    "elevation",
    "elevation_vulnerability",
    "latitude",
    "longitude",
    "doy_sin",
    "doy_cos",
    "month_sin",
    "month_cos"
]

TARGET_DEPTH: str = "inundation_depth_cm"
TARGET_SCORE: str = "flood_risk_score"
TARGET_CATEGORY: str = "risk_category"


def get_flood_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES)
        ],
        remainder="drop"
    )


def prepare_flood_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "rainfall" not in df.columns:
        df["rainfall"] = 0.0
    if "rainfall_rolling_3d" not in df.columns:
        df["rainfall_rolling_3d"] = df["rainfall"] * 2.2
    if "rainfall_rolling_7d" not in df.columns:
        df["rainfall_rolling_7d"] = df["rainfall"] * 3.5
    if "rainfall_delta_1d" not in df.columns:
        df["rainfall_delta_1d"] = 0.0
    if "temp_range" not in df.columns:
        if "max_temp" in df.columns and "min_temp" in df.columns:
            df["temp_range"] = (df["max_temp"] - df["min_temp"]).clip(lower=0.0)
        else:
            df["temp_range"] = 4.5
    if "barometric_depression" not in df.columns:
        if "air_pressure" in df.columns:
            df["barometric_depression"] = (1013.25 - df["air_pressure"]).clip(lower=0.0)
        else:
            df["air_pressure"] = 1008.0
            df["barometric_depression"] = 5.25
    if "elevation_vulnerability" not in df.columns:
        elev = df["elevation"] if "elevation" in df.columns else 6.0
        df["elevation_vulnerability"] = (15.0 - elev).clip(lower=1.0)
    if "doy_sin" not in df.columns:
        df["doy_sin"] = 0.0
        df["doy_cos"] = 1.0
    if "month_sin" not in df.columns:
        df["month_sin"] = 0.0
        df["month_cos"] = 1.0
    if "wind_speed" not in df.columns:
        df["wind_speed"] = 15.0
    if "latitude" not in df.columns:
        df["latitude"] = 19.0760
    if "longitude" not in df.columns:
        df["longitude"] = 72.8777
    if "elevation" not in df.columns:
        df["elevation"] = 6.0
    return df
