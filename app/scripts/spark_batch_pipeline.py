from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, todate
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    BooleanType, TimestampType, StructType as ST
)

def getschema():
    return StructType([
        StructField("fieldid", StringType(), True),
        StructField("sensorid", StringType(), True),
        StructField("timestamp", StringType(), True),
        StructField("sensortype", StringType(), True),
        StructField("croptype", StringType(), True),
        StructField("location", ST([
            StructField("lat", DoubleType(), True),
            StructField("lon", DoubleType(), True)
        ]), True),
        StructField("soil", ST([
            StructField("moisture", DoubleType(), True),
            StructField("temperature", DoubleType(), True),
            StructField("ph", DoubleType(), True)
        ]), True),
        StructField("atmosphere", ST([
            StructField("temperature", DoubleType(), True),
            StructField("humidity", DoubleType(), True),
            StructField("light", DoubleType(), True)
        ]), True),
        StructField("qualityflags", ST([
            StructField("outlier", BooleanType(), True),
            StructField("imputed", BooleanType(), True)
        ]), True),
        StructField("derived", ST([
            StructField("droughtrisk", StringType(), True),
            StructField("diseaseriskscore", DoubleType(), True)
        ]), True)
    ])

def main():
    spark = SparkSession.builder \
        .appName("SmartAgriBatchPipeline") \
        .getOrCreate()

    schema = getschema()

    rawpath = "hdfs://namenode:9000/data/agri/sensors////sensorbatch.json"
    dfraw = spark.read.schema(schema).json(rawpath)

    df = dfraw.withColumn("timestampts", col("timestamp").cast(TimestampType()))
    df = df.withColumn("date", todate(col("timestampts")))

    df = df.dropna(subset=["fieldid", "timestampts", "soil.moisture", "atmosphere.temperature"])
    df = df.filter((col("soil.moisture") >= 0) & (col("soil.moisture") <= 1))
    df = df.filter((col("soil.ph") >= 3.5) & (col("soil.ph") <= 9.5))

    diseasedf = spark.read.option("header", True).csv(
        "hdfs://namenode:9000/data/agri/disease/diseasemetadataclean.csv"
    )

    aggdaily = df.groupBy("date", "fieldid", "croptype").agg(
        avg(col("soil.moisture")).alias("avgsoilmoisture"),
        avg(col("soil.temperature")).alias("avgsoiltemp"),
        avg(col("atmosphere.temperature")).alias("avgairtemp"),
        avg(col("atmosphere.humidity")).alias("avgairhumidity")
    )

    aggdaily.write.mode("overwrite").parquet(
        "hdfs://namenode:9000/data/agri/output/aggdaily"
    )

    diseasestats = diseasedf.groupBy("plant").count().withColumnRenamed("count", "ndiseases")
    diseasestats.write.mode("overwrite").parquet(
        "hdfs://namenode:9000/data/agri/output/disease_stats"
    )

    spark.stop()

if name == "main":
    main()