# Quick Start Guide – Smart Agri BigData

This guide shows you how to run and test the entire project end-to-end.

## Part A: Dashboard Only (5 minutes)

No Docker needed. Just Streamlit UI with sample data.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Streamlit

```bash
python -m streamlit run app/interface.py
```

Open **http://localhost:8501** in your browser.

### 3. Explore the UI

- **Home**: Project overview
- **Runbook**: Commands for full stack setup
- **Data**: Preview CSVs from `app/data/` and `app/results/` (no Mongo needed)
- **Analytics**: Falls back to demo chart if Mongo unavailable
- **Architecture & Docs**: System overview

**That's it!** You can explore the UI, preview sample data, and run generators locally.

---

## Part B: Full Stack (Docker + Spark + Hadoop + MongoDB)

### 1. Create `.env` file

Create a file named `.env` in the project root:

```
MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb
```

### 2. Start Docker Services

```bash
docker compose up -d
```

Verify all containers are running:

```bash
docker ps
```

Expected output (5 containers):
- `hadoop-namenode` (Up)
- `hadoop-datanode` (Up)
- `spark` (Up)
- `mongodb` (Up)
- `app` (Up)

### 3. Generate Sample Data (Host)

```bash
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py
```

✅ Output:
- `app/data/gateway_output/*.json` — 96 sensor readings (15-min intervals)
- `app/data/disease_metadata_clean.csv` — cleaned disease data
- MongoDB `diseasemetadata` collection — populated

### 4. Verify Data in MongoDB (Optional)

```bash
docker exec -it mongodb mongosh -u root -p example --authenticationDatabase admin agridb --eval "db.diseasemetadata.countDocuments()"
```

Should output a number > 0.

### 5. Push Data to HDFS

```bash
docker exec hadoop-namenode bash -lc "\
  /opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data/agri/sensors /data/agri/disease && \
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/gateway_output/*.json /data/agri/sensors && \
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/disease_metadata_clean.csv /data/agri/disease/"
```

Verify files in HDFS:

```bash
docker exec hadoop-namenode bash -lc "/opt/hadoop-3.2.1/bin/hdfs dfs -ls /data/agri/sensors"
```

### 6. Run Spark Batch Job

```bash
docker exec spark bash -lc "cd /opt/app/scripts && spark-submit spark_batch_pipeline.py"
```

⏱️ Takes ~30-60 seconds. Output:
- `/data/agri/output/aggdaily/` — daily aggregated metrics
- `/data/agri/output/diseasestats/` — disease counts by crop

### 7. Load Analytics to MongoDB

```bash
docker exec spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"
```

Creates `analyticsdaily` collection in MongoDB.

### 8. View Live Analytics in UI

If Streamlit is still running, refresh http://localhost:8501 → **Analytics** tab now shows:
- ✅ Live plots (soil moisture time-series, disease counts, drought risk)
- ✅ Filters by crop type and field ID
- ✅ Download button for CSV export

---

## Testing Checklist

### Quick Test (No Docker)

```bash
# Install deps
pip install -r requirements.txt

# Start UI
python -m streamlit run app/interface.py

# At http://localhost:8501:
# ✓ Home tab loads README
# ✓ Runbook tab shows commands
# ✓ Data tab previews app/data/*.csv and app/results/*.csv
# ✓ Analytics tab shows demo chart (MongoDB disconnected)
# ✓ Architecture tab displays docs
```

### Full Stack Test (Docker)

```bash
# 1. Create .env
echo "MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb" > .env

# 2. Start containers
docker compose up -d

# 3. Generate data
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py

# 4. Push to HDFS
docker exec hadoop-namenode bash -lc "\
  /opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data/agri/sensors /data/agri/disease && \
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/gateway_output/*.json /data/agri/sensors && \
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/disease_metadata_clean.csv /data/agri/disease/"

# 5. Run Spark job
docker exec spark bash -lc "cd /opt/app/scripts && spark-submit spark_batch_pipeline.py"

# 6. Load to MongoDB
docker exec spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"

# 7. View in UI
# Start Streamlit (if not already running)
python -m streamlit run app/interface.py

# At http://localhost:8501 → Analytics tab:
# ✓ Connected to MongoDB
# ✓ Shows time-series chart (soil moisture)
# ✓ Shows bar chart (disease by crop)
# ✓ Shows drought risk distribution
# ✓ Filters work (crop type, field ID)
# ✓ CSV download button works
```

---

## Troubleshooting

### Streamlit won't start

```bash
# Debug mode
python -m streamlit run app/interface.py --logger.level=debug

# Check deps
pip list | grep -i streamlit
```

### MongoDB connection fails (Analytics shows demo)

Check env vars and MongoDB container:

```bash
docker ps | grep mongodb
docker exec mongodb mongosh --version
```

Reconnect by refreshing the page (cache resets every 30 seconds).

### Spark job fails

Check logs:

```bash
docker exec spark tail -100 /tmp/spark.log 2>/dev/null || echo "No spark.log"
```

Verify HDFS files exist:

```bash
docker exec hadoop-namenode bash -lc \
  "/opt/hadoop-3.2.1/bin/hdfs dfs -ls /data/agri/sensors | head -5"
```

### Hadoop datanode not healthy

Wait 10-15 seconds (initialization takes time), then:

```bash
docker logs hadoop-datanode | tail -20
```

---

## File Structure After Testing

```
app/
├── data/
│   ├── disease_metadata_raw.csv
│   ├── disease_metadata_clean.csv
│   ├── gateway_output/*.json        ← Generated (96 files)
│   └── yoursample.csv
├── results/
│   ├── aggdaily_sample.csv          ← Sample output
│   └── diseasestats_sample.csv      ← Sample output
├── scripts/
│   ├── simulate_sensors_gateway.py
│   ├── prepare_disease_metadata.py
│   ├── spark_batch_pipeline.py
│   └── load_analytics_to_mongo.py
└── interface.py                       ← Main UI (Streamlit)
```

---

## What Each Script Does

1. **simulate_sensors_gateway.py** — Generates 96 JSON files (one every 15 min for 24 hours) with simulated sensor readings
2. **prepare_disease_metadata.py** — Cleans disease CSV and inserts into MongoDB `diseasemetadata` collection
3. **spark_batch_pipeline.py** — Runs on Spark; reads JSONs + CSVs from HDFS; writes aggregated parquet to HDFS (`/data/agri/output/*`)
4. **load_analytics_to_mongo.py** — Reads parquet from HDFS; converts to Pandas; inserts into MongoDB `analyticsdaily` collection
5. **interface.py** — Streamlit UI; connects to MongoDB, displays plots, allows filtering & download

---

## Key Ports

- **Streamlit UI**: http://localhost:8501
- **HDFS NameNode UI**: http://localhost:9870
- **MongoDB**: localhost:27017 (root/example)

---

## Tips

- Sensor data is generated with timestamps from 2025-12-09 (editable in `simulate_sensors_gateway.py`).
- MongoDB is auto-seeded with schema on first run (`mongo-init.js`).
- Spark job duration depends on cluster size; expect 30-60 seconds for demo data.
- All container logs accessible via `docker logs <container_name>`.
- Volumes persist across restarts (HDFS, MongoDB).

---

**Next Steps:**
- Extend Spark pipeline with more analytics.
- Add real sensor data ingestion.
- Deploy to cloud (AWS, Azure, GCP).
- Document results in your coursework report.

Enjoy! 🚀
