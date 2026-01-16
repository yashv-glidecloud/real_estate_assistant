import re
import json
from typing import Dict, Any, Optional

from app.services.llm_service import LLMService


class IntentExtractor:
    """
    HYBRID INTENT EXTRACTION

    - Regex → deterministic signals (bhk, price, balcony)
    - LLM   → semantic signals (city, area)
    - Merge with strict priority rules

    This guarantees high accuracy while still using LLM correctly.
    """

    def __init__(self):
        self.llm = LLMService()

    def _extract_signals(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()

        signals = {
            "bhk": None,
            "max_price_lakhs": None,
            "balcony": None,
        }

        bhk_match = re.search(r"(\d+)\s*bhk", text_lower)
        if bhk_match:
            signals["bhk"] = int(bhk_match.group(1))


        price_match = re.search(
            r"under\s*(\d+(?:\.\d+)?)\s*(cr|crore|lakhs|lacs|lac|l)",
            text_lower
        )
        if price_match:
            value = float(price_match.group(1))
            unit = price_match.group(2)

            if unit.startswith("cr"):
                signals["max_price_lakhs"] = value * 100
            else:
                signals["max_price_lakhs"] = value

        if "balcony" in text_lower:
            signals["balcony"] = True

        return signals

    def _extract_json_block(self, text: str) -> Optional[str]:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        return text[start:end + 1]


    def _extract_city_area(self, text: str) -> Dict[str, Any]:
        system_prompt = """
You are a strict JSON extraction engine.

Extract ONLY city and area from the user query.

Rules:
- Output ONLY valid JSON
- No explanations
- Use null if missing
- City must be the broader city (e.g. Delhi, Pune)
- Area must be locality (e.g. Saket, Hinjewadi)

JSON schema:
{
  "city": string | null,
  "area": string | null
}
""".strip()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]

        raw = self.llm.chat(messages)
        json_block = self._extract_json_block(raw)

        if not json_block:
            return {"city": None, "area": None}

        try:
            data = json.loads(json_block)
        except json.JSONDecodeError:
            return {"city": None, "area": None}

        city = data.get("city")
        area = data.get("area")

        if city in ("null", "", None):
            city = None
        if area in ("null", "", None):
            area = None

        return {"city": city, "area": area}

    def extract(self, text: str) -> Dict[str, Any]:
        regex_signals = self._extract_signals(text)
        llm_location = self._extract_city_area(text)

        return {
            "city": llm_location["city"],
            "area": llm_location["area"],
            "bhk": regex_signals["bhk"],
            "max_price_lakhs": regex_signals["max_price_lakhs"],
            "balcony": regex_signals["balcony"],
            "top_k": 5,
        }
