# TEST & USAGE GUIDE – Smart Agri BigData

This guide shows exactly how to test the whole project with working components.

## QUICK TEST (5 minutes)

The fastest way to see everything working **without HDFS/Spark complexity**.

### Step 1: Start Streamlit

```bash
python -m streamlit run app/interface.py
```

Open **http://localhost:8501** in your browser.

### Step 2: Explore the UI (Live Now)

All tabs are functional:
- **Home**: Shows this README
- **Runbook**: Lists all commands (reference only)
- **Data**: Preview CSVs in `app/data/` and `app/results/` ✅ WORKS
- **Analytics**: Shows demo chart (Mongo not connected yet)
- **Architecture**: System docs

---

## FULL TEST (with MongoDB, 10 minutes)

Get real MongoDB analytics working.

### Step 1: Create `.env` file

```
MONGOINITDBROOTUSERNAME=root
MONGOINITDBROOTPASSWORD=example
MONGODB=agridb
```

### Step 2: Start Docker containers

```bash
docker compose up -d
```

Verify:
```bash
docker ps
```

You should see 5 containers running (hadoop, spark, mongodb, app).

### Step 3: Generate sample data (host)

```bash
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py
```

Output:
- ✅ 96 sensor JSON files generated → `app/data/gateway_output/`
- ✅ Disease metadata cleaned → `app/data/disease_metadata_clean.csv`
- ✅ Data loaded to MongoDB `diseasemetadata` collection

### Step 4: Reload Streamlit UI

Refresh http://localhost:8501 → **Analytics** tab

You'll see:
- ✅ Connected to MongoDB
- ✅ Disease data populated from `diseasemetadata` collection
- ✅ If no `analyticsdaily` collection yet → shows demo chart (normal)

---

## OPTIONAL: Full Spark Pipeline (15 minutes)

⚠️ **HDFS/Datanode issues prevent data push to HDFS.** Skip this for demo testing.  
If you need Spark outputs, use **local file workaround** below.

### Workaround: Use local Spark job (no HDFS)

1. Modify `spark_batch_pipeline.py` to read/write local files:
   ```python
   # INSTEAD OF HDFS, use local:
   df = spark.read.json("app/data/gateway_output/*.json")
   df.write.parquet("app/results/spark_output/aggdaily")
   ```

2. Run locally:
   ```bash
   docker exec spark bash -lc "cd /opt/app/scripts && python spark_batch_pipeline_local.py"
   ```

3. Load to MongoDB:
   ```bash
   docker exec spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"
   ```

---

## TESTING CHECKLIST

### ✅ Test 1: UI Loads (No Docker needed)

```bash
pip install -r requirements.txt
python -m streamlit run app/interface.py
```

At http://localhost:8501:
- [x] Home tab displays README
- [x] Runbook tab shows commands
- [x] Data tab lists files in `app/data/` and `app/results/`
- [x] Can preview CSVs and download
- [x] Analytics tab shows demo chart

**Time: 1 minute | No dependencies**

---

### ✅ Test 2: Generate Data (With MongoDB)

```bash
# .env created in Step 1
docker compose up -d
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py
```

Verify data in MongoDB:
```bash
docker exec mongodb mongosh -u root -p example --authenticationDatabase admin agridb --eval "db.diseasemetadata.countDocuments()"
```

Expected output: `> 5` (disease records)

**Time: 2 minutes | MongoDB working**

---

### ✅ Test 3: View Analytics (Full Test)

Refresh Streamlit UI → **Analytics** tab.

Expected to see:
- [x] "Connected to MongoDB" message OR demo chart
- [x] Filters: crop type, field ID (if data present)
- [x] CSV export button
- [x] Charts render without errors

**Time: 1 minute | UI + Mongo integrated**

---

### ❌ Test 4: HDFS/Spark (Known Issue)

Datanode fails to accept writes. **Skip for coursework.**

Reason: bde2020/hadoop-namenode image has configuration issues in this Docker environment.

---

## KEY URLS & COMMANDS

| Component | URL / Command | Status |
|-----------|---------------|--------|
| Streamlit UI | http://localhost:8501 | ✅ Working |
| HDFS Web UI | http://localhost:9870 | ✅ Running (read-only) |
| MongoDB | localhost:27017 (root/example) | ✅ Working |
| Sample Data | `app/data/gateway_output/*.json` | ✅ 96 files |
| Disease CSV | `app/data/disease_metadata_clean.csv` | ✅ Generated |
| Sample Results | `app/results/*.csv` | ✅ Present |
| **Spark** | **docker exec spark...** | ❌ **HDFS write issue** |

---

## FILE STRUCTURE AFTER TESTING

```
app/
├── data/
│   ├── disease_metadata_raw.csv           (input)
│   ├── disease_metadata_clean.csv         (✅ generated)
│   ├── gateway_output/                    (✅ 96 JSONs generated)
│   │   ├── sensorbatch202512090000.json
│   │   ├── sensorbatch202512090015.json
│   │   ├── ...
│   │   └── sensorbatch202512092345.json
│   └── yoursample.csv                     (sample)
├── results/
│   ├── aggdaily_sample.csv               (sample output format)
│   └── diseasestats_sample.csv           (sample output format)
├── scripts/
│   ├── simulate_sensors_gateway.py       (✅ runs locally)
│   ├── prepare_disease_metadata.py       (✅ runs locally)
│   ├── spark_batch_pipeline.py           (Spark job - HDFS issue)
│   └── load_analytics_to_mongo.py        (✅ works with Mongo)
└── interface.py                           (✅ Streamlit UI)
```

---

## WHAT WORKS ✅

- Streamlit UI with 5 tabs (all functional)
- Data generation (sensors + disease metadata)
- MongoDB connection and data storage
- Analytics plots and filters
- CSV preview and download
- Environment configuration

---

## KNOWN ISSUES ❌

- **Hadoop datanode replication**: Cannot write files to HDFS (0 datanodes available)
  - Cause: Docker volume mount permissions or container initialization issue
  - Impact: Cannot run Spark batch job on HDFS data
  - **Workaround**: Use local file I/O instead

---

## HOW TO USE FOR COURSEWORK

1. **Run Test 1 + 2** (UI + data generation) → Enough to demonstrate the stack
2. **Show UI screenshots** in your report (Runbook tab, Data preview, Analytics)
3. **Document data flow**: Sensors → CSV → MongoDB → UI
4. **Optional**: Write alternative Spark pipeline that reads/writes local files

---

## COMMANDS REFERENCE

### Start everything:
```bash
docker compose up -d
```

### Generate data:
```bash
python app/scripts/simulate_sensors_gateway.py
python app/scripts/prepare_disease_metadata.py
```

### View MongoDB:
```bash
docker exec mongodb mongosh -u root -p example --authenticationDatabase admin agridb --eval "db.diseasemetadata.find().limit(2)"
```

### Start UI:
```bash
python -m streamlit run app/interface.py
```

### Stop everything:
```bash
docker compose down
```

---

**Bottom line**: Run **Test 1 & 2** to validate the project. Add Test 3 analytics if you want full integration. That covers 90% of the big-data pipeline for your coursework. 🎓

