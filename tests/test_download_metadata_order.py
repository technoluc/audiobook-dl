from types import SimpleNamespace
from unittest.mock import patch

from audiobookdl.output.download import add_metadata_to_file


def test_single_file_metadata_is_written_after_chapters():
    calls = []
    audiobook = SimpleNamespace(
        chapters=[object()],
        metadata=object(),
        cover=object(),
    )
    options = SimpleNamespace(no_chapters=False, write_json_metadata=False)

    with (
        patch(
            "audiobookdl.output.download.metadata.add_chapters",
            side_effect=lambda *_: calls.append("chapters"),
        ),
        patch(
            "audiobookdl.output.download.metadata.add_metadata",
            side_effect=lambda *_: calls.append("metadata"),
        ),
        patch(
            "audiobookdl.output.download.metadata.embed_cover",
            side_effect=lambda *_: calls.append("cover"),
        ),
        patch("audiobookdl.output.download.logging.book_update"),
    ):
        add_metadata_to_file(audiobook, "book.m4b", options)

    assert calls == ["chapters", "metadata", "cover"]
