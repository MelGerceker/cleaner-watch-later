from pathlib import Path
from typing import Set, Optional
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

# Returns video ID from url
def _extract_video_id(url: str) -> Optional[str]:
    if not url:
        return None
    u = urlparse(url)
    host = (u.netloc or "").lower()
    
    # normal links like https://www.youtube.com/watch?v=abc123
    if "youtube.com" in host and u.path == "/watch":
        return parse_qs(u.query).get("v", [None])[0]
    
    # short links like https://youtu.be/abc123
    if "youtu.be" in host and u.path:
        return u.path.lstrip("/")
    
    return None

# Scans watch-history.html for links, returns set of normalized IDs
def load_watched_ids_from_html(path: Path) -> Set[str]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "lxml")

    ids: Set[str] = set()
    for a in soup.find_all("a", href=True):
        vid = _extract_video_id(a["href"])
        if vid:
            ids.add(vid)

    return ids
