import chromadb

CHROMA_PERSIST_DIR = "app/vectordb/chroma_store"


class ChromaDB:
    def __init__(self):
        # ✅ Persistent client (NEW API)
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR
        )

    def get_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)
