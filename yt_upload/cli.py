from __future__ import annotations

import os
from functools import partial
from pathlib import Path
import click

from .auth import build_youtube_resource_from_files, build_youtube_resource_from_pass
from .playlists import add_video_to_playlist
from .parsers import parse_upload_metadata, validate_category, CATEGORY_ID
from .upload import upload
from .__version__ import __version__


WATCH_VIDEO_URL = "https://www.youtube.com/watch?v={id}"
PATH_PARAM_TYPE = click.Path(exists=True, dir_okay=False, path_type=Path, resolve_path=True)
Choice = partial(click.Choice, case_sensitive=False)


@click.command()
@click.argument("video-to-upload", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.version_option(__version__)

# Video Metadata
@click.option('-t', "--title")
@click.option('-g', "--genre", "category", type=Choice(list(CATEGORY_ID.keys())), callback=validate_category, default=None)
@click.option('-d', "--description", default=None)
@click.option("-p", '--playlist', help="add video to <playlist>, creating it if non-existent", default=None)
@click.option("-n", '--thumbnail', type=click.Path(exists=True, dir_okay=False, path_type=Path), help='.jpg or .png', default=None)
@click.option("-T", "--tag", "tags", multiple=True, help="this option may be used several times", default=None)
@click.option("-D", '--date-to-publish', type=click.DateTime(), default=None, help="formatted like ISO 8601")
@click.option("-r", '--recording-date', type=click.DateTime(), default=None, help="formatted like ISO 8601")
@click.option("-l", '--language', default=None, help="ISO 639-1: <en|fr|de|pt|...>")
@click.option("-a", '--audio-language', default=None, help="ISO 639-1: <en|fr|de|pt|...>")
@click.option("-L", '--license', type=Choice(['youtube', 'creativeCommon']), default='youtube')
@click.option('--location-latitude', default=None, type=float)
@click.option('--location-longitude', default=None, type=float)
@click.option('--location-altitude', default=None, type=float)

# Other Video Options
@click.option("-V", '--visibility', type=click.Choice(["public", "unlisted", "private"], case_sensitive=False), default="public")
@click.option("-e", '--embeddable', type=bool, default=False, help='make video is embeddable')

# Authentication
@click.option("-s", '--client-secrets-file', type=PATH_PARAM_TYPE, help='Secrets JSON file', default=None)
@click.option("-c", '--credentials-file', type=PATH_PARAM_TYPE, help='Credentials JSON file', default=None)
@click.option("-S", '--client-secrets-pass', help="client secrets entry in 'pass'", default=None)
@click.option("-C", '--credentials-pass', help="credentials entry in 'pass'", default=None)

# Miscellaneous
@click.option('--chunksize', type=int, default=1024*1024*8, help='Progress bar step, in bytes')
def cli_main(*args, **kwargs) -> None:
    return main(*args, **kwargs)


def main(
    video_to_upload: Path,
    client_secrets_file: Path | None=None,
    credentials_file: Path | None=None,
    client_secrets_pass: str | None=None,
    credentials_pass: str | None=None,
    thumbnail: Path | None=None,
    playlist: str | None=None,
    chunksize: int=1024*1024*8,
    **raw_metadata
) -> None:
    data_home = Path(os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share")))
    data_home.mkdir(exist_ok=True)
    self_home = data_home / "yt-upload"
    self_home.mkdir(exist_ok=True)

    if client_secrets_pass is not None and credentials_pass is not None:
        youtube_api = build_youtube_resource_from_pass(client_secrets_pass, credentials_pass)
    else:
        if client_secrets_file is None:
            client_secrets_file = self_home / "client_secrets.json"
        if credentials_file is None:
            credentials_file = self_home / "credentials.json"
        youtube_api = build_youtube_resource_from_files(client_secrets_file, credentials_file)

    metadata = parse_upload_metadata(title=raw_metadata.pop("title") or video_to_upload.name, **raw_metadata)
    video_id = upload(youtube_api, video_to_upload, metadata, chunksize=chunksize)
    print(WATCH_VIDEO_URL.format(id=video_id))

    if thumbnail is not None:
        youtube_api.thumbnails().set(videoId=video_id, media_body=thumbnail).execute()
    if playlist is not None:
        add_video_to_playlist(youtube_api, video_id, title=playlist, visibility=metadata["visibility"])


if __name__ == "__main__":
    cli_main()

