"""
Traffic Model using 5 Features to predict Travel Time and Congestion Level.
Member 1: Data Engineering & Machine Learning
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier

from ml.features.traffic_features import (
    get_traffic_preprocessor,
    prepare_traffic_features,
    TARGET_TRAVEL_TIME,
    TARGET_CONGESTION_LEVEL
)


class MumbaiTrafficModel:
    def __init__(self):
        self.version = "2.1.0"
        self.city = "Mumbai"
        self.preprocessor = get_traffic_preprocessor()

        self.travel_time_regressor = HistGradientBoostingRegressor(
            max_iter=150,
            learning_rate=0.08,
            max_depth=6,
            random_state=42
        )

        self.classifier = HistGradientBoostingClassifier(
            max_iter=150,
            learning_rate=0.08,
            max_depth=6,
            random_state=42
        )

        self.is_fitted = False

    def fit(self, df: pd.DataFrame):
        df_feat = prepare_traffic_features(df)
        X_trans = self.preprocessor.fit_transform(df_feat)

        if TARGET_TRAVEL_TIME not in df_feat.columns:
            # Fallback kinematic calculation if missing
            df_feat[TARGET_TRAVEL_TIME] = (df_feat["Road_Length"] / df_feat["Traffic_Speed"].clip(lower=1.0)) * 60.0

        if TARGET_CONGESTION_LEVEL not in df_feat.columns:
            df_feat[TARGET_CONGESTION_LEVEL] = np.where(
                df_feat["Traffic_Speed"] < 35, "High",
                np.where(df_feat["Traffic_Speed"] < 60, "Medium", "Low")
            )

        y_tt = df_feat[TARGET_TRAVEL_TIME].values
        y_cls = df_feat[TARGET_CONGESTION_LEVEL].astype(str).str.strip().str.capitalize().values

        print("[Traffic Model] Training Travel Time Regressor on 5 features...")
        self.travel_time_regressor.fit(X_trans, y_tt)

        print("[Traffic Model] Training Congestion Level Classifier on 5 features...")
        self.classifier.fit(X_trans, y_cls)

        self.is_fitted = True
        print("[Traffic Model] Successfully fitted all traffic models.")

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.is_fitted:
            raise RuntimeError("Traffic model is not fitted yet.")

        df_feat = prepare_traffic_features(df)
        X_trans = self.preprocessor.transform(df_feat)

        pred_tt = np.clip(self.travel_time_regressor.predict(X_trans), 0.5, 300.0).round(2)
        pred_cls = self.classifier.predict(X_trans)
        pred_probs = self.classifier.predict_proba(X_trans)
        classes = self.classifier.classes_

        results = df.copy()
        results["predicted_travel_time_min"] = pred_tt
        results["predicted_congestion_level"] = pred_cls

        for i, cls_name in enumerate(classes):
            results[f"prob_{str(cls_name).lower()}"] = pred_probs[:, i].round(3)

        # Backwards compatibility fields
        results["predicted_average_speed_kmh"] = df_feat["Traffic_Speed"].values.round(1)
        max_speed = 120.0
        results["predicted_congestion_index"] = np.clip(1.0 - (df_feat["Traffic_Speed"].values / max_speed), 0.0, 1.0).round(3)

        return results

    def save(self, model_dir: str):
        os.makedirs(model_dir, exist_ok=True)
        artifact_path = os.path.join(model_dir, "mumbai_traffic_model.joblib")
        payload = {
            "version": self.version,
            "city": self.city,
            "preprocessor": self.preprocessor,
            "travel_time_regressor": self.travel_time_regressor,
            "classifier": self.classifier
        }
        joblib.dump(payload, artifact_path)
        print(f"[Traffic Model] Saved model artifacts to {artifact_path}")

    @classmethod
    def load(cls, model_dir: str) -> "MumbaiTrafficModel":
        artifact_path = os.path.join(model_dir, "mumbai_traffic_model.joblib")
        if not os.path.exists(artifact_path):
            raise FileNotFoundError(f"Model file not found at {artifact_path}")
        payload = joblib.load(artifact_path)
        instance = cls()
        instance.version = payload.get("version", "2.1.0")
        instance.city = payload.get("city", "Mumbai")
        instance.preprocessor = payload["preprocessor"]
        instance.travel_time_regressor = payload.get("travel_time_regressor", payload.get("speed_regressor"))
        instance.classifier = payload["classifier"]
        instance.is_fitted = True
        return instance
