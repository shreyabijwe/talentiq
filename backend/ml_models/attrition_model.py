import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, confusion_matrix,
                             classification_report)
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# ── Load Data ──────────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv('exports/employees.csv')
    return df

# ── Preprocess ─────────────────────────────────────────────────────────────────
def preprocess(df):
    df = df.copy()
    le = LabelEncoder()
    for col in ['nationality', 'department', 'job_title']:
        df[col] = le.fit_transform(df[col])
    df = df.drop(columns=['employee_id', 'name', 'join_date'])
    return df

# ── Train Model ────────────────────────────────────────────────────────────────
def train_model(df):
    X = df.drop(columns=['attrition'])
    y = df['attrition']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\n── Model Evaluation ──────────────────────────────")
    print(f"Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision : {precision_score(y_test, y_pred):.4f}")
    print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
    print(f"F1 Score  : {f1_score(y_test, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    return model, X_test, y_test, y_pred, X

# ── Confusion Matrix ───────────────────────────────────────────────────────────
def plot_confusion_matrix(y_test, y_pred):
    os.makedirs('exports/charts', exist_ok=True)
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Stayed', 'Left'],
                yticklabels=['Stayed', 'Left'])
    plt.title('Confusion Matrix — Attrition Prediction')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig('exports/charts/confusion_matrix.png', dpi=150)
    plt.close()
    print("Confusion matrix saved.")

# ── Feature Importance ─────────────────────────────────────────────────────────
def plot_feature_importance(model, X):
    importance = pd.Series(model.feature_importances_, index=X.columns)
    importance = importance.sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=importance.values, y=importance.index, palette='Blues_r')
    plt.title('Feature Importance — Attrition Prediction')
    plt.xlabel('Importance Score')
    plt.tight_layout()
    plt.savefig('exports/charts/feature_importance.png', dpi=150)
    plt.close()
    print("Feature importance chart saved.")
    print("\nTop Features:")
    print(importance.head(5))

# ── Save Model ─────────────────────────────────────────────────────────────────
def save_model(model):
    os.makedirs('backend/ml_models', exist_ok=True)
    joblib.dump(model, 'backend/ml_models/attrition_model.pkl')
    print("Model saved to backend/ml_models/attrition_model.pkl")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading data...")
    df = load_data()
    print(f"Dataset shape: {df.shape}")

    print("Preprocessing...")
    df_processed = preprocess(df)

    print("Training Random Forest model...")
    model, X_test, y_test, y_pred, X = train_model(df_processed)

    plot_confusion_matrix(y_test, y_pred)
    plot_feature_importance(model, X)
    save_model(model)

    print("\nPhase 3 complete.")