from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Borderline backend is alive 🚀"}