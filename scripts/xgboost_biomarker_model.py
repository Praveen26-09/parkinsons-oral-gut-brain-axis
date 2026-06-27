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

from xgboost import XGBClassifier

from imblearn.over_sampling import SMOTE

# ================================
# Load dataset
# ================================

df = pd.read_csv("ML_dataset_proper.csv")

df.columns = df.columns.str.strip()

label_column = "Group"

# ================================
# ⭐ Method 6 — Add Biological Features
# ================================

# OES transformations
df["log_OES"] = np.log1p(df["OES"])
df["sqrt_OES"] = np.sqrt(df["OES"])




# Species richness (number of detected species)
species_columns = df.drop(columns=[label_column]).columns
df["Richness"] = (df[species_columns] > 0).sum(axis=1)

print("Added biological features:")
print(["log_OES", "sqrt_OES", "Richness"])

# ================================
# Prepare Features
# ================================

X = df.drop(columns=[label_column])

# Encode labels
le = LabelEncoder()
y = df[label_column]   
y = le.fit_transform(y)

# Scale features
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
# ⭐ Method 4 — Hyperparameter Tuning
# ================================

param_grid = {

    'max_depth': [6,8,10],

    'learning_rate': [0.01,0.02],

    'n_estimators': [800,1000],

    'subsample': [0.8,0.9],

    'colsample_bytree': [0.8,0.9]

}

grid = GridSearchCV(

    XGBClassifier(),

    param_grid,

    cv=5,

    scoring='accuracy',

    n_jobs=-1

)

print("\nRunning GridSearchCV...")

grid.fit(X_train, y_train)

print("\nBest Parameters:")

print(grid.best_params_)

# Use best model
model = grid.best_estimator_

# ================================
# Prediction
# ================================

y_pred = model.predict(X_test)

print("\nAccuracy:")

print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")

print(confusion_matrix(y_test, y_pred))

# ================================
# ⭐ Method 5 — Cross Validation
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
# Feature Importance Mapping
# ================================

importance = model.get_booster().get_score(

    importance_type='gain'

)

feature_names = X.columns

mapped_importance = []

for k, v in importance.items():

    index = int(k[1:])

    species_name = feature_names[index]

    mapped_importance.append((species_name, v))

mapped_importance = sorted(

    mapped_importance,

    key=lambda x: x[1],

    reverse=True

)

print("\nTop 20 Biomarkers:")

for item in mapped_importance[:20]:

    print(item)



from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt

y_prob = model.predict_proba(X_test)[:,1]

fpr, tpr, _ = roc_curve(y_test, y_prob)

roc_auc = auc(fpr, tpr)

plt.plot(fpr, tpr)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve (AUC = %0.2f)" % roc_auc)

plt.show()














######################


####precision and recall 
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt

# Get prediction probabilities
y_prob = model.predict_proba(X_test)[:,1]

# Compute precision-recall
precision, recall, _ = precision_recall_curve(
    y_test,
    y_prob
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)

# Plot PR Curve
plt.plot(recall, precision)

plt.xlabel("Recall")
plt.ylabel("Precision")

plt.title(
    "Precision-Recall Curve (AUC = %0.2f)" % pr_auc
)

plt.show()

print("PR AUC:", pr_auc)





################
### Biomarker Table

import pandas as pd

# Convert importance list to dataframe
df_biomarkers = pd.DataFrame(
    mapped_importance,
    columns=["Biomarker", "Importance"]
)

# Select top 20
top20_df = df_biomarkers.head(20)

# Save file
top20_df.to_csv(
    "Final_PD_Biomarkers_Top20.csv",
    index=False
)

print(top20_df)

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

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





