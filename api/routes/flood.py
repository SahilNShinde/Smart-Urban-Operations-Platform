"""
Flood routes for real dataset prediction.
Member 1: Data Engineering & Machine Learning
"""

from typing import List
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends

from api.schemas import FloodPredictionInput, FloodPredictionOutput
from api.dependencies import get_flood_model, get_db_manager, MumbaiFloodModel, DatabaseManager

router = APIRouter(prefix="/api/v1/flood", tags=["Flood Intelligence"])


@router.get("/zones", summary="List Mumbai Flood Hotspots")
def list_flood_zones(db: DatabaseManager = Depends(get_db_manager)):
    return db.get_all_flood_zones()


@router.post("/predict", response_model=FloodPredictionOutput)
def predict_flood(
    payload: FloodPredictionInput,
    model: MumbaiFloodModel = Depends(get_flood_model),
    db: DatabaseManager = Depends(get_db_manager)
):
    zones = {z["zone_id"]: z for z in db.get_all_flood_zones()}
    zone_info = zones.get(payload.zone_id, {"name": "Monitored Flood Hotspot", "elevation_m": 4.0})

    inp = {
        "rainfall": [payload.rainfall],
        "rainfall_rolling_3d": [payload.rainfall_rolling_3d or payload.rainfall * 2.2],
        "rainfall_rolling_7d": [payload.rainfall_rolling_7d or payload.rainfall * 3.5],
        "air_pressure": [payload.air_pressure or 1004.0],
        "wind_speed": [payload.wind_speed or 20.0],
        "elevation": [payload.elevation or zone_info.get("elevation_m", 4.0)]
    }
    pred_df = model.predict(pd.DataFrame(inp)).iloc[0]

    prob_keys = [c for c in pred_df.index if c.startswith("prob_")]
    conf_probs = {k.replace("prob_", "").upper(): float(pred_df[k]) for k in prob_keys}

    strain = round(payload.rainfall / 50.0, 2)
    marine_locked = bool(payload.rainfall > 35.0 and (payload.air_pressure or 1004.0) < 1002.0)

    return FloodPredictionOutput(
        zone_id=payload.zone_id,
        zone_name=zone_info.get("name", "Mumbai Hotspot"),
        predicted_inundation_depth_cm=float(pred_df["predicted_inundation_depth_cm"]),
        predicted_flood_risk_score=float(pred_df["predicted_flood_risk_score"]),
        predicted_risk_category=str(pred_df["predicted_risk_category"]),
        confidence_probabilities=conf_probs,
        drainage_strain=strain,
        is_marine_locked=marine_locked
    )


@router.get("/current", response_model=List[FloodPredictionOutput])
def get_current_flood(
    rainfall: float = 30.0,
    model: MumbaiFloodModel = Depends(get_flood_model),
    db: DatabaseManager = Depends(get_db_manager)
):
    zones = db.get_all_flood_zones()
    results = []
    for z in zones:
        inp = {
            "rainfall": [rainfall],
            "rainfall_rolling_3d": [rainfall * 2.2],
            "rainfall_rolling_7d": [rainfall * 3.5],
            "air_pressure": [1005.0],
            "wind_speed": [18.0],
            "elevation": [z.get("elevation_m", 4.0)]
        }
        pred_df = model.predict(pd.DataFrame(inp)).iloc[0]
        prob_keys = [c for c in pred_df.index if c.startswith("prob_")]
        conf_probs = {k.replace("prob_", "").upper(): float(pred_df[k]) for k in prob_keys}

        results.append(FloodPredictionOutput(
            zone_id=z["zone_id"],
            zone_name=z["name"],
            predicted_inundation_depth_cm=float(pred_df["predicted_inundation_depth_cm"]),
            predicted_flood_risk_score=float(pred_df["predicted_flood_risk_score"]),
            predicted_risk_category=str(pred_df["predicted_risk_category"]),
            confidence_probabilities=conf_probs,
            drainage_strain=round(rainfall / 50.0, 2),
            is_marine_locked=False
        ))
    return results
