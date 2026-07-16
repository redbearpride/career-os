from fastapi import FastAPI

app = FastAPI(
    title="Executive Career OS",
    version="0.1.0",
    description="AI Career Intelligence Platform"
)


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