import re
from typing import Dict


def parse_query(text: str) -> Dict:
    text_lower = text.lower()

    result = {
        "query": text,
        "city": None,
        "bhk": None,
        "price_min": None,
        "price_max": None,
        "balcony": None,
    }

    # ---- BHK ----
    bhk_match = re.search(r'(\d+)\s*bhk', text_lower)
    if bhk_match:
        result["bhk"] = int(bhk_match.group(1))

    # ---- City ----
    if "pune" in text_lower:
        result["city"] = "Pune"
    elif "mumbai" in text_lower:
        result["city"] = "Mumbai"
    elif "bangalore" in text_lower:
        result["city"] = "Bangalore"

    # ---- Price ----
    price_match = re.search(r'under\s*(\d+)\s*(lakh|lakhs|cr|crore)', text_lower)
    if price_match:
        value = int(price_match.group(1))
        unit = price_match.group(2)

        if "lakh" in unit:
            result["price_max"] = value * 100000
        else:
            result["price_max"] = value * 10000000

    # ---- Balcony ----
    if "balcony" in text_lower:
        result["balcony"] = True

    # ---- Clean semantic query ----
    cleaned = text_lower
    cleaned = re.sub(r'\d+\s*bhk', '', cleaned)
    cleaned = re.sub(r'under\s*\d+\s*(lakh|lakhs|cr|crore)', '', cleaned)
    cleaned = re.sub(r'\b(pune|mumbai|bangalore)\b', '', cleaned)
    cleaned = cleaned.replace("balcony", "")
    result["query"] = cleaned.strip()

    return result
