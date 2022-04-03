from __future__ import annotations

import webbrowser
import sys

from contextlib import redirect_stdout
from getpass import getpass
from pathlib import Path
from typing import Callable

import httplib2

from oauth2client.client import OAuth2Credentials, Credentials, Flow, OOB_CALLBACK_URN, flow_from_clientsecrets
from oauth2client.file import Storage
from googleapiclient.discovery import Resource, build as build_resource


YOUTUBE_UPLOAD_SCOPE = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"]


def get_oauth2_token(url: str) -> str:
    webbrowser.open_new_tab(url)
    with redirect_stdout(sys.stderr):
        return getpass("Paste here the OAuth2 token (won't be echoed): ")


def _fetch_credentials(storage: Storage, flow: Flow) -> OAuth2Credentials:
    """Return the credentials asking the user."""
    flow.redirect_uri = OOB_CALLBACK_URN
    credentials = flow.step2_exchange(get_oauth2_token(flow.step1_get_authorize_url()), http=None)
    storage.put(credentials)
    credentials.set_store(storage)
    return credentials


def _load_credentials(storage: Storage) -> Credentials | None:
    """Return the user credentials. If not found, run the interactive flow."""
    existing_credentials: Credentials | None = storage.get()
    if existing_credentials is None or existing_credentials.invalid:
        raise RuntimeError("InvalidCredentials")
    return existing_credentials


def build_youtube_resource(client_secrets: Path, credentials_file: Path) -> Resource:
    """Authenticate and return a googleapiclient.discovery.Resource object."""
    storage = Storage(credentials_file)
    if (credentials := _load_credentials(storage)) is None:
        flow = flow_from_clientsecrets(client_secrets, scope=YOUTUBE_UPLOAD_SCOPE)
        credentials = _fetch_credentials(storage, flow)

    # http_client = httplib2.Http()
    # http_client.redirect_codes = httplib.redirect_codes - {308}
    # authorized_client = credentials.authorize(http_client)
    # return build_resource(serviceName="youtube", version="v3", http=authorized_client)

    return build_resource(serviceName="youtube", version="v3", credentials=credentials)

