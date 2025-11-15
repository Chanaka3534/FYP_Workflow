import requests
from datetime import date, timedelta

def get_catchment_rainfall(latitude, longitude, timezone="Asia/Colombo"):
    """
    Fetch yesterday's catchment rainfall (in mm) for the given latitude and longitude
    using the Open-Meteo Historical Weather API.
    If no data is available, returns 0.
    """
    # Calculate yesterday's date
    yesterday = date.today() - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    # Build Open-Meteo archive API URL
    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}&longitude={longitude}"
        f"&start_date={date_str}&end_date={date_str}"
        "&daily=precipitation_sum"
        f"&timezone={timezone}"
    )

    # Send request
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()

    # Extract rainfall value, return 0 if missing or null
    catchment_rainfall = 0
    if "daily" in data and "precipitation_sum" in data["daily"]:
        values = data["daily"]["precipitation_sum"]
        if values and values[0] is not None:
            catchment_rainfall = values[0]

    return date_str, catchment_rainfall