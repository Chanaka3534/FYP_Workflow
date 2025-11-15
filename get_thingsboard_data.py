import requests

def get_thingsboard_data(username, password, device_id):
    THINGSBOARD_URL = "https://demo.thingsboard.io"
    login_url = f"{THINGSBOARD_URL}/api/auth/login"
    login_payload = {"username": username, "password": password}

    login_resp = requests.post(login_url, json=login_payload)
    login_resp.raise_for_status()
    jwt_token = login_resp.json()["token"]

    telemetry_url = f"{THINGSBOARD_URL}/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys=rainfall,waterlevel"
    headers = {"X-Authorization": f"Bearer {jwt_token}"}

    resp = requests.get(telemetry_url, headers=headers)
    resp.raise_for_status()

    data = resp.json()
    rainfall = data.get("rainfall", [{}])[-1].get("value")
    waterlevel = data.get("waterlevel", [{}])[-1].get("value")

    return float(rainfall), float(waterlevel)
