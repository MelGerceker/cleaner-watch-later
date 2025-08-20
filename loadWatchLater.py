from pathlib import Path
import csv

CSV_PATH = Path("personalData/watch-later.csv")

#Returns ordered list of video IDs
#Column names: Video ID and Added Date

def load_watch_later_ids(path: Path = CSV_PATH) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at: {path}")

    ids: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)

        expected = {"Video ID", "Added Date"}
        if not r.fieldnames or set(map(str.strip, r.fieldnames)) != expected:
            raise ValueError(
                f"Expected headers {expected}, got {r.fieldnames}. "
                "Ensure the CSV has exactly: 'Video ID,Added Date'."
            )

        seen: set[str] = set()
        for row in r:
            vid = (row["Video ID"] or "").strip()
            if vid and vid not in seen:
                seen.add(vid)
                ids.append(vid)

    return ids


if __name__ == "__main__":
    vids = load_watch_later_ids()
    print(f"Loaded {len(vids)} IDs.")
    print("Sample:", vids[:5])
