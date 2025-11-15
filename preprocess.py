# preprocess.py
def prepare_input(catchment_rainfall, downstream_rainfall, water_depth, spilling_cusec, waterlevel):
    """
    Return a flat list of 5 values in the correct order
    """
    return [
        catchment_rainfall,
        downstream_rainfall,
        waterlevel,      # Reservoir water level
        spilling_cusec,  # Discharge rate
        water_depth      # Kaliodai water level
    ]
