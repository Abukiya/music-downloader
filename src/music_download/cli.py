from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import __version__

YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def default_output_directory() -> Path:
    return Path.cwd()


def is_youtube_url(value: str) -> bool:
    parsed = urlparse(value)
    host = parsed.netloc.lower().split(":", 1)[0]
    return parsed.scheme in {"http", "https"} and host in YOUTUBE_HOSTS


def is_playlist_url(value: str) -> bool:
    parsed = urlparse(value)
    host = parsed.netloc.lower().split(":", 1)[0]
    query = parse_qs(parsed.query)
    return (
        host in {"youtube.com", "www.youtube.com", "m.youtube.com"}
        and parsed.path.rstrip("/") == "/playlist"
        and bool(query.get("list"))
    ) or bool(query.get("list")) and host in YOUTUBE_HOSTS


def build_command(
    url: str,
    output_directory: Path,
    audio_format: str,
    embed_metadata: bool,
    embed_thumbnail: bool,
    dry_run: bool,
) -> list[str]:
    playlist = is_playlist_url(url)
    template = (
        "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s"
        if playlist
        else "%(title)s.%(ext)s"
    )
    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--format",
        "bestaudio/best",
        "--extract-audio",
        "--audio-format",
        audio_format,
        "--output",
        str(output_directory / template),
        "--no-overwrites",
        "--windows-filenames",
        "--newline",
    ]
    command.append("--yes-playlist" if playlist else "--no-playlist")
    if embed_metadata:
        command.append("--embed-metadata")
    if embed_thumbnail:
        command.extend(["--embed-thumbnail", "--convert-thumbnails", "jpg"])
    if dry_run:
        command.append("--simulate")
    command.append(url)
    return command


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        prog="music-download",
        description="Download a YouTube video or playlist as tagged audio.",
    )
    result.add_argument("url", help="YouTube video or playlist URL")
    result.add_argument(
        "-o",
        "--output",
        type=Path,
        default=default_output_directory(),
        help="destination directory (default: current working directory)",
    )
    result.add_argument(
        "--audio-format",
        choices=("mp3", "m4a", "opus", "wav", "flac"),
        default="mp3",
        help="audio format passed to yt-dlp (default: mp3)",
    )
    result.add_argument(
        "--no-metadata",
        action="store_true",
        help="do not embed title/artist/album metadata",
    )
    result.add_argument(
        "--no-thumbnail",
        action="store_true",
        help="do not embed thumbnail artwork",
    )
    result.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be downloaded without downloading",
    )
    result.add_argument("--version", action="version", version=__version__)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not is_youtube_url(args.url):
        print("error: URL must be an http(s) YouTube video or playlist URL", file=sys.stderr)
        return 2

    if shutil.which("ffmpeg") is None:
        print(
            "error: FFmpeg is required for audio conversion and thumbnail embedding",
            file=sys.stderr,
        )
        return 1

    args.output.expanduser().mkdir(parents=True, exist_ok=True)
    command = build_command(
        args.url,
        args.output.expanduser(),
        args.audio_format,
        not args.no_metadata,
        not args.no_thumbnail,
        args.dry_run,
    )
    try:
        return subprocess.run(command, check=False).returncode
    except OSError as error:
        print(f"error: could not start yt-dlp: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
