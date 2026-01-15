from app.services.intent_extractor import IntentExtractor


def test_extract_bhk_and_price():
    ie = IntentExtractor()
    result = ie.extract("3 bhk flats under 90 lakhs")

    assert result["bhk"] == 3
    assert result["max_price_lakhs"] == 90


def test_extract_no_price():
    ie = IntentExtractor()
    result = ie.extract("2 bhk flats in Pune")

    assert result["bhk"] == 2
    assert result["max_price_lakhs"] is None