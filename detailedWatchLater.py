from pathlib import Path
from typing import Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

from auth import get_credentials
from loadWatchLater import load_watch_later_ids

BATCH_SIZE = 50

# Returns: video_id: {"title": str, "channel": str}
def fetch_video_meta(youtube, ids: list[str]) -> Dict[str, Dict[str, str]]:
    meta: Dict[str, Dict[str, str]] = {}

    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i+BATCH_SIZE]
        try:
            resp = youtube.videos().list(
                part="snippet",
                id=",".join(batch),
                maxResults=BATCH_SIZE 
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

# Returns data.json used by index.html
def write_json(ids: list[str], meta: Dict[str, Dict[str, str]], out_file: Path = Path("data.json")):
    data = []
    for vid in ids:
        info = meta.get(vid, {"title": "(unavailable)", "channel": ""})
        data.append({
            "id": vid,
            "title": info["title"],
            "channel": info["channel"],
            "url": f"https://youtu.be/{vid}",
            "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        })
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_file.resolve()} ({len(data)} items)")

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

    # Fetch metadata
    meta = fetch_video_meta(yt, ids)
    write_json(ids, meta, Path("data.json"))

    #missing = [v for v in ids if v not in meta]  # deleted/private/unavailable
    #print(f"Resolved {len(meta)} via API; {len(missing)} missing.")


    # Print a sample
    """
    for vid in ids[:10]:
        info = meta.get(vid, {"title": "(unavailable)", "channel": ""})
        print(f"- {info['title']} — {info['channel']} — https://youtu.be/{vid}")
    """

if __name__ == "__main__":
    main()
