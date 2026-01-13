# Smart Agri Big Data Dashboard - User Guide

## Overview
The Dash Web Application provides a modern, user-friendly interface for monitoring and analyzing agricultural sensor data with big data processing capabilities.

## Dashboard Features

### 1. **Home Tab** 🏠
- **Quick Start Actions**: Run the complete data pipeline with one click
- **System Status**: Real-time connection status for MongoDB, HDFS, and Spark
- **Data Status**: View current dataset information
- **Pipeline Logs**: Monitor pipeline execution and view detailed logs

### 2. **Analytics Tab** 📊
Access comprehensive analytics powered by your processed data:

#### **Daily Aggregation Charts**
- Soil Moisture Trends
- Soil Temperature Monitoring
- Air Temperature & Humidity Patterns
- Rainfall Distribution

#### **Disease Statistics**
- Disease Prevalence by Area
- Severity Distribution
- Temporal Trends
- Predictive Alerts

#### **Crop Advisory**
- Real-time recommendations based on current conditions
- Moisture, temperature, and humidity analysis
- Actionable insights for irrigation and pest management

### 3. **Sensor Data Tab** 📡
Raw sensor data visualization:
- Real-time data from gateway
- Sensor readings table with filtering
- Data quality metrics
- Individual sensor tracking

### 4. **Architecture Tab** 🏗️
Comprehensive system architecture documentation:

#### **System Architecture Diagram**
Visual representation of:
- Data Generation & Sources (IoT Sensors, Generator Script, Disease Metadata)
- Data Ingestion & Storage (Hadoop HDFS, MongoDB Raw Collections)
- Batch Processing (Apache Spark Job with aggregation, detection, statistics)
- Real-Time Analytics & Visualization (Dash Dashboard on Port 8050)
- Technology Stack & Docker Containerization

#### **Data Pipeline Flowchart**
Four-phase pipeline visualization:
1. **Phase 1: Data Generation & Ingestion**
   - Sensor Data Generator Script
   - Hadoop HDFS Storage
   - MongoDB Raw Data Collections

2. **Phase 2: Batch Processing**
   - Apache Spark Job
   - Data aggregation and anomaly detection
   - Statistical analysis

3. **Phase 3: Analytics Loading**
   - MongoDB Analytics Collections
   - Processed data storage (aggDaily, diseaseStats, warnings)

4. **Phase 4: Real-Time Visualization**
   - Dash Web Application (Port 8050)
   - Interactive dashboards and analytics

#### **Technology Stack**
- **Data Ingestion & Storage**: Hadoop HDFS, Apache Spark, MongoDB
- **Application & Visualization**: Python 3.12, Plotly/Dash, Docker

### 5. **System Status Tab** ⚙️
Monitor system health and performance:
- Service Status (MongoDB, HDFS, Spark)
- Database Statistics
- Pipeline Performance Metrics
- Data Pipeline Health

## Running the Dashboard

### Start the Dashboard
```bash
cd app/
python dashboard.py
```

### Access the Web Interface
Open your browser and navigate to:
```
http://localhost:8050
```

## Data Pipeline Workflow

The complete data flow:
1. **IoT Sensors** → Capture environmental data (temperature, moisture, humidity)
2. **Generator Script** → Simulates and batches sensor data
3. **Hadoop HDFS** → Stores raw data files (JSON batches)
4. **MongoDB** → Raw data collections for quick access
5. **Apache Spark** → Processes, aggregates, and analyzes data
6. **MongoDB** → Analytics collections store computed results
7. **Dash Dashboard** → Visualizes insights and metrics

## Features in Action

### Run Complete Pipeline
1. Go to **Home** tab
2. Click **"▶️ Run Full Pipeline"** button
3. Monitor execution in the logs section
4. Once complete, switch to **Analytics** tab to see results

### View Analytics
1. Navigate to **Analytics** tab
2. Explore various charts and metrics
3. Check **Crop Advisory** for actionable recommendations
4. Analyze disease statistics and trends

### Monitor Architecture
1. Go to **Architecture** tab
2. Review the System Architecture Diagram
3. Study the Data Pipeline Flowchart
4. Check Technology Stack details

### System Health Check
1. Navigate to **System Status** tab
2. Verify all services are operational
3. Check database statistics
4. Monitor pipeline performance

## Key Metrics Explained

### Soil Moisture
- **Low (<30%)**: Risk of water stress, requires increased irrigation
- **Optimal (30-70%)**: Ideal range for most crops
- **High (>70%)**: Risk of root rot, reduce watering

### Temperature
- **Soil Temp**: Optimal range 15-25°C for most crops
- **Air Temp**: Monitor for heat stress (>35°C) or cold stress (<10°C)
- **Humidity**: 60-80% ideal for most crop stages

### Disease Detection
Automatic detection based on:
- Temperature and humidity combinations
- Historical disease patterns
- Environmental risk factors
- Severity assessment

## Troubleshooting

### Dashboard Won't Load
- Ensure MongoDB is running: Check **System Status** tab
- Verify HDFS connectivity
- Check browser console for errors

### No Data Appears
- Run the pipeline from the **Home** tab first
- Wait for Spark job to complete (typically 2-5 minutes)
- Check MongoDB connection status

### Charts Not Updating
- Refresh the page (Ctrl+R or Cmd+R)
- Check **System Status** for MongoDB connectivity
- Verify pipeline has been run recently

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Dash/Plotly | Modern interactive dashboard |
| Processing | Apache Spark | Distributed batch processing |
| Storage | Hadoop HDFS | Distributed file storage |
| Database | MongoDB | Analytics data storage |
| Language | Python 3.12 | Core application language |
| Containerization | Docker | Service isolation and deployment |

## Additional Resources

- [Dash Documentation](https://dash.plotly.com/)
- [Apache Spark Guide](https://spark.apache.org/docs/latest/)
- [Hadoop HDFS Overview](https://hadoop.apache.org/docs/r3.2.1/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)
- [MongoDB Manual](https://docs.mongodb.com/manual/)

## Performance Tips

1. **For Large Datasets**: Consider increasing Spark memory allocation
2. **Dashboard Responsiveness**: Regular MongoDB maintenance ensures smooth operation
3. **Pipeline Efficiency**: Run pipeline during off-peak hours for faster processing
4. **Data Retention**: Archive old sensor data to maintain database performance

---

**Smart Agri BigData** - Empowering agriculture with data-driven insights! 🌾
