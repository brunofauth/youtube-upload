from __future__ import annotations

import os
from pathlib import Path
import click

from .auth import build_youtube_resource
from .playlists import add_video_to_playlist
from .parsers import parse_upload_metadata, validate_category, CATEGORY_ID
from .upload import upload


WATCH_VIDEO_URL = "https://www.youtube.com/watch?v={id}"


@click.command()
@click.argument("video-to-upload", type=click.Path(exists=True, dir_okay=False, path_type=Path))

# Video Metadata
@click.option('-t', "--title")
@click.option('-c', "--category", type=click.Choice(list(CATEGORY_ID.keys()), case_sensitive=False), callback=validate_category, default=None)
@click.option('-d', "--description", default=None)
@click.option("-p", '--playlist', help="add video to <playlist>, creating it if non-existent", default=None)
@click.option("-n", '--thumbnail', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='.jpg or .png', default=None)
@click.option("-T", "--tag", "tags", multiple=True, help="this option may be used several times", default=None)
@click.option("-D", '--date-to-publish', type=click.DateTime(), default=None, help="formatted like ISO 8601")
@click.option("-r", '--recording-date', type=click.DateTime(), default=None, help="formatted like ISO 8601")
@click.option("-l", '--language', default=None, help="ISO 639-1: <en|fr|de|pt|...>")
@click.option("-a", '--audio-language', default=None, help="ISO 639-1: <en|fr|de|pt|...>")
@click.option("-L", '--license', type=click.Choice(['youtube', 'creativeCommon'], case_sensitive=False), default='youtube')
@click.option('--location-latitude', default=None, type=float)
@click.option('--location-longitude', default=None, type=float)
@click.option('--location-altitude', default=None, type=float)

# Other Video Options
@click.option("-V", '--visibility', type=click.Choice(["public", "unlisted", "private"], case_sensitive=False), default="public")
@click.option("-e", '--embeddable', type=bool, default=False, help='make video is embeddable')

# Authentication
@click.option("-s", '--client-secrets', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='Secrets JSON file', default=None)
@click.option("-C", '--credentials', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='Credentials JSON file', default=None)

# Miscellaneous
@click.option('--chunksize', type=int, default=1024*1024*8, help='Progress bar step, in bytes')
def cli_main(*args, **kwargs) -> None:
    return main(*args, **kwargs)


def main(
    video_to_upload: Path,
    client_secrets: Path | None=None,
    credentials: Path | None=None,
    thumbnail: Path | None=None,
    playlist: str | None=None,
    chunksize: int=1024*1024*8,
    **raw_metadata
) -> None:
    data_home = Path(os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")))
    data_home.mkdir(exist_ok=True)
    self_home = data_home / "yt-upload"
    self_home.mkdir(exist_ok=True)

    if client_secrets is None:
        client_secrets = self_home / "client_secrets.json"
    if credentials is None:
        credentials = self_home / "credentials.json"

    youtube_api = build_youtube_resource(client_secrets, credentials)
    metadata = parse_upload_metadata(title=raw_metadata.pop("title") or video_to_upload.name, **raw_metadata)
    video_id = upload(youtube_api, video_to_upload, metadata, chunksize=chunksize)
    print(WATCH_VIDEO_URL.format(id=video_id))

    if thumbnail is not None:
        youtube_api.thumbnails().set(videoId=video_id, media_body=thumbnail).execute()
    if playlist is not None:
        add_video_to_playlist(youtube_api, video_id, title=playlist, visibility=metadata["visibility"])


if __name__ == "__main__":
    cli_main()

