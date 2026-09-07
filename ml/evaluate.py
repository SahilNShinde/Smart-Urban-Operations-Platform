"""
Model Evaluation Suite for Real Mumbai Traffic and Flood Models.
Member 1: Data Engineering & Machine Learning
"""

import json
import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_recall_fscore_support,
    classification_report
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.models.traffic_model import MumbaiTrafficModel
from ml.models.flood_model import MumbaiFloodModel

SAVED_MODELS_DIR = os.path.join(BASE_DIR, "ml", "saved_models")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


def evaluate_traffic_model() -> dict:
    test_path = os.path.join(PROCESSED_DATA_DIR, "traffic_test_split.csv")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test split not found at {test_path}")

    df_test = pd.read_csv(test_path)
    model = MumbaiTrafficModel.load(SAVED_MODELS_DIR)
    preds = model.predict(df_test)

    # Travel Time Regression (Target 1)
    y_true_tt = df_test["Travel_Time"].values if "Travel_Time" in df_test.columns else ((df_test["Road_Length"] / df_test["Traffic_Speed"].clip(lower=1.0)) * 60.0).values
    y_pred_tt = preds["predicted_travel_time_min"].values
    mae_tt = float(mean_absolute_error(y_true_tt, y_pred_tt))
    rmse_tt = float(np.sqrt(mean_squared_error(y_true_tt, y_pred_tt)))
    r2_tt = float(r2_score(y_true_tt, y_pred_tt))

    # Classification: Congestion Level (Target 2)
    y_true_cls = df_test["Congestion_Level"].astype(str).str.strip().str.capitalize().values
    y_pred_cls = preds["predicted_congestion_level"].astype(str).str.strip().str.capitalize().values
    acc_cls = float(accuracy_score(y_true_cls, y_pred_cls))
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true_cls, y_pred_cls, average="macro", zero_division=0)
    p_weight, r_weight, f1_weight, _ = precision_recall_fscore_support(y_true_cls, y_pred_cls, average="weighted", zero_division=0)
    clf_rep = classification_report(y_true_cls, y_pred_cls, output_dict=True, zero_division=0)

    return {
        "travel_time_regression": {
            "MAE": round(mae_tt, 2),
            "RMSE": round(rmse_tt, 2),
            "R2": round(r2_tt, 4)
        },
        "congestion_level_classification": {
            "Accuracy": round(acc_cls, 4),
            "Macro_F1": round(float(f1_macro), 4),
            "Weighted_F1": round(float(f1_weight), 4),
            "Detailed_Report": clf_rep
        }
    }


def evaluate_flood_model() -> dict:
    test_path = os.path.join(PROCESSED_DATA_DIR, "flood_test_split.csv")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test split not found at {test_path}")

    df_test = pd.read_csv(test_path)
    model = MumbaiFloodModel.load(SAVED_MODELS_DIR)
    preds = model.predict(df_test)

    # Inundation Depth
    y_true_dpth = df_test["inundation_depth_cm"].values
    y_pred_dpth = preds["predicted_inundation_depth_cm"].values
    mae_dpth = float(mean_absolute_error(y_true_dpth, y_pred_dpth))
    rmse_dpth = float(np.sqrt(mean_squared_error(y_true_dpth, y_pred_dpth)))
    r2_dpth = float(r2_score(y_true_dpth, y_pred_dpth))

    # Flood Risk Score
    y_true_scr = df_test["flood_risk_score"].values
    y_pred_scr = preds["predicted_flood_risk_score"].values
    mae_scr = float(mean_absolute_error(y_true_scr, y_pred_scr))
    rmse_scr = float(np.sqrt(mean_squared_error(y_true_scr, y_pred_scr)))
    r2_scr = float(r2_score(y_true_scr, y_pred_scr))

    # Classification
    y_true_cat = df_test["risk_category"].values
    y_pred_cat = preds["predicted_risk_category"].values
    acc_cat = float(accuracy_score(y_true_cat, y_pred_cat))
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(y_true_cat, y_pred_cat, average="macro", zero_division=0)
    p_weight, r_weight, f1_weight, _ = precision_recall_fscore_support(y_true_cat, y_pred_cat, average="weighted", zero_division=0)
    clf_rep = classification_report(y_true_cat, y_pred_cat, output_dict=True, zero_division=0)

    return {
        "inundation_depth_cm_regression": {
            "MAE": round(mae_dpth, 2),
            "RMSE": round(rmse_dpth, 2),
            "R2": round(r2_dpth, 4)
        },
        "flood_risk_score_regression": {
            "MAE": round(mae_scr, 4),
            "RMSE": round(rmse_scr, 4),
            "R2": round(r2_scr, 4)
        },
        "risk_category_classification": {
            "Accuracy": round(acc_cat, 4),
            "Macro_F1": round(float(f1_macro), 4),
            "Weighted_F1": round(float(f1_weight), 4),
            "Detailed_Report": clf_rep
        }
    }


def generate_evaluation_report():
    print("\n==========================================")
    print(" EVALUATING REAL DATASET TRAINED MODELS")
    print("==========================================")

    traffic_metrics = evaluate_traffic_model()
    print("[Traffic Model Evaluation Results]:")
    print("  - Travel Time (min): MAE =", traffic_metrics["travel_time_regression"]["MAE"], "min, R2 =", traffic_metrics["travel_time_regression"]["R2"])
    print("  - Classification:    Accuracy =", traffic_metrics["congestion_level_classification"]["Accuracy"], "F1 =", traffic_metrics["congestion_level_classification"]["Weighted_F1"])

    flood_metrics = evaluate_flood_model()
    print("\n[Flood Risk Model Evaluation Results]:")
    print("  - Inundation Depth: MAE =", flood_metrics["inundation_depth_cm_regression"]["MAE"], "cm, R2 =", flood_metrics["inundation_depth_cm_regression"]["R2"])
    print("  - Flood Risk Score: MAE =", flood_metrics["flood_risk_score_regression"]["MAE"], "R2 =", flood_metrics["flood_risk_score_regression"]["R2"])
    print("  - Classification:   Accuracy =", flood_metrics["risk_category_classification"]["Accuracy"], "F1 =", flood_metrics["risk_category_classification"]["Weighted_F1"])

    all_metrics = {
        "city": "Mumbai",
        "dataset_source": "User Datasets: flood_dataset.csv & all_features_traffic_dataset.csv",
        "traffic_model": traffic_metrics,
        "flood_model": flood_metrics
    }

    json_path = os.path.join(REPORTS_DIR, "metrics.json")
    with open(json_path, "w") as f:
        json.dump(all_metrics, f, indent=2)

    md_path = os.path.join(REPORTS_DIR, "model_evaluation_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Mumbai Urban Operations - Real ML Model Evaluation Report\n\n")
        f.write("Evaluation results for Member 1 trained on real user datasets:\n")
        f.write("- `data/raw/flood_dataset.csv` (Mumbai historical weather & rainfall telemetry)\n")
        f.write("- `data/raw/all_features_traffic_dataset.csv` (Traffic volume, speed, density & congestion)\n\n")

        f.write("## 1. Traffic Prediction Model Performance (5 Features -> Travel Time & Congestion Level)\n\n")
        f.write("| Metric Target | MAE | RMSE | $R^2$ Score |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        f.write(f"| **Predicted Travel Time** (min) | {traffic_metrics['travel_time_regression']['MAE']} min | {traffic_metrics['travel_time_regression']['RMSE']} min | {traffic_metrics['travel_time_regression']['R2']} |\n\n")

        f.write(f"- **Classification Accuracy**: `{traffic_metrics['congestion_level_classification']['Accuracy'] * 100:.2f}%`\n")
        f.write(f"- **Macro F1-Score**: `{traffic_metrics['congestion_level_classification']['Macro_F1']:.4f}`\n")
        f.write(f"- **Weighted F1-Score**: `{traffic_metrics['congestion_level_classification']['Weighted_F1']:.4f}`\n\n")

        f.write("## 2. Flood Risk & Inundation Model Performance\n\n")
        f.write("| Metric Target | MAE | RMSE | $R^2$ Score |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        f.write(f"| **Inundation Depth** (cm) | {flood_metrics['inundation_depth_cm_regression']['MAE']} cm | {flood_metrics['inundation_depth_cm_regression']['RMSE']} cm | {flood_metrics['inundation_depth_cm_regression']['R2']} |\n")
        f.write(f"| **Flood Risk Score** (0-1) | {flood_metrics['flood_risk_score_regression']['MAE']} | {flood_metrics['flood_risk_score_regression']['RMSE']} | {flood_metrics['flood_risk_score_regression']['R2']} |\n\n")

        f.write(f"- **Classification Accuracy**: `{flood_metrics['risk_category_classification']['Accuracy'] * 100:.2f}%`\n")
        f.write(f"- **Macro F1-Score**: `{flood_metrics['risk_category_classification']['Macro_F1']:.4f}`\n")
        f.write(f"- **Weighted F1-Score**: `{flood_metrics['risk_category_classification']['Weighted_F1']:.4f}`\n\n")

    print(f"\n[Evaluation Complete] Reports generated at {md_path} and {json_path}")
    return all_metrics


if __name__ == "__main__":
    generate_evaluation_report()
