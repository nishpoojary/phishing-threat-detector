import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
app = FastAPI(
    title="Phishing Email Detector API",
    description="AI-powered phishing email detection system",
    version="1.0.0"
)


def _cors_origins() -> list[str]:
    origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    extra = os.getenv("FRONTEND_URL", "")
    origins.extend(
        origin.strip().rstrip("/")
        for origin in extra.split(",")
        if origin.strip()
    )
    return origins


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Routes
# --------------------------------------------------

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Phishing Email Detector API is running",
        "version": "1.0.0"
    }