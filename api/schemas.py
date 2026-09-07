"""
Pydantic API Schemas for Smart Urban Operations Platform - Mumbai City
Member 1: Data Engineering & Machine Learning
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TrafficPredictionInput(BaseModel):
    # 5 Core Features
    hour: int = Field(default=9, description="Timestamp / Hour of day (0-23)", ge=0, le=23)
    dow: int = Field(default=1, description="Day of Week (0=Monday, 6=Sunday)", ge=0, le=6)
    Traffic_Volume: int = Field(default=2800, description="Traffic volume (vehicle count per hour)")
    Average_Speed: float = Field(default=45.0, description="Average speed in km/h", gt=0.0)
    Road_Length: float = Field(default=5.4, description="Road distance/length in km", gt=0.0)
    # Metadata context
    segment_id: Optional[str] = Field(default="ROAD_WEH_01", description="Road segment ID (optional)", json_schema_extra={"example": "ROAD_WEH_01"})

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if isinstance(obj, dict):
            if "Traffic_Speed" in obj and "Average_Speed" not in obj:
                obj["Average_Speed"] = obj["Traffic_Speed"]
            if "Road_Distance" in obj and "Road_Length" not in obj:
                obj["Road_Length"] = obj["Road_Distance"]
        return super().model_validate(obj, *args, **kwargs)


class TrafficPredictionOutput(BaseModel):
    segment_id: str
    road_name: str
    predicted_travel_time_min: float
    predicted_congestion_level: str
    confidence_probabilities: Dict[str, float]
    speed_limit_kmh: int
    is_closed: bool
    predicted_average_speed_kmh: Optional[float] = None
    predicted_congestion_index: Optional[float] = None


class FloodPredictionInput(BaseModel):
    zone_id: str = Field(default="FLOOD_HINDMATA", json_schema_extra={"example": "FLOOD_HINDMATA"})
    rainfall: float = Field(default=45.0, description="Rainfall in mm")
    rainfall_rolling_3d: Optional[float] = Field(default=95.0)
    rainfall_rolling_7d: Optional[float] = Field(default=160.0)
    air_pressure: Optional[float] = Field(default=1003.5)
    wind_speed: Optional[float] = Field(default=22.0)
    elevation: Optional[float] = Field(default=2.8)


class FloodPredictionOutput(BaseModel):
    zone_id: str
    zone_name: str
    predicted_inundation_depth_cm: float
    predicted_flood_risk_score: float
    predicted_risk_category: str
    confidence_probabilities: Dict[str, float]
    drainage_strain: float
    is_marine_locked: bool


class WhatIfSimulationRequest(BaseModel):
    scenario_type: str = Field(..., json_schema_extra={"example": "increased_rainfall"})
    rainfall_delta_pct: Optional[float] = Field(default=0.0)
    absolute_rainfall_mm: Optional[float] = Field(default=None)
    closed_segment_ids: Optional[List[str]] = Field(default_factory=list)
    unavailable_hospital_ids: Optional[List[str]] = Field(default_factory=list)


class SimulationImpactResponse(BaseModel):
    scenario_type: str
    simulation_timestamp: str
    summary_message: str
    affected_flood_zones: List[FloodPredictionOutput]
    affected_road_segments: List[TrafficPredictionOutput]
    hospital_status_impact: List[Dict[str, Any]]
    recommendations: List[str]


class HospitalStatusResponse(BaseModel):
    hospital_id: str
    name: str
    zone: str
    category: str
    total_beds: int
    available_beds: int
    icu_total: int
    icu_available: int
    occupancy_rate_pct: float
    has_emergency_ward: bool
    is_operational: bool
    flood_isolation_risk: str
    coordinates: List[float]
