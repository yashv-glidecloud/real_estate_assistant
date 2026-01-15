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