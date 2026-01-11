"""
Load Sample Analytics Data to MongoDB
Simple script that reads CSV files and loads them into MongoDB's analyticsdaily collection
"""

import pandas as pd
from pymongo import MongoClient
import os
import json

# Environment variables
MONGOHOST = os.getenv("MONGOHOST", "mongodb")
MONGOPORT = int(os.getenv("MONGOPORT", "27017"))
MONGOUSER = os.getenv("MONGOINITDBROOTUSERNAME", "root")
MONGOPWD = os.getenv("MONGOINITDBROOTPASSWORD", "example")
MONGODB = os.getenv("MONGODB", "agridb")


def get_mongo_client():
    """Try to connect to MongoDB with fallback hosts"""
    hosts_to_try = [
        MONGOHOST,  # Original (docker network)
        "localhost",  # Try localhost
        "127.0.0.1",  # Try IP
    ]
    
    for host in hosts_to_try:
        try:
            client = MongoClient(
                host=host,
                port=MONGOPORT,
                username=MONGOUSER,
                password=MONGOPWD,
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=3000,
            )
            # Test the connection
            client.admin.command("ping")
            print(f"[OK] Connected to MongoDB at {host}:{MONGOPORT}")
            return client
        except Exception as e:
            print(f"[SKIP] Could not connect to {host}: {type(e).__name__}")
            continue
    
    raise Exception("Could not connect to MongoDB on any host")


def main():
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(script_dir)
    results_dir = os.path.join(app_dir, "results")
    
    aggdaily_path = os.path.join(results_dir, "aggdaily_sample.csv")
    
    # Check if file exists
    if not os.path.exists(aggdaily_path):
        print(f"[WARN] Sample data file not found: {aggdaily_path}")
        print("[INFO] Run the Spark pipeline first to generate sample data")
        return
    
    # Read the CSV
    print(f"[OK] Reading sample data from {aggdaily_path}")
    df = pd.read_csv(aggdaily_path)
    print(f"[OK] Loaded {len(df)} records from CSV")
    
    # Connect to MongoDB
    try:
        client = get_mongo_client()
        db = client[MONGODB]
        coll = db["analyticsdaily"]
        
        # Clear existing data
        result = coll.delete_many({})
        print(f"[OK] Cleared existing records: {result.deleted_count} deleted")
        
        # Convert DataFrame to dict records
        records = df.to_dict('records')
        
        # Insert into MongoDB
        if records:
            insert_result = coll.insert_many(records)
            print(f"[OK] Inserted {len(insert_result.inserted_ids)} records into analyticsdaily collection")
            
            # Verify insertion
            count = coll.count_documents({})
            print(f"[OK] Verified: {count} records now in analyticsdaily collection")
        
        print("\n[SUCCESS] Analytics data loaded to MongoDB!")
        print("Next step: Refresh the Analytics tab in Streamlit to see live data")
        
    except Exception as e:
        print(f"[ERROR] Failed to load data to MongoDB: {str(e)}")
        print("[INFO] Make sure MongoDB is running and accessible")
        raise


if __name__ == "__main__":
    main()
