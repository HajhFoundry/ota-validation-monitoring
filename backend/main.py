import json
from fastapi import FastAPI
from pydantic import BaseModel
from backend.ota_controller import (start_ota, pause_ota, resume_ota, get_ota_status, update_ota_status)


app = FastAPI(
    title="OTA Validation & Monitoring Mock API",
    description="Mock backend API for automotive OTA campaign and vehicle validation workflows.",
    version="1.0.0"
)

class OTAStartRequest(BaseModel):
    vin: str
    campaign_id: str

class OTAStatusUpdateRequest(BaseModel):
    vin: str
    campaign_id: str
    state: str
    progress: int
    message: str = "OTA status updated"

def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


@app.get("/")
def health_check():
    return {
        "service": "OTA Validation Backend",
        "status": "running"
    }

@app.get("/debug/routes")
def debug_routes():
    return [route.path for route in app.routes]
    
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

@app.post("/ota/start")
def api_start_ota(request: OTAStartRequest):
    return start_ota(request.vin, request.campaign_id)


@app.post("/ota/pause/{vin}")
def api_pause_ota(vin: str):
    return pause_ota(vin)


@app.post("/ota/resume/{vin}")
def api_resume_ota(vin: str):
    return resume_ota(vin)

@app.post("/ota/update-status")
def api_update_ota_status(request: OTAStatusUpdateRequest):
    return update_ota_status(
        request.vin,
        request.campaign_id,
        request.state,
        request.progress,
        request.message
    )

@app.get("/ota/status/{vin}")
def api_get_ota_status(vin: str):
    return get_ota_status(vin)

