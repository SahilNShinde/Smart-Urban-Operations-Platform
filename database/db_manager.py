"""
Database Manager with SQLite fallback for Mumbai Urban Operations Platform.
Member 1: Data Engineering & Machine Learning
"""

import json
import os
import sqlite3
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "urban_operations.db")
GEOJSON_DIR = os.path.join(BASE_DIR, "data", "geojson")


class DatabaseManager:
    def __init__(self, pg_uri: Optional[str] = None):
        self.pg_uri = pg_uri or os.getenv("DATABASE_URL")
        self.sqlite_path = DB_PATH
        self.init_sqlite_tables()
        self.seed_database_if_empty()

    def get_sqlite_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_sqlite_tables(self):
        with self.get_sqlite_conn() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS road_segments (
                    segment_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    corridor TEXT,
                    zone TEXT NOT NULL,
                    road_type TEXT NOT NULL,
                    lanes INTEGER NOT NULL,
                    speed_limit_kmh INTEGER NOT NULL,
                    length_km REAL NOT NULL,
                    capacity_vph INTEGER NOT NULL,
                    elevation_m REAL,
                    is_flood_prone INTEGER DEFAULT 0,
                    coordinates_json TEXT
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flood_risk_zones (
                    zone_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    ward TEXT NOT NULL,
                    catchment_basin TEXT,
                    elevation_m REAL NOT NULL,
                    drainage_capacity_index REAL NOT NULL,
                    critical_threshold_rainfall_mm_h REAL NOT NULL,
                    has_pumping_station INTEGER DEFAULT 0,
                    polygon_json TEXT
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hospitals (
                    hospital_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    zone TEXT NOT NULL,
                    category TEXT NOT NULL,
                    total_beds INTEGER NOT NULL,
                    available_beds INTEGER NOT NULL,
                    icu_total INTEGER NOT NULL,
                    icu_available INTEGER NOT NULL,
                    has_emergency_ward INTEGER DEFAULT 1,
                    is_operational INTEGER DEFAULT 1,
                    flood_isolation_risk TEXT DEFAULT 'LOW',
                    coordinates_json TEXT
                );
            """)
            conn.commit()

    def seed_database_if_empty(self):
        with self.get_sqlite_conn() as conn:
            count = conn.execute("SELECT count(*) FROM road_segments").fetchone()[0]
            if count > 0:
                return

        # Seed roads
        roads_file = os.path.join(GEOJSON_DIR, "mumbai_roads.geojson")
        if os.path.exists(roads_file):
            with open(roads_file, "r") as f:
                roads_data = json.load(f)
            with self.get_sqlite_conn() as conn:
                for feat in roads_data["features"]:
                    p = feat["properties"]
                    coords = json.dumps(feat["geometry"]["coordinates"])
                    conn.execute("""
                        INSERT OR REPLACE INTO road_segments 
                        (segment_id, name, corridor, zone, road_type, lanes, speed_limit_kmh, length_km, capacity_vph, elevation_m, is_flood_prone, coordinates_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        p["segment_id"], p["name"], p.get("corridor", "Arterial"), p["zone"], p["road_type"],
                        p["lanes"], p["speed_limit_kmh"], p["length_km"], p["capacity_vph"],
                        p.get("elevation_m", 10.0), int(p.get("is_flood_prone", False)), coords
                    ))
                conn.commit()

        # Seed flood zones
        flood_file = os.path.join(GEOJSON_DIR, "mumbai_flood_zones.geojson")
        if os.path.exists(flood_file):
            with open(flood_file, "r") as f:
                flood_data = json.load(f)
            with self.get_sqlite_conn() as conn:
                for feat in flood_data["features"]:
                    p = feat["properties"]
                    poly = json.dumps(feat["geometry"]["coordinates"])
                    conn.execute("""
                        INSERT OR REPLACE INTO flood_risk_zones 
                        (zone_id, name, ward, catchment_basin, elevation_m, drainage_capacity_index, critical_threshold_rainfall_mm_h, has_pumping_station, polygon_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        p["zone_id"], p["name"], p["ward"], p["catchment_basin"],
                        p["elevation_m"], p["drainage_capacity_index"], p["critical_threshold_rainfall_mm_h"],
                        int(p.get("has_pumping_station", False)), poly
                    ))
                conn.commit()

        # Seed hospitals
        hosp_file = os.path.join(GEOJSON_DIR, "mumbai_hospitals.geojson")
        if os.path.exists(hosp_file):
            with open(hosp_file, "r") as f:
                hosp_data = json.load(f)
            with self.get_sqlite_conn() as conn:
                for feat in hosp_data["features"]:
                    p = feat["properties"]
                    coords = json.dumps(feat["geometry"]["coordinates"])
                    conn.execute("""
                        INSERT OR REPLACE INTO hospitals 
                        (hospital_id, name, zone, category, total_beds, available_beds, icu_total, icu_available, has_emergency_ward, is_operational, flood_isolation_risk, coordinates_json)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        p["hospital_id"], p["name"], p["zone"], p["category"],
                        p["total_beds"], p["available_beds"], p["icu_total"], p["icu_available"],
                        int(p.get("has_emergency_ward", True)), int(p.get("is_operational", True)),
                        p.get("flood_isolation_risk", "LOW"), coords
                    ))
                conn.commit()

    def get_all_hospitals(self) -> List[Dict[str, Any]]:
        with self.get_sqlite_conn() as conn:
            rows = conn.execute("SELECT * FROM hospitals").fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if d.get("coordinates_json"):
                    d["coordinates"] = json.loads(d["coordinates_json"])
                result.append(d)
            return result

    def get_all_roads(self) -> List[Dict[str, Any]]:
        with self.get_sqlite_conn() as conn:
            rows = conn.execute("SELECT * FROM road_segments").fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if d.get("coordinates_json"):
                    d["coordinates"] = json.loads(d["coordinates_json"])
                result.append(d)
            return result

    def get_all_flood_zones(self) -> List[Dict[str, Any]]:
        with self.get_sqlite_conn() as conn:
            rows = conn.execute("SELECT * FROM flood_risk_zones").fetchall()
            result = []
            for r in rows:
                d = dict(r)
                if d.get("polygon_json"):
                    d["polygon"] = json.loads(d["polygon_json"])
                result.append(d)
            return result
