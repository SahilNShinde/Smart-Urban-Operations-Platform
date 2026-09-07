-- Smart Urban Operations Platform - Mumbai City
-- PostgreSQL + PostGIS Spatial Database Schema
-- Member 1: Data Engineering & Machine Learning

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS road_segments (
    segment_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    corridor VARCHAR(100),
    zone VARCHAR(50) NOT NULL,
    road_type VARCHAR(50) NOT NULL,
    lanes INT NOT NULL DEFAULT 4,
    speed_limit_kmh INT NOT NULL DEFAULT 60,
    length_km NUMERIC(6, 3) NOT NULL,
    capacity_vph INT NOT NULL,
    elevation_m NUMERIC(5, 2) DEFAULT 10.0,
    is_flood_prone BOOLEAN DEFAULT FALSE,
    geom GEOMETRY(LineString, 4326)
);

CREATE TABLE IF NOT EXISTS flood_risk_zones (
    zone_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    ward VARCHAR(20) NOT NULL,
    catchment_basin VARCHAR(100),
    elevation_m NUMERIC(5, 2) NOT NULL,
    drainage_capacity_index NUMERIC(3, 2) NOT NULL,
    critical_threshold_rainfall_mm_h NUMERIC(5, 2) NOT NULL,
    has_pumping_station BOOLEAN DEFAULT FALSE,
    geom GEOMETRY(Polygon, 4326)
);

CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    zone VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    total_beds INT NOT NULL,
    available_beds INT NOT NULL,
    icu_total INT NOT NULL,
    icu_available INT NOT NULL,
    has_emergency_ward BOOLEAN DEFAULT TRUE,
    is_operational BOOLEAN DEFAULT TRUE,
    flood_isolation_risk VARCHAR(20) DEFAULT 'LOW',
    geom GEOMETRY(Point, 4326)
);
