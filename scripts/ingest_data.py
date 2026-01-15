import json
import re
from pathlib import Path
from app.services.embedding import EmbeddingService
from app.vectordb.chroma import ChromaDB

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "app" / "data" / "properties.json"

def extract_bhk(text: str):
    match = re.search(r"(\d+)\s*BHK", text, re.IGNORECASE)
    return int(match.group(1)) if match else None

def ingest_properties():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        properties = json.load(f)

    embedder = EmbeddingService()
    chroma = ChromaDB()
    collection = chroma.get_collection("real_estate_properties")

    for prop in properties:
        bhk = extract_bhk(prop["title"])

        # 👇 THIS IS WHAT SIMILARITY SEARCH USES
        text_to_embed = (
            f"{bhk}BHK apartment in {prop['area']} {prop['city']}. "
            f"Price category: {prop['price_category']}. "
            f"Bathrooms: {prop['bathrooms']}. "
            f"{prop['description']}"
        )

        embedding = embedder.embed_text(text_to_embed)

        metadata = {
            "property_id": prop["property_id"],
            "city": prop["city"],
            "area": prop["area"],
            "price": prop["price"],
            "price_category": prop["price_category"],
            "bathrooms": prop["bathrooms"],
            "balcony": prop["balcony"],
            "latitude": prop["latitude"],
            "longitude": prop["longitude"],
            "bhk": bhk
        }

        collection.add(
            ids=[prop["property_id"]],
            documents=[text_to_embed],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    print(f"✅ Ingested {len(properties)} properties")

if __name__ == "__main__":
    ingest_properties()