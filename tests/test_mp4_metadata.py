from unittest.mock import patch

from audiobookdl import AudiobookMetadata
from audiobookdl.output.metadata.mp4 import add_mp4_metadata


class FakeEasyMP4:
    Get = {}

    def __init__(self, _path):
        self.values = {}
        self.saved = False
        self.tags = self

    def RegisterFreeformKey(self, *args, **kwargs):
        return None

    def __setitem__(self, key, value):
        self.values[key] = value

    def save(self):
        self.saved = True


def test_mp4_metadata_writes_audiobookshelf_series_tags():
    metadata = AudiobookMetadata(
        "Stil maar",
        series="Gina Harte",
        series_order=1,
    )
    audio = FakeEasyMP4("unused")

    with patch("audiobookdl.output.metadata.mp4.EasyMP4", return_value=audio):
        add_mp4_metadata("Stil maar.m4b", metadata)

    assert audio.values["title"] == "Stil maar"
    assert audio.values["album"] == "Stil maar"
    assert audio.values["series"] == "Gina Harte"
    assert audio.values["series-part"] == "1"
    assert audio.values["tracknumber"] == "1"
    assert audio.saved is True


def test_mp4_metadata_copies_title_to_album_without_series():
    metadata = AudiobookMetadata("Book title")
    audio = FakeEasyMP4("unused")

    with patch("audiobookdl.output.metadata.mp4.EasyMP4", return_value=audio):
        add_mp4_metadata("book.m4b", metadata)

    assert audio.values["title"] == "Book title"
    assert audio.values["album"] == "Book title"
    assert "series" not in audio.values
    assert "series-part" not in audio.values
