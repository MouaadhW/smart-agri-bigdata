import os
from datetime import datetime

import io
import json
import subprocess
from datetime import date as pydate

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pymongo import MongoClient


st.set_page_config(
    page_title="Smart Agri BigData Dashboard",
    layout="wide",
)


# ----------- Styling Utilities ----------- #
def show_date_banner() -> None:
    """Render a simple date/time banner."""
    st.markdown(
        f"""
        <div style="padding:12px 16px; border-radius:8px; background:#f0f7f4; border:1px solid #d6efe0;">
            <div style="font-size:20px; font-weight:700;">🌱 Smart Agri BigData Dashboard</div>
            <div style="font-size:14px; color:#1b4332;">🕒 {datetime.now().strftime("%A, %d %B %Y – %H:%M:%S")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Sidebar navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    ["Home", "Pipeline Guide", "Runbook", "Data", "Analytics", "Architecture & Docs"],
    index=0,
)

st.sidebar.info(
    "Add data to /app/data/.\n\nPlace diagrams in /app/images/.\n\n"
    "Always see the top for date/time!"
)

# Paths
APP_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
DATA_DIR = os.path.join(APP_DIR, "data")
IMAGE_DIR = os.path.join(APP_DIR, "images")
RESULTS_DIR = os.path.join(APP_DIR, "results")

# ------------- Main Banner -------------- #
show_date_banner()


# --------------- Home ------------------- #
if section == "Home":
    st.subheader("🌻 Project Overview")

    readme_path = os.path.join(PROJECT_ROOT, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme = f.read()
            st.markdown(readme)
    else:
        st.warning(
            "README.md not found in project root! Please add it for project summary."
        )

    st.markdown("---")
    st.success("Use the sidebar to view data, analytics, and system diagrams.")


elif section == "Pipeline Guide":
    st.subheader("📊 Data Processing Pipeline — Step-by-Step Guide")
    
    st.markdown("""
The Smart Agri BigData pipeline processes IoT sensor data through multiple stages. 
Follow these steps in order to populate MongoDB with analytics.
""")
    
    # ===== ONE-CLICK AUTOMATION SECTION =====
    st.markdown("---")
    st.markdown("## ⚡ One-Click Automation")
    st.info("🚀 **Run the entire pipeline automatically in one click!** This will execute all 5 steps in sequence and show you real-time progress.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        run_full_pipeline = st.button(
            "🤖 Run Full Pipeline (Auto)",
            key="run_full_pipeline",
            use_container_width=False,
            help="Runs all 5 pipeline steps automatically: Sensor Data → Disease Metadata → HDFS → Spark → MongoDB"
        )
    
    if run_full_pipeline:
        # Create a progress container
        progress_container = st.container()
        status_placeholder = progress_container.empty()
        
        with status_placeholder.container():
            st.info("⏳ Running pipeline... This may take 2-5 minutes. Check the progress below:")
            
            # Use a placeholder for the log output
            log_output = st.empty()
            
            try:
                # Run the full pipeline script
                result = subprocess.run(
                    ["python", "app/scripts/run_full_pipeline.py"],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=600  # 10 minutes timeout
                )
                
                # Display the output in a code block for readability
                if result.stdout:
                    log_output.code(result.stdout, language="text")
                
                # Check if successful
                if result.returncode == 0:
                    st.success("✅ **Pipeline Completed Successfully!** MongoDB is now populated with analytics.")
                    st.balloons()
                    st.info("👉 Switch to the **Analytics** tab to view live dashboards!")
                else:
                    st.warning("⚠️ **Pipeline completed with some errors.** Check the log above for details.")
                    if result.stderr:
                        st.error(f"Error output:\n{result.stderr}")
                        
            except subprocess.TimeoutExpired:
                st.error("❌ Pipeline execution timed out (exceeded 10 minutes). Please check the system logs.")
            except Exception as e:
                st.error(f"❌ Error running pipeline: {str(e)}")
    
    st.markdown("---")
    st.markdown("## 📋 Manual Step-by-Step Guide")
    st.markdown("**Prefer to run steps manually?** Use the guide below to execute each step individually:")
    
    # Step 1
    with st.container():
        st.markdown("### Step 1: Generate Sensor Data")
        st.markdown("""
**What it does**: Simulates 96 batches of IoT sensor readings (24 hours at 15-min intervals)

**Files generated**: 
- `app/data/gateway_output/sensorbatch*.json` (96 files)

**Command** (run from project root):
```bash
python app/scripts/simulate_sensors_gateway.py
```

**Expected output**:
```
Sensor simulation finished. Files in data/gateway_output/
```
        """)
        if st.button("🔄 Run Step 1 Only", key="gen_sensor_only"):
            try:
                result = subprocess.run(
                    ["python", "app/scripts/simulate_sensors_gateway.py"],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    st.success("✅ Sensor data generated successfully!")
                    st.info(f"{len([f for f in os.listdir(os.path.join(DATA_DIR, 'gateway_output')) if f.endswith('.json')])} JSON files created")
                else:
                    st.error(f"Error: {result.stderr}")
            except Exception as e:
                st.error(f"Error running script: {e}")
    
    st.markdown("---")
    
    # Step 2
    with st.container():
        st.markdown("### Step 2: Prepare Disease Metadata")
        st.markdown("""
**What it does**: Cleans and prepares disease metadata CSV for processing

**Files created**:
- `app/data/disease_metadata_clean.csv`

**Command** (run from project root):
```bash
python app/scripts/prepare_disease_metadata.py
```

**Expected output**:
```
Disease metadata cleaned and loaded into MongoDB.
```
        """)
        if st.button("🏥 Run Step 2 Only", key="prep_disease_only"):
            try:
                result = subprocess.run(
                    ["python", "app/scripts/prepare_disease_metadata.py"],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    st.success("✅ Disease metadata prepared successfully!")
                else:
                    st.error(f"Note: May fail if MongoDB unreachable, but CSV is still created")
                    st.info("CSV file created: disease_metadata_clean.csv")
            except Exception as e:
                st.error(f"Error running script: {e}")
    
    st.markdown("---")
    
    # Step 3
    with st.container():
        st.markdown("### Step 3: Push Data to HDFS (Docker)")
        st.markdown("""
**What it does**: Copies sensor and disease data to Hadoop distributed filesystem

**Command** (run from project root):
```bash
docker exec hadoop-namenode bash -lc "\\
  /opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data/agri/sensors /data/agri/disease && \\
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/gateway_output/*.json /data/agri/sensors && \\
  /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/disease_metadata_clean.csv /data/agri/disease/"
```

**Check HDFS UI**: http://localhost:9870/dfshealth.html
        """)
    
    st.markdown("---")
    
    # Step 4
    with st.container():
        st.markdown("### Step 4: Run Spark Batch Pipeline (Docker)")
        st.markdown("""
**What it does**: 
- Reads sensor JSON from HDFS
- Validates data (outlier detection, range checks)
- Aggregates by date, field, and crop type
- Computes daily averages (soil moisture, temp, air humidity, etc.)
- Outputs Parquet files

**Command** (run from project root):
```bash
docker exec -it spark bash -lc "cd /opt/app/scripts && spark-submit spark_batch_pipeline.py"
```

**Expected output**:
```
HDFS paths created:
- /data/agri/output/aggdaily (Parquet)
- /data/agri/output/diseasestats (Parquet)
```
        """)
    
    st.markdown("---")
    
    # Step 5
    with st.container():
        st.markdown("### Step 5: Load Analytics to MongoDB (Docker)")
        st.markdown("""
**What it does**: Converts Parquet output to MongoDB documents and inserts into `analyticsdaily` collection

**Command** (run from project root):
```bash
docker exec -it spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"
```

**Expected output**:
```
Loaded X analytics records into MongoDB
```

**Collections created**:
- `analyticsdaily` — Daily aggregated sensor metrics
- `diseasemetadata` — Disease reference data
        """)
    
    st.markdown("---")
    
    # Step 6
    with st.container():
        st.markdown("### Step 6: View Live Analytics")
        st.markdown("""
**What it does**: Dashboard connects to MongoDB and displays real-time analytics

**Command**: Simply switch to the **Analytics** tab in this dashboard!

**You will see**:
- Soil moisture trends (time series)
- Disease occurrence by crop type (bar chart)
- Drought risk distribution (bar chart)
- Live filtering by crop type and field ID
        """)
    
    st.markdown("---")
    
    # Summary table
    st.markdown("### Pipeline Summary")
    pipeline_steps = {
        "Step": [
            "1️⃣ Generate Sensors",
            "2️⃣ Prepare Disease Data",
            "3️⃣ Push to HDFS",
            "4️⃣ Spark Processing",
            "5️⃣ Load to MongoDB",
            "6️⃣ View Analytics"
        ],
        "Location": [
            "Host machine",
            "Host machine",
            "Docker (Hadoop)",
            "Docker (Spark)",
            "Docker (Spark)",
            "Streamlit Dashboard"
        ],
        "Time": [
            "~5 seconds",
            "~2 seconds",
            "~10 seconds",
            "~30 seconds",
            "~5 seconds",
            "Real-time"
        ],
        "Output": [
            "96 JSON files",
            "1 CSV file",
            "HDFS /data/agri/",
            "Parquet files",
            "MongoDB docs",
            "Live plots"
        ]
    }
    st.table(pipeline_steps)
    
    st.markdown("---")
    
    st.info("""
**⚡ Quick Start (All Steps)**:
1. Open terminal in project root
2. Run: `python app/scripts/simulate_sensors_gateway.py`
3. Run: `python app/scripts/prepare_disease_metadata.py`
4. Run: `docker exec hadoop-namenode bash -lc "/opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data/agri/sensors /data/agri/disease && /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /opt/data/gateway_output/*.json /data/agri/sensors"`
5. Run: `docker exec -it spark bash -lc "cd /opt/app/scripts && spark-submit spark_batch_pipeline.py"`
6. Run: `docker exec -it spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"`
7. Refresh Analytics tab to see live data!
    """)


elif section == "Runbook":
    st.subheader("🛠️ Runbook — How to run the full pipeline")
    st.markdown(
        """
        This runbook contains the minimal, copyable commands to run the full stack locally.

        1. Create `.env` in the repo root with MongoDB credentials:
        ```
        MONGOINITDBROOTUSERNAME=root
        MONGOINITDBROOTPASSWORD=example
        MONGODB=agridb
        ```

        2. Start services with Docker Compose (from repo root):
        ```bash
        docker compose up -d
        ```

        3. (Host) Generate sample sensor JSONs and disease metadata:
        ```bash
        python app/scripts/simulate_sensors_gateway.py
        python app/scripts/prepare_disease_metadata.py
        ```

        4. Push sample files into HDFS (run on host, adjusted to your container names):
        ```bash
        docker exec -it hadoop-namenode bash -lc "\
          hdfs dfs -mkdir -p /data/agri/sensors /data/agri/disease && \
          hdfs dfs -put -f /opt/data/gateway_output/*.json /data/agri/sensors && \
          hdfs dfs -put -f /opt/data/disease_metadata_clean.csv /data/agri/disease/"
        ```

        5. Run the Spark batch job (in `spark` container):
        ```bash
        docker exec -it spark bash -lc "cd /opt/app/scripts && spark-submit spark_batch_pipeline.py"
        ```

        6. Load analytics into MongoDB (from `spark` or `app` container):
        ```bash
        docker exec -it spark bash -lc "cd /opt/app/scripts && python load_analytics_to_mongo.py"
        ```

        7. Open the Streamlit UI on the host:
        ```bash
        python -m streamlit run app/interface.py
        ```
        """
    )

    st.markdown("---")
    st.info("See `docker-compose.yml` and `README.md` in the project root for more details.")

elif section == "Data":
    st.subheader("📁 Data Explorer — preview and download")

    # Ensure results dir exists
    if not os.path.isdir(DATA_DIR):
        st.warning("/app/data/ folder does not exist! Please create and add data files.")
    else:
        st.markdown("**Sample Data (app/data/)**")
        data_files = sorted(os.listdir(DATA_DIR))
        if data_files:
            choice = st.selectbox("Select a file to preview:", data_files)
            preview_path = os.path.join(DATA_DIR, choice)
            try:
                if choice.lower().endswith(".csv"):
                    df = pd.read_csv(preview_path)
                    st.write(f"Preview: {choice}")
                    st.dataframe(df.head(200), use_container_width=True)
                    csv_bytes = df.to_csv(index=False).encode("utf-8")
                    st.download_button("Download CSV", data=csv_bytes, file_name=choice, mime="text/csv")
                else:
                    with open(preview_path, "rb") as f:
                        data = f.read()
                        st.download_button("Download file", data=data, file_name=choice)
            except Exception as e:  # pragma: no cover - shown in UI
                st.error(f"Error reading file: {e}")
        else:
            st.info("No files found in /app/data/.")

        # quick local generator actions
        with st.expander("Generate sample data (runs scripts locally)"):
            st.markdown(
                "Run the generator/prep scripts to create sample sensor JSONs and cleaned disease metadata."
            )
            run_gen = st.button("Run simulate_sensors_gateway.py")
            run_prep = st.button("Run prepare_disease_metadata.py")
            if run_gen:
                script = os.path.join(APP_DIR, "scripts", "simulate_sensors_gateway.py")
                with st.spinner("Running generator..."):
                    try:
                        res = subprocess.run(["python", script], capture_output=True, text=True, check=True)
                        st.success("Generator finished")
                        st.text(res.stdout or res.stderr)
                    except subprocess.CalledProcessError as e:
                        st.error(f"Generator failed: {e}\n{e.stdout}\n{e.stderr}")
            if run_prep:
                script = os.path.join(APP_DIR, "scripts", "prepare_disease_metadata.py")
                with st.spinner("Running metadata prep..."):
                    try:
                        res = subprocess.run(["python", script], capture_output=True, text=True, check=True)
                        st.success("Metadata prep finished")
                        st.text(res.stdout or res.stderr)
                    except subprocess.CalledProcessError as e:
                        st.error(f"Prep failed: {e}\n{e.stdout}\n{e.stderr}")

    # Results dir preview (if present)
    st.markdown("---")
    st.markdown("**Pipeline Results (app/results/)**")
    if not os.path.isdir(RESULTS_DIR):
        st.info("No results directory found. Run the Spark job to produce outputs to /app/results or HDFS.")
    else:
        result_files = sorted(os.listdir(RESULTS_DIR))
        if result_files:
            rchoice = st.selectbox("Select a results file:", result_files, key="results_select")
            rpath = os.path.join(RESULTS_DIR, rchoice)
            try:
                if rchoice.lower().endswith(".csv"):
                    rdf = pd.read_csv(rpath)
                    st.dataframe(rdf.head(200), use_container_width=True)
                    st.download_button("Download Results CSV", data=rdf.to_csv(index=False).encode("utf-8"), file_name=rchoice, mime="text/csv")
                else:
                    st.info("Non-CSV result. Mount or convert parquet/other formats to preview here.")
            except Exception as e:
                st.error(f"Error reading results file: {e}")


# ------------- Analytics ---------------- #
elif section == "Analytics":
    st.subheader("📈 Analytics & Batch Results")
    st.write(
        "Display the results of your batch/Spark processing here. "
        "Expand to pull real outputs as your pipeline matures!"
    )
    # Try to connect to MongoDB and load `analyticsdaily` collection
    MONGOHOST = os.getenv("MONGOHOST", "mongodb")
    MONGOPORT = int(os.getenv("MONGOPORT", "27017"))
    MONGOUSER = os.getenv("MONGOINITDBROOTUSERNAME", "root")
    MONGOPWD = os.getenv("MONGOINITDBROOTPASSWORD", "example")
    MONGODB = os.getenv("MONGODB", "agridb")

    def get_mongo_client():
        """Try to connect to MongoDB with fallback to localhost if Docker name fails"""
        hosts_to_try = [MONGOHOST, "localhost", "127.0.0.1"]
        
        for host in hosts_to_try:
            try:
                client = MongoClient(
                    host=host, 
                    port=MONGOPORT, 
                    username=MONGOUSER, 
                    password=MONGOPWD, 
                    serverSelectionTimeoutMS=2000,
                    connectTimeoutMS=2000,
                    socketTimeoutMS=2000
                )
                # attempt server selection
                client.server_info()
                return client
            except Exception as e:
                continue
        return None

    @st.cache_data(ttl=30)
    def load_analytics_from_mongo():
        client = get_mongo_client()
        if not client:
            return None
        db = client[MONGODB]
        coll = db.get_collection("analyticsdaily")
        docs = list(coll.find({}))
        if not docs:
            return pd.DataFrame()
        # normalize docs into DataFrame
        rows = []
        for d in docs:
            row = dict(d)
            # remove Mongo _id if present
            row.pop("_id", None)
            rows.append(row)
        df = pd.json_normalize(rows)
        # try parse date column
        if "date" in df.columns:
            try:
                df["date"] = pd.to_datetime(df["date"]).dt.date
            except Exception:
                pass
        return df

    df = load_analytics_from_mongo()
    if df is None:
        st.error("❌ Could not connect to MongoDB. Make sure MongoDB container is running.")
        st.markdown("""
**Troubleshooting**:
- Check if MongoDB is running: `docker ps | grep mongodb`
- Restart MongoDB: `docker-compose restart mongodb`
- Verify connection in Docker: `docker logs mongodb`
        """)
    else:
        if df.empty:
            st.info("📊 Connected to MongoDB but analyticsdaily is empty!")
            st.markdown("""
### How to Populate MongoDB with Analytics

Your MongoDB is connected and ready, but the `analyticsdaily` collection is empty. 
Follow these steps to populate it with processed sensor data:

#### Option A: Use the Pipeline Guide (Recommended) 🚀
1. Click **"Pipeline Guide"** in the sidebar
2. Click the **"🤖 Run Full Pipeline (Auto)"** button
3. Wait for completion (about 1 minute)
4. Refresh this page to see live analytics!

#### Option B: Manual Commands (Fast Track)
Run these commands in order from the project root:

```bash
# Step 1: Generate sensor data (96 files)
python app/scripts/simulate_sensors_gateway.py

# Step 2: Prepare disease metadata
python app/scripts/prepare_disease_metadata.py

# Step 3-5: Run Spark pipeline and load to MongoDB
docker exec spark bash -c "cd /opt/app/scripts && python load_analytics_to_mongo.py"
```

After the commands complete, **refresh this page** to see live analytics! 🎉
            """)
            st.success("💡 Tip: Use the **Pipeline Guide** tab for the easiest one-click automation!")
        else:
            st.success(f"📊 Connected to MongoDB with {len(df)} analytics records!")
            
            # Display the raw data table first
            with st.expander("📋 View Raw Data Table"):
                st.dataframe(df, use_container_width=True)
            
            # Create tabs for different visualizations
            chart_tabs = st.tabs(["📈 Soil Metrics", "🌡️ Temperature", "💧 Humidity", "📊 Summary Stats"])
            
            with chart_tabs[0]:
                # Soil Moisture Over Time
                st.markdown("### Soil Moisture by Field")
                if "date" in df.columns and "avgsoilmoisture" in df.columns:
                    fig_moisture = plt.figure(figsize=(12, 5))
                    for crop in df["croptype"].unique() if "croptype" in df.columns else [None]:
                        if crop:
                            crop_data = df[df["croptype"] == crop].sort_values("date") if "croptype" in df.columns else df.sort_values("date")
                            plt.plot(crop_data["date"], crop_data["avgsoilmoisture"], marker="o", label=str(crop), linewidth=2)
                    plt.xlabel("Date")
                    plt.ylabel("Avg Soil Moisture")
                    plt.title("Soil Moisture Trends")
                    plt.legend()
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig_moisture)
                
                # Soil Moisture by Crop Type (Bar Chart)
                st.markdown("### Soil Moisture by Crop Type")
                if "croptype" in df.columns:
                    moisture_by_crop = df.groupby("croptype")["avgsoilmoisture"].mean()
                    fig_crop = plt.figure(figsize=(10, 5))
                    bars = plt.bar(moisture_by_crop.index, moisture_by_crop.values, color="#66bb6a")
                    plt.ylabel("Average Soil Moisture")
                    plt.xlabel("Crop Type")
                    plt.title("Average Soil Moisture by Crop Type")
                    plt.xticks(rotation=45)
                    for bar in bars:
                        height = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.2f}', ha='center', va='bottom')
                    plt.tight_layout()
                    st.pyplot(fig_crop)
            
            with chart_tabs[1]:
                # Temperature Trends
                st.markdown("### Temperature Trends by Field")
                if "date" in df.columns and "avgsoiltemp" in df.columns and "avgairtemp" in df.columns:
                    fig_temp = plt.figure(figsize=(12, 6))
                    df_sorted = df.sort_values("date")
                    plt.plot(df_sorted["date"], df_sorted["avgsoiltemp"], marker="o", label="Soil Temp", linewidth=2, color="orange")
                    plt.plot(df_sorted["date"], df_sorted["avgairtemp"], marker="s", label="Air Temp", linewidth=2, color="red")
                    plt.xlabel("Date")
                    plt.ylabel("Temperature (°C)")
                    plt.title("Temperature Comparison: Soil vs Air")
                    plt.legend()
                    plt.xticks(rotation=45)
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig_temp)
                
                # Temperature Stats by Crop
                st.markdown("### Temperature Statistics by Crop")
                if "croptype" in df.columns:
                    temp_stats = df.groupby("croptype")[["avgsoiltemp", "avgairtemp"]].mean()
                    fig_temp_bar = plt.figure(figsize=(10, 5))
                    x = range(len(temp_stats.index))
                    width = 0.35
                    bars1 = plt.bar([i - width/2 for i in x], temp_stats["avgsoiltemp"], width, label="Soil Temp", color="orange")
                    bars2 = plt.bar([i + width/2 for i in x], temp_stats["avgairtemp"], width, label="Air Temp", color="red")
                    plt.xlabel("Crop Type")
                    plt.ylabel("Temperature (°C)")
                    plt.title("Average Temperature by Crop Type")
                    plt.xticks(x, temp_stats.index, rotation=45)
                    plt.legend()
                    plt.tight_layout()
                    st.pyplot(fig_temp_bar)
            
            with chart_tabs[2]:
                # Humidity Over Time
                st.markdown("### Air Humidity Over Time")
                if "date" in df.columns and "avgairhumidity" in df.columns:
                    fig_humidity = plt.figure(figsize=(12, 5))
                    df_sorted = df.sort_values("date")
                    plt.fill_between(range(len(df_sorted)), df_sorted["avgairhumidity"], alpha=0.5, color="steelblue")
                    plt.plot(df_sorted["date"], df_sorted["avgairhumidity"], marker="o", color="steelblue", linewidth=2)
                    plt.xlabel("Date")
                    plt.ylabel("Air Humidity (%)")
                    plt.title("Air Humidity Trends")
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig_humidity)
                
                # Humidity by Crop
                st.markdown("### Humidity by Crop Type")
                if "croptype" in df.columns:
                    humidity_by_crop = df.groupby("croptype")["avgairhumidity"].mean()
                    fig_humidity_crop = plt.figure(figsize=(10, 5))
                    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
                    bars = plt.bar(humidity_by_crop.index, humidity_by_crop.values, color=colors[:len(humidity_by_crop)])
                    plt.ylabel("Average Humidity (%)")
                    plt.xlabel("Crop Type")
                    plt.title("Average Humidity by Crop Type")
                    plt.xticks(rotation=45)
                    for bar in bars:
                        height = bar.get_height()
                        plt.text(bar.get_x() + bar.get_width()/2., height,
                                f'{height:.1f}%', ha='center', va='bottom')
                    plt.tight_layout()
                    st.pyplot(fig_humidity_crop)
            
            with chart_tabs[3]:
                # Summary Statistics
                st.markdown("### Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                if "avgsoilmoisture" in df.columns:
                    with col1:
                        st.metric("Avg Soil Moisture", f"{df['avgsoilmoisture'].mean():.2f}")
                
                if "avgsoiltemp" in df.columns:
                    with col2:
                        st.metric("Avg Soil Temp", f"{df['avgsoiltemp'].mean():.1f}°C")
                
                if "avgairtemp" in df.columns:
                    with col3:
                        st.metric("Avg Air Temp", f"{df['avgairtemp'].mean():.1f}°C")
                
                if "avgairhumidity" in df.columns:
                    with col4:
                        st.metric("Avg Humidity", f"{df['avgairhumidity'].mean():.1f}%")
                
                # Detailed statistics table
                st.markdown("### Detailed Statistics")
                stats_df = df[["avgsoilmoisture", "avgsoiltemp", "avgairtemp", "avgairhumidity"]].describe()
                st.dataframe(stats_df, use_container_width=True)
            
            # Filters section
            st.markdown("---")
            st.markdown("### Filters")
            cols_for_filter = {}
            if "croptype" in df.columns:
                croptypes = sorted(df["croptype"].dropna().unique().tolist())
                sel_crop = st.selectbox("Filter by crop type", ["All"] + croptypes)
                if sel_crop != "All":
                    df = df[df["croptype"] == sel_crop]
            if "fieldid" in df.columns:
                fids = sorted(df["fieldid"].dropna().unique().tolist())
                sel_field = st.selectbox("Filter by field id", ["All"] + fids)
                if sel_field != "All":
                    df = df[df["fieldid"] == sel_field]

            # Time series: avgsoilmoisture by date
            if "date" in df.columns and "metrics.avgsoilmoisture" in df.columns:
                ts = df.groupby("date")["metrics.avgsoilmoisture"].mean().reset_index()
                st.markdown("#### Avg Soil Moisture (time series)")
                st.line_chart(ts.rename(columns={"date": "index"}).set_index("index"))

            # Disease counts by crop type (if diseasestats present)
            if "croptype" in df.columns and "diseasestats" in df.columns:
                # diseasestats is stored as list; try to extract occurrencecount
                def extract_occurrence(ds):
                    try:
                        if isinstance(ds, list) and len(ds) > 0:
                            first = ds[0]
                            return float(first.get("occurrencecount", 0))
                    except Exception:
                        return 0
                    return 0

                df["diseases_count"] = df["diseasestats"].apply(extract_occurrence)
                agg = df.groupby("croptype")["diseases_count"].sum().sort_values(ascending=False)
                st.markdown("#### Disease occurrence by Crop Type")
                fig2, ax2 = plt.subplots(figsize=(6, 4))
                agg.plot(kind="bar", ax=ax2, color="#f28c8c")
                ax2.set_ylabel("Occurrence count")
                st.pyplot(fig2)

            # Drought risk distribution
            if "metrics.droughtrisklevel" in df.columns:
                st.markdown("#### Drought Risk Distribution")
                dist = df["metrics.droughtrisklevel"].value_counts()
                st.bar_chart(dist)

            st.markdown("---")
            st.download_button("Download analytics as CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="analytics_export.csv", mime="text/csv")


# -------- Architecture & Docs ----------- #
elif section == "Architecture & Docs":
    st.subheader("🗺️ System Architecture & Documentation")

    img_path = os.path.join(IMAGE_DIR, "sys_arch.png")
    if os.path.exists(img_path):
        st.image(img_path, caption="System/Architecture Diagram", use_container_width=True)
    else:
        st.warning(
            "System diagram not found at /app/images/sys_arch.png. "
            "Please add your architecture image."
        )

    st.markdown("---")
    st.markdown(
        """
Ecosystem Technologies:
• 🗄️ HDFS – Distributed storage for scalable batch data
• 📂 MongoDB – Flexible NoSQL storage for sensor and metadata
• ⚡ Spark – Batch analytics, aggregation, and data cleaning
• 🐍 Python – Orchestrates ETL steps and dashboards

Data Flow:
Sensors generate CSV files, transferred via gateways to the data lake.
Data lands in HDFS for batch processing or is ingested to MongoDB for fast access.
Spark jobs run on the cluster, producing analytics (disease count, statistics, alerts, ...)
Visual results and summaries shown on this dashboard.

Document all steps, system decisions, and results in your report, referencing this interface for reproducible results and demos!
"""
    )


st.caption(
    "Smart Agri BigData · Academic Prototype · Horizon School of Digital Technologies (2025-2026)"
)

