from pydantic import BaseModel, field_validator, model_validator
from typing import List
from datetime import datetime

class TweetModel(BaseModel):
    id: int
    # ticker_symbol: str
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


class StockPriceModel(BaseModel):
    ticker_symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: datetime
    day_date: datetime

    @field_validator('ticker_symbol')
    def validate_ticker_symbol(cls, val):
        if not val.strip():
            raise ValueError("Ticker symbol cannot be empty")
        return val.upper()

    @field_validator('open', 'high', 'low', 'close')
    def validate_prices(cls, val, info):
        if val <= 0:
            raise ValueError(f"{info.field_name} price must be a positive number")
        return val

    @field_validator('volume')
    def validate_volume(cls, val):
        if val < 0:
            raise ValueError("Volume must be positive")
        return val

    @field_validator('timestamp', 'day_date')
    def validate_dates(cls, val, info):
        if val > datetime.now():
            raise ValueError(f"{info.field_name} cannot be in the future")
        return val

    @model_validator(mode='after')
    def validate_price_relationships(self):
        if not (self.low <= self.open <= self.high):
            raise ValueError("Invalid relationship: expected low <= open <= high")
        return self