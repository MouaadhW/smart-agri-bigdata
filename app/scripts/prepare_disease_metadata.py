import pandas as pd
from pymongo import MongoClient
import os

# Environment variables come from docker-compose / .env
MONGOHOST = os.getenv("MONGOHOST", "mongodb")
MONGOPORT = int(os.getenv("MONGOPORT", "27017"))
MONGOUSER = os.getenv("MONGOINITDBROOTUSERNAME", "root")
MONGOPWD = os.getenv("MONGOINITDBROOTPASSWORD", "example")
MONGODB = os.getenv("MONGODB", "agridb")


def main():
    rawpath = "data/disease_metadata_raw.csv"
    cleanpath = "data/disease_metadata_clean.csv"

    # 1. Read CSV
    df = pd.read_csv(rawpath)

    # 2. Clean basic fields
    df["plant"] = df["plant"].astype(str).str.strip().str.lower()
    df["diseasename"] = df["diseasename"].astype(str).str.strip()

    # 3. Save cleaned version for HDFS ingestion
    df.to_csv(cleanpath, index=False)

    # 4. Insert into MongoDB
    client = MongoClient(
        host=MONGOHOST,
        port=MONGOPORT,
        username=MONGOUSER,
        password=MONGOPWD,
    )
    db = client[MONGODB]
    coll = db["diseasemetadata"]

    # Clear existing for demo
    coll.delete_many({})

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

    print("Disease metadata cleaned and loaded into MongoDB.")


if __name__ == "__main__":
    main()