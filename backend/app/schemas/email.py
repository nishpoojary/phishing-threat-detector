from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class EmailResponse(BaseModel):
    is_phishing: bool
    prediction: str
    phishing_probability: float
    safe_probability: float
    risk_level: str
    indicators: list[str]