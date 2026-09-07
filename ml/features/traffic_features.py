"""
Feature definitions and transformer for Traffic Dataset.
Features used (5 total):
1. Timestamp / Hour
2. Day of Week
3. Traffic Volume
4. Average Speed
5. Road Distance/Length

Targets:
1. Predicted Travel Time (Travel_Time, minutes)
2. Congestion Level (Congestion_Level: Low, Medium, High)
"""

from typing import List
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler

NUMERICAL_FEATURES: List[str] = [
    "hour",
    "dow",
    "Traffic_Volume",
    "Traffic_Speed",
    "Road_Length",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "speed_feature"
]

TARGET_TRAVEL_TIME: str = "Travel_Time"
TARGET_CONGESTION_LEVEL: str = "Congestion_Level"
# Backward-compatibility aliases
TARGET_SPEED: str = "Traffic_Speed"
TARGET_CONGESTION_INDEX: str = "Congestion_Index"
TARGET_CLASSIFICATION: str = "Congestion_Level"


def get_traffic_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), NUMERICAL_FEATURES)
        ],
        remainder="drop"
    )


def prepare_traffic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes and computes the 5 features:
    1. Timestamp / Hour (hour, hour_sin, hour_cos)
    2. Day of Week (dow, dow_sin, dow_cos)
    3. Traffic Volume (Traffic_Volume)
    4. Average Speed (Traffic_Speed)
    5. Road Distance/Length (Road_Length)
    Plus derived physical travel time estimate: speed_feature (Road_Length / Traffic_Speed * 60).
    """
    df = df.copy()

    # 1. Map Average Speed
    if "Average_Speed" in df.columns and "Traffic_Speed" not in df.columns:
        df["Traffic_Speed"] = df["Average_Speed"]
    elif "average_speed" in df.columns and "Traffic_Speed" not in df.columns:
        df["Traffic_Speed"] = df["average_speed"]
    elif "Traffic_Speed" not in df.columns:
        df["Traffic_Speed"] = 50.0

    # 2. Map Road Distance / Length
    if "Road_Distance" in df.columns and "Road_Length" not in df.columns:
        df["Road_Length"] = df["Road_Distance"]
    elif "road_distance" in df.columns and "Road_Length" not in df.columns:
        df["Road_Length"] = df["road_distance"]
    elif "length_km" in df.columns and "Road_Length" not in df.columns:
        df["Road_Length"] = df["length_km"]
    elif "Road_Length" not in df.columns:
        df["Road_Length"] = 5.0

    # 3. Map Traffic Volume
    if "traffic_volume" in df.columns and "Traffic_Volume" not in df.columns:
        df["Traffic_Volume"] = df["traffic_volume"]
    elif "Volume" in df.columns and "Traffic_Volume" not in df.columns:
        df["Traffic_Volume"] = df["Volume"]
    elif "Traffic_Volume" not in df.columns:
        df["Traffic_Volume"] = 2500

    # 4. Map Timestamp / Hour
    if "hour" in df.columns:
        df["hour"] = pd.to_numeric(df["hour"], errors="coerce").fillna(10).astype(int)
    elif "Time_of_Day" in df.columns:
        df["hour"] = pd.to_numeric(df["Time_of_Day"], errors="coerce").fillna(10).astype(int)
    elif "Timestamp" in df.columns:
        ts = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["hour"] = ts.dt.hour.fillna(10).astype(int)
    else:
        df["hour"] = 10

    # 5. Map Day of Week
    if "dow" in df.columns:
        df["dow"] = pd.to_numeric(df["dow"], errors="coerce").fillna(2).astype(int)
    elif "Day_of_Week" in df.columns:
        df["dow"] = pd.to_numeric(df["Day_of_Week"], errors="coerce").fillna(2).astype(int)
    elif "Timestamp" in df.columns:
        ts = pd.to_datetime(df["Timestamp"], errors="coerce")
        df["dow"] = ts.dt.dayofweek.fillna(2).astype(int)
    else:
        df["dow"] = 2

    # Derived cyclical encodings
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0).round(4)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0).round(4)
    df["dow_sin"] = np.sin(2 * np.pi * df["dow"] / 7.0).round(4)
    df["dow_cos"] = np.cos(2 * np.pi * df["dow"] / 7.0).round(4)

    # Derived kinematic feature: distance / speed in minutes
    df["speed_feature"] = (df["Road_Length"] / df["Traffic_Speed"].clip(lower=1.0)) * 60.0

    return df
