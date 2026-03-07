import time
import requests
from api_config import get_access_token, get_client_id

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
    """
    Fetches up to 300 active listings for a brand from the Browse API.
    Paginates using offset until target is reached or listings are exhausted.
    """
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_GB",
        "Content-Type": "application/json"
    }

    all_items = []
    offset = 0       # starting with the very first item in the list
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
    """
    Fetches up to 300 sold listings for a brand from the Finding API.
    Paginates using page_number until target is reached or pages are exhausted.
    """
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

        # Navigate Finding API's nested response structure
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


def print_item(item):
    """Prints a single transformed item's key fields in a readable format."""
    print(f"    Title:     {item.get('title')}")
    print(f"    Price:     {item.get('price', 'N/A')} {item.get('currency', '')}")
    print(f"    Condition: {item.get('condition', 'N/A')}")
    print(f"    URL:       {item.get('url', 'N/A')}")
    print(f"    {'-' * 55}")


def run_brand_search():
    """
    Loops through all brands, fetches 300 active and 300 sold
    listings per brand, transforms and accumulates all results.
    """
    all_data = []

    for category, brands in BRANDS.items():
        print(f"\n{'=' * 60}")
        print(f"  CATEGORY: {category.upper()}")
        print(f"{'=' * 60}")

        for brand in brands:
            print(f"\n  Brand: {brand}")
            print(f"  {'-' * 55}")

            try:
                # Active listings — Extract then Transform
                print(f"\n  Fetching active listings...")
                raw_active = fetch_active_listings(brand)
                structured_active = transform_items(
                    raw_active, brand, category, listing_type="active"
                )
                print(f"  {len(structured_active)} active listings collected.")

                # Sold listings — Extract then Transform
                print(f"\n  Fetching sold listings...")
                raw_sold = fetch_sold_listings(brand)
                structured_sold = transform_items(
                    raw_sold, brand, category, listing_type="sold"
                )
                print(f"  {len(structured_sold)} sold listings collected.")

                # Preview first 3 active listings
                print(f"\n  Preview (first 3 active listings):")
                for item in structured_active[:3]:
                    print_item(item)

                all_data.extend(structured_active)
                all_data.extend(structured_sold)

            except requests.exceptions.HTTPError as e:
                print(f"  HTTP error fetching {brand}: {e}")

            except Exception as e:
                print(f"  Unexpected error fetching {brand}: {e}")

    total_expected = len(BRANDS["designer"] + BRANDS["streetwear"]) * 2 * TARGET
    print(f"\n{'=' * 60}")
    print(f"  COMPLETE — {len(all_data)} total records collected")
    print(f"  Expected:  {total_expected} records (6 brands x 2 types x 300)")
    print(f"{'=' * 60}\n")

    return all_data


# --- Entry Point ---
if __name__ == "__main__":
    all_data = run_brand_search()