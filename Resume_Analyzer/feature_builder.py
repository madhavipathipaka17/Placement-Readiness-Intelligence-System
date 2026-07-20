import pandas as pd
import joblib


# Load feature names saved during training
feature_names = joblib.load("models/feature_names.pkl")


def build_feature_dataframe(llm_features):
    """
    Convert LLM JSON output into a DataFrame
    with the correct feature order.
    """

    # Create DataFrame
    df = pd.DataFrame([llm_features])

    # Reorder columns to match training
    df = df[feature_names]

    return df
