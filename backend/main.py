import json
from fastapi import FastAPI

app = FastAPI(
    title="OTA Validation & Monitoring Mock API",
    description="Mock backend API for automotive OTA campaign and vehicle validation workflows.",
    version="1.0.0"
)


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


@app.get("/")
def health_check():
    return {
        "service": "OTA Validation Backend",
        "status": "running"
    }


@app.get("/vehicles")
def get_vehicles():
    return load_json("data/vehicles.json")


@app.get("/campaigns")
def get_campaigns():
    return load_json("data/campaigns.json")


@app.get("/vehicles/{vin}")
def get_vehicle_by_vin(vin: str):
    vehicles = load_json("data/vehicles.json")

    for vehicle in vehicles:
        if vehicle["vin"] == vin:
            return vehicle

    return {
        "error": "Vehicle not found",
        "vin": vin
    }


@app.get("/campaigns/{campaign_id}")
def get_campaign_by_id(campaign_id: str):
    campaigns = load_json("data/campaigns.json")

    for campaign in campaigns:
        if campaign["campaign_id"] == campaign_id:
            return campaign

    return {
        "error": "Campaign not found",
        "campaign_id": campaign_id
    }