"""
FastAPI Application for Mumbai Smart Urban Operations Platform.
Member 1: Data Engineering & Machine Learning
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import traffic, flood, simulation, hospitals, gis
from api.dependencies import get_traffic_model, get_flood_model, get_db_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[FastAPI] Preloading database and models...")
    get_db_manager()
    get_traffic_model()
    get_flood_model()
    print("[FastAPI] Startup ready.")
    yield


app = FastAPI(
    title="Smart Urban Operations Platform (Mumbai City)",
    description="Machine Learning & Prediction APIs trained on Real Mumbai Datasets.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic.router)
app.include_router(flood.router)
app.include_router(simulation.router)
app.include_router(hospitals.router)
app.include_router(gis.router)


@app.get("/api/v1/health", tags=["System Health"])
def health_check():
    return {
        "status": "HEALTHY",
        "city": "Mumbai",
        "dataset_mode": "Real Datasets (flood_dataset.csv, all_features_traffic_dataset.csv)",
        "models_loaded": ["real_traffic_model", "real_flood_model"],
        "version": "2.0.0"
    }


@app.get("/api/v1/metadata", tags=["System Health"])
def metadata():
    return {
        "platform": "Smart Urban Operations Platform",
        "city": "Mumbai",
        "member_role": "Member 1: Data Engineering + ML (25%)",
        "supported_scenarios": ["increased_rainfall", "road_closure", "hospital_unavailable"]
    }
