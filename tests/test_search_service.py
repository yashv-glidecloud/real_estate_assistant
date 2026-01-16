from app.services.search_service import SearchService


def test_search_with_city_and_bhk():
    service = SearchService()
    results = service.search(city="Pune", bhk=2)

    for r in results:
        assert r["city"] == "Pune"
        assert r["bhk"] == 2


def test_search_no_results():
    service = SearchService()
    results = service.search(city="Mars")

    assert results == []


def test_search_with_price_filter():
    service = SearchService()
    results = service.search(max_price_lakhs=50)

    for r in results:
        assert r["price_lakhs"] <= 50



def test_search_top_k_limit():
    service = SearchService()
    results = service.search(top_k=2)

    assert len(results) <= 2