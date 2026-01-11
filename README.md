# Smart Agriculture Big Data Platform

End-to-end big data system for agricultural IoT monitoring, batch processing, and analytics using Hadoop, Spark, MongoDB, and Streamlit.

## 🚀 Quick Start

### Option 1: Dashboard Only (5 minutes)
```bash
pip install -r requirements.txt
python -m streamlit run app/interface.py
```
Open http://localhost:8501 — explore sample data and charts without Docker.

### Option 2: Full Stack (with Docker)
```bash
docker-compose up -d
```
Then run the dashboard (same command above). MongoDB will contain real analytics data.

---

## 📋 What This Project Does

- **IoT Simulation**: Generates realistic sensor data (soil, atmosphere, crop health)
- **Batch Processing**: Apache Spark aggregates sensor readings daily
- **Distributed Storage**: Hadoop HDFS + MongoDB for data persistence
- **Live Analytics**: Streamlit dashboard with charts and data exploration
- **One-Click Pipeline**: Run entire pipeline via dashboard button

---

## 🏗️ Architecture

```
Data Flow:
Simulated Sensors (JSON) → Hadoop/HDFS → Apache Spark → MongoDB → Streamlit UI
```

**Services** (via Docker Compose):
- **Hadoop** (NameNode + DataNode): Distributed file storage
- **Spark**: Batch processing engine
- **MongoDB**: Analytics database (port 27017)
- **Streamlit App**: Web dashboard (port 8502)

---

## 📂 Project Structure

```
smart-agri-bigdata/
├── app/
│   ├── interface.py          # Main Streamlit dashboard
│   ├── scripts/
│   │   ├── simulate_sensors_gateway.py         # Generate sensor data
│   │   ├── prepare_disease_metadata.py         # Prepare crop disease data
│   │   ├── run_full_pipeline.py                # One-click pipeline automation
│   │   ├── load_sample_analytics.py            # Load analytics to MongoDB
│   │   └── spark_batch_pipeline.py             # Spark aggregation jobs
│   ├── data/
│   │   ├── gateway_output/              # Generated sensor JSON files
│   │   └── disease_metadata_clean.csv   # Disease reference data
│   └── results/
│       ├── aggdaily_sample.csv          # Daily aggregated metrics
│       └── diseasestats_sample.csv      # Disease statistics
├── docker-compose.yml                   # Full-stack service orchestration
├── requirements.txt                     # Python dependencies
└── hadoop/, spark/, mongodb/            # Dockerfile configs for each service
```

---

## 💻 Dashboard Features

**Home Tab**
- Project overview and architecture diagram

**Pipeline Guide Tab**
- 5-step pipeline explanation and status

**Data Tab**
- Browse and download CSV files
- Run individual scripts (simulate sensors, prepare metadata)

**Analytics Tab** ⭐ *Requires Docker + MongoDB*
- 4 visualization tabs with real-time charts:
  - 📈 Soil Metrics (moisture over time)
  - 🌡️ Temperature (soil vs air trends)
  - 💧 Humidity patterns
  - 📊 Summary statistics table

**One-Click Automation**
- 🤖 Run Full Pipeline button: Executes all 5 pipeline steps (~30 seconds)

**Architecture & Docs Tab**
- System diagram and documentation links

---

## 🔧 Prerequisites

- Python 3.10+ (tested with 3.12)
- Docker + Docker Compose (optional, for full-stack)
- 4GB RAM minimum

---

## 🐳 Full Stack Setup

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Verify containers are running**:
   ```bash
   docker ps
   ```
   You should see 5 containers: hadoop-namenode, hadoop-datanode, spark, mongodb, app

3. **Start the dashboard**:
   ```bash
   python -m streamlit run app/interface.py
   ```

4. **Run the pipeline** (via dashboard or command line):
   ```bash
   python app/scripts/run_full_pipeline.py
   ```

---

## 📊 Data Pipeline (5 Steps)

1. **Sensor Simulation** → Generates 96 JSON files with sensor readings
2. **Disease Metadata** → Prepares crop disease reference data
3. **Hadoop Storage** → Moves data to HDFS
4. **Spark Aggregation** → Computes daily averages by field/crop
5. **MongoDB Analytics** → Stores results for dashboard visualization

---

## 🧪 Testing

Run individual pipeline steps from the **Data** tab in the dashboard, or execute scripts directly:

```bash
# Generate sensor data (creates 96 JSON files)
python app/scripts/simulate_sensors_gateway.py

# Prepare disease metadata (loads to MongoDB)
python app/scripts/prepare_disease_metadata.py

# Run full pipeline
python app/scripts/run_full_pipeline.py
```

---

## 📈 Expected Outputs

After running the pipeline, you'll have:
- **96 sensor JSON files** in `app/data/gateway_output/`
- **4 analytics records** in MongoDB (`analyticsdaily` collection)
- **5 disease records** in MongoDB (`diseases` collection)
- **Live charts** visible in the Analytics tab

---

## ⚠️ Common Issues

**Q: Charts not showing in Analytics tab?**
- Ensure Docker containers are running: `docker ps`
- Run the pipeline to populate MongoDB: Click 🤖 button or run `python app/scripts/run_full_pipeline.py`

**Q: "Could not connect to MongoDB"?**
- Check MongoDB container is running: `docker logs mongodb` 
- Verify port 27017 is not blocked

**Q: Streamlit on wrong port?**
- Dashboard runs on port **8502** (not 8501)
- Open: http://localhost:8502

---

## 📝 License

This is an educational project demonstrating modern big data architectures for precision agriculture.

---

## ✅ Verified Status

- ✅ All 5 Docker containers healthy
- ✅ Sensor data generation working (96 files generated)
- ✅ MongoDB connectivity with local fallbacks
- ✅ Full pipeline achieves 100% success (5/5 steps)
- ✅ Analytics dashboard with interactive charts
- ✅ One-click pipeline automation functional
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
