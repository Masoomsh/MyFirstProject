from fastapi import FastAPI

app = FastAPI(title="My FastAPI Application")

@app.get("/")
def home():
    return {"message": "Welcome to My FastAPI Application!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/response")
def response():
    return {"message": "How are you doing today?"}