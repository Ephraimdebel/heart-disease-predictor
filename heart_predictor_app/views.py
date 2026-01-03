from django.shortcuts import render
import joblib
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and selected features
MODEL_PATH = os.path.join(BASE_DIR, "ml/decision_tree_heart_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "ml/selected_features.pkl")

model = joblib.load(MODEL_PATH)
selected_features = joblib.load(FEATURES_PATH)

def predict_view(request):
    prediction = None
    feature_inputs = selected_features  # For dynamic form rendering

    if request.method == "POST":
        # Gather user inputs in the same order as selected_features
        features = [float(request.POST[f.replace(" ", "_")]) for f in selected_features]

        # Create DataFrame with correct column names
        X = pd.DataFrame([features], columns=selected_features)

        # Predict
        result = model.predict(X)[0]
        prediction = "Heart Disease Risk" if result == 1 else "No Heart Disease"

    return render(request, "heart_predictor_app/index.html", {
        "prediction": prediction,
        "feature_inputs": feature_inputs
    })
