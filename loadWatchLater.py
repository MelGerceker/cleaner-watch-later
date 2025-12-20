from pathlib import Path
import csv
import json

CSV_PATH = Path("personalData/watch-later.csv")
OUT_JSON = Path("data/watch_later_ids.json")

#Returns ordered list of video IDs
#Column names: Video ID,Added Date

def load_watch_later_ids(path: Path = CSV_PATH) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at: {path}")

    ids: list[str] = []
    seen: set[str] = set()

    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)

        expected = {"Video ID", "Added Date"}
        if not r.fieldnames or set(map(str.strip, r.fieldnames)) != expected:
            raise ValueError(
                f"Expected headers {expected}, got {r.fieldnames}. "
                "Ensure the CSV has exactly: 'Video ID,Added Date'."
            )

        for row in r:
            vid = (row["Video ID"] or "").strip()
            if vid and vid not in seen:
                seen.add(vid)
                ids.append(vid)

    return ids

def main():
    ids = load_watch_later_ids(CSV_PATH)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(ids, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(ids)} IDs → {OUT_JSON.resolve()}")


if __name__ == "__main__":
    main()
