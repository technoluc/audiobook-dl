from audiobookdl.sources.nextory import NextorySource


def test_extract_series_metadata_uses_top_level_volume():
    name, position = NextorySource._extract_series_metadata(
        {
            "series": {"name": " Het Lied van IJs en Vuur ", "vol": 0},
            "volume": "1",
        }
    )

    assert name == "Het Lied van IJs en Vuur"
    assert position == 1


def test_extract_series_metadata_ignores_invalid_or_missing_values():
    assert NextorySource._extract_series_metadata({}) == (None, None)
    assert NextorySource._extract_series_metadata({"series": []}) == (None, None)
    assert NextorySource._extract_series_metadata({"series": {"name": " "}}) == (
        None,
        None,
    )
    assert NextorySource._extract_series_metadata(
        {"series": {"name": "Saga"}, "volume": True}
    ) == ("Saga", None)
    assert NextorySource._extract_series_metadata(
        {"series": {"name": "Saga"}, "volume": "not-a-number"}
    ) == ("Saga", None)
