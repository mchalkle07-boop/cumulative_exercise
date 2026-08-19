"""FastAPI app for serving a welcome message and geocoding conversion endpoint."""

import requests
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    """Return the default welcome message."""
    return {"message": "Hello World"}


@app.post("/convert/{state}/{city}")
def convert(state: str, city: str):
    """Convert a city/state into latitude and longitude coordinates."""
    print("Converting lat long")

    lat = None
    long = None
    api_key = "6a7f57138e04b429290986wxia11d90"

    payload = {"api_key": api_key, "state": state, "city": city}

    response = requests.get(
        "https://geocode.maps.co/search", params=payload, timeout=10
    )

    best_result = response.json()[0]
    lat = best_result["lat"]
    long = best_result["lon"]

    result = {"lat": lat, "long": long}
    return result
