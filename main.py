"""
Unified Entrypoint CLI for Smart Urban Operations Platform.
Member 1: Data Engineering & Machine Learning

Exclusively operates on user datasets:
- data/raw/flood_dataset.csv
- data/raw/all_features_traffic_dataset.csv
"""

import argparse
import os
import sys
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from pipelines.etl_pipeline import UrbanOperationsETL
from database.db_manager import DatabaseManager
from ml.train import train_traffic, train_flood
from ml.evaluate import generate_evaluation_report


def run_full_pipeline():
    print("\n[Step 1/3] Running Authoritative ETL on User Raw Datasets...")
    etl = UrbanOperationsETL()
    etl.run_all()

    print("\n[Step 2/3] Verifying Database Setup...")
    DatabaseManager()

    print("\n[Step 3/3] Training Models on Processed User Datasets...")
    train_traffic()
    train_flood()

    print("\n[Complete] Evaluating Models and Generating Reports...")
    generate_evaluation_report()
    print("\n>>> Pipeline successfully executed exclusively on user datasets!")


def run_demo_inference():
    print("\n=======================================================")
    print(" SMART URBAN OPERATIONS - USER DATASET MODEL INFERENCE DEMO")
    print("=======================================================")
    from api.dependencies import get_traffic_model, get_flood_model, get_db_manager
    import pandas as pd

    db = get_db_manager()
    traffic_model = get_traffic_model()
    flood_model = get_flood_model()

    print("\n1. Traffic Model Inference (5 Features -> Travel Time & Congestion Level):")
    sample_traffic = pd.DataFrame([{
        "hour": 9,
        "dow": 1,
        "Traffic_Volume": 3450,
        "Average_Speed": 45.0,
        "Road_Length": 6.2
    }])
    pred_t = traffic_model.predict(sample_traffic).iloc[0]
    print(f"  - Predicted Travel Time: {pred_t['predicted_travel_time_min']} mins")
    print(f"  - Congestion Level:      {pred_t['predicted_congestion_level']}")
    if "prob_high" in pred_t:
        print(f"  - Probabilities:         High: {pred_t.get('prob_high')}, Med: {pred_t.get('prob_medium')}, Low: {pred_t.get('prob_low')}")

    print("\n2. Flood Model Inference (flood_dataset):")
    sample_flood = pd.DataFrame([{
        "rainfall": 82.5,
        "rainfall_rolling_3d": 145.0,
        "rainfall_rolling_7d": 210.0,
        "air_pressure": 1001.0,
        "wind_speed": 26.0,
        "elevation": 4.0
    }])
    pred_f = flood_model.predict(sample_flood).iloc[0]
    print(f"  - Inundation Depth:     {pred_f['predicted_inundation_depth_cm']} cm")
    print(f"  - Flood Risk Score:     {pred_f['predicted_flood_risk_score']}")
    print(f"  - Risk Category:        {pred_f['predicted_risk_category']}")

    print("\n3. Mumbai Trauma Hospitals Telemetry:")
    hospitals = db.get_all_hospitals()
    for h in hospitals[:2]:
        print(f"  - {h['name']}: {h['available_beds']}/{h['total_beds']} beds, {h['icu_available']}/{h['icu_total']} ICU units available (Flood Risk: {h['flood_isolation_risk']})")


def main():
    parser = argparse.ArgumentParser(description="Smart Urban Operations Platform CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("pipeline", help="Run ETL and ML training on user datasets")

    serve_parser = subparsers.add_parser("serve", help="Launch FastAPI server")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host address")
    serve_parser.add_argument("--port", type=int, default=8000, help="Port number")
    serve_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    subparsers.add_parser("demo", help="Run quick demo inference")

    args = parser.parse_args()

    if args.command == "pipeline":
        run_full_pipeline()
    elif args.command == "serve":
        print(f"Starting Smart Urban Operations FastAPI Server on http://{args.host}:{args.port}")
        uvicorn.run("api.app:app", host=args.host, port=args.port, reload=args.reload)
    elif args.command == "demo":
        run_demo_inference()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
