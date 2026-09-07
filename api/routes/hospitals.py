"""
Hospital telemetry endpoints.
Member 1: Data Engineering & Machine Learning
"""

from typing import List
from fastapi import APIRouter, Depends

from api.schemas import HospitalStatusResponse
from api.dependencies import get_db_manager, DatabaseManager

router = APIRouter(prefix="/api/v1/hospitals", tags=["Emergency Healthcare Infrastructure"])


@router.get("/status", response_model=List[HospitalStatusResponse])
def get_hospitals_status(db: DatabaseManager = Depends(get_db_manager)):
    hospitals = db.get_all_hospitals()
    results = []
    for h in hospitals:
        tot = h["total_beds"]
        avail = h["available_beds"]
        occ = round(((tot - avail) / max(1, tot)) * 100.0, 1)
        results.append(HospitalStatusResponse(
            hospital_id=h["hospital_id"],
            name=h["name"],
            zone=h["zone"],
            category=h["category"],
            total_beds=tot,
            available_beds=avail,
            icu_total=h["icu_total"],
            icu_available=h["icu_available"],
            occupancy_rate_pct=occ,
            has_emergency_ward=bool(h.get("has_emergency_ward", 1)),
            is_operational=bool(h.get("is_operational", 1)),
            flood_isolation_risk=h.get("flood_isolation_risk", "LOW"),
            coordinates=h.get("coordinates", [72.84, 19.00])
        ))
    return results
