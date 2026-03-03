import requests
import base64
import json  # importing packages needed to read json credentials/encode+decode and call the api


# 1. getting access token using the client credentials method:
def get_access_token():

    with open("api_creds.json", "r") as credentials:
        api_creds = json.load(credentials)

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

    def get_client_id():
        with open ("api_creds.json", "r") as credentials2:
            api_creds = json.load(credentials2)
            return api_creds["app_client_id"]

    response.raise_for_status()

    access_token = response.json().get("access_token")
    if not access_token:
        raise ValueError(f"Failed to get token: {response.json()}")

    return access_token




