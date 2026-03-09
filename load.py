import json
import psycopg2

# loading the database credentials
def load_credentials(db_creds):
    with open(db_creds) as credentials:
        return json.load(credentials)


def db_connection():
    credentials = load_credentials()
    return psycopg2.connect(credentials)


def load_brands(transformed_brands):
    connect = db_connection()
    try:
        with connect:
            with connect.cursor() as cursor:
                insert_data = """
                INSERT INTO
                
                
                
                """