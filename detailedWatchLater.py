from pathlib import Path
from typing import Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials
from loadWatchLater import load_watch_later_ids

#TODO: Better error handling and hardcoded batch size of 50

def fetch_video_meta(youtube, ids: list[str]) -> Dict[str, Dict[str, str]]:
    """
    Call videos.list in batches (<=50) and return:
      { video_id: {"title": str, "channel": str} }
    """
    meta: Dict[str, Dict[str, str]] = {}

    for i in range(0, len(ids), 50):
        batch = ids[i:i+50]
        try:
            resp = youtube.videos().list(
                part="snippet",
                id=",".join(batch),
                maxResults=50 
            ).execute()
        except HttpError as e:
            print(f"[WARN] videos.list failed for batch starting {i}: {e}")
            continue

        for item in resp.get("items", []):
            vid = item.get("id")
            sn = item.get("snippet", {})
            if not vid:
                continue
            meta[vid] = {
                "title": sn.get("title", ""),
                "channel": sn.get("channelTitle", "")
            }
    return meta

def main():
    # Auth
    creds = get_credentials()
    yt = build("youtube", "v3", credentials=creds)

    # Load IDs from Takeout CSV
    csv_path = Path("personalData/watch-later.csv")
    ids = load_watch_later_ids(csv_path)
    if not ids:
        print("No IDs found in watch-later.csv")
        return
    print(f"Read {len(ids)} video IDs from Takeout.")

    # Fetch metadata
    meta = fetch_video_meta(yt, ids)
    missing = [v for v in ids if v not in meta]  # deleted/private/unavailable
    print(f"Resolved {len(meta)} via API; {len(missing)} missing.")

    # Print a sample (first 10)
    for vid in ids[:10]:
        info = meta.get(vid, {"title": "(unavailable)", "channel": ""})
        print(f"- {info['title']} — {info['channel']} — https://youtu.be/{vid}")

if __name__ == "__main__":
    main()
