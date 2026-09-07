"""
Simulation routes for What-If scenarios.
Member 1: Data Engineering & Machine Learning
"""

from typing import List, Dict, Any
from datetime import datetime
import pandas as pd
from fastapi import APIRouter, Depends

from api.schemas import (
    WhatIfSimulationRequest,
    SimulationImpactResponse,
    FloodPredictionOutput,
    TrafficPredictionOutput
)
from api.dependencies import (
    get_traffic_model,
    get_flood_model,
    get_db_manager,
    MumbaiTrafficModel,
    MumbaiFloodModel,
    DatabaseManager
)

router = APIRouter(prefix="/api/v1/simulation", tags=["What-If Scenario Simulation"])


@router.post("/predict-impact", response_model=SimulationImpactResponse)
def simulate_impact(
    payload: WhatIfSimulationRequest,
    traffic_model: MumbaiTrafficModel = Depends(get_traffic_model),
    flood_model: MumbaiFloodModel = Depends(get_flood_model),
    db: DatabaseManager = Depends(get_db_manager)
):
    now_str = datetime.now().isoformat()
    roads = db.get_all_roads()
    zones = db.get_all_flood_zones()
    hospitals = db.get_all_hospitals()

    flood_outputs: List[FloodPredictionOutput] = []
    traffic_outputs: List[TrafficPredictionOutput] = []
    hospital_impacts: List[Dict[str, Any]] = []
    recommendations: List[str] = []

    eff_rain = payload.absolute_rainfall_mm if payload.absolute_rainfall_mm is not None else max(0.0, 30.0 * (1.0 + (payload.rainfall_delta_pct or 0.0) / 100.0))
    summary = f"Simulated urban impact for scenario '{payload.scenario_type}' at {eff_rain:.1f}mm rainfall."

    for z in zones:
        inp = {
            "rainfall": [eff_rain],
            "rainfall_rolling_3d": [eff_rain * 2.2],
            "rainfall_rolling_7d": [eff_rain * 3.5],
            "air_pressure": [1003.0 if eff_rain > 50 else 1008.0],
            "wind_speed": [24.0 if eff_rain > 50 else 15.0],
            "elevation": [z.get("elevation_m", 4.0)]
        }
        pred_df = flood_model.predict(pd.DataFrame(inp)).iloc[0]
        prob_keys = [c for c in pred_df.index if c.startswith("prob_")]
        conf_probs = {k.replace("prob_", "").upper(): float(pred_df[k]) for k in prob_keys}

        flood_outputs.append(FloodPredictionOutput(
            zone_id=z["zone_id"],
            zone_name=z["name"],
            predicted_inundation_depth_cm=float(pred_df["predicted_inundation_depth_cm"]),
            predicted_flood_risk_score=float(pred_df["predicted_flood_risk_score"]),
            predicted_risk_category=str(pred_df["predicted_risk_category"]),
            confidence_probabilities=conf_probs,
            drainage_strain=round(eff_rain / 50.0, 2),
            is_marine_locked=bool(eff_rain > 50.0)
        ))

    closed_ids = set(payload.closed_segment_ids or [])
    for r in roads:
        rid = r["segment_id"]
        is_closed = (rid in closed_ids) or (eff_rain > 100.0 and r.get("is_flood_prone"))
        base_speed = 5.0 if is_closed else float(r.get("speed_limit_kmh", 50.0)) * (0.5 if eff_rain > 30 else 0.8)
        road_len = float(r.get("length_km", 5.0))
        vol = 100 if is_closed else int(r.get("capacity_vph", 4000) * (0.95 if eff_rain > 30 else 0.7))

        inp = {
            "hour": [10],
            "dow": [2],
            "Traffic_Volume": [vol],
            "Traffic_Speed": [base_speed],
            "Road_Length": [road_len]
        }
        pred_df = traffic_model.predict(pd.DataFrame(inp)).iloc[0]
        prob_keys = [c for c in pred_df.index if c.startswith("prob_")]
        conf_probs = {k.replace("prob_", "").upper(): float(pred_df[k]) for k in prob_keys}

        traffic_outputs.append(TrafficPredictionOutput(
            segment_id=rid,
            road_name=r["name"],
            predicted_travel_time_min=60.0 if is_closed else float(pred_df["predicted_travel_time_min"]),
            predicted_congestion_level="High" if is_closed else str(pred_df["predicted_congestion_level"]),
            confidence_probabilities=conf_probs,
            speed_limit_kmh=int(r.get("speed_limit_kmh", 60)),
            is_closed=is_closed,
            predicted_average_speed_kmh=5.0 if is_closed else float(pred_df.get("predicted_average_speed_kmh", base_speed)),
            predicted_congestion_index=0.98 if is_closed else float(pred_df.get("predicted_congestion_index", 0.5))
        ))

    unavail_ids = set(payload.unavailable_hospital_ids or [])
    for h in hospitals:
        hid = h["hospital_id"]
        is_off = hid in unavail_ids
        hospital_impacts.append({
            "hospital_id": hid,
            "name": h["name"],
            "is_operational": not is_off,
            "available_beds": 0 if is_off else h["available_beds"],
            "icu_available": 0 if is_off else h["icu_available"]
        })

    if eff_rain > 50:
        recommendations.append("Severe rain alert: deploy municipal de-watering pumps to low-lying subways.")
    if closed_ids:
        recommendations.append(f"Traffic re-routing required for closed segments: {list(closed_ids)}.")

    return SimulationImpactResponse(
        scenario_type=payload.scenario_type,
        simulation_timestamp=now_str,
        summary_message=summary,
        affected_flood_zones=flood_outputs,
        affected_road_segments=traffic_outputs,
        hospital_status_impact=hospital_impacts,
        recommendations=recommendations
    )
