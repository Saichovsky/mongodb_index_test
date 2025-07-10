import os
import random
import time
from faker import Faker
from pymongo import MongoClient, errors
import argparse

def wait_for_mongodb(mongo_uri, timeout=60, interval=2):
    """Wait until MongoDB is available or timeout expires."""
    start_time = time.time()
    while True:
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
            # The ismaster command is cheap and does not require auth
            client.admin.command('ismaster')
            print("MongoDB is available!")
            return client
        except errors.ServerSelectionTimeoutError:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(f"Could not connect to MongoDB within {timeout} seconds.")
            print(f"Waiting for MongoDB to be available... retrying in {interval} seconds.")
            time.sleep(interval)

def generate_random_document(fake):
    return {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "age": random.randint(18, 80),
        "registered_at": fake.date_time_this_decade()
    }

def seed_database(client, db_name, collection_name, num_records, ttl):
    db = client[db_name]
    collection = db[collection_name]
    collection.create_index("registered_at", expireAfterSeconds=ttl)  # 1 year

    fake = Faker()

    print(f"Inserting {num_records} random documents into {db_name}.{collection_name}...")

    documents = [generate_random_document(fake) for _ in range(num_records)]
    result = collection.insert_many(documents)

    print(f"Inserted {len(result.inserted_ids)} documents successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MongoDB with random data.")
    parser.add_argument("--db-name", type=str, default="testdb", help="Database name")
    parser.add_argument("--collection-name", type=str, default="users", help="Collection name")
    parser.add_argument("--num-records", type=int, default=100, help="Number of random records to insert")
    parser.add_argument("--ttl", type=int, default=31536000, help="Time-to-live (TTL) in seconds for documents. Default is 1 year")

    args = parser.parse_args()

    # Initialize MongoDB client
    mongo_uri = os.environ.get("MONGODB_DEFAULT_HOST", "mongodb://root:example@mongodb:27017")
    client = wait_for_mongodb(mongo_uri)

    # Seed the database
    seed_database(client, args.db_name, args.collection_name, args.num_records, args.ttl)
