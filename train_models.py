import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset (Replace with correct dataset path if needed)
df = pd.read_csv("India Agriculture Crop Production.csv")

# Select only relevant columns
df = df.dropna(subset=["Crop", "Season", "Area", "Production", "Yield"])

# Encode categorical variables
label_encoders = {}
for column in ["Crop", "Season"]:
    le = LabelEncoder()
    
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Define Features (X) and Targets (y)
X = df[["Crop", "Season", "Area"]]
y_harvest = df["Yield"]  # Using Yield as a proxy for harvest time
y_roi = df["Production"]  # Using Production as a proxy for ROI

# Normalize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset for training & testing
X_train, X_test, y_train_harvest, y_test_harvest = train_test_split(X_scaled, y_harvest, test_size=0.2, random_state=42)
X_train, X_test, y_train_roi, y_test_roi = train_test_split(X_scaled, y_roi, test_size=0.2, random_state=42)

# Train RandomForest Models
rf_harvest = RandomForestRegressor(n_estimators=100, random_state=42)
rf_harvest.fit(X_train, y_train_harvest)

rf_roi = RandomForestRegressor(n_estimators=100, random_state=42)
rf_roi.fit(X_train, y_train_roi)

# Save models and preprocessing tools
joblib.dump(rf_harvest, "harvest_rf_model.pkl")
joblib.dump(rf_roi, "roi_rf_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Models trained and saved successfully!")
