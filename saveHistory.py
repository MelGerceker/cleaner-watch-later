# save_history.py
from pathlib import Path
import json
from historyParser import load_watched_ids_from_html

DATA = Path("data")
HISTORY_HTMLS = [Path("personalData/watch-history.html")]

def save_watched_ids(ids: set[str]):
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA/"watched_ids.json").write_text(
        json.dumps(sorted(ids), ensure_ascii=False, indent=2), encoding="utf-8"
    )

def main():
    all_ids: set[str] = set()
    for p in HISTORY_HTMLS:
        all_ids |= load_watched_ids_from_html(p)
    save_watched_ids(all_ids)
    print(f"Saved {len(all_ids)} watched IDs to data/watched_ids.json")

if __name__ == "__main__":
    main()
