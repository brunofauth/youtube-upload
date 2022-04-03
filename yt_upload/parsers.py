from __future__ import annotations

import sys

from datetime import datetime
from typing import Any

import click


CATEGORY_ID = {
    "Film & Animation": 1, "Autos & Vehicles": 2, "Music": 10, "Pets & Animals": 15,
    "Sports": 17, "Short Movies": 18, "Travel & Events": 19, "Gaming": 20,
    "Videoblogging": 21, "People & Blogs": 22, "Comedy": 23, "Entertainment": 24,
    "News & Politics": 25, "Howto & Style": 26, "Education": 27, "Science & Technology": 28,
    "Nonprofits & Activism": 29, "Movies": 30, "Anime/Animation": 31, "Action/Adventure": 32,
    "Classics": 33, "Documentary": 35, "Drama": 36, "Family": 37, "Foreign": 38, "Horror": 39,
    "Sci-Fi/Fantasy": 40, "Thriller": 41, "Shorts": 42, "Shows": 43, "Trailers": 44}


def validate_genre(ctx: click.Context, param: str, value: str) -> int | None:
    if value is None:
        return value
    try:
        return CATEGORY_ID[value]
    except KeyError as error:
        raise ValueError(f"{param!r} must be one of: {list(CATEGORY_ID.keys())!r}") from error


def print_genres(ctx: click.Context, param: str, value: str) -> int | None:
    if not value or ctx.resilient_parsing:
        return
    click.echo("Available genres:", file=sys.stdout)
    for categ in CATEGORY_ID.keys():
        click.echo(f"    {categ!r}", file=sys.stdout)
    ctx.exit()


def _set_if_not_none(d: dict[str, Any], key: str, value: Any) -> None:
    if value is not None:
        d[key] = value


def parse_upload_metadata(
    title: str,
    description: str | None=None,
    genre: int | None=None,
    tags: list[str] | None=None,
    language: str | None=None,
    audio_language: str | None=None, 

    embeddable: bool=False,
    visibility: str="private",
    date_to_publish: datetime | None=None, 
    license: str="youtube", 

    recording_date: datetime | None=None, 
    location_latitude: float | None=None,
    location_longitude: float | None=None,
    location_altitude: float | None=None
) -> dict[str, Any]:
    snippet = {"title": title}
    _set_if_not_none(snippet, "description",          description)
    _set_if_not_none(snippet, "categoryId",           genre)
    _set_if_not_none(snippet, "tags",                 tags)
    _set_if_not_none(snippet, "defaultLanguage",      language)
    _set_if_not_none(snippet, "defaultAudioLanguage", audio_language)

    status = {"embeddable": embeddable, "privacyStatus": visibility, "license": license}
    if date_to_publish is not None:
        status["publishAt"] = date_to_publish.isoformat()

    location: dict[str, float] = {}
    _set_if_not_none(location, "latitude",  location_latitude)
    _set_if_not_none(location, "longitude", location_longitude)
    _set_if_not_none(location, "altitude",  location_altitude)

    recording_details = {"location": location}
    if recording_date is not None:
        status["recordingDate"] = recording_date.isoformat()

    return {"snippet": snippet, "status": status, "recordingDetails": recording_details}
