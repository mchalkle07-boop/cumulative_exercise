from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.post("/convert/{state}/{city}")
def convert(state, city):
    print("Converting lat long")
    lat = None
    long = None

    api_key = "6a7f57138e04b429290986wxia11d90"
    payload = {"api_key": api_key, "state": state, "city": city}

    response = requests.get("https://geocode.maps.co/search", params=payload)
    best_result = response.json()[0]
    lat = best_result["lat"]
    long = best_result["lon"]
    result = {"lat": lat, "long": long}

    return result
