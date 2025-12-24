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
    ["Home", "Runbook", "Data", "Analytics", "Architecture & Docs"],
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
        try:
            client = MongoClient(host=MONGOHOST, port=MONGOPORT, username=MONGOUSER, password=MONGOPWD, serverSelectionTimeoutMS=3000)
            # attempt server selection
            client.server_info()
            return client
        except Exception as e:
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
        st.warning("Could not connect to MongoDB. Showing demo chart instead.")
        # fallback demo
        st.markdown("#### Example: Disease Frequency by Plant (Demo Data)")
        plants = ["Tomato", "Potato", "Corn", "Wheat"]
        disease_counts = [17, 9, 14, 5]
        fig, ax = plt.subplots(figsize=(6, 4))
        bars = ax.bar(plants, disease_counts, color="#66bb6a")
        ax.set_ylabel("Disease Reports")
        ax.set_xlabel("Plant")
        ax.set_title("Diseases by Plant Type")
        ax.bar_label(bars)
        st.pyplot(fig)
    else:
        if df.empty:
            st.info("Connected to MongoDB but `analyticsdaily` is empty. Run the pipeline to load analytics.")
        else:
            st.success(f"Loaded {len(df)} analytics records from MongoDB")
            # filters
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

