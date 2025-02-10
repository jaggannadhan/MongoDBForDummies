from fastapi import APIRouter, HTTPException, Depends, Form
from bson import ObjectId
from typing import List, Annotated
from fastapi import Request
from dependencies import get_workouts_db  
import uuid
from pydantic import BaseModel

workout_router = APIRouter()

def workout_helper(workout) -> dict:
    return {
        "id": str(workout["_id"]) or uuid.uuid4(),
        "user_id": workout["user_id"],
        "date": workout["date"],
        "workout_type": workout["workout_type"],
        "duration_minutes": workout["duration_minutes"],
        "calories_burned": workout["calories_burned"],
        "notes": workout.get("notes", "")
    }

class WorkoutModel(BaseModel):
    user_id: str
    date: str
    workout_type: str
    duration_minutes: int
    calories_burned: int
    notes: str



# Get all workouts
@workout_router.get("/", response_description="List all workouts")
async def list_workouts(workout_collection=Depends(get_workouts_db)) -> List[dict]:
    workouts = []
    cursor = workout_collection.find().limit(100)
    async for workout in cursor:
        workouts.append(workout_helper(workout))
    return workouts


# Create a new workout entry
@workout_router.post("/", response_description="Add new workout")
async def add_workout(
    workout_data: Annotated[WorkoutModel, Form()],
    workout_collection=Depends(get_workouts_db)
) -> dict:
    workout = await workout_collection.insert_one(workout_data.dict())
    saved_workout = await workout_collection.find_one({"_id": workout.inserted_id})
    saved_workout["_id"] = str(saved_workout.get("_id"))
    print(f"This is the save data: {saved_workout}")
    return saved_workout


# Get a specific workout by ID
@workout_router.get("/{id}", response_description="Get a single workout")
async def show_workout(id: str, workout_collection=Depends(get_workouts_db)) -> dict:
    if (workout := await workout_collection.find_one({"_id": ObjectId(id)})) is not None:
        return workout_helper(workout)
    raise HTTPException(status_code=404, detail=f"Workout {id} not found")


# Update a workout entry
@workout_router.put("/{id}", response_description="Update a workout")
async def update_workout(id: str, workout_data: dict, workout_collection=Depends(get_workouts_db)) -> dict:
    if len(workout_data) < 1:
        raise HTTPException(status_code=400, detail="Invalid input data")
    
    if (workout := await workout_collection.find_one({"_id": ObjectId(id)})) is not None:
        updated_workout = await workout_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": workout_data}
        )
        if updated_workout.modified_count == 1:
            if (updated := await workout_collection.find_one({"_id": ObjectId(id)})) is not None:
                return workout_helper(updated)
    raise HTTPException(status_code=404, detail=f"Workout {id} not found")


# Delete a workout entry
@workout_router.delete("/{id}", response_description="Delete a workout")
async def delete_workout(id: str, workout_collection=Depends(get_workouts_db)) -> dict:
    delete_result = await workout_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": f"Workout {id} deleted successfully"}
    raise HTTPException(status_code=404, detail=f"Workout {id} not found")