from typing import Optional, List
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    bhk: Optional[int] = None
    max_price_lakhs: Optional[float] = None
    balcony: Optional[bool] = None
    top_k: int = 5


class PropertyResult(BaseModel):
    property_id: str
    property_name: str
    bhk: int
    city: str
    area: str
    price_lakhs: float
    description: str


class SearchResponse(BaseModel):
    results: List[PropertyResult]
    message: Optional[str] = None