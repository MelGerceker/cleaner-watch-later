from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Least-privilege scope: read-only access to YouTube account
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

CLIENT_SECRET_FILE = Path("client_secret.json")
TOKEN_FILE = Path("token.json") # created after first login

#Returns valid user creditentials for the Youtube API
def get_credentials() -> Credentials:
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no creds or invalid, either refresh or run browser login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh silently using the refresh token
            creds.refresh(Request())
        else:
            # First-time login: open a local browser for OAuth
            # port=0 picks a random free port for the redirect URL
            if not CLIENT_SECRET_FILE.exists():
                raise FileNotFoundError(
                    "client_secret.json not found. "
                    "Download it from Google Cloud → Credentials → OAuth client ID."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
            creds = flow.run_local_server(port=0) #starts HTTP server for OAuth redirect

        # Save the token for next runs
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return creds


def main():
    # Authenticate and build the YouTube client
    creds = get_credentials()
    youtube = build("youtube", "v3", credentials=creds) #allows to make API calls

    # Minimal API call for testing
    # part controls which fields you want; these are common, safe choices
    resp = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    ).execute()

    # Basic sanity check
    items = resp.get("items", [])
    if not items:
        print("No channel found for this account.")
        return

    me = items[0]
    title = me["snippet"]["title"]
    channel_id = me["id"]
    subs = me["statistics"].get("subscriberCount", "unknown")

    print("OAuth success & API call worked.")
    print(f"Authenticated as: {title}")
    print(f"Channel ID:      {channel_id}")
    print(f"Subscribers:     {subs}")


if __name__ == "__main__":
    main()
