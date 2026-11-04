# music-download

`music-download` is a reusable command-line wrapper around `yt-dlp`. Install it once, then download a single video or an entire playlist from any directory without repeating the full yt-dlp command.

## Requirements

- Python 3.9 or newer
- FFmpeg available on `PATH`

Install the package in an isolated environment:

```bash
python3 -m venv ~/.venvs/music-download
~/.venvs/music-download/bin/python -m pip install .
~/.venvs/music-download/bin/music-download --version
```

To make the command directly available in every shell, add the virtual environment's `bin` directory to `PATH`:

```bash
echo 'export PATH="$HOME/.venvs/music-download/bin:$PATH"' >> ~/.bashrc
```

Open a new shell or run `source ~/.bashrc`, then use:

```bash
music-download "https://www.youtube.com/watch?v=VIDEO_ID"
music-download "https://www.youtube.com/playlist?list=PLAYLIST_ID"
```

By default, files go to `~/Music`. Override that destination for one download:

```bash
music-download --output ~/Music/Amharic "PLAYLIST_URL"
```

To choose a persistent default destination, set `MUSIC_DOWNLOAD_DIR`:

```bash
export MUSIC_DOWNLOAD_DIR="$HOME/Music"
```

The command defaults to MP3 extraction, metadata and thumbnail embedding, playlist-specific folders, and skipping files that already exist. Useful options include `--audio-format m4a`, `--no-thumbnail`, `--no-metadata`, and `--dry-run`.

Downloads are written to the selected output directory, not into this source repository unless you explicitly choose it.
