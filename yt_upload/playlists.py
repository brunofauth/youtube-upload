from __future__ import annotations

from googleapiclient.discovery import Resource


def get_playlist(youtube: Resource, title: str) -> str | None:
    """Return users's playlist ID by title (None if not found)"""
    playlists = youtube.playlists()
    request = playlists.list(mine=True, part="id,snippet")
    
    while request:
        results = request.execute()
        titles = (item["id"] for item in results["items"] if item["snippet"]["title"] == title)
        if (match := next(titles, None)) is not None:
            return match
        request = playlists.list_next(request, results)
    return None


def create_playlist(youtube: Resource, title: str, visibility: str="public") -> str:
    metadata = {"snippet": {"title": title}, "status": {"privacyStatus": visibility}}
    response = youtube.playlists().insert(part="snippet,status", body=metadata).execute()
    return response["id"]
    

def add_video_to_playlist(youtube: Resource, video_id: str, title: str, visibility: str="public"):
    """Add video to playlist (by title) and return the full response."""
    playlist_id = get_playlist(youtube, title) or create_playlist(youtube, title, visibility)
    return youtube.playlistItems().insert(part="snippet", body={
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {"kind": "youtube#video", "videoId": video_id}
        }
    }).execute()

