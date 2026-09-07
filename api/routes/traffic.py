"""
Traffic routes for real dataset prediction.
Member 1: Data Engineering & Machine Learning
"""

from typing import List
from datetime import datetime
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends

from api.schemas import TrafficPredictionInput, TrafficPredictionOutput
from api.dependencies import get_traffic_model, get_db_manager, MumbaiTrafficModel, DatabaseManager

router = APIRouter(prefix="/api/v1/traffic", tags=["Traffic Intelligence"])


@router.get("/roads", summary="List Mumbai Roads")
def list_roads(db: DatabaseManager = Depends(get_db_manager)):
    return db.get_all_roads()


@router.post("/predict", response_model=TrafficPredictionOutput)
def predict_traffic(
    payload: TrafficPredictionInput,
    model: MumbaiTrafficModel = Depends(get_traffic_model),
    db: DatabaseManager = Depends(get_db_manager)
):
    roads = {r["segment_id"]: r for r in db.get_all_roads()}
    road_info = roads.get(payload.segment_id, {
        "name": "Arterial Road",
        "speed_limit_kmh": 60,
        "Number_of_Lanes": 4,
        "Road_Length": 5.0
    })

    speed = payload.Average_Speed if payload.Average_Speed is not None else (payload.Traffic_Speed or float(road_info.get("speed_limit_kmh", 50.0)))
    length = payload.Road_Length if payload.Road_Length is not None else (payload.Road_Distance or float(road_info.get("length_km", 5.0)))

    inp = {
        "hour": [payload.hour if payload.hour is not None else 10],
        "dow": [payload.dow if payload.dow is not None else 2],
        "Traffic_Volume": [payload.Traffic_Volume if payload.Traffic_Volume is not None else 2800],
        "Traffic_Speed": [speed],
        "Road_Length": [length]
    }
    pred_df = model.predict(pd.DataFrame(inp)).iloc[0]

    prob_keys = [c for c in pred_df.index if c.startswith("prob_")]
    conf_probs = {k.replace("prob_", "").upper(): float(pred_df[k]) for k in prob_keys}

    return TrafficPredictionOutput(
        segment_id=payload.segment_id or "ROAD_CUSTOM",
        road_name=road_info.get("name", "Mumbai Arterial"),
        predicted_travel_time_min=float(pred_df["predicted_travel_time_min"]),
        predicted_congestion_level=str(pred_df["predicted_congestion_level"]),
        confidence_probabilities=conf_probs,
        speed_limit_kmh=int(road_info.get("speed_limit_kmh", 60)),
        is_closed=False,
        predicted_average_speed_kmh=float(pred_df.get("predicted_average_speed_kmh", speed)),
        predicted_congestion_index=float(pred_df.get("predicted_congestion_index", 0.5))
    )


@router.get("/current", response_model=List[TrafficPredictionOutput])
def get_current_traffic(
    model: MumbaiTrafficModel = Depends(get_traffic_model),
    db: DatabaseManager = Depends(get_db_manager)
):
    roads = db.get_all_roads()
    results = []
    for r in roads:
        spd_lim = float(r.get("speed_limit_kmh", 50.0))
        inp = {
            "hour": [10],
            "dow": [1],
            "Traffic_Volume": [int(r.get("capacity_vph", 4000) * 0.70)],
            "Traffic_Speed": [spd_lim * 0.75],
            "Road_Length": [float(r.get("length_km", 5.0))]
        }
        pred_df = model.predict(pd.DataFrame(inp)).iloc[0]
        prob_keys = [c for c in pred_df.index if c.startswith("prob_")]
        conf_probs = {k.replace("prob_", "").upper(): float(pred_df[k]) for k in prob_keys}

        results.append(TrafficPredictionOutput(
            segment_id=r["segment_id"],
            road_name=r["name"],
            predicted_travel_time_min=float(pred_df["predicted_travel_time_min"]),
            predicted_congestion_level=str(pred_df["predicted_congestion_level"]),
            confidence_probabilities=conf_probs,
            speed_limit_kmh=int(r.get("speed_limit_kmh", 60)),
            is_closed=False,
            predicted_average_speed_kmh=float(pred_df.get("predicted_average_speed_kmh", spd_lim * 0.75)),
            predicted_congestion_index=float(pred_df.get("predicted_congestion_index", 0.5))
        ))
    return results
