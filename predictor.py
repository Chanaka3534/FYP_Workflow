import numpy as np
import pandas as pd
from model_utils import load_models

# Helper function: convert water level to flood risk label
def get_flood_risk_label(level):
    """Return flood risk based on threshold"""
    return 'NEGATIVE' if level < 3000 else 'POSITIVE'

def predict_flood(input_data, model_lstm, model_xgb, scaler_X, scaler_y, le):
    """
    Predict flood risk (ensemble) and water level (LSTM)
    
    Parameters:
        input_data: list of 5 feature values
                    [Catchment Rainfall, Downstream rainfall, Reservoir water level,
                     Discharge rate, Kaliodai water level]
        model_lstm: trained LSTM model
        model_xgb: trained XGBoost model
        scaler_X: scaler for LSTM features
        scaler_y: scaler for LSTM target
        le: label encoder for flood risk

    Returns:
        dict: {
            'predicted_water_level': float,
            'lstm_risk': str,
            'xgb_risk': str,
            'final_ensemble_risk': str
        }
    """
    features = ["Catchment Rainfall", "Downstream rainfall", "Resovior water level(m)",
                "Resovior discharge rate", "Water level(Kaliodai)"]

    # Convert input to DataFrame
    input_df = pd.DataFrame([input_data], columns=features)

    # =======================
    # 🔹 LSTM Prediction
    # =======================
    X_scaled = scaler_X.transform(input_df)               # scale features for LSTM
    X_lstm_input = X_scaled.reshape(1, 1, len(features))  # LSTM expects 3D input
    y_pred_scaled = model_lstm.predict(X_lstm_input)
    predicted_water_level = scaler_y.inverse_transform(y_pred_scaled)[0][0]
    lstm_risk = get_flood_risk_label(predicted_water_level)

    # =======================
    # 🔹 XGBoost Prediction
    # =======================
    X_xgb_input = input_df.values  # use raw input (not scaled)
    xgb_label_encoded = model_xgb.predict(X_xgb_input)
    xgb_risk = le.inverse_transform(xgb_label_encoded)[0]

    # =======================
    # 🔹 Ensemble (safety-first)
    # =======================
    final_ensemble_risk = lstm_risk if lstm_risk == xgb_risk else 'POSITIVE'

    return {
        'predicted_water_level': round(predicted_water_level, 2),
        'lstm_risk': lstm_risk,
        'xgb_risk': xgb_risk,
        'final_ensemble_risk': final_ensemble_risk
    }
