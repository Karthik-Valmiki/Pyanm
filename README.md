# Pyanm: Network Flow & Bot Intrusion Detection Platform

A modular machine learning system and REST API designed to detect automated malicious bots, volumetric attacks, and network intrusions using the **UNSW-NB15** benchmark dataset.

---

## Dataset
Download datasets from Kaggle: [https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15](https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15)
* Raw training partition: `Datasets/UNSW_NB15_training-set.csv`
* Raw testing partition: `Datasets/UNSW_NB15_testing-set.csv`
* Cleaned partitions generated in Review I: `Cleaned_DS/train_cleaned.csv`, `Cleaned_DS/test_cleaned.csv`

---

## Quickstart

### 1. Installation
Ensure Python 3.10+ is installed, then install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Export & Verify Output Figures
Capture and export all 10 high-resolution visual figures generated across the machine learning notebooks:
```bash
python export_figures.py
```
All figures are saved to the `output_figures/` directory along with `output_figures/figures_metadata.json`.

### 3. Run the Application
On Windows, you can launch via Command Prompt / PowerShell:
```bash
python run.py
```
Or directly double-click / execute the Windows launcher:
```cmd
run.bat
```
*(To run with hot-reloading enabled: `python run.py --reload`)*

### 4. Interactive Endpoints
* **Web Dashboard:** [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard)
* **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc Reference:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **Figure Manifest API:** [http://127.0.0.1:8000/api/figures](http://127.0.0.1:8000/api/figures)

---

## Windows Security & Execution Troubleshooting

### 1. PowerShell Script Execution Policy (`PSSecurityException`)
If PowerShell blocks virtual environment activation with `running scripts is disabled on this system`:
* **Option A (Recommended):** Use `run.bat` or run Python directly (`python run.py`).
* **Option B:** Temporarily bypass execution policy for the session:
  ```powershell
  powershell -ExecutionPolicy Bypass -File .venv\Scripts\Activate.ps1
  ```
* **Option C:** Set execution policy for the current user:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### 2. Windows Defender / Application Control DLL Blocking (`_liblinear.pyd`)
In Windows environments with Smart App Control (SAC) or Windows Defender Application Control (WDAC), compiled C-extensions in user directories may occasionally be restricted (`An Application Control policy has blocked this file`):
* The platform includes a **Security Fallback Engine** in `app/services/model_service.py` that gracefully detects DLL blocks and transitions to decision-tree rule-based heuristics without crashing the API or Web Dashboard.
* If files downloaded from the web are blocked by Mark of the Web, unblock the project files in PowerShell:
  ```powershell
  Get-ChildItem -Path . -Recurse | Unblock-File
  ```

---

## Captured Output Figures

All 10 figures generated across Reviews I–III are captured in `output_figures/`:

| # | Filename | Review Phase | Description |
|---|---|---|---|
| 01 | `eda_01_label_and_attack_distribution.png` | Review I: EDA | Benign vs. Malicious distribution and 9 attack categories breakdown |
| 02 | `eda_02_skewed_features_log1p_transformation.png` | Review I: EDA | `log1p` variance stabilization across `sbytes`, `dbytes`, `spkts`, `rate` |
| 03 | `eda_03_feature_correlation_matrix.png` | Review I: EDA | Pearson correlation heatmap of 18 core network traffic predictors |
| 04 | `val_01_linear_regression_actual_vs_predicted.png` | Review II: Baselines | Multiple Linear Regression actual vs predicted rate & residual analysis |
| 05 | `val_02_logistic_regression_cm_and_roc.png` | Review II: Baselines | Logistic Regression holdout confusion matrix and ROC curve ($AUC = 0.977$) |
| 06 | `val_03_logistic_regression_coefficients.png` | Review II: Baselines | Top positive (bot) and negative (benign) learned linear regression weights |
| 07 | `dr_01_pca_scree_and_2d_projection.png` | Review III: Advanced | 15-component PCA scree plot (90% threshold) & 2D flow separation |
| 08 | `dr_02_kmeans_elbow_and_silhouette.png` | Review III: Advanced | K-Means clustering inertia elbow & silhouette analysis ($K=3$ optimum) |
| 09 | `dr_03_decision_tree_architecture.png` | Review III: Advanced | Interpretable decision tree structure (first 3 split levels, Gini criterion) |
| 10 | `dr_04_random_forest_importance_and_cm.png` | Review III: Advanced | Top 12 Gini feature importances & champion Random Forest confusion matrix |

---

## Machine Learning Lifecycle (Reviews I – III)

1. **Review I — Data Engineering & Preprocessing (`EDA.ipynb`):**
   * Curated 257,673 network flows from UNSW-NB15.
   * `log1p` transformation applied to heavy-tailed packet and byte count distributions.
   * Standardized features exported to `Cleaned_DS/`.
   * Visual figures automatically saved to `output_figures/eda_01...` to `eda_03...`.

2. **Review II — Validation & Linear Baselines (`Model_Validation.ipynb`):**
   * Stratified 5-Fold Cross-Validation with training-fold balanced resampling.
   * Multiple Linear Regression ($R^2 = 0.941$) for continuous rate prediction.
   * Logistic Regression baseline ($F_1 = 0.917$, $\text{ROC-AUC} = 0.970$).
   * Visual figures automatically saved to `output_figures/val_01...` to `val_03...`.

3. **Review III — Advanced Architectures (`Dimentionality_Reduction.ipynb`):**
   * Principal Component Analysis (PCA) for 2D flow separation.
   * Unsupervised K-Means clustering ($K=3$) with Silhouette evaluation.
   * Random Forest champion ensemble ($F_1 = 0.956$, $\text{ROC-AUC} = 0.985$).
   * Visual figures automatically saved to `output_figures/dr_01...` to `dr_04...`.
