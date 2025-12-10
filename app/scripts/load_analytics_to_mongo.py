from pyspark.sql import SparkSession
from pymongo import MongoClient
import os

# Match docker-compose/.env names
MONGOHOST = os.getenv("MONGOHOST", "mongodb")
MONGOPORT = int(os.getenv("MONGOPORT", "27017"))
MONGOUSER = os.getenv("MONGOINITDBROOTUSERNAME", "root")
MONGOPWD = os.getenv("MONGOINITDBROOTPASSWORD", "example")
MONGODB = os.getenv("MONGODB", "agridb")


def droughtlabel(avgsm: float) -> str:
    """Simple rule-based drought label from average soil moisture."""
    if avgsm is None:
        return "unknown"
    try:
        v = float(avgsm)
    except Exception:
        return "unknown"
    if v < 0.2:
        return "high"
    elif v < 0.3:
        return "medium"
    return "low"


def main():
    spark = SparkSession.builder.appName("LoadAnalyticsToMongo").getOrCreate()

    # These paths must match spark_batch_pipeline.py outputs
    aggdailypath = "hdfs://namenode:9000/data/agri/output/aggdaily"
    diseasestatspath = "hdfs://namenode:9000/data/agri/output/diseasestats"

    aggdaily = spark.read.parquet(aggdailypath)
    diseasestats = spark.read.parquet(diseasestatspath)

    pdfagg = aggdaily.toPandas()
    pdfdis = diseasestats.toPandas()

    plantdiseasecounts = {
        row.get("plant"): int(row.get("ndiseases", 0) or 0)
        for _, row in pdfdis.iterrows()
    }

    client = MongoClient(
        host=MONGOHOST,
        port=MONGOPORT,
        username=MONGOUSER,
        password=MONGOPWD,
    )
    db = client[MONGODB]
    coll = db["analyticsdaily"]

    # Clear previous data
    coll.delete_many({})

    docs = []
    for _, row in pdfagg.iterrows():
        avgsm = float(row.get("avgsoilmoisture", 0) or 0)
        croptype = row.get("croptype")

        doc = {
            "date": str(row.get("date")),
            "fieldid": row.get("fieldid"),
            "croptype": croptype,
            "metrics": {
                "avgsoilmoisture": avgsm,
                "avgsoiltemp": float(row.get("avgsoiltemp", 0) or 0),
                "avgairtemp": float(row.get("avgairtemp", 0) or 0),
                "avgairhumidity": float(row.get("avgairhumidity", 0) or 0),
                "droughtrisklevel": droughtlabel(avgsm),
                "diseaserisklevel": "medium",
            },
            "diseasestats": [
                {
                    "diseasename": "ALL",
                    "occurrencecount": plantdiseasecounts.get(croptype, 0),
                    "relativefrequency": 1.0,
                }
            ],
        }
        docs.append(doc)

    if docs:
        coll.insert_many(docs)

    print("Analytics loaded into MongoDB.")

    spark.stop()


if __name__ == "__main__":
    main()