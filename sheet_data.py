import requests
import pandas as pd
from io import StringIO

def get_sheet_data(csv_url):
    try:
        # Fetch CSV from Google Sheets
        response = requests.get(csv_url)
        response.raise_for_status()

        # Read CSV into DataFrame
        df = pd.read_csv(StringIO(response.text))

        # Strip extra spaces from column names
        df.columns = df.columns.str.strip()

        # Ensure there are at least 9 rows
        if len(df) >= 8:
            # Get the 9th row (index 7)
            row = df.iloc[7]

            # Fetch values
            water_depth = row.get("Water Depth_ft", None)
            spilling_cusec = row.get("Spilling_Cusec", 0)

            # Handle NaN
            if pd.isna(spilling_cusec):
                spilling_cusec = 0

            return float(water_depth), float(spilling_cusec)
        else:
            raise ValueError("CSV does not have 9 rows yet")

    except Exception as e:
        print(f"Error fetching sheet data: {e}")
        return None, None