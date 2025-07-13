from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db

router = APIRouter(prefix="/trucks", tags=["Trucks"])
collection = db["resource_truck"]

# resource_truck = [
#     {
#         "TruckID": "T1",
#         "AvailableResources": {"food": 250, "water": 300},
#         "TravelTimeToArea": {"A1": 5, "A2": 3, "A3": 5, "A4": 3}
#     },
#     {
#         "TruckID": "T2",
#         "AvailableResources": {"medicine": 60},
#         "TravelTimeToArea": {"A1": 4, "A2": 2, "A3":4, "A4":2}
#     }
# ]

class ResourceTruckRequest(BaseModel):
    TruckID : str
    AvailableResources : dict
    TravelTimeToArea : dict

class ResourceTruckResponse(BaseModel):
    TruckID : str
    AvailableResources : dict
    TravelTimeToArea : dict

@router.get("/",response_model=list[ResourceTruckResponse])
async def get_trucks():
    resource_truck = [truck async for truck in collection.find()]
    return resource_truck

@router.post("/",response_model=list[ResourceTruckResponse])
async def add_trucks(truck : ResourceTruckRequest):
    is_existing = await collection.find_one({"TruckID":truck.TruckID})
    if is_existing:
        raise HTTPException(status_code=400, detail="TruckID already exists.")
    await collection.insert_one(truck.model_dump())
    resource_truck = [truck async for truck in collection.find()]
    return resource_truck