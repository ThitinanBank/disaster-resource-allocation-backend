from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.assign import assign_resources
# from routers.areas import affect_area
# from routers.trucks import resource_truck
from database import db
from services.redis import redis_set, redis_get, redis_delete
import time

router = APIRouter(prefix="/assignments", tags=["Assignments"])
collection_area = db["affect_area"]
collection_truck = db["resource_truck"]

class NonAssign(BaseModel):
    AreaID: str
    reason: str

class AssignFlag(BaseModel):
    is_resource_matching: bool
    is_fulfill: bool
    is_time_achieve: bool
    is_truck_available: bool
    is_urgent: bool

class ResourcesDelivered(BaseModel):
    food: Optional[int] = None
    water: Optional[int] = None
    medicine: Optional[int] = None

class Assign(BaseModel):
    AreaID: str
    TruckID: str
    ResourcesDelivered: ResourcesDelivered

class AssignResponse(BaseModel):
    assign: list[Assign]
    non_assign: list[NonAssign]

# @router.post("/")
@router.post("/",response_model=AssignResponse)
async def assignments():
    affect_area = [area async for area in collection_area.find()]
    resource_truck = [truck async for truck in collection_truck.find()]
    # assigns, non_assigns, assign_log = assign_resources(affect_area, resource_truck)

    results = redis_get('results')
    if results is None:
        print("No results found in Redis.")
        time.sleep(2)
        assigns, non_assigns, assign_log = assign_resources(affect_area, resource_truck)
        results = {
            "assign": assigns,
            "non_assign": non_assigns,
            # "assign_log": assign_log
        }
        redis_set('results',results,ex=1800)
        return results
    else:
        print("Results found in Redis.")
        return results

@router.get("/",response_model=AssignResponse)
def get_assignments():
    assigns = redis_get("results")
    if not assigns:
        raise HTTPException(status_code=404,detail="Assign not found")
    return assigns

@router.delete("/")
def delete_assignments():
    redis_delete("results")
    return