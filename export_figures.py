"""
Pyanm Figure Export & Capture Utility
Extracts and generates all high-resolution output figures from Review I-III notebooks.
"""

import os
import json
import base64
from PIL import Image
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(BASE_DIR, "output_figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

FIGURE_SPECIFICATIONS = [
    {
        "id": "eda_01",
        "filename": "eda_01_label_and_attack_distribution.png",
        "notebook": "EDA.ipynb",
        "cell_index": 7,
        "phase": "Review I: Data Engineering & Preprocessing",
        "title": "Binary Label & Attack Category Distribution",
        "description": "Dual-panel distribution: Benign vs Malicious flow counts, followed by frequency breakdown across 9 granular attack categories (Generic, Exploits, Fuzzers, DoS, Reconnaissance, etc.)."
    },
    {
        "id": "eda_02",
        "filename": "eda_02_skewed_features_log1p_transformation.png",
        "notebook": "EDA.ipynb",
        "cell_index": 11,
        "phase": "Review I: Data Engineering & Preprocessing",
        "title": "Log1p Transformation on Heavy-Tailed Network Features",
        "description": "Histograms of critical packet and byte predictors (sbytes, dbytes, spkts, rate) showing skew reduction and variance stabilization via log1p transformation."
    },
    {
        "id": "eda_03",
        "filename": "eda_03_feature_correlation_matrix.png",
        "notebook": "EDA.ipynb",
        "cell_index": 13,
        "phase": "Review I: Data Engineering & Preprocessing",
        "title": "Pearson Correlation Matrix of Core Predictors",
        "description": "Heatmap of 18 key traffic features displaying pairwise Pearson correlation coefficients, identifying multi-collinearity and strong linear indicators for bot classification."
    },
    {
        "id": "val_01",
        "filename": "val_01_linear_regression_actual_vs_predicted.png",
        "notebook": "Model_Validation.ipynb",
        "cell_index": 8,
        "phase": "Review II: Validation Schemes & Linear Baselines",
        "title": "Multiple Linear Regression: Actual vs Predicted Rate & Residuals",
        "description": "Dual-panel regression diagnostics: Actual vs predicted transmission rate (log scale) along with residual scatter plot verifying error homoscedasticity."
    },
    {
        "id": "val_02",
        "filename": "val_02_logistic_regression_cm_and_roc.png",
        "notebook": "Model_Validation.ipynb",
        "cell_index": 12,
        "phase": "Review II: Validation Schemes & Linear Baselines",
        "title": "Logistic Regression: Confusion Matrix & ROC Curve",
        "description": "Holdout test performance of baseline classifier: Annotated 2x2 confusion matrix (TN, FP, FN, TP) alongside ROC curve achieving ROC-AUC of 0.9770."
    },
    {
        "id": "val_03",
        "filename": "val_03_logistic_regression_coefficients.png",
        "notebook": "Model_Validation.ipynb",
        "cell_index": 14,
        "phase": "Review II: Validation Schemes & Linear Baselines",
        "title": "Logistic Regression Feature Coefficients (Log-Odds Impact)",
        "description": "Horizontal bar chart visualizing the top positive (bot indicator) and negative (benign indicator) learned regression weights across network flow features."
    },
    {
        "id": "dr_01",
        "filename": "dr_01_pca_scree_and_2d_projection.png",
        "notebook": "Dimentionality_Reduction.ipynb",
        "cell_index": 5,
        "phase": "Review III: Advanced Architectures & Dimensionality Reduction",
        "title": "PCA Scree Plot & 2D Projection Space",
        "description": "Principal Component Analysis across 15 components with cumulative variance curve reaching 90% threshold, paired with 2D scatter projection separating normal and bot traffic."
    },
    {
        "id": "dr_02",
        "filename": "dr_02_kmeans_elbow_and_silhouette.png",
        "notebook": "Dimentionality_Reduction.ipynb",
        "cell_index": 7,
        "phase": "Review III: Advanced Architectures & Dimensionality Reduction",
        "title": "Unsupervised K-Means: Inertia Elbow & Silhouette Scores",
        "description": "Clustering validation across K=2 to 7 comparing within-cluster sum of squares (inertia) with mean silhouette coefficients, confirming optimal cluster structure at K=3."
    },
    {
        "id": "dr_03",
        "filename": "dr_03_decision_tree_architecture.png",
        "notebook": "Dimentionality_Reduction.ipynb",
        "cell_index": 9,
        "phase": "Review III: Advanced Architectures & Dimensionality Reduction",
        "title": "Decision Tree Architecture (First 3 Split Levels - Gini Criterion)",
        "description": "Interpretable hierarchical tree structure displaying root decision thresholds, Gini impurity values, sample sizes, and class balance across initial splits."
    },
    {
        "id": "dr_04",
        "filename": "dr_04_random_forest_importance_and_cm.png",
        "notebook": "Dimentionality_Reduction.ipynb",
        "cell_index": 11,
        "phase": "Review III: Advanced Architectures & Dimensionality Reduction",
        "title": "Random Forest Champion: Feature Importance & Confusion Matrix",
        "description": "Top 12 features ranked by Gini importance (mean decrease in impurity) alongside holdout confusion matrix demonstrating 94.39% accuracy and 0.9907 ROC-AUC."
    }
]

def export_all_figures():
    """Extract and write all figures from notebook JSON outputs to disk."""
    print("=" * 70)
    print("Pyanm: Exporting Output Figures from Notebook Workflows")
    print("=" * 70)

    notebook_cache = {}
    manifest = []

    for spec in FIGURE_SPECIFICATIONS:
        nb_filename = spec["notebook"]
        if nb_filename not in notebook_cache:
            nb_path = os.path.join(BASE_DIR, nb_filename)
            if not os.path.exists(nb_path):
                print(f"[ERROR] Notebook not found: {nb_path}")
                continue
            with open(nb_path, "r", encoding="utf-8") as f:
                notebook_cache[nb_filename] = json.load(f)

        nb = notebook_cache[nb_filename]
        cell_idx = spec["cell_index"]
        
        if cell_idx >= len(nb["cells"]):
            print(f"[ERROR] Cell index {cell_idx} out of range in {nb_filename}")
            continue

        cell = nb["cells"][cell_idx]
        image_found = False

        for output in cell.get("outputs", []):
            data = output.get("data", {})
            if "image/png" in data:
                raw_b64 = data["image/png"]
                if isinstance(raw_b64, list):
                    raw_b64 = "".join(raw_b64)
                
                img_bytes = base64.b64decode(raw_b64.strip())
                dest_path = os.path.join(FIGURES_DIR, spec["filename"])
                
                with open(dest_path, "wb") as out_f:
                    out_f.write(img_bytes)

                # Open with PIL for metadata validation
                img = Image.open(io.BytesIO(img_bytes))
                width, height = img.size
                file_size_kb = round(len(img_bytes) / 1024, 1)

                manifest.append({
                    **spec,
                    "width": width,
                    "height": height,
                    "file_size_kb": file_size_kb,
                    "relative_path": f"output_figures/{spec['filename']}",
                    "api_url": f"/output_figures/{spec['filename']}"
                })

                print(f" [OK] Captured: {spec['filename']} ({width}x{height}, {file_size_kb} KB)")
                image_found = True
                break

        if not image_found:
            print(f" [WARN] No image found in {nb_filename} (Cell {cell_idx})")

    # Write metadata manifest
    manifest_path = os.path.join(FIGURES_DIR, "figures_metadata.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("=" * 70)
    print(f"Export Complete: {len(manifest)}/{len(FIGURE_SPECIFICATIONS)} figures captured.")
    print(f"Metadata manifest saved to: {manifest_path}")
    print("=" * 70)
    return manifest

if __name__ == "__main__":
    export_all_figures()
