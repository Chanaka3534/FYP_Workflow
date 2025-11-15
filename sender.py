import requests # type: ignore

def send_to_thingsboard_demo(device_token, date, water_depth, spilling_cusec, catchment_rainfall, predicted_water_level, final_risk_label):
    """
    Send telemetry data to ThingsBoard Demo.

    final_risk_label: 'NEGATIVE' or 'POSITIVE' (converted to 0/1)
    """
    url = f"https://demo.thingsboard.io/api/v1/{device_token}/telemetry"

    C_water_depth = round(float(water_depth*0.3048), 1)
    C_PredictedWaterLevel = round(float(predicted_water_level)/1000, 2)
    
    payload = {
        "Date" : date,
        "WaterDepth": C_water_depth,  
        "SpillingCusec": float(spilling_cusec),
        "CatchmentRainfall": float(catchment_rainfall),
        "PredictedWaterLevel": C_PredictedWaterLevel,
        "FinalEnsembleRisk": final_risk_label
    }

    print("C_water_depth:", C_water_depth)
    print("C_PredictedWaterLevel:", C_PredictedWaterLevel)
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Data sent to ThingsBoard Demo successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print("❌ Failed to send data:", e)
        return False
