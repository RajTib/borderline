from fastapi import FastAPI
from pydantic import BaseModel
import math
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

player_paths = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Location(BaseModel):
    user_id:int
    lat:float
    long:float


def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)


@app.get("/")
def read_root():
    return "Hello World"


@app.post("/update-location")
def update_location(loc:Location):
    if loc.user_id not in player_paths:
        player_paths[loc.user_id] = []

    path = player_paths[loc.user_id]

    if not path:
        path.append((loc.lat, loc.long))
    else:
        last_lat, last_long = path[-1]

    if distance(loc.lat, loc.long, last_lat, last_long) > 0.0001:
        path.append((loc.lat, loc.long))

    return {
        "points tracked" : len(path)
    }


@app.get("/path/{user_id}")
def get_path(user_id: int):
    return{
        "path": player_paths.get(user_id, [])
    }

# @app.get("/collision-detection")
# def collision_detection(loc:Location):
#     if loc.user_id !=
