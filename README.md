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
├── index.html     # Browser interface to display results
├── style.css     # Styling for the browser interface
├── testing/    # Includes testing for API calls and watch history parser
├── data/     # Stores cached data (JSON, CSV, etc.)
│ ├── meta_cache.json
│ ├── watch_later_ids.json     # From loadWatchLater.py
│ ├── watch-later.csv     # Data from Google Takout
│ ├── watched_ids.json     # From saveHistory.py
│ ├── watch-history.html     # Data from Google Takout

```
## Example Preview

<img width="1517" height="413" alt="image" src="https://github.com/user-attachments/assets/242b2446-6e45-49b5-b6ad-c672079337a6" />

## How to Run
````
git clone https://github.com/MelGerceker/cleaner-watch-later.git
cd cleaner-watch-later

python -m venv .venv
.\.venv\Scripts\activate.bat

pip install -r requirements.txt
````
To add Youtube API credentials:

1. Go to: https://console.cloud.google.com
2. Create credentials → OAuth Client ID
3. Download the JSON and save it as: client_secret.json

token.json will be automatically created by auth flow during the first run, if it expires delete the json and login again.

Run the preferred python files to load, parse, and build your data.
Recommended to run index.html with VS Code Live Server.
