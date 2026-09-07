"""
GIS Spatial Layer Endpoints for Mumbai Smart Urban Operations Platform.
Provides GeoJSON FeatureCollections for roads, flood vulnerability zones, and trauma hospitals.
"""

import json
import os
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GEOJSON_DIR = os.path.join(BASE_DIR, "data", "geojson")

router = APIRouter(prefix="/api/v1/gis", tags=["GIS & Spatial Infrastructure"])


def _load_geojson(filename: str) -> Dict[str, Any]:
    path = os.path.join(GEOJSON_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"GeoJSON layer '{filename}' not found on server.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/layers", summary="Get catalog of available spatial GIS layers")
def get_available_layers() -> Dict[str, Any]:
    return {
        "city": "Mumbai",
        "crs": "EPSG:4326 (WGS 84)",
        "layers": [
            {
                "id": "roads",
                "name": "Mumbai Major Arterial Corridors",
                "endpoint": "/api/v1/gis/roads",
                "geometry_type": "LineString",
                "description": "15 major arterial highways and expressways across Western, Eastern, and Harbor corridors."
            },
            {
                "id": "flood_zones",
                "name": "Monsoon Inundation Vulnerability Hotspots",
                "endpoint": "/api/v1/gis/flood-zones",
                "geometry_type": "Polygon",
                "description": "Historical chronic waterlogging zones (Hindmata, Milan Subway, Kurla, Dharavi, etc.)."
            },
            {
                "id": "hospitals",
                "name": "Designated Trauma & Municipal Emergency Centers",
                "endpoint": "/api/v1/gis/hospitals",
                "geometry_type": "Point",
                "description": "8 major tertiary and secondary trauma hospitals with bed and ICU capacity telemetry."
            }
        ]
    }


@router.get("/roads", summary="Get Mumbai road network GeoJSON")
def get_roads_geojson() -> Dict[str, Any]:
    return _load_geojson("mumbai_roads.geojson")


@router.get("/flood-zones", summary="Get Mumbai flood vulnerable zones GeoJSON")
def get_flood_zones_geojson() -> Dict[str, Any]:
    return _load_geojson("mumbai_flood_zones.geojson")


@router.get("/hospitals", summary="Get Mumbai emergency hospitals GeoJSON")
def get_hospitals_geojson() -> Dict[str, Any]:
    return _load_geojson("mumbai_hospitals.geojson")


@router.get("/unified-view", summary="Get complete unified spatial overlay (Roads, Floods, Hospitals)")
def get_unified_gis_overlay() -> Dict[str, Any]:
    return {
        "city": "Mumbai",
        "type": "UnifiedSpatialBundle",
        "roads": _load_geojson("mumbai_roads.geojson"),
        "flood_zones": _load_geojson("mumbai_flood_zones.geojson"),
        "hospitals": _load_geojson("mumbai_hospitals.geojson")
    }
