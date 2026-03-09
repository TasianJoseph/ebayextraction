from api import run_brand_search
from transform import transform_all
from load import load_brands, load_listings, load_sales


def main():
    print("\n" + "=" * 60)
    print("  Starting process: ")
    print("=" * 60)

    # Step 1: Extracting data from API:
    print("\n[1/3] Extrac data from eBay API...")
    raw_active, raw_sold = run_brand_search()
    print(f"  Active listings fetched: {len(raw_active)}")
    print(f"  Sold listings fetched:   {len(raw_sold)}")

    # Step 2: Transforming the data from API into conventions:
    print("\n[2/3] TRANSFORMING data...")
    brands, listings, sales = transform_all(raw_active, raw_sold)

    # Step 3: Loading the data
    print("\n[3/3] LOADING data into PostgreSQL...")
    brand_lookup = load_brands(brands)
    load_listings(listings, brand_lookup)
    load_sales(sales)

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
