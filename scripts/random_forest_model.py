"""
Project:
Multi-Omics Characterization of the Oral–Gut–Brain Axis in Parkinson's Disease

Description:
Machine learning pipeline for Parkinson's disease classification and microbial biomarker discovery using XGBoost.

Author: Praveen Kumar S
Year: 2026
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

from sklearn.ensemble import RandomForestClassifier

from imblearn.over_sampling import SMOTE

import matplotlib.pyplot as plt
import seaborn as sns

# ================================
# Load dataset
# ================================

df = pd.read_csv("ML_dataset_proper.csv")

df.columns = df.columns.str.strip()

label_column = "Group"

# ================================
# Add Biological Features
# ================================

# OES transformations
df["log_OES"] = np.log1p(df["OES"])

df["sqrt_OES"] = np.sqrt(df["OES"])

# Species richness
species_columns = df.drop(columns=[label_column]).columns

# Convert to numeric safely
df[species_columns] = df[species_columns].apply(
    pd.to_numeric,
    errors='coerce'
)

df[species_columns] = df[species_columns].fillna(0)

# Richness calculation
df["Richness"] = (
    df[species_columns] > 0
).sum(axis=1)

print("Added biological features:")

print(["log_OES", "sqrt_OES", "Richness"])

# ================================
# Prepare Features
# ================================

X = df.drop(columns=[label_column])

# Keep only numeric
X = X.apply(pd.to_numeric, errors='coerce')

X = X.fillna(0)

# Labels
le = LabelEncoder()

y = le.fit_transform(df[label_column])

# ================================
# Scale Features
# ================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ================================
# Apply SMOTE
# ================================

smote = SMOTE(random_state=42)

X_resampled, y_resampled = smote.fit_resample(
    X_scaled,
    y
)

print("\nAfter SMOTE class balance:")

print(pd.Series(y_resampled).value_counts())

# ================================
# Train/Test Split
# ================================

X_train, X_test, y_train, y_test = train_test_split(
    X_resampled,
    y_resampled,
    test_size=0.3,
    stratify=y_resampled,
    random_state=42
)

# ================================
# Hyperparameter Tuning
# ================================

param_grid = {

    'n_estimators': [200, 500],

    'max_depth': [10, 20, None],

    'min_samples_split': [2, 5],

    'min_samples_leaf': [1, 2],

    'max_features': ['sqrt']

}

grid = GridSearchCV(

    RandomForestClassifier(random_state=42),

    param_grid,

    cv=5,

    scoring='accuracy',

    n_jobs=-1

)

print("\nRunning GridSearchCV...")

grid.fit(X_train, y_train)

print("\nBest Parameters:")

print(grid.best_params_)

# Best model
model = grid.best_estimator_

# ================================
# Prediction
# ================================

y_pred = model.predict(X_test)

print("\nAccuracy:")

print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")

cm = confusion_matrix(y_test, y_pred)

print(cm)

# ================================
# Cross Validation
# ================================

cv_scores = cross_val_score(

    model,

    X_resampled,

    y_resampled,

    cv=5

)

print("\nCross-validation accuracy:")

print(cv_scores)

print("Mean CV accuracy:")

print(cv_scores.mean())

# ================================
# ROC Curve
# ================================

y_prob = model.predict_proba(X_test)[:,1]

fpr, tpr, _ = roc_curve(y_test, y_prob)

roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6,6))

plt.plot(fpr, tpr)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve (AUC = %0.2f)" % roc_auc)

plt.show()

# ================================
# Precision Recall Curve
# ================================

precision, recall, _ = precision_recall_curve(
    y_test,
    y_prob
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)

plt.figure(figsize=(6,6))

plt.plot(recall, precision)

plt.xlabel("Recall")

plt.ylabel("Precision")

plt.title(
    "Precision-Recall Curve (AUC = %0.2f)" % pr_auc
)

plt.show()

print("PR AUC:", pr_auc)

# ================================
# Feature Importance
# ================================

importance = model.feature_importances_

mapped_importance = list(
    zip(X.columns, importance)
)

mapped_importance = sorted(

    mapped_importance,

    key=lambda x: x[1],

    reverse=True

)

print("\nTop 20 Biomarkers:")

for item in mapped_importance[:20]:

    print(item)

# ================================
# Save Biomarkers
# ================================

df_biomarkers = pd.DataFrame(

    mapped_importance,

    columns=["Biomarker", "Importance"]

)

top20_df = df_biomarkers.head(20)

top20_df.to_csv(

    "RF_PD_Biomarkers_Top20.csv",

    index=False

)

print(top20_df)

# ================================
# Confusion Matrix Heatmap
# ================================

plt.figure(figsize=(6,5))

sns.heatmap(

    cm,

    annot=True,

    fmt="d",

    cmap="Blues"

)

plt.xlabel("Predicted")

plt.ylabel("Actual")

plt.title("Confusion Matrix")

plt.show()