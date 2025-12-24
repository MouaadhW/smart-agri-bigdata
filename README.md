# smart-agri-bigdata

End-to-end big data demo for smart agriculture with Streamlit UI, Spark batch jobs, Hadoop/HDFS, and MongoDB.

## Prerequisites
- Python 3.10+ (tested with 3.12)
- Docker + Docker Compose

## Quick Start (Dashboard Only)

No Docker needed—just the Streamlit UI with sample data preview and local script execution.

```bash
pip install -r requirements.txt
python -m streamlit run app/interface.py
```

Open http://localhost:8501 to explore:
- **Home**: Project overview (this README).
- **Runbook**: Step-by-step commands for full-stack deployment.
- **Data**: Preview and download CSVs from `app/data/` and `app/results/`.
- **Analytics**: Connect to MongoDB `analyticsdaily` collection (live plots if Mongo is running).
- **Architecture & Docs**: System overview and troubleshooting.

## Full Stack Setup (Hadoop + Spark + Mongo)

### 1. Create `.env` file

From repo root:
```
MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb
```

### 2. Start Docker services

```bash
docker compose up -d
```

Services running:
- HDFS NameNode UI: http://localhost:9870
- MongoDB: localhost:27017 (root/example)
- Spark container: available for batch jobs
- App container: mounts `./app` at `/opt/app`

### 3. Generate sample data (host)

```bash
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py
```

Outputs:
- `app/data/gateway_output/*.json` — sensor readings (96 x 15-min batches)
- `app/data/disease_metadata_clean.csv` — cleaned disease data + loaded to MongoDB

### 4. Push data to HDFS (optional, for Spark jobs)

```bash
docker exec hadoop-namenode bash -lc "\
  /opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data/agri/sensors /data/agri/disease && \
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/gateway_output/*.json /data/agri/sensors && \
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/disease_metadata_clean.csv /data/agri/disease/"
```

### 5. Run Spark batch job (optional)

```bash
docker exec -it spark bash -lc "cd /opt/app/scripts && spark-submit spark_batch_pipeline.py"
```

Outputs to HDFS: `/data/agri/output/aggdaily`, `/data/agri/output/diseasestats`

### 6. Load analytics to MongoDB

```bash
docker exec -it spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"
```

Inserts documents into `analyticsdaily` collection.

### 7. Launch Streamlit UI (if not running)

```bash
python -m streamlit run app/interface.py
```

## UI Tabs

- **Runbook**: Copy-pasteable commands for each step (no manual edits needed).
- **Data**: Preview CSVs from `app/data/` and `app/results/`; run generators locally with buttons.
- **Analytics**: Live plots from MongoDB if connected (soil moisture, disease counts, drought risk).
- **Architecture & Docs**: System overview and quick troubleshooting.

## Troubleshooting

**Streamlit doesn't start:**
```bash
python -m streamlit run app/interface.py --logger.level=debug
```

**MongoDB not reachable (Analytics tab shows demo):**
- Check env vars: `MONGOHOST`, `MONGOPORT`, `MONGOINITDBROOTUSERNAME`, `MONGOINITDBROOTPASSWORD`.
- Ensure `.env` is in repo root.
- Verify MongoDB container: `docker ps | grep mongodb`.

**Hadoop/Spark containers fail to start:**
- Docker image pull failures: Try `docker compose pull` then `docker compose up -d`.
- Namenode logs: `docker logs hadoop-namenode --tail 50`.
- Datanode logs: `docker logs hadoop-datanode --tail 50`.

**HDFS put command fails ("no datanode running"):**
- Datanode may still be initializing. Wait 10-15 seconds and retry.
- Check datanode logs: `docker logs hadoop-datanode --tail 50`.

**Python script import errors:**
- Install deps: `pip install -r requirements.txt` (host) and `pip install -r app/requirements.txt` (inside Docker).

## Project Structure

```
.
├── docker-compose.yml          # Service definitions (Hadoop, Spark, Mongo, App)
├── .env                        # Mongo credentials (create this)
├── requirements.txt            # Python deps (host)
├── app/
│   ├── interface.py            # Streamlit UI (runbook, data, analytics tabs)
│   ├── requirements.txt        # Python deps (Docker app container)
│   ├── Dockerfile              # App container definition
│   ├── data/
│   │   ├── disease_metadata_raw.csv          # Input disease data
│   │   ├── disease_metadata_clean.csv        # Cleaned output
│   │   ├── gateway_output/                   # Generated sensor JSONs
│   │   └── yoursample.csv                    # Example data
│   ├── results/                              # Spark output CSVs (aggdaily_sample.csv, etc.)
│   ├── images/                               # Add sys_arch.png here
│   └── scripts/
│       ├── simulate_sensors_gateway.py       # Generate 96 sensor readings
│       ├── prepare_disease_metadata.py       # Clean CSV & load Mongo
│       ├── spark_batch_pipeline.py           # Spark ETL
│       └── load_analytics_to_mongo.py        # Load Spark outputs to Mongo
├── hadoop/
│   ├── Dockerfile
│   ├── core-site.xml
│   └── hdfs-site.xml
├── mongodb/
│   ├── Dockerfile
│   └── mongo-init.js
└── spark/
    └── Dockerfile
```

## Key Data Flow

1. **Data Generation** → sensor JSONs + disease CSV (host)
2. **Ingestion** → HDFS + Mongo (Docker)
3. **Processing** → Spark batch job (Spark container)
4. **Analytics** → Mongo `analyticsdaily` collection
5. **Visualization** → Streamlit UI (host) reads Mongo + previews CSVs

## Notes

- HDFS volumes persist across container restarts (`hadoopnamenode`, `hadoopdatanode`).
- `./app/data` is mounted into containers at `/opt/data` (shared host-container folder).
- Example sample files in `app/results/` demonstrate analytics output format.
- Streamlit caches MongoDB reads (30-second TTL) to avoid overload.
- Extend tabs in `app/interface.py` to add custom plots, filters, or exports.

## Next Steps

- Deploy to cloud (AWS S3 for HDFS, MongoDB Atlas, etc.).
- Add real sensor data ingestion from IoT devices.
- Expand Spark pipeline with more analytics (time-series forecasting, anomaly detection).
- Document results and insights in your coursework report.

---

**Smart Agri BigData** · Academic Prototype · Horizon School of Digital Technologies (2025-2026)
