from pathlib import Path
from historyParser import load_watched_ids_from_html

def main():
    path = Path("personalData/watch-history.html")
    ids = load_watched_ids_from_html(path)

    print(f"Found {len(ids)} watched video IDs")
    # Print the first 20 as a sanity check
    for i, vid in enumerate(list(ids)[:20], 1):
        print(f"{i}. https://youtu.be/{vid}")

if __name__ == "__main__":
    main()
