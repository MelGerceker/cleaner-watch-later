from pathlib import Path
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials

#Paths
DATA_DIR   = Path("data")
IDS_JSON   = DATA_DIR / "watch_later_ids.json"
META_CACHE = DATA_DIR / "meta_cache.json"
OUT_JSON   = DATA_DIR / "detailed-watch-later.json"

BATCH_SIZE = 50

def _load_json(p: Path, default):
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return default

def _save_json(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


# Returns: video_id: {"title": str, "channel": str}
def _fetch_video_meta(youtube, ids: list[str]) -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}

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

# Load cache, fetch missing and save
def _ensure_meta_cache(ids: list[str]) -> dict[str, dict[str, str]]:
    cache: dict[str, dict[str, str]] = _load_json(META_CACHE, {})
    missing = [v for v in ids if v not in cache]
    if missing:
        # auth
        creds = get_credentials()
        yt = build("youtube", "v3", credentials=creds)
        fetched = _fetch_video_meta(yt, missing)
        cache.update(fetched)
        _save_json(META_CACHE, cache)
        print(f"meta_cache: +{len(fetched)} (total {len(cache)})")
    else:
        print(f"meta_cache already covers all {len(ids)} IDs.")
    return cache

# Returns render ready (detailed) list in order
def _build_detailed(ids: list[str], meta: dict[str, dict[str, str]]) -> list[dict]:
    out = []
    for vid in ids:
        info = meta.get(vid, {"title": "(unavailable)", "channel": ""})
        out.append({
            "id": vid,
            "title": info["title"],
            "channel": info["channel"],
            "url":  f"https://youtu.be/{vid}",
            "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
        })
    return out


def main():
    ids: list[str] = _load_json(IDS_JSON, [])
    if not ids:
        raise SystemExit(f"No IDs found. Run loadWatchLater.py to create {IDS_JSON}.")

    meta = _ensure_meta_cache(ids)
    detailed = _build_detailed(ids, meta)
    _save_json(OUT_JSON, detailed)
    print(f"Wrote {len(detailed)} items → {OUT_JSON.resolve()}")

if __name__ == "__main__":
    main()
