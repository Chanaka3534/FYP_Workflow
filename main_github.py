import os
from datetime import datetime

from get_thingsboard_data import get_thingsboard_data
from sheet_data import get_sheet_data
from catchment_rainfall import get_catchment_rainfall
from preprocess import prepare_input
from model_utils import load_models
from predictor import predict_flood
from sender import send_to_thingsboard_demo as send_to_thingsboard
from save_daily_data_csv import save_daily_data_csv

def main():
    try:
        print(f"🚀 Starting Flood Prediction at {datetime.now()}")
        
        # =========================
        # Config - FROM ENVIRONMENT VARIABLES (SECURE)
        # =========================
        USERNAME = os.getenv('THINGSBOARD_USERNAME')
        PASSWORD = os.getenv('THINGSBOARD_PASSWORD')
        DEVICE_ID = os.getenv('THINGSBOARD_DEVICE_ID')
        CSV_URL = os.getenv('SHEET_URL')
        DEVICE_TOKEN = os.getenv('THINGSBOARD_TOKEN')
        
        # Check if all environment variables are set
        if not all([USERNAME, PASSWORD, DEVICE_ID, CSV_URL, DEVICE_TOKEN]):
            missing = []
            if not USERNAME: missing.append('THINGSBOARD_USERNAME')
            if not PASSWORD: missing.append('THINGSBOARD_PASSWORD')
            if not DEVICE_ID: missing.append('THINGSBOARD_DEVICE_ID')
            if not CSV_URL: missing.append('SHEET_URL')
            if not DEVICE_TOKEN: missing.append('THINGSBOARD_TOKEN')
            
            print(f"❌ Missing environment variables: {', '.join(missing)}")
            print("💡 Please set these as GitHub Secrets in your repository settings")
            return False

        print("✅ All environment variables loaded successfully")

        # =========================
        # Load Models
        # =========================
        print("📦 Loading AI models...")
        model_lstm, model_xgb, scaler_X, scaler_y, le = load_models()

        # Step 1: Get ThingsBoard data
        print("📡 Getting ThingsBoard data...")
        rainfall, waterlevel_m = get_thingsboard_data(USERNAME, PASSWORD, DEVICE_ID)
        waterlevel = waterlevel_m * 1000  # Convert to mm
        print(f"Rainfall: {rainfall}, Waterlevel: {waterlevel}")

        # Step 2: Get Google Sheet data
        print("📊 Getting Google Sheet data...")
        water_depth, spilling_cusec = get_sheet_data(CSV_URL)
        print(f"Water Depth: {water_depth}, Spilling Cusec: {spilling_cusec}")

        # Step 3: Get catchment rainfall
        print("🌧️ Getting catchment rainfall...")
        lat, lon = 7.158947456029211, 81.22391608291566
        _, catchment_rainfall = get_catchment_rainfall(lat, lon)
        print(f"Catchment Rainfall: {catchment_rainfall}")

        # Step 4: Prepare input
        input_data = [catchment_rainfall, rainfall, water_depth, spilling_cusec, waterlevel]
        print(f"Input Data: {input_data}")

        # Step 5: Predict
        print("🤖 Making predictions...")
        prediction = predict_flood(input_data, model_lstm, model_xgb, scaler_X, scaler_y, le)
        print("✅ Prediction Results:")
        print(f"LSTM Water Level: {prediction['predicted_water_level']} mm")
        print(f"LSTM Risk: {prediction['lstm_risk']}, XGBoost Risk: {prediction['xgb_risk']}")
        print(f"Final Ensemble Risk: {prediction['final_ensemble_risk']}")

        # Step 6: Send to ThingsBoard
        print("📤 Sending to ThingsBoard...")
        status = send_to_thingsboard(
            DEVICE_TOKEN,
            datetime.now().strftime("%Y-%m-%d"),
            water_depth,
            spilling_cusec,
            catchment_rainfall,
            prediction['predicted_water_level'],
            prediction['final_ensemble_risk']
        )
        print(f"ThingsBoard HTTP Status: {status}")

        # Step 7: Save to CSV
        print("💾 Saving data to CSV...")
        save_daily_data_csv(
            rainfall,
            waterlevel,
            water_depth,
            spilling_cusec,
            catchment_rainfall,
            prediction['predicted_water_level'],
            prediction['final_ensemble_risk'],
        )
        print("✅ Data saved successfully!")
        
        return True

    except Exception as e:
        print(f"❌ Error in flood prediction: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)