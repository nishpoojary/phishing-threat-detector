from fastapi import APIRouter

from backend.app.schemas.email import EmailRequest, EmailResponse
from backend.app.schemas.url import URLRequest, URLResponse

from backend.app.services.detector import detect_phishing
from backend.app.services.url_detector import analyze_url
router = APIRouter(
    prefix="/api",
    tags=["Phishing Detection"]
)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Phishing Email Detector"
    }


# --------------------------------------------------
# Email Detection
# --------------------------------------------------

@router.post(
    "/detect",
    response_model=EmailResponse
)
def detect_email(request: EmailRequest):

    return detect_phishing(
        request.subject,
        request.body
    )


# --------------------------------------------------
# URL Detection
# --------------------------------------------------

@router.post(
    "/detect-url",
    response_model=URLResponse
)
def detect_url(request: URLRequest):

    return analyze_url(request.url)