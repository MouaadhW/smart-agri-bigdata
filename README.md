# 🌾 Smart Agriculture Big Data Platform

End-to-end big data system for agricultural IoT monitoring, batch processing, and analytics using Hadoop, Spark, MongoDB, and modern Dash/Plotly dashboards.

**Status**: ✅ Complete and Production-Ready | **Version**: 2.0 | **Location**: Tunisia 🇹🇳 | **Currency**: USD 💵

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start dashboard
cd app/
python dashboard.py

# 3. Open in browser
# http://localhost:8050
```

**That's it!** Explore 7 interactive tabs with sample data, real weather forecasts, and farm economics analysis.

---

## 📊 Dashboard Features

### 7 Main Tabs:

| Tab | Icon | Features |
|-----|------|----------|
| **Home** | 🏠 | System overview, quick start guide, technology stack |
| **Pipeline** | 🚀 | One-click automation button (runs all 5 processing steps) |
| **Analytics** | 📈 | Interactive charts, disease metrics, crop advisory system |
| **Architecture** | 🏗️ | System architecture diagram, pipeline flowchart, tech details |
| **Weather & Climate** | 🌤️ | Real-time forecasts, climate risk analysis, irrigation planning |
| **Cost-Benefit** | 💰 | ROI calculator, crop profitability, market scenarios |
| **Sensor Data** | 📡 | Real-time sensor readings table (when MongoDB available) |

### Key Capabilities:

- ✅ **IoT Simulation**: Generates realistic sensor data (moisture, temperature, humidity)
- ✅ **Batch Processing**: Apache Spark aggregates sensor readings daily
- ✅ **Distributed Storage**: Hadoop HDFS + MongoDB for data persistence
- ✅ **Modern Dashboard**: Interactive Dash/Plotly UI with responsive design
- ✅ **Intelligent Crop Advisory**: AI-powered recommendations based on environmental conditions
- ✅ **One-Click Pipeline**: Automate entire data processing pipeline via dashboard button
- ✅ **Architecture Visualization**: System diagrams showing 4-layer architecture and 4-phase pipeline
- ✅ **🌤️ Weather Intelligence**: Real-time weather API + 7-day forecasts + climate risk analysis
- ✅ **💰 Farm Economics**: ROI calculations, crop profitability analysis, market price scenarios

---

## 🌤️ Weather & Climate Intelligence

**Real-time weather data from OpenWeatherMap API** with advanced climate risk analysis for **Tunisia** (Tunis region):

### Features:
- 📡 **Current Weather**: Temperature, humidity, wind, pressure (live updates)
- 📊 **7-Day Forecast**: Interactive charts with temperature ranges and rainfall probability
- 🔍 **Climate Risk Analysis**: Frost, heat stress, excessive rainfall, drought, wind damage, disease risk
- 💧 **Irrigation Scheduling**: Automated recommendations based on rainfall and temperature
- 🎯 **Color-Coded Alerts**: Red (immediate action) → Yellow (plan) → Green (monitor)

### Example Output (Tunisia):
```
Location: Tunis, Tunisia (Lat 33.89°, Lon 9.54°)
Current: 12.4°C, 51% humidity, Clear Sky ☀️
7-Day: Temp 10-18°C, 20% rain probability
Climate Risk: ☀️ Drought risk - Plan irrigation schedule 💨 Strong winds expected - Stake tall crops
Irrigation Need: 52% (Schedule irrigation) 💧
```

---

## 💰 Cost-Benefit & Farm Economics

**Complete financial analysis for 8 crops with ROI calculations and market scenarios** (all values in **USD $**):

### Features:
- 💧 **Irrigation ROI**: Calculate water investment returns in days
- 💵 **Crop Profitability**: Revenue, costs, profit, margin, and ROI for each crop
- 📊 **Crop Comparison**: Visual ranking of all 8 crops by profitability
- 💰 **Cost Breakdown**: Pie chart showing budget allocation (water, labor, seeds, etc.)
- 📈 **Price Scenarios**: Profit analysis under ±10% market price variations
- ✅ **Break-Even Analysis**: Safety margin and risk assessment

### Supported Crops:
🌾 Wheat | 🍚 Rice | 🌻 Cotton | 🎋 Sugarcane | 🌽 Maize | 🥔 Potato | 🧅 Onion | 🍅 Tomato

### Example Profitability (1 hectare):
```
Wheat:  Revenue $1,500 | Cost $385  | Profit $1,115  | Margin 74.3% | ROI 289.6%
Rice:   Revenue $1,265 | Cost $401  | Profit $864   | Margin 68.3% | ROI 215.5%
Cotton: Revenue $1,188 | Cost $431  | Profit $757   | Margin 63.7% | ROI 175.6%
```

---

## 🏗️ System Architecture

```
IoT Sensors (Simulated)
    ↓
Generator Script (Python)
    ↓ (JSON Batches)
Hadoop HDFS ←→ MongoDB (Raw Data)
    ↓
Apache Spark Job
  • Aggregation
  • Disease Detection  
  • Statistics
    ↓ (Processed Data)
MongoDB Analytics Collections
  • aggDaily
  • diseaseStats
  • warnings
    ↓
Dash Dashboard (Port 8050)
  • Interactive Charts
  • Real-time Metrics
  • Crop Recommendations
  • Architecture Diagrams
```

**Services** (Docker Compose):
- **Hadoop**: HDFS NameNode + DataNode (distributed file storage)
- **Spark**: Batch processing engine
- **MongoDB**: NoSQL analytics database (port 27017)
- **Dash App**: Modern web dashboard (port 8050)

---

## 📂 Project Structure

```
smart-agri-bigdata/
├── app/
│   ├── dashboard.py                    # Main Dash dashboard (775 lines)
│   ├── weather_integration.py          # Weather API integration (NEW)
│   ├── cost_benefit_analysis.py        # Farm economics module (NEW)
│   ├── create_architecture_diagram.py  # Architecture visualizer
│   ├── create_pipeline_flowchart.py    # Pipeline visualizer
│   ├── DASHBOARD_USER_GUIDE.md         # User documentation
│   ├── Dockerfile                      # Container config
│   ├── requirements.txt                # Python dependencies
│   ├── data/
│   │   ├── gateway_output/             # Generated sensor JSON files
│   │   └── disease_metadata_*.csv      # Disease reference data
│   ├── images/
│   │   ├── architecture_diagram.png    # System architecture (300 DPI)
│   │   └── pipeline_flowchart.png      # Data pipeline (300 DPI)
│   ├── results/
│   │   ├── aggdaily_sample.csv         # Daily aggregated metrics
│   │   └── diseasestats_sample.csv     # Disease statistics
│   └── scripts/
│       ├── simulate_sensors_gateway.py
│       ├── prepare_disease_metadata.py
│       ├── run_full_pipeline.py
│       ├── load_analytics_to_mongo.py
│       └── spark_batch_pipeline.py
├── hadoop/                             # Hadoop Docker config
├── mongodb/                            # MongoDB Docker config
├── spark/                              # Spark Docker config
├── docker-compose.yml                  # Service orchestration
├── requirements.txt                    # Python dependencies
├── UML_DIAGRAMS.md                     # Complete UML documentation (NEW)
├── NEW_FEATURES.md                     # Weather & Economics guide
└── README.md                           # This file
```

---

## 💻 Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Processing** | Apache Spark 3.x, Python 3.12, PySpark |
| **Storage** | Hadoop HDFS 3.2+, MongoDB 4.4+ |
| **Visualization** | Dash 2.x, Plotly, Dash Bootstrap Components |
| **Infrastructure** | Docker, Docker Compose |

---

## 🔧 Prerequisites

- Python 3.10+ (tested with 3.12)
- Docker + Docker Compose (optional, for full-stack)
- 4GB RAM minimum

---

## 📋 Installation & Setup

### Option 1: Dashboard Only (Recommended for Quick Demo)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Navigate to app directory
cd app/

# Start the dashboard
python dashboard.py
```

Dashboard opens at: **http://localhost:8050**

This works with sample data - no Docker required!

### Option 2: Full Stack (with Docker)

```bash
# Start all services in background
docker-compose up -d

# Verify containers are running
docker ps

# Then start the dashboard
cd app/
python dashboard.py
```

Services running:
- HDFS NameNode: http://localhost:9870
- MongoDB: localhost:27017 (credentials: root/example)
- Dashboard: http://localhost:8050

---

## 📊 Data Pipeline (5 Steps)

1. **Sensor Simulation** → Generates 96 JSON files with 15-min sensor readings
2. **Disease Metadata** → Prepares crop disease reference data  
3. **Hadoop Storage** → Moves data to HDFS distributed storage
4. **Spark Aggregation** → Computes daily averages by field/crop
5. **MongoDB Analytics** → Stores results for dashboard visualization

**One-Click Automation**: Click "🤖 Run Full Pipeline" button in Pipeline tab to execute all 5 steps (~1 minute).

---

## 🧪 Running the Pipeline

### Via Dashboard (Recommended)

1. Open dashboard: **http://localhost:8050**
2. Go to **🚀 Pipeline** tab
3. Click **🤖 Run Full Pipeline** button
4. Monitor progress in output logs
5. Check **📈 Analytics** tab for results

### Via Command Line

```bash
# Run complete pipeline
python app/scripts/run_full_pipeline.py

# Or run individual steps
python app/scripts/simulate_sensors_gateway.py      # Step 1
python app/scripts/prepare_disease_metadata.py      # Step 2
python app/scripts/spark_batch_pipeline.py          # Step 4
python app/scripts/load_analytics_to_mongo.py       # Step 5
```

---

## 📈 Expected Outputs

After running the pipeline:
- **96 sensor JSON files** in `app/data/gateway_output/` (15-min batches)
- **4 analytics records** in MongoDB `analyticsdaily` collection
- **5 disease records** in MongoDB `diseases` collection
- **Interactive charts** in Analytics tab
- **Crop recommendations** based on conditions

---

## 🎨 Architecture Visualization

The dashboard includes two high-quality diagrams:

### System Architecture Diagram (4 Layers)
- Layer 1: Data Generation & Sources (Sensors, Generator, Disease Metadata)
- Layer 2: Data Ingestion & Storage (HDFS, MongoDB Raw Collections)
- Layer 3: Batch Processing & Transformation (Apache Spark)
- Layer 4: Real-Time Visualization (Dash Dashboard)

### Data Pipeline Flowchart (4 Phases)
- Phase 1: Data Generation & Ingestion
- Phase 2: Batch Processing (Spark Job)
- Phase 3: Analytics Loading (MongoDB Collections)
- Phase 4: Real-Time Visualization (Dash UI)

Both diagrams are 300 DPI high-quality PNG files displayed in the **🏗️ Architecture** tab.

---

## 🌾 Crop Advisory System

The Intelligent Crop Advisory analyzes:
- **Soil Moisture**: Alerts for drought (<30%) or waterlogging (>70%)
- **Temperature**: Detects heat stress (>35°C) and cold stress (<10°C)
- **Humidity**: Optimal range 60-80% for most crop stages
- **Combined Analysis**: Predicts likely crop outcomes and provides actionable recommendations

---

## ⚠️ Common Issues & Troubleshooting

### Q: Charts not showing in Analytics tab?
**A**: 
- Ensure Docker containers are running: `docker ps`
- Run the pipeline to populate MongoDB
- Click 🤖 **Run Full Pipeline** button

### Q: "Could not connect to MongoDB"?
**A**:
- Check MongoDB container: `docker logs mongodb`
- Verify port 27017 not blocked
- Or use dashboard without Docker (sample data only)

### Q: Dashboard on wrong port?
**A**:
- Dashboard runs on port **8050** (Dash framework)
- Open: **http://127.0.0.1:8050**

### Q: Crop advisory not showing?
**A**:
- Scroll down in Analytics tab below the charts
- Requires MongoDB data (run pipeline first)

### Q: Pipeline fails?
**A**:
- Check Docker containers running: `docker-compose ps`
- Review logs: `docker logs <container_name>`
- Ensure sufficient disk space

---

## 🧪 Testing & Verification

The system includes pre-generated sample data:
- **Sample analytics**: `app/results/aggdaily_sample.csv`
- **Sample disease stats**: `app/results/diseasestats_sample.csv`
- **Sample data**: Works without Docker for quick demos

To verify the full pipeline:
```bash
# Check generated sensor files
ls -la app/data/gateway_output/*.json | wc -l  # Should show 96 files

# Check MongoDB collections (requires Docker)
docker exec mongodb mongosh -u root -p example --eval "db.agridb.analyticsdaily.countDocuments()"
```

---

## 📱 UI Design Features

- **Farm-Themed Colors**: Dark green, bright green, earth tones, sky blue
- **Responsive Layout**: Bootstrap grid system (desktop and tablet)
- **Interactive Charts**: Plotly with hover info and export
- **Metric Cards**: KPI displays for quick assessment
- **Professional Design**: Clean interface optimized for agricultural use

---

## � UML Diagrams & Documentation

Comprehensive UML documentation available in **UML_DIAGRAMS.md** including:

1. **Component Diagram** - System architecture overview
2. **Class Diagrams** - Weather and Cost-Benefit modules
3. **Sequence Diagrams** - Weather and Economics data flows
4. **Activity Diagram** - Complete data pipeline process
5. **State Diagram** - Dashboard navigation
6. **Use Case Diagram** - System features and actors
7. **Deployment Diagram** - Infrastructure layout
8. **ER Diagram** - MongoDB collections

All diagrams use Mermaid format for easy rendering in GitHub, VS Code, and documentation tools.

---

## �🚀 Next Steps (Future Enhancements)

1. **Cloud Deployment**: Deploy Dash to AWS EC2, Heroku, or similar
2. **Real Sensor Integration**: Connect actual IoT devices
3. **Advanced Analytics**: Add time-series forecasting, anomaly detection
4. **Location Customization**: Add UI to change weather location
5. **User Authentication**: Add farm-specific dashboards
6. **Mobile App**: Responsive design for phones/tablets

---

## 📝 License

Educational project demonstrating modern big data architectures for precision agriculture.

---

## ✅ Project Status

- ✅ Dashboard fully functional with **7 interactive tabs**
- ✅ Weather API integration (OpenWeatherMap)
- ✅ Cost-benefit analysis with 8 crops
- ✅ Tunisia location configured (Tunis)
- ✅ USD currency throughout
- ✅ Architecture diagrams generated and displayed
- ✅ UML documentation complete (10 diagrams)
- ✅ One-click pipeline automation working
- ✅ Crop advisory system operational
- ✅ Comprehensive error handling
- ✅ Docker containerization complete
- ✅ Sample data included
- ✅ Production-ready code

---

## 📞 Support

For issues or questions:
1. Check the **Architecture** tab for system diagrams
2. Review error messages in **Home** tab logs
3. Refer to **Dashboard User Guide** in `app/DASHBOARD_USER_GUIDE.md`
4. Check service status: `docker-compose ps`

---

**Smart Agri BigData** · Modern Big Data Platform for Precision Agriculture  
Powered by Hadoop, Spark, MongoDB, Dash/Plotly · Educational Project (2025-2026)

Version 2.0 | Status: Production Ready ✅ | Location: Tunisia 🇹🇳 | Currency: USD 💵
