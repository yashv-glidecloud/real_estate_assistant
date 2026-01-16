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


def test_extract_price_in_crores():
    ie = IntentExtractor()
    result = ie.extract("4 bhk villa under 1.5 crore")

    assert result["bhk"] == 4
    assert result["max_price_lakhs"] == 150


def test_extract_balcony_flag():
    ie = IntentExtractor()
    result = ie.extract("3 bhk flat with balcony")

    assert result["balcony"] is True


def test_extract_defaults():
    ie = IntentExtractor()
    result = ie.extract("show flats")

    assert result["bhk"] is None
    assert result["max_price_lakhs"] is None
    assert result["top_k"] == 5