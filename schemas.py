from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    prediction: float

class LogResponse(BaseModel):
    id: int
    day: int
    prediction: float
    created_at: datetime

class LogsResponse(BaseModel):
    logs: list[LogResponse]
