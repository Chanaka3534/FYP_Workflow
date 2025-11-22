import requests  # type: ignore
from datetime import datetime
from zoneinfo import ZoneInfo

def send_to_thingsboard_demo(device_token, date, water_depth, spilling_cusec, catchment_rainfall, predicted_water_level, final_risk_label):
    """
    Send telemetry data to ThingsBoard Demo.

    Only the DATE (Sri Lankan time) is sent.
    """

    # 🇱🇰 Convert to Sri Lankan DATE only (no time)
    sri_lanka_date = datetime.now(ZoneInfo("Asia/Colombo")).strftime("%Y-%m-%d")

    url = f"https://demo.thingsboard.io/api/v1/{device_token}/telemetry"

    C_water_depth = round(float(water_depth * 0.3048), 1)
    C_PredictedWaterLevel = round(float(predicted_water_level) / 1000, 2)
    
    payload = {
        "Date": sri_lanka_date,   # <-- Send only date
        "WaterDepth": C_water_depth,
        "SpillingCusec": float(spilling_cusec),
        "CatchmentRainfall": float(catchment_rainfall),
        "PredictedWaterLevel": C_PredictedWaterLevel,
        "FinalEnsembleRisk": final_risk_label
    }

    print("Sending Date (Sri Lanka):", sri_lanka_date)

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Data sent to ThingsBoard Demo successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print("❌ Failed to send data:", e)
        return False
