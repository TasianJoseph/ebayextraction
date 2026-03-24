import json
import psycopg2
import os
# loading the database credentials


def load_credentials(db_creds="db_creds.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    creds_path = os.path.join(script_dir, db_creds)
    with open(creds_path) as credentials:
        return json.load(credentials)


def db_connection():
    credentials = load_credentials()
    return psycopg2.connect(**credentials)


# inserts brands into the brand table and returns a look-up dictionary to map brand_name and brand_id to use in the
# load_listings
def load_brands(transformed_brands):
    connect = db_connection()
    try:
        with connect:
            with connect.cursor() as cursor:
                insert_data = """
                INSERT INTO brands (brand_name, brand_type)
                VALUES (%(brand_name)s, %(brand_type)s)
                ON CONFLICT (brand_name) DO NOTHING;
                """
                cursor.executemany(insert_data, transformed_brands)

                # querying to ask postgres to return the columns brand_ids postgresql assigned to each brand_name to
                # returning all the relevant rows - returns them as tuples ([1, Balenciaga])

                cursor.execute("SELECT brand_id, brand_name FROM brands")
                brand_lookup = {row[1]: row[0] for row in cursor.fetchall()}

        print(f"  Brands loaded: {len(brand_lookup)}")
        return brand_lookup

    finally:
        connect.close()


# this function uses the load_brands function's brand dictionary from the databases allocated brand_ids to insert the
# listings into the db listings table

def load_listings(transformed_listings, brand_lookup):
    connect = db_connection()
    try:
        with connect:
            with connect.cursor() as cursor:
                listings_to_insert = []
                for listing in transformed_listings:
                    brand_name = listing.get("brand_name")
                    listings_to_insert.append({
                        "brand_id": brand_lookup[brand_name],
                        "title": listing["title"],
                        "price": listing["price"],
                        "currency": listing["currency"],
                        "condition": listing["condition"],
                        "url": listing["url"],
                        "listing_type": listing["listing_type"],
                        "listing_status": listing["listing_status"],
                        "snapshot_date": listing["snapshot_date"],
                        "search_week": listing["search_week"]
                    })

                    insert_query = """
                        INSERT INTO listings (
                        brand_id, title, price, currency, condition, url, listing_type, listing_status, snapshot_date,
                        search_week
                        )
                        VALUES (
                        %(brand_id)s, %(title)s, %(price)s, %(currency)s, %(condition)s, %(url)s, %(listing_type)s,
                        %(listing_status)s, %(snapshot_date)s, %(search_week)s
                        );
                    """
                cursor.executemany(insert_query, transformed_listings)

        print(f"  Listings loaded: {len(transformed_listings)}")

    finally:
        connect.close()

# inserting sold listings into the sales table


def load_sales(transformed_sales):
    if not transformed_sales:
        print("  No sales data to load — skipping.")
        return

    connect = db_connection()
    try:
        with connect:
            with connect.cursor() as cursor:
                insert_query = """
                                       INSERT INTO sales (
                                           listing_id, sold_price, sold_currency, sold_date, snapshot_date
                                       )
                                       VALUES (
                                           %(listing_id)s, %(sold_price)s, %(sold_currency)s, %(sold_date)s, 
                                           %(snapshot_date)s
                                       )
                                       ON CONFLICT (sale_id) DO UPDATE SET
                                           listing_id      = EXCLUDED.listing_id,
                                           sold_price      = EXCLUDED.sold_price,
                                           sold_currency   = EXCLUDED.sold_currency,
                                           sold_date       = EXCLUDED.sold_date,
                                           snapshot_date   = EXCLUDED.snapshot_date;
                                   """
                cursor.executemany(insert_query, transformed_sales)

        print(f"  Sales loaded: {len(transformed_sales)}")

    finally:
        connect.close()
