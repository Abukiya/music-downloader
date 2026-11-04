import unittest
from pathlib import Path

from music_download.cli import (
    build_command,
    default_output_directory,
    is_playlist_url,
    is_youtube_url,
)


class CliTests(unittest.TestCase):
    def test_accepts_video_and_playlist_urls(self):
        self.assertTrue(is_youtube_url("https://www.youtube.com/watch?v=abc"))
        self.assertTrue(is_youtube_url("https://youtu.be/abc"))
        self.assertTrue(is_youtube_url("https://www.youtube.com/playlist?list=xyz"))

    def test_rejects_non_youtube_urls(self):
        self.assertFalse(is_youtube_url("https://example.com/video"))
        self.assertFalse(is_youtube_url("not a url"))

    def test_classifies_playlist_url(self):
        self.assertTrue(is_playlist_url("https://www.youtube.com/playlist?list=xyz"))
        self.assertFalse(is_playlist_url("https://www.youtube.com/watch?v=abc"))

    def test_builds_playlist_command(self):
        command = build_command(
            "https://www.youtube.com/playlist?list=xyz",
            Path("/tmp/Music"),
            "mp3",
            True,
            True,
            False,
        )
        self.assertIn("--yes-playlist", command)
        self.assertTrue(
            any(
                item.endswith(
                    "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s"
                )
                for item in command
            )
        )
        self.assertIn("--no-overwrites", command)
        self.assertIn("--embed-thumbnail", command)

    def test_builds_single_video_command(self):
        command = build_command(
            "https://youtu.be/abc",
            Path("/tmp/Music"),
            "mp3",
            True,
            True,
            False,
        )
        self.assertIn("--no-playlist", command)
        self.assertNotIn("--yes-playlist", command)
        self.assertTrue(any(item.endswith("%(title)s.%(ext)s") for item in command))

    def test_default_directory_is_absolute(self):
        self.assertTrue(default_output_directory().is_absolute())


if __name__ == "__main__":
    unittest.main()
