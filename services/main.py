from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import upload_data, generate_data, search
from logger import startup_logger, teardown_logger, get_logger

# Initialize logger
startup_logger()
logger = get_logger()

app = FastAPI(
    title="Demo Search AI",
    description="API for AI-powered search",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate_data.router, prefix="/api/v1/generate", tags=["advisory"])
app.include_router(upload_data.router, prefix="/api/v1/upload", tags=["upload"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])


@app.on_event("startup")
async def startup_event():
    """Initialize application resources on startup."""
    logger.info("Starting AI Financial Assistant API")
    startup_logger()

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up application resources on shutdown."""
    logger.info("Shutting down AI Financial Assistant API")
    teardown_logger()

@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to AI Financial Assistant API"} 

@app.get("/health")
async def healthcheck():
    logger.info("Healthcheck endpoint called")
    return {"status": "healthy"} 