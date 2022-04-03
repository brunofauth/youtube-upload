from __future__ import annotations

import math
import sys
import os

from contextlib import suppress
from pathlib import Path
from typing import Any, Iterable

from googleapiclient.discovery import Resource
from googleapiclient.http import MediaFileUpload, HttpRequest, ResumableUploadError
from tqdm import tqdm

from .log import logger


# def _iter_request_chunks(request: HttpRequest) -> Iterable[tuple[ResumableMediaStatus, dict[str, Any]]]:
def _iter_request_chunks(request: HttpRequest, num_retries: int) -> Iterable[tuple[Any, dict[str, Any]]]:
    response = None
    while response is None:
        status, response = request.next_chunk(num_retries=num_retries)
        yield status, response


# https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.videos.html
def upload(resource: Resource, video: Path, metadata: dict[str, Any], chunksize: int=4*1024*1024, max_retries: int=3) -> str:
    media = MediaFileUpload(video, chunksize=chunksize, resumable=True, mimetype="application/octet-stream")
    request: HttpRequest = resource.videos().insert(part=",".join(metadata.keys()), body=metadata, media_body=media)
    total_chunks = math.ceil(os.path.getsize(video) / chunksize)

    for _ in range(max_retries):
        try:
            for _, response in tqdm(_iter_request_chunks(request, max_retries), total=total_chunks):
                pass
            else:
                return response["id"]
        except Exception as exception:
            logger.warning("Ran into the following exception while uploading a chunk of the video's... retrying.")
            logger.warning("%s: %s", exception, exception.args)
    raise RuntimeError("Couldn't upload file {video!r}, because we ran into too many errors ({max_retries!r})")

