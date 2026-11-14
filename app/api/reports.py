import os
import json
from fastapi import APIRouter
from app.core.config import settings
from app.services.model_service import model_service

router = APIRouter(prefix="", tags=["Review Reports"])

@router.get("/overview")
def get_dataset_overview():
    meta_path = os.path.join(settings.CLEANED_DIR, "feature_metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            return json.load(f)
    return {"status": "Metadata file not found."}

@router.get("/metrics/review2")
def get_review2_metrics():
    return {
        "phase": "Review II: Validation & Linear Baselines",
        "methodology": "Stratified 5-Fold Cross-Validation + Balanced Bootstrapping",
        "records": model_service.review2_summary
    }

@router.get("/metrics/review3")
def get_review3_metrics():
    return {
        "phase": "Review III: Advanced Models & PCA",
        "champion_model": "Random Forest Ensemble",
        "benchmark": model_service.review3_summary
    }

@router.get("/figures")
def get_output_figures():
    manifest_path = os.path.join(settings.FIGURES_DIR, "figures_metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            return {
                "total_figures": 10,
                "figures": json.load(f)
            }
    return {
        "total_figures": 0,
        "figures": [],
        "message": "Figures metadata not found. Run export_figures.py to capture images."
    }

