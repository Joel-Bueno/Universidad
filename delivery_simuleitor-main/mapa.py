import os
import requests
from city import City

BASE_URL_GEOCODE = "https://api.openrouteservice.org/geocode/search"
BASE_URL_ROUTE = "https://api.openrouteservice.org/v2/directions/driving-car"


def _get_api_key():
    key = os.getenv("ORS_API_KEY")
    if not key:
        raise RuntimeError("No ORS_API_KEY encontrada.")
    return key


def _geocode(place_name: str, key: str):
    params = {"api_key": key, "text": place_name, "size": 1}
    resp = requests.get(BASE_URL_GEOCODE, params=params)
    data = resp.json()

    if "features" not in data or not data["features"]:
        raise ValueError(f"No se pudo encontrar '{place_name}'")

    coords = data["features"][0]["geometry"]["coordinates"]
    return coords[0], coords[1]


def get_distance_km(origin: City, destination: City):
    key = _get_api_key()
    start = _geocode(origin.name, key)
    end = _geocode(destination.name, key)

    body = {
        "coordinates": [start, end],
        "units": "km"
    }

    headers = {"Authorization": key, "Content-Type": "application/json"}
    resp = requests.post(BASE_URL_ROUTE, json=body, headers=headers)
    data = resp.json()

    if "routes" not in data:
        raise RuntimeError("Error en API de mapas")

    dist = data["routes"][0]["summary"]["distance"]
    return round(dist, 2)