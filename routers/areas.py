from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db
from threading import Timer

router = APIRouter(prefix="/areas", tags=["Areas"])
collection = db["affect_area"]

# affect_area = [
#     {
#         "AreaID": "A1",
#         "UrgencyLevel": 5,
#         "RequiredResources": {"food": 200, "water": 300},
#         "TimeConstaint": 6
#     },
#     {
#         "AreaID": "A3",
#         "UrgencyLevel": 4,
#         "RequiredResources": {"food": 200, "water": 300},
#         "TimeConstaint": 6
#     },
#     {
#         "AreaID": "A2",
#         "UrgencyLevel": 4,
#         "RequiredResources": {"medicine": 50},
#         "TimeConstaint": 4
#     },
#     {
#         "AreaID": "A4",
#         "UrgencyLevel": 3,
#         "RequiredResources": {"medicine": 50},
#         "TimeConstaint": 4
#     }
# ]

class AffectAreaRequest(BaseModel):
    AreaID: str
    UrgencyLevel: int
    RequiredResources: dict
    TimeConstaint: int

class AffectAreaResponse(BaseModel):
    AreaID: str
    UrgencyLevel: int
    RequiredResources: dict
    TimeConstaint: int

@router.get("/",response_model=list[AffectAreaResponse])
async def get_areas():
    affect_area = [area async for area in collection.find()]
    return affect_area

@router.post("/",response_model=list[AffectAreaResponse])
async def add_areas(area : AffectAreaRequest):
    is_existing = await collection.find_one({"AreaID":area.AreaID})
    if is_existing:
        raise HTTPException(status_code=400, detail="AreaID already exists.")
    await collection.insert_one(area.model_dump())
    affect_area = [area async for area in collection.find()]
    return affect_area