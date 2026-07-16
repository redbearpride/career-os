from fastapi import FastAPI

from app.api.routes import router as api_router

app = FastAPI(
    title="Executive Career OS",
    version="0.1.0",
    description="AI Career Intelligence Platform"
)

app.include_router(api_router)


@app.get("/")
def root():
    return {
        "system": "Executive Career OS",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
