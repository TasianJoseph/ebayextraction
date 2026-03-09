from datetime import datetime
from datetime import date

# setting up the snapshot constraints
snapshot_date = datetime.now()
search_week = date.today()

# the brand categories

brand_categories = {
    "Balenciaga": "designer",
    "Loewe": "designer",
    "The Row": "designer",
    "Corteiz": "streetwear",
    "Stussy": "streetwear",
    "Supreme": "streetwear"
}

# returning fixed list of brand dictionaries to insert into the brands table


def transform_brands():
    return [
        {"brand_name": brand_name, "brand_type": brand_type}
        for brand_name, brand_type in brand_categories.items()
    ]


# mapping the raw browse listing fields to the listings table schema

def transform_listings(raw_active):
    listings = []

    for item in raw_active:
        listings.append({
            "brand_name":           item.get("_brand"),
            "title":                item.get("title"),
            "price":                float(item.get("price", {}).get("value", 0)),  # converting a string into a number
            "currency":             item.get("price", {}).get("currency", "GBP"),
            "condition":            item.get("condition", "Not Specified"),
            "url":                  item.get("itemWebUrl"),
            "listing_type":         item.get("buyingOptions", [None])[0],  # e.g. FIXED_PRICE, AUCTION
            "listing_status":       item.get("_listing_type"),  # "active"
            "snapshot_date":        snapshot_date,
            "search_week":          search_week
        })

    return listings

# mapping the raw Finding API sold listing fields to the sales table schema


def transform_sales(raw_sold):
    # Placeholder — Finding API response structure differs from Browse API
    # Will be implemented once sold listings are accessible
    sales = []
    return sales

# will be called by the main.py script to return all 3 lists ready to load into postgresql


def transform_all(raw_active, raw_sold):
    brands   = transform_brands()
    listings = transform_listings(raw_active)
    sales    = transform_sales(raw_sold)

    print(f"  Brands to insert:   {len(brands)}")
    print(f"  Listings to insert: {len(listings)}")
    print(f"  Sales to insert:    {len(sales)}")

    return brands, listings, sales
