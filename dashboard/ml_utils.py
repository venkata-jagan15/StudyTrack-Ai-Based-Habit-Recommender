
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Path to the dataset
# Adjust this path as needed. Assuming we are running from 'milestone 3/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, '..', 'milestone 2', 'studytrack_dataset.csv')

_lr_model = None
_kmeans_model = None
_scaler = None
_feature_names = None

def load_and_train_models():
    global _lr_model, _kmeans_model, _scaler, _feature_names
    
    if not os.path.exists(CSV_PATH):
        print(f"Dataset not found at {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    # CLEANUP: Strip whitespace from column names to handle " Study_Hours" issue
    df.columns = df.columns.str.strip()

    # FIX: "Test_Score" is missing in older datasets, but "Attendance_Percentage" has the score values.
    # Map Attendance_Percentage -> Test_Score if needed
    if "Test_Score" not in df.columns and "Attendance_Percentage" in df.columns:
        print("Note: 'Test_Score' column missing. Using 'Attendance_Percentage' as 'Test_Score'.")
        df.rename(columns={"Attendance_Percentage": "Test_Score"}, inplace=True)
    
    # --- Train Linear Regression (Prediction) ---
    X = df[["Study_Hours", "Sleep_Hours", "Assignments_Completed"]]
    y = df["Test_Score"]
    
    # We use all data for better training in this persistent model
    _lr_model = LinearRegression()
    _lr_model.fit(X, y)
    
    # --- Train K-Means (Clustering) ---
    # Dropping Student_ID as in original code
    data_for_clustering = df.drop(columns=['Student_ID'])
    _feature_names = data_for_clustering.columns.tolist()
    
    _scaler = StandardScaler()
    scaled_data = _scaler.fit_transform(data_for_clustering)
    
    # Using k=3 as decided in milestone 2
    _kmeans_model = KMeans(n_clusters=3, random_state=42)
    _kmeans_model.fit(scaled_data)
    
    # Force cluster labelling consistency is tricky without labeled data, 
    # but for now we trust the model's structural consistency.
    
    print("ML Models trained successfully.")

def predict_score(study_hours, sleep_hours, assignments):
    """
    Predicts the test score based on inputs.
    """
    if _lr_model is None:
        load_and_train_models()
    
    if _lr_model is None:
        return 0.0
        
    input_data = pd.DataFrame(
        [[study_hours, sleep_hours, assignments]], 
        columns=["Study_Hours", "Sleep_Hours", "Assignments_Completed"]
    )
    predicted = _lr_model.predict(input_data)
    return max(0, min(100, predicted[0])) # Clamp between 0 and 100

def get_recommendation(study_hours, sleep_hours, assignments, current_score):
    """
    Determines cluster and returns recommendation.
    """
    cluster = predict_cluster(study_hours, sleep_hours, assignments, current_score)

    if cluster == "Unable to generate recommendation.":
        return cluster

    # Using the logic from milestone 2
    if cluster == 0:
        return "Increase study hours, reduce social media time."
    elif cluster == 1:
        return "Good balance, keep maintaining study & sleep."
    elif cluster == 2:
        return "Focus on sleep and assignment completion for better scores."
    else:
        return "General improvement needed."

def predict_cluster(study_hours, sleep_hours, assignments, current_score):
    """
    Returns the cluster ID for the student.
    """
    if _kmeans_model is None:
        load_and_train_models()
        
    if _kmeans_model is None:
        return "Unable to generate recommendation."

    input_dict = {
        "Study_Hours": study_hours,
        "Sleep_Hours": sleep_hours,
        "Assignments_Completed": assignments,
        "Test_Score": current_score
    }
    
    if _feature_names:
        row_data = [input_dict.get(col, 0) for col in _feature_names]
        row = pd.DataFrame([row_data], columns=_feature_names)
    else:
        row = pd.DataFrame([input_dict])
    
    scaled_input = _scaler.transform(row)
    cluster = _kmeans_model.predict(scaled_input)[0]
    return int(cluster)

# Initial load
try:
    load_and_train_models()
except Exception as e:
    print(f"Error loading models: {e}")
