import requests
import base64
import json  # importing packages needed to read json credentials/encode+decode and call the api


# 1. reading the credentials json so that the file is opened once for use for the client credentials and access token:
def load_credentials():
    with open("api_creds.json", "r") as credentials:
        return json.load(credentials)

# returning the client id from the credentials json to use the FindingAPI for sold listings:


def get_client_id():
    api_creds = load_credentials()
    return api_creds["app_client_id"]


# returning the client credentials access token from the credentials json to authenticate and use the BrowseAPI:

def get_access_token():
    api_creds = load_credentials()

    client_id = api_creds["app_client_id"]
    client_secret = api_creds["client_secret"]

    encoded_credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode()

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope"
        }
    )
    response.raise_for_status()

    access_token = response.json().get("access_token")
    if not access_token:
        raise ValueError(f"Failed to get token: {response.json()}")

# completing the function.
    return access_token
