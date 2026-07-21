# predictor.py

import joblib
import pandas as pd

# Load trained model
model = joblib.load("models/placement_readiness_model.pkl")

# Load label encoder
label_encoder = joblib.load("models/readiness_label_encoder.pkl")


def predict_readiness(feature_df):
    """
    Predict placement readiness using the trained Random Forest model.

    Parameters
    ----------
    feature_df : pandas.DataFrame
        DataFrame containing the 11 ML features.

    Returns
    -------
    prediction : str
        Predicted placement readiness category.

    confidence : dict
        Confidence (%) for every class.
    """

    # Ensure input is DataFrame
    if not isinstance(feature_df, pd.DataFrame):
        feature_df = pd.DataFrame([feature_df])

    # Predict class index
    prediction_index = model.predict(feature_df)[0]

    # Convert numeric label to class name
    prediction = label_encoder.inverse_transform([prediction_index])[0]

    # Predict probabilities
    probs = model.predict_proba(feature_df)[0]

    # Confidence dictionary
    confidence = {
        label: round(prob * 100, 2)
        for label, prob in zip(label_encoder.classes_, probs)
    }

    return prediction, confidence