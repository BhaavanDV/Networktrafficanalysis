from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Network Intrusion Detection API Running"}