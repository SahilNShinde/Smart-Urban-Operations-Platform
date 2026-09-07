# Mumbai Urban Operations - Real ML Model Evaluation Report

Evaluation results for Member 1 trained on real user datasets:
- `data/raw/flood_dataset.csv` (Mumbai historical weather & rainfall telemetry)
- `data/raw/all_features_traffic_dataset.csv` (Traffic volume, speed, density & congestion)

## 1. Traffic Prediction Model Performance (5 Features -> Travel Time & Congestion Level)

| Metric Target | MAE | RMSE | $R^2$ Score |
| :--- | :--- | :--- | :--- |
| **Predicted Travel Time** (min) | 2.39 min | 3.05 min | 0.8013 |

- **Classification Accuracy**: `84.12%`
- **Macro F1-Score**: `0.8429`
- **Weighted F1-Score**: `0.8418`

## 2. Flood Risk & Inundation Model Performance

| Metric Target | MAE | RMSE | $R^2$ Score |
| :--- | :--- | :--- | :--- |
| **Inundation Depth** (cm) | 5.14 cm | 8.18 cm | 0.8079 |
| **Flood Risk Score** (0-1) | 0.0782 | 0.1031 | 0.8311 |

- **Classification Accuracy**: `81.73%`
- **Macro F1-Score**: `0.8569`
- **Weighted F1-Score**: `0.8167`

