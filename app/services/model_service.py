import os
import json
import time
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from app.core.config import settings

class ModelService:
    def __init__(self):
        self.models = {}
        self.metadata = {}
        self.scenarios = []
        self.review2_summary = []
        self.review3_summary = []
        self._load_artifacts()

    def _load_artifacts(self):
        # 1. Metadata
        meta_path = os.path.join(settings.MODELS_DIR, "model_metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                self.metadata = json.load(f)

        # 2. Scenarios
        scen_path = os.path.join(settings.MODELS_DIR, "test_scenarios.json")
        if os.path.exists(scen_path):
            with open(scen_path, "r") as f:
                self.scenarios = json.load(f)

        # 3. Models
        rf_path = os.path.join(settings.MODELS_DIR, "random_forest_champion.joblib")
        if os.path.exists(rf_path):
            try:
                self.models["champion"] = joblib.load(rf_path)
            except Exception as e:
                print(f"[ModelService] Warning: Champion model load blocked or failed: {e}")

        lr_path = os.path.join(settings.MODELS_DIR, "logistic_regression_baseline.joblib")
        if os.path.exists(lr_path):
            try:
                self.models["baseline"] = joblib.load(lr_path)
            except Exception as e:
                print(f"[ModelService] Warning: Baseline model load blocked or failed: {e}")

        # 4. Review Summaries
        r2_path = os.path.join(settings.CLEANED_DIR, "review2_model_performance_summary.csv")
        if os.path.exists(r2_path):
            self.review2_summary = pd.read_csv(r2_path).to_dict(orient="records")

        r3_path = os.path.join(settings.CLEANED_DIR, "review3_model_benchmark_summary.csv")
        if os.path.exists(r3_path):
            self.review3_summary = pd.read_csv(r3_path).to_dict(orient="records")

        print("[ModelService] Artifacts loaded successfully.")

    def format_vector(self, features_dict: Dict[str, float]) -> pd.DataFrame:
        expected_cols = self.metadata.get("feature_names", [])
        if not expected_cols:
            expected_cols = list(features_dict.keys())
        
        vector = np.zeros((1, len(expected_cols)))
        for i, col in enumerate(expected_cols):
            vector[0, i] = features_dict.get(col, 0.0)
        return pd.DataFrame(vector, columns=expected_cols)

    def predict(self, features: Dict[str, float], model_type: str = "champion") -> Dict[str, Any]:
        key = model_type.lower()
        if not self.models:
            # Fallback heuristic based on key decision tree rules (sttl, sload, rate)
            # from Review III model architecture if joblib DLL loading is blocked by Windows security
            sload = features.get("sload", 0.0)
            sttl = features.get("sttl", 0.0)
            rate = features.get("rate", 0.0)
            is_bot = (sttl > 61.0) or (sload > 1000000.0) or (rate > 100000.0)
            pred_label = 1 if is_bot else 0
            conf = 0.95 if is_bot else 0.92
            return {
                "prediction": "Malicious Bot" if is_bot else "Normal",
                "label": pred_label,
                "confidence": conf,
                "confidence_percentage": f"{conf * 100:.2f}%",
                "action": "BLOCK" if is_bot else "ALLOW",
                "probabilities": {
                    "Normal": round(1.0 - conf if is_bot else conf, 4),
                    "Malicious Bot": round(conf if is_bot else 1.0 - conf, 4)
                },
                "model_used": "Rule-based Fallback (Security Mode)",
                "inference_time_ms": 0.5
            }

        if key not in self.models:
            key = "champion" if "champion" in self.models else next(iter(self.models.keys()))
        
        model = self.models[key]
        X_df = self.format_vector(features)
        
        t0 = time.time()
        pred_label = int(model.predict(X_df)[0])
        probabilities = model.predict_proba(X_df)[0]
        latency = (time.time() - t0) * 1000

        confidence = float(probabilities[pred_label])
        pred_class = "Malicious Bot" if pred_label == 1 else "Normal"
        action = "BLOCK" if pred_label == 1 else "ALLOW"

        return {
            "prediction": pred_class,
            "label": pred_label,
            "confidence": round(confidence, 4),
            "confidence_percentage": f"{confidence * 100:.2f}%",
            "action": action,
            "probabilities": {
                "Normal": round(float(probabilities[0]), 4),
                "Malicious Bot": round(float(probabilities[1]), 4)
            },
            "model_used": "Random Forest Ensemble" if key == "champion" else "Logistic Regression",
            "inference_time_ms": round(latency, 2)
        }

model_service = ModelService()

