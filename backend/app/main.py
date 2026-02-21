from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal, engine
from .models import *
from typing import List

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str

class PointIn(BaseModel):
    lat: float
    lon: float

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "id": new_user.id,
        "username": new_user.username,
        "total_area": new_user.total_area,
    }


@app.post("/activity/start")
def start_activity(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()                # Extract the user based on User ID
    if not user:
        return {"error": "User not found"}

    # prevent multiple active sessions
    existing = db.query(Activity).filter(
        Activity.user_id == user_id,
        Activity.is_active == True
    ).first()

    if existing:
        return {"error": "User already has an active activity"}

    activity = Activity(user_id=user_id)
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return {
        "activity_id": activity.id,
        "start_time": activity.start_time
    }

@app.post("/actvitiy/{activity_id}/points")
def add_points(activity_id: int, points: List[PointIn], db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()

    if not activity:
        return {"Error: Invalid or Inactive activity"}

    for point in points:
        db.add(ActivityPoint(
            activity_id = activity.id,
            lat = point.lat,
            lon = point.lon
        ))

    db.commit()

    return {"Message: Points Added"}