# save_daily_data_csv.py
import csv
import os
from datetime import datetime

def save_daily_data_csv(rainfall, waterlevel, water_depth, spilling_cusec, 
                       catchment_rainfall, predicted_water_level, final_risk):
    """
    Save daily flood prediction data to CSV file
    """
    filename = "daily_flood_data.csv"
    file_exists = os.path.isfile(filename)

    # Convert risk to 0/1
    risk_value = 0 if final_risk == "NEGATIVE" else 1

    # Convert waterlevel from mm to meters
    waterlevel_m = float(waterlevel) / 1000
    
    # Convert predicted water level from mm to meters
    predicted_water_level_m = float(predicted_water_level) / 1000
    
    # Convert water depth from feet to meters
    water_depth_m = float(water_depth) * 0.3048

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write header only once
        if not file_exists:
            writer.writerow([
                "Date", 
                "Downstream Rainfall(mm)", 
                "Waterlevel(m)", 
                "Water Depth(Sena Dam)m", 
                "Spilling (Sena Dam) Cusec",
                "Catchment Rainfall(mm)", 
                "Predicted Water Level (LSTM)(m)", 
                "Final Ensemble Flood Risk"
            ])

        # Write data row
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            float(rainfall),
            round(waterlevel_m, 3),  # In meters, rounded to 3 decimal places
            round(water_depth_m, 3),  # In meters, rounded to 3 decimal places
            float(spilling_cusec),
            float(catchment_rainfall),
            round(predicted_water_level_m, 3),  # In meters, rounded to 3 decimal places
            risk_value
        ])