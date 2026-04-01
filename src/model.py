# =============================
# Imports
# =============================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

import warnings
warnings.filterwarnings('ignore')

import joblib


# =============================
# Load Data
# =============================
DATA_PATH = '../data/malicious_urls_prepared_supplement.csv'

df = pd.read_csv(DATA_PATH)


# =============================
# Train/Test Split
# =============================
RANDOM_SEED = 42
TEST_SIZE = 0.2

X = df.drop(columns=['type', 'type_encoded'])
y = df['type_encoded']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_SEED,
    stratify=y
)


# =============================
# Train Models
# =============================
trained_models = {}

# Logistic Regression
model_1 = LogisticRegression(random_state=RANDOM_SEED, max_iter=1000)
model_1.fit(X_train, y_train)
trained_models['Logistic Regression'] = model_1

# Random Forest
model_2 = RandomForestClassifier(random_state=RANDOM_SEED, n_estimators=100)
model_2.fit(X_train, y_train)
trained_models['Random Forest'] = model_2

# Gradient Boosting
model_3 = GradientBoostingClassifier(random_state=RANDOM_SEED)
model_3.fit(X_train, y_train)
trained_models['Gradient Boosting'] = model_3

# SVM
model_4 = SVC(random_state=RANDOM_SEED)
model_4.fit(X_train, y_train)
trained_models['SVM'] = model_4


# =============================
# Hyperparameter Tuning (Random Forest)
# =============================
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=RANDOM_SEED),
    param_grid=param_grid,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1
)

grid_search.fit(X_train, y_train)

trained_models['Random Forest (Tuned)'] = grid_search.best_estimator_


# =============================
# Evaluate Models
# =============================
results = []

for name, model in trained_models.items():
    y_pred = model.predict(X_test)

    results.append({
        'Model': name,
        'Accuracy': accuracy_score(y_test, y_pred),
        'Precision': precision_score(y_test, y_pred, average='weighted'),
        'Recall': recall_score(y_test, y_pred, average='weighted'),
        'F1-Score': f1_score(y_test, y_pred, average='weighted')
    })

results_df = pd.DataFrame(results).set_index('Model').sort_values(by='F1-Score', ascending=False)

print("\n=== Model Comparison ===")
print(results_df.round(4))


# =============================
# Best Model Evaluation
# =============================
best_model_name = results_df['F1-Score'].idxmax()
best_model = trained_models[best_model_name]

y_pred_best = best_model.predict(X_test)

print(f"\n=== Best Model: {best_model_name} ===\n")
print(classification_report(y_test, y_pred_best))

# =============================
# Save Model
# =============================
MODEL_PATH = '../models/best_model.joblib'

joblib.dump(best_model, MODEL_PATH)

print(f"Model saved to {MODEL_PATH}")

# =============================
# Confusion Matrix
# =============================
cm = confusion_matrix(y_test, y_pred_best)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title(f'Confusion Matrix — {best_model_name}')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.show()


# =============================
# Cross Validation
# =============================
cv_scores = cross_val_score(
    best_model,
    X,
    y,
    cv=5,
    scoring='f1_weighted'
)

print("\n=== Cross-Validation ===")
print(f"F1 Scores: {cv_scores.round(4)}")
print(f"Mean: {cv_scores.mean():.4f}")
print(f"Std:  {cv_scores.std():.4f}")