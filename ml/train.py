"""
Model Training Engine for Smart Urban Operations Platform.
Member 1: Data Engineering & Machine Learning

Exclusively trains models on the user's processed datasets:
- data/processed/flood_processed.csv
- data/processed/traffic_processed.csv
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.models.traffic_model import MumbaiTrafficModel
from ml.models.flood_model import MumbaiFloodModel

SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(SAVED_MODELS_DIR, exist_ok=True)


def train_traffic(test_size: float = 0.2, random_state: int = 42):
    print("\n==========================================")
    print(" TRAIN TRAFFIC MODEL (all_features_traffic_dataset)")
    print("==========================================")
    data_path = os.path.join(PROCESSED_DATA_DIR, "traffic_processed.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed traffic data not found at {data_path}. Run pipelines/etl_pipeline.py first.")

    df = pd.read_csv(data_path)
    print(f"[Train Traffic] Loaded {len(df)} records.")

    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    print(f"[Train Traffic] Split: {len(train_df)} train, {len(test_df)} test.")

    model = MumbaiTrafficModel()
    model.fit(train_df)

    # Save trained model
    model.save(SAVED_MODELS_DIR)

    # Save test set for evaluation
    test_path = os.path.join(PROCESSED_DATA_DIR, "traffic_test_split.csv")
    test_df.to_csv(test_path, index=False)
    print(f"[Train Traffic] Saved test split to {test_path}")

    return model, test_df


def train_flood(test_size: float = 0.2, random_state: int = 42):
    print("\n==========================================")
    print(" TRAIN FLOOD MODEL (flood_dataset)")
    print("==========================================")
    data_path = os.path.join(PROCESSED_DATA_DIR, "flood_processed.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed flood data not found at {data_path}. Run pipelines/etl_pipeline.py first.")

    df = pd.read_csv(data_path)
    print(f"[Train Flood] Loaded {len(df)} records.")

    train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    print(f"[Train Flood] Split: {len(train_df)} train, {len(test_df)} test.")

    model = MumbaiFloodModel()
    model.fit(train_df)

    # Save trained model
    model.save(SAVED_MODELS_DIR)

    # Save test set for evaluation
    test_path = os.path.join(PROCESSED_DATA_DIR, "flood_test_split.csv")
    test_df.to_csv(test_path, index=False)
    print(f"[Train Flood] Saved test split to {test_path}")

    return model, test_df


def main():
    parser = argparse.ArgumentParser(description="Train ML Models on User Datasets")
    parser.add_argument(
        "--models",
        choices=["all", "traffic", "flood"],
        default="all",
        help="Models to train"
    )
    args = parser.parse_args()

    metadata = {
        "dataset_source": "User Raw Datasets (flood_dataset.csv, all_features_traffic_dataset.csv)",
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "models": {}
    }

    if args.models in ["all", "traffic"]:
        _, traffic_test = train_traffic()
        metadata["models"]["traffic"] = {
            "version": "2.0.0",
            "test_samples": len(traffic_test),
            "algorithm": "HistGradientBoosting (Speed Regressor + Congestion Index + Classifier)"
        }

    if args.models in ["all", "flood"]:
        _, flood_test = train_flood()
        metadata["models"]["flood"] = {
            "version": "2.0.0",
            "test_samples": len(flood_test),
            "algorithm": "HistGradientBoosting (Depth + Risk Score + Classifier)"
        }

    meta_file = os.path.join(SAVED_MODELS_DIR, "metadata.json")
    with open(meta_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\n[Training Complete] Metadata saved to {meta_file}")


if __name__ == "__main__":
    main()
