"""
Flood Model for Real Flood Dataset.
Member 1: Data Engineering & Machine Learning
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier

from ml.features.flood_features import (
    get_flood_preprocessor,
    prepare_flood_features,
    TARGET_DEPTH,
    TARGET_SCORE,
    TARGET_CATEGORY
)


class MumbaiFloodModel:
    def __init__(self):
        self.version = "2.0.0"
        self.city = "Mumbai"
        self.preprocessor = get_flood_preprocessor()

        self.depth_regressor = HistGradientBoostingRegressor(
            max_iter=150,
            learning_rate=0.08,
            max_depth=6,
            random_state=42
        )

        self.score_regressor = HistGradientBoostingRegressor(
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
        df_feat = prepare_flood_features(df)
        X_trans = self.preprocessor.fit_transform(df_feat)

        y_dpth = df_feat[TARGET_DEPTH].values
        y_scr = df_feat[TARGET_SCORE].values
        y_cat = df_feat[TARGET_CATEGORY].values

        print("[Flood Model] Training Inundation Depth Regressor...")
        self.depth_regressor.fit(X_trans, y_dpth)

        print("[Flood Model] Training Flood Risk Score Regressor...")
        self.score_regressor.fit(X_trans, y_scr)

        print("[Flood Model] Training Risk Category Classifier...")
        self.classifier.fit(X_trans, y_cat)

        self.is_fitted = True
        print("[Flood Model] Successfully fitted all flood models.")

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.is_fitted:
            raise RuntimeError("Flood model is not fitted yet.")

        df_feat = prepare_flood_features(df)
        X_trans = self.preprocessor.transform(df_feat)

        pred_depth = np.clip(self.depth_regressor.predict(X_trans), 0.0, 250.0).round(1)
        pred_score = np.clip(self.score_regressor.predict(X_trans), 0.0, 1.0).round(4)
        pred_cat = self.classifier.predict(X_trans)
        pred_probs = self.classifier.predict_proba(X_trans)
        classes = self.classifier.classes_

        results = df.copy()
        results["predicted_inundation_depth_cm"] = pred_depth
        results["predicted_flood_risk_score"] = pred_score
        results["predicted_risk_category"] = pred_cat

        for i, cls_name in enumerate(classes):
            results[f"prob_{str(cls_name).lower()}"] = pred_probs[:, i].round(3)

        return results

    def save(self, model_dir: str):
        os.makedirs(model_dir, exist_ok=True)
        artifact_path = os.path.join(model_dir, "mumbai_flood_model.joblib")
        payload = {
            "version": self.version,
            "city": self.city,
            "preprocessor": self.preprocessor,
            "depth_regressor": self.depth_regressor,
            "score_regressor": self.score_regressor,
            "classifier": self.classifier
        }
        joblib.dump(payload, artifact_path)
        print(f"[Flood Model] Saved model artifacts to {artifact_path}")

    @classmethod
    def load(cls, model_dir: str) -> "MumbaiFloodModel":
        artifact_path = os.path.join(model_dir, "mumbai_flood_model.joblib")
        if not os.path.exists(artifact_path):
            raise FileNotFoundError(f"Model file not found at {artifact_path}")
        payload = joblib.load(artifact_path)
        instance = cls()
        instance.version = payload.get("version", "2.0.0")
        instance.city = payload.get("city", "Mumbai")
        instance.preprocessor = payload["preprocessor"]
        instance.depth_regressor = payload["depth_regressor"]
        instance.score_regressor = payload["score_regressor"]
        instance.classifier = payload["classifier"]
        instance.is_fitted = True
        return instance
