# Smart Agriculture Big Data Platform

A complete end-to-end big data system for intelligent agricultural monitoring and analysis. This project combines **IoT sensor data**, **batch processing**, **distributed storage**, and **real-time analytics** to support precision farming decisions.

## 📋 Project Overview

Smart Agri BigData is a full-stack demonstration of modern big data technologies applied to agriculture:

- **Data Generation**: Simulated IoT sensors generating real-time field data (soil, atmosphere, crop health)
- **Data Ingestion**: Apache Hadoop/HDFS for distributed storage
- **Batch Processing**: Apache Spark pipelines for aggregating and analyzing sensor data
- **Analytics Storage**: MongoDB for storing processed analytics and historical data
- **Interactive Dashboard**: Streamlit web interface for visualization and data exploration

### Key Features
- 🌾 **Multi-field monitoring**: Soil moisture, temperature, pH; atmospheric conditions; disease risk scoring
- 📊 **Batch analytics**: Daily aggregations of sensor metrics by field and crop type
- 🏥 **Disease tracking**: Plant disease metadata with prevalence analysis
- 📈 **Real-time visualization**: Live plots from MongoDB analytics collections
- 🐳 **Docker containerization**: Isolated services for scalable deployment
- 🔄 **Modular architecture**: Each component (Hadoop, Spark, Mongo, UI) can be independently scaled

---

## Prerequisites

- **Python 3.10+** (tested with 3.12)
- **Docker + Docker Compose** (for full-stack deployment)
- **Git** (optional, for cloning the repository)

---

## 🚀 Quick Start (Streamlit Dashboard Only)

**Time**: ~5 minutes | **Docker needed**: ❌ No

Start the interactive dashboard with sample data preview and local data generation scripts—no container orchestration required.

```bash
pip install -r requirements.txt
python -m streamlit run app/interface.py
```

Open **http://localhost:8501** in your browser to explore:

| Tab | Functionality |
|-----|---------------|
| **Home** | Project overview and architecture summary |
| **Runbook** | Copy-pasteable commands for full-stack setup (reference) |
| **Data** | Preview and download CSVs; run data generators locally |
| **Analytics** | Live MongoDB analytics plots (if Mongo is running) |
| **Architecture & Docs** | System architecture and troubleshooting guide |

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
