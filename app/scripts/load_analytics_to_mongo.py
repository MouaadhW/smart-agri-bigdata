from pyspark.sql import SparkSession
from pymongo import MongoClient
import os

MONGOHOST = os.getenv("MONGOHOST", "mongodb")
MONGOPORT = int(os.getenv("MONGOPORT", "27017"))
MONGOUSER = os.getenv("MONGOINITDBROOTUSERNAME", "root")
MONGOPWD = os.getenv("MONGOINITDBROOTPASSWORD", "example")
MONGODB = os.getenv("MONGODB", "agridb")

def droughtlabel(avgsm):
    if avgsm is None:
        return "unknown"
    if avgsm < 0.2:
        return "high"
    elif avgsm < 0.3:
        return "medium"
    return "low"

def main():
    spark = SparkSession.builder.appName("LoadAnalyticsToMongo").getOrCreate()

    aggdaily = spark.read.parquet("hdfs://namenode:9000/data/agri/output/aggdaily")
    diseasestats = spark.read.parquet("hdfs://namenode:9000/data/agri/output/diseasestats")

    pdfagg = aggdaily.toPandas()
    pdfdis = diseasestats.toPandas()

    plantdiseasecounts = {
        row["plant"]: int(row["ndiseases"])
        for , row in pdfdis.iterrows()
    }

    client = MongoClient(
        host=MONGOHOST,
        port=MONGOPORT,
        username=MONGOUSER,
        password=MONGOPWD
    )
    db = client[MONGODB]
    coll = db["analyticsdaily"]
    coll.deletemany({})

    docs = []
    for , row in pdfagg.iterrows():
        avgsm = float(row["avgsoilmoisture"])
        d = {
            "date": str(row["date"]),
            "fieldid": row["fieldid"],
            "croptype": row["croptype"],
            "metrics": {
                "avgsoilmoisture": avgsm,
                "avgsoiltemp": float(row["avgsoiltemp"]),
                "avgairtemp": float(row["avgairtemp"]),
                "avgairhumidity": float(row["avgairhumidity"]),
                "droughtrisklevel": droughtlabel(avgsm),
                "diseaserisklevel": "medium"
            },
            "diseasestats": [
                {
                    "diseasename": "ALL",
                    "occurrencecount": plantdiseasecounts.get(row["croptype"], 0),
                    "relativefrequency": 1.0
                }
            ]
        }
        docs.append(d)

    if docs:
        coll.insertmany(docs)
    print("Analytics loaded into MongoDB.")

    spark.stop()

if name == "main":
    main()