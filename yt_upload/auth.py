from __future__ import annotations

import webbrowser
import sys

from contextlib import redirect_stdout
from getpass import getpass
from pathlib import Path
from typing import Callable, TypeVar

from oauth2client.client import OAuth2Credentials, Credentials, Flow, OOB_CALLBACK_URN, flow_from_clientsecrets, Storage as BaseStorage
from oauth2client.file import Storage
from googleapiclient.discovery import Resource, build as build_resource

from .pass_store import PassStorage, flow_from_pass


T = TypeVar("T", str, Path)


YOUTUBE_UPLOAD_SCOPE = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"]


def get_oauth2_token(url: str) -> str:
    webbrowser.open_new_tab(url)
    with redirect_stdout(sys.stderr):
        print("A new tab on your browser should've appeared, for you to authenticate and get a code.")
        print(f"If it didn't show up, go to {url!r}, to authenticate and get said token.")
        return getpass("Paste here the OAuth2 token (won't be echoed): ")


def _fetch_credentials(storage: BaseStorage, flow: Flow) -> OAuth2Credentials:
    """Return the credentials asking the user."""
    flow.redirect_uri = OOB_CALLBACK_URN
    credentials = flow.step2_exchange(get_oauth2_token(flow.step1_get_authorize_url()), http=None)
    storage.put(credentials)
    credentials.set_store(storage)
    return credentials


def _load_credentials(storage: BaseStorage) -> Credentials | None:
    """Return the user credentials. If not found, run the interactive flow."""
    existing_credentials: Credentials | None = storage.get()
    if existing_credentials is None or existing_credentials.invalid:
        return None
    return existing_credentials


def _build_youtube_resource(
    client_secrets: T,
    raw_credentials: T,
    storage_type: BaseStorage,
    flow_factory: Callable[[T, list[str]], Flow]
) -> Resource:
    storage: BaseStorage = storage_type(raw_credentials)
    if (credentials := _load_credentials(storage)) is None:
        flow = flow_factory(client_secrets, YOUTUBE_UPLOAD_SCOPE)
        credentials = _fetch_credentials(storage, flow)
    return build_resource(serviceName="youtube", version="v3", credentials=credentials)


def build_youtube_resource_from_files(client_secrets: Path, credentials_file: Path) -> Resource:
    """Authenticate and return a googleapiclient.discovery.Resource object."""
    return _build_youtube_resource(client_secrets, credentials_file, Storage, flow_from_clientsecrets)


def build_youtube_resource_from_pass(client_secrets_key: str, credentials_file_key: str) -> Resource:
    """Authenticate and return a googleapiclient.discovery.Resource object."""
    return _build_youtube_resource(client_secrets_key, credentials_file_key, PassStorage, flow_from_pass)

