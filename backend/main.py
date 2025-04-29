from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import weather, farm, auth, routes
import uvicorn

app = FastAPI(
    title="AgroGPT Uganda API",
    description="API for AgroGPT Uganda - Agricultural Advisory and Support System",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from different modules
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(farm.router, prefix="/api/v1", tags=["Farm Management"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])
app.include_router(routes.router, prefix="/api/v1", tags=["General"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to AgroGPT Uganda API",
        "version": "1.0.0",
        "status": "active"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 