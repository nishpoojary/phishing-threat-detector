from pydantic import BaseModel, Field


class URLRequest(BaseModel):
    url: str = Field(..., min_length=5)


class URLResponse(BaseModel):
    is_suspicious: bool
    prediction: str
    risk_level: str
    risk_score: int
    indicators: list[str]