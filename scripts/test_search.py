from app.services.search_service import SearchService

def run_test():
    search_service = SearchService()

    results = search_service.search(
        query="2BHK near Hinjewadi",
        city="Pune",
        top_k=3
    )

    print("\n🔍 Search Results:\n")
    for r in results:
        print("Property ID:", r["property_id"])
        print("Score:", r["score"])
        print("City:", r["metadata"]["city"])
        print("Area:", r["metadata"]["area"])
        print("Price:", r["metadata"]["price"])
        print("-" * 40)


if __name__ == "__main__":
    run_test()