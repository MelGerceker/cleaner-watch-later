from pathlib import Path
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials
from detailedWatchLater import _save_json, _ensure_meta_cache, _build_detailed, META_CACHE


OUT_JSON   = Path("data/sudoku-uploads.json")

# TODO: Fill with the real channel ID, but does youtube use @handle now?
# TODO: Get this input from user?
CHANNEL_ID = "UCC-UOdK8-mIjxBQm_ot1T-Q"

BATCH_SIZE = 50


def _get_uploads_playlist_id(youtube, channel_id: str) -> str | None:

    try:
        resp = youtube.channels().list(part="contentDetails", id = channel_id).execute()
    except HttpError as e:
            print(f"Failed to fetch channel info for {channel_id}: {e}")
            return None
        
    items = resp.get("items", [])
    if not items:
        return None
    
    item = items[0]
    
    uploads_id = (
    item.get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads")
    )

    return uploads_id



def _fetch_all_upload_ids(youtube, uploads_playlist_id: str) -> list[str]:
    
    all_ids = []
    page_token = None
    
    while True:
        try:
            resp = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=page_token
            ).execute()
            
            for item in resp.get("items", []):
                vid = item.get("snippet", {}).get("resourceId", {}).get("videoId")

                if not vid:
                    continue
                all_ids.append(vid)

            #show progress
            print(f"Fetched {len(all_ids)} items total so far.")

            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        
        except HttpError as e:
            print("Failed to fetch all videos due to API error")
            break
    
    return all_ids



def main() -> None:

    # Auth
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds)

    # Get uploads playlist
    uploads_id = _get_uploads_playlist_id(youtube, CHANNEL_ID)
    if not uploads_id:
        raise SystemExit(f"Could not find uploads playlist for channel {CHANNEL_ID}")
    
    #for testing:
    print(f"Uploads playlist ID: {uploads_id}")

    # Fetch all upload IDs
    ids = _fetch_all_upload_ids(youtube, uploads_id)
    if not ids:
        print(f"No uploads found for channel {CHANNEL_ID}")
        return

    meta = _ensure_meta_cache(ids)

    # Current format [{"id", "title", "channel", "url", "thumb"}]
    # TODO: Add duration of vids?
    detailed = _build_detailed(ids, meta)
    _save_json(OUT_JSON, detailed)
    print(f"Wrote {len(detailed)} items → {OUT_JSON.resolve()}")

    pass


if __name__ == "__main__":
    main()
