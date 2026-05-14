from fastapi import FastAPI
from app.api import stream, checkout
from app.core.orchestrator import Orchestrator

app = FastAPI(title="Drive-Thru Ordering VA (FOSS Stack)")

# Initialize the central orchestrator
orchestrator = Orchestrator()

@app.get("/")
async def root():
    return {"message": "Welcome to the Open-Source Drive-Thru VA API"}

app.include_router(checkout.router, prefix="/api/checkout", tags=["Checkout"])
# The stream.py will handle WebSocket audio and route to the orchestrator
app.include_router(stream.router, prefix="/api/stream", tags=["Audio Pipeline"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)