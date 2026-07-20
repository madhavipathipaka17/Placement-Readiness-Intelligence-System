import joblib


# Load the trained model
model = joblib.load("models/placement_readiness_model.pkl")

# Load the label encoder
label_encoder = joblib.load("models/readiness_label_encoder.pkl")


def predict_readiness(feature_df):
    """
    Predict placement readiness.

    Parameters
    ----------
    feature_df : pandas.DataFrame
        DataFrame containing the 11 input features.

    Returns
    -------
    dict
        Predicted class and probabilities.
    """

    # Predict class
    prediction = model.predict(feature_df)[0]

    # Convert numeric prediction back to label
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    # Predict probabilities
    probabilities = model.predict_proba(feature_df)[0]

    # Create probability dictionary
    probability_dict = {}

    for label, prob in zip(label_encoder.classes_, probabilities):
        probability_dict[label] = round(prob * 100, 2)

    return {
        "predicted_class": predicted_label,
        "probabilities": probability_dict
    }
