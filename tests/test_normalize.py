from scraper.pipeline.normalize import parse_price_eur


def test_parse_price_eur_comma_decimals() -> None:
    assert parse_price_eur("799,00 €") == 799.00


def test_parse_price_eur_no_decimals() -> None:
    assert parse_price_eur("999 €") == 999.0


def test_parse_price_eur_thousands_separator() -> None:
    assert parse_price_eur("1.099,99 €") == 1099.99


def test_parse_price_eur_nbsp() -> None:
    # some pages include non-breaking spaces
    assert parse_price_eur("799,00\xa0€") == 799.00


def test_parse_price_eur_invalid() -> None:
    try:
        parse_price_eur("free")
        raise AssertionError("Expected ValueError")
    except ValueError:
        pass
