import requests
import pandas as pd
import math
from io import StringIO

def get_sheet_data(csv_url):
    try:
        response = requests.get(csv_url)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text))
        df.columns = df.columns.str.strip()

        if len(df) >= 8:
            row = df.iloc[7]

            def clean_number(value):
                if value is None:
                    #return None
                    return 0.0
                    #
                if isinstance(value, str):
                    value = value.replace(",", "").strip()
                try:
                    #
                     value = float(vlaue)
                    if math.isnan(value) or math.isinf(value):
                   return 0.0

                return value
                        #
                  #  return float(value)
                
                except:
                    return 0.0
                #    return None

            water_depth = clean_number(row.get("Water Depth_ft"))
            spilling_cusec = clean_number(row.get("Spilling_Cusec"))

            return water_depth, spilling_cusec
        
        else:
            raise ValueError("CSV does not have 9 rows yet")

    except Exception as e:
        print(f"Error fetching sheet data: {e}")
        return None, None
