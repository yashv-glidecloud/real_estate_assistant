from fastapi import APIRouter
from pydantic import BaseModel
from app.services.intent_extractor import IntentExtractor
from app.services.search_service import SearchService

router = APIRouter(prefix="/chat", tags=["chat"])

search_service = SearchService()
intent_extractor = IntentExtractor()

# 🧠 In-memory intent memory
# session_id -> last known intent
INTENT_MEMORY = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = "default"


def merge_intent(old: dict, new: dict) -> dict:
    """
    Merge intent objects.
    New values override old ONLY if they are not None.
    """
    merged = old.copy()
    for k, v in new.items():
        if v is not None:
            merged[k] = v
    return merged


@router.post("")
def chat(req: ChatRequest):
    session_id = req.session_id or "default"

    new_intent = intent_extractor.extract(req.message)

    if session_id in INTENT_MEMORY:
        intent = merge_intent(INTENT_MEMORY[session_id], new_intent)
    else:
        intent = new_intent

    INTENT_MEMORY[session_id] = intent

    results = search_service.search(
        city=intent["city"],
        area=intent["area"],
        bhk=intent["bhk"],
        max_price_lakhs=intent["max_price_lakhs"],
        balcony=intent["balcony"],
        top_k=intent["top_k"],
    )

    if not results:
        return {
            "answer": "No properties found matching your request.",
            "filters_used": intent,
            "results": []
        }

    return {
        "answer": f"Found {len(results)} properties matching your request.",
        "filters_used": intent,
        "results": results
    }