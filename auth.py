from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CLIENT_SECRET_FILE = Path("client_secret.json")  # download from Google Cloud Console
TOKEN_FILE = Path("token.json")  # created after first login

#TODO: Catch RefreshError 
def get_credentials() -> Credentials:

    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no creds or invalid, either refresh or run browser login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                raise FileNotFoundError(
                    "client_secret.json not found. "
                    "Download it from Google Cloud → Credentials → OAuth client ID."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next runs
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return creds
