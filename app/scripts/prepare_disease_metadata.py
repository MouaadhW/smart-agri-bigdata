import pandas as pd
from pymongo import MongoClient
import os

MONGOHOST = os.getenv("MONGOHOST", "mongodb")
MONGOPORT = int(os.getenv("MONGOPORT", "27017"))
MONGOUSER = os.getenv("MONGOINITDBROOTUSERNAME", "root")
MONGOPWD = os.getenv("MONGOINITDBROOTPASSWORD", "example")
MONGODB = os.getenv("MONGODB", "agridb")

def main():
    rawpath = "data/diseasemetadataraw.csv"
    cleanpath = "data/diseasemetadataclean.csv"

    df = pd.readcsv(rawpath)
    df["plant"] = df["plant"].str.strip().str.lower()
    df["diseasename"] = df["diseasename"].str.strip()

    df.tocsv(cleanpath, index=False)

    client = MongoClient(
        host=MONGOHOST,
        port=MONGOPORT,
        username=MONGOUSER,
        password=MONGOPWD
    )

    db = client[MONGODB]
    coll = db["diseasemetadata"]
    coll.deletemany({})

    docs = []
    for , row in df.iterrows():
        docs.append({
            "plant": row["plant"],
            "diseasename": row["diseasename"],
            "label": row["label"],
            "severityscale": "medium",
            "favorableconditions": {
                "mintemp": float(row["mintemp"]),
                "maxtemp": float(row["maxtemp"]),
                "minhumidity": float(row["minhumidity"]),
                "maxhumidity": float(row["maxhumidity"]),
                "notes": row.get("notes", "")
            }
        })

    if docs:
        coll.insertmany(docs)
    print("Disease metadata prepared and stored in MongoDB.")

if name == "main":
    main()