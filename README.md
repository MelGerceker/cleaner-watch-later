# Cleaner Watch Later

A Python + HTML tool to clean up and inspect your YouTube **Watch Later** playlist by showing only the **unwatched videos**.  
YouTube doesn’t natively provide this feature - this tool parses your data and surfaces the difference between *watched* and *unwatched* videos.

---

## Features
- Parse YouTube **Watch Later** and **Watch History** data.
- Compare watched vs. unwatched items.
- Cache metadata (video titles, channel names, thumbnails).
- Simple browser interface (`index.html`) to visualize results.
- Organized output files stored in the `data/` folder for inspection and reuse.

---

## Repository Structure
```
├── auth.py     # Handles authentication with the YouTube API
├── detailedWatchLater.py     # Loads/caches metadata for Watch Later videos
├── historyParser.py     # Parses watched video IDs from history
├── loadWatchLater.py     # Loads Watch Later IDs
├── saveHistory.py     # Saves history data to JSON
├── testForAPI.py     # Initial API test script
├── testForHistory.py     # History parsing test script
├── index.html     # Browser interface to display results
├── style.css     # Styling for the browser interface
├── data/     # Stores cached data (JSON, CSV, etc.)
│ ├── meta_cache.json
│ ├── watch_later_ids.json     # From loadWatchLater.py
│ ├── watch-later.csv     # Data from Google Takout
│ ├── watched_ids.json     # From saveHistory.py
│ ├── watch-history.html     # Data from Google Takout

```
## Example Preview

<img width="1517" height="413" alt="image" src="https://github.com/user-attachments/assets/242b2446-6e45-49b5-b6ad-c672079337a6" />
