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


# Returns: video_id: {"title": str, "channel": str, "duration":str}
def _fetch_video_meta(youtube, ids: list[str]) -> dict[str, dict[str, str]]:
    meta: dict[str, dict[str, str]] = {}

    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i+BATCH_SIZE]
        try:
            resp = youtube.videos().list(
                part="snippet,contentDetails",
                id=",".join(batch),
                maxResults=BATCH_SIZE 
            ).execute()
        except HttpError as e:
            print(f"[WARN] videos.list failed for batch starting {i}: {e}")
            continue

        for item in resp.get("items", []):
            vid = item.get("id")
            sn = item.get("snippet", {})
            cd = item.get("contentDetails", {})
            if not vid:
                continue
            meta[vid] = {
                "title": sn.get("title", ""),
                "channel": sn.get("channelTitle", ""),
                "duration": cd.get("duration",""),
            }
    return meta

# Load cache, fetch missing and save
def _ensure_meta_cache(ids: list[str]) -> dict[str, dict[str, str]]:
    cache: dict[str, dict[str, str]] = _load_json(META_CACHE, {})
    missing = [v for v in ids if v not in cache or "duration" not in cache[v]]
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
        info = meta.get(vid, {"title": "(unavailable)", "channel": "", "duration":""},)
        duration,approxdur =  _parse_iso_duration(info.get("duration", ""))
        out.append({
            "id": vid,
            "title": info["title"],
            "channel": info["channel"],
            "duration":duration,
            "approxdur":approxdur,
            "url":  f"https://youtu.be/{vid}",
            "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
        })
    return out

#Convert Youtube API duration ISO: ex. from PT2H34M12S to 2:34:12
#returns tuple: first value for display, second value for filtering
def _parse_iso_duration(iso_str):
    hours = 0
    minutes = 0
    seconds = 0
    
    #empty
    if not iso_str:
        return ("", None)
    
    if not iso_str.startswith("PT"):
        print(f"[WARN] Unexpected duration format: {iso_str!r}")
        return ("", None)
    
    iso_array = iso_str.split("PT")[1] # remove PT
    
    if iso_array.find("H") != -1:
        hours = int(iso_array.split("H")[0])
        iso_array=iso_array.split("H")[1] # after H
        
    if iso_array.find("M") != -1:
        minutes = int(iso_array.split("M")[0])
        iso_array=iso_array.split("M")[1] # after M
    
    if iso_array.find("S") != -1:
        seconds = int(iso_array.split("S")[0])
        
    # For duration filtering:
    aproximateDuration = hours*60 + minutes

    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}",aproximateDuration
    elif minutes > 0:
        return f"{minutes}:{seconds:02}",aproximateDuration
    else:
        return f"{seconds}s", aproximateDuration
    
    
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
