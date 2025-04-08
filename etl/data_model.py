from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime

class TweetModel(BaseModel):
    id: int
    author: str
    post_date: str
    clean_text: str
    comment_num: int
    retweet_num: int
    like_num: int
    tokens: List[str]

    @field_validator('post_date')
    def valid_datetime(cls, val_date):
        try:
            datetime.fromisoformat(val_date)
            return val_date
        except Exception:
            raise ValueError("Invalid date format")