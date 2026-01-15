from fastapi import APIRouter
from app.models.search import SearchRequest, SearchResponse
from app.services.search_service import SearchService
from app.services.chat_rag_service import ChatRAGService

router = APIRouter()
search_service = SearchService()
chat_service = ChatRAGService()


@router.post("/search", response_model=SearchResponse)
def search(req: SearchRequest):
    results = search_service.search(
        city=req.city,
        area=req.area,
        bhk=req.bhk,
        max_price_lakhs=req.max_price_lakhs,
        balcony=req.balcony,
        top_k=req.top_k,
    )

    if not results:
        return {
            "results": [],
            "message": "No properties found matching your criteria."
        }

    return {"results": results}
