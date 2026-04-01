from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello World"

@app.post("/update-location")
def update_location(lat: float, lng: float):
    return {"message": "received", "lat": lat, "lng": lng}
