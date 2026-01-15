import json
from pathlib import Path
from typing import List, Dict, Optional

DATA_PATH = Path("app/data/properties.json")


class SearchService:
    def __init__(self):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            self.properties: List[Dict] = json.load(f)

    def search(
        self,
        city: Optional[str] = None,
        area: Optional[str] = None,
        bhk: Optional[int] = None,
        max_price_lakhs: Optional[float] = None,
        balcony: Optional[bool] = None,
        top_k: int = 5,
    ) -> List[Dict]:

        results = []

        for prop in self.properties:
            if city and prop["city"].lower() != city.lower():
                continue

            if area and prop["area"].lower() != area.lower():
                continue

            if bhk and prop["bhk"] != bhk:
                continue

            if max_price_lakhs and prop["price_lakhs"] > max_price_lakhs:
                continue

            if balcony is not None and prop["balcony"] != balcony:
                continue

            results.append({
                "property_id": prop["property_id"],
                "property_name": prop["property_name"],
                "bhk": prop["bhk"],
                "city": prop["city"],
                "area": prop["area"],
                "price_lakhs": prop["price_lakhs"],
                "description": prop["description"],
            })

        return results[:top_k]