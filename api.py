import time
import requests
from api_config import get_access_token, get_client_id
import json

# --- Constants ---
BROWSE_ENDPOINT = "https://api.ebay.com/buy/browse/v1/item_summary/search"
FINDING_ENDPOINT = "https://svcs.ebay.com/services/search/FindingService/v1"

PAGE_SIZE_ACTIVE = 50
PAGE_SIZE_SOLD = 100
TARGET = 300

# Dictionary of brands for designer and streetwear sample
BRANDS = {
    "designer": ["Balenciaga", "Loewe", "The Row"],
    "streetwear": ["Corteiz", "Stussy", "Supreme"]
}


def fetch_active_listings(query, max_items=TARGET):
    #  Fetching 300 active listings for each brand from the Browse API. Paginates using offset until target is reached.

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB",
        "Content-Type": "application/json"
    }

    all_items = []
    offset = 0  # starting with the very first item in the list
    page_number = 1  # counter for number of page results shown in terminal

    while len(all_items) < max_items:
        print(f"[Active] {query} - page {page_number} ({len(all_items)} fetched so far)...")

        response = requests.get(
            BROWSE_ENDPOINT,
            headers=headers,
            params={
                "q": query,
                "limit": PAGE_SIZE_ACTIVE,
                "offset": offset
            }
        )
        response.raise_for_status()

        # Number of API calls remaining for the day
        remaining = response.headers.get("X-RateLimit-Remaining", "N/A")
        print(f"[Rate Limit Remaining: {remaining}]")

        # Converting the JSON response into a Python dictionary
        data = response.json()
        items = data.get("itemSummaries", [])

        if not items:
            print(f"No more active listings found for {query}.")
            break

        all_items.extend(items)

        if not data.get("next"):
            break

        offset += PAGE_SIZE_ACTIVE
        page_number += 1
        time.sleep(0.5)

    return all_items[:max_items]


def fetch_sold_listings(query, max_items=TARGET, page_size=PAGE_SIZE_SOLD):
    #  Fetching 300 sold listings for each brand from the Browse API. Paginates using offset until target is reached.

    client_id = get_client_id()

    all_items = []
    page_number = 1

    while len(all_items) < max_items:
        print(f"[Sold] {query} - page {page_number} ({len(all_items)} fetched so far)...")

        response = requests.get(
            FINDING_ENDPOINT,
            params={
                "OPERATION-NAME": "findCompletedItems",
                "SERVICE-VERSION": "1.0.0",
                "SECURITY-APPNAME": client_id,
                "RESPONSE-DATA-FORMAT": "JSON",
                "keywords": query,
                "itemFilter(0).name": "SoldItemsOnly",
                "itemFilter(0).value": "true",
                "itemFilter(1).name": "LocatedIn",
                "itemFilter(1).value": "GB",
                "paginationInput.entriesPerPage": page_size,
                "paginationInput.pageNumber": page_number
            }
        )
        response.raise_for_status()

        data = response.json()

        # Navigate Finding APIs nested response structure
        search_result = (
            data
            .get("findCompletedItemsResponse", [{}])[0]
            .get("searchResult", [{}])[0]
        )

        items = search_result.get("item", [])

        if not items:
            print(f"No more sold listings found for {query}.")
            break

        all_items.extend(items)

        total_pages = int(
            data
            .get("findCompletedItemsResponse", [{}])[0]
            .get("paginationOutput", [{}])[0]
            .get("totalPages", [1])[0]
        )

        if page_number >= total_pages:
            break

        page_number += 1
        time.sleep(0.5)

    return all_items[:max_items]


def run_brand_search():
    # Loops through all brands, fetches 300 active and 300 sold listings per brand, transforms and ac

    all_active = []
    all_sold = []

    for category, brands in BRANDS.items():
        print(f"\n{'=' * 60}")
        print(f"  CATEGORY: {category.upper()}")
        print(f"{'=' * 60}")

        for brand in brands:
            print(f"\n  Brand: {brand}")
            print(f"  {'-' * 55}")

            try:
                # Active listings printed
                print(f"\n  Fetching active listings...")
                raw_active = fetch_active_listings(brand)
                for item in raw_active:
                    item["_brand"] = brand
                    item["_category"] = category
                    item["_listing_type"] = "active"
                all_active.extend(raw_active)
                print(f"  {len(raw_active)} active listings collected.")

            except Exception as error:
                print(f" Unexpected error fetching {brand}: {error}")

            try:
                # Sold listings printed
                print(f"\n  Fetching sold listings...")
                raw_sold = fetch_sold_listings(brand)
                for item in raw_sold:
                    item["_brand"] = brand
                    item["_category"] = category
                    item["_listing_type"] = "sold"
                all_sold.extend(raw_sold)
                print(f"  {len(raw_sold)} sold listings collected.")
            except requests.exceptions.HTTPError as error:
                print(f" Unexpected error fetching {brand}: {error}")

                # Tagging each item with brand + category before returning because the raw api response omits this info





                # Adds each brand list together and returns them as one result, using extend adds each item individually







    # returned is 6 brands, 2 types of listing (active/sold), with a target of 300 listings each
    # so the total should be 3600
    total = len(all_active) + len(all_sold)
    total_expected = len(BRANDS["designer"] + BRANDS["streetwear"]) * 2 * TARGET
    print(f"\n{"=" * 60}")
    print(f"  COMPLETE - {total} total records collected.")
    print(f"  Expected {total_expected} records (6 brands x 2 brand types x 300 listings)")
    print(f"{"=" * 60}\n")

    return all_active, all_sold


# --- Entry Point ---
if __name__ == "__main__":
    raw_active, raw_sold = run_brand_search()

    if raw_active:
        print(json.dumps(raw_active[0], indent=2))
    else:
        print("No active listings returned")

    if raw_sold:
        print(json.dumps(raw_sold[0], indent=2))
    else:
        print("No sold listings returned")