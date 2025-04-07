from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime

class TweetModel(BaseModel):
    id: int
    created_at: str
    cleaned_text: str
    tokens: List[str]

    @field_validator('created_at')
    def valid_datetime(cls, v):
        try:
            datetime.fromisoformat(v)
            return v
        except Exception:
            raise ValueError("Invalid date format")