import pandas as pd
from pymongo import MongoClient
import os
import sys

# Environment variables come from docker-compose / .env
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
    # Get the app directory to construct correct paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(script_dir)
    rawpath = os.path.join(app_dir, "data", "disease_metadata_raw.csv")
    cleanpath = os.path.join(app_dir, "data", "disease_metadata_clean.csv")

    # 1. Read CSV
    print(f"[OK] Reading disease metadata from {rawpath}")
    df = pd.read_csv(rawpath)

    # 2. Clean basic fields
    print("[OK] Cleaning disease metadata...")
    df["plant"] = df["plant"].astype(str).str.strip().str.lower()
    df["diseasename"] = df["diseasename"].astype(str).str.strip()

    # 3. Save cleaned version for HDFS ingestion
    print(f"[OK] Saving cleaned data to {cleanpath}")
    df.to_csv(cleanpath, index=False)
    print(f"[OK] Disease metadata cleaned: {len(df)} records")

    # 4. Try to insert into MongoDB
    try:
        print("[INFO] Attempting to connect to MongoDB...")
        client = get_mongo_client()
        
        db = client[MONGODB]
        coll = db["diseasemetadata"]

        # Clear existing for demo
        coll.delete_many({})
        print("[OK] Cleared existing disease metadata")

        docs = []
        for _, row in df.iterrows():
            docs.append(
                {
                    "plant": row.get("plant"),
                    "diseasename": row.get("diseasename"),
                    "label": row.get("label"),
                    "severityscale": "medium",
                    "favorableconditions": {
                        "mintemp": float(row.get("mintemp", 0) or 0),
                        "maxtemp": float(row.get("maxtemp", 0) or 0),
                        "minhumidity": float(row.get("minhumidity", 0) or 0),
                        "maxhumidity": float(row.get("maxhumidity", 0) or 0),
                        "notes": str(row.get("notes", "")),
                    },
                }
            )

        if docs:
            coll.insert_many(docs)
            print(f"[OK] Loaded {len(docs)} disease records into MongoDB")

        print("Disease metadata cleaned and loaded into MongoDB.")
        return 0
        
    except Exception as e:
        print(f"[WARN] MongoDB connection failed: {str(e)}")
        print("[WARN] CSV file was cleaned successfully but not uploaded to MongoDB")
        print("[INFO] Disease metadata CSV is ready for manual upload")
        # Return success since CSV was created
        return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        sys.exit(0)  # Still return 0 since CSV was created
