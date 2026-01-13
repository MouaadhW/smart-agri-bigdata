"""
Smart Agri BigData Dashboard - Modern Dash Application
Farm-themed, user-friendly interface with advanced analytics
"""

import os
import json
import subprocess
import base64
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pymongo import MongoClient
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# Import new modules
from weather_integration import WeatherManager, create_weather_card, create_forecast_chart, create_climate_risk_card, create_irrigation_forecast
from cost_benefit_analysis import CostBenefitAnalyzer, create_irrigation_roi_card, create_crop_profitability_chart, create_cost_breakdown_card, create_profitability_metrics, create_price_scenario_chart

# ============= CONFIGURATION =============
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
DATA_DIR = os.path.join(APP_DIR, "data")
IMAGE_DIR = os.path.join(APP_DIR, "images")
RESULTS_DIR = os.path.join(APP_DIR, "results")

# ============= DATABASE FUNCTIONS =============
def get_mongo_client():
    """Connect to MongoDB with fallback"""
    hosts = ["mongodb", "localhost", "127.0.0.1"]
    for host in hosts:
        try:
            client = MongoClient(
                host=host, port=27017, username="root", password="example",
                serverSelectionTimeoutMS=2000, connectTimeoutMS=2000,
            )
            client.server_info()
            return client
        except:
            continue
    return None

def load_analytics():
    """Load analytics from MongoDB"""
    client = get_mongo_client()
    if not client:
        return None
    try:
        db = client["agridb"]
        docs = list(db.analyticsdaily.find({}))
        if not docs:
            return pd.DataFrame()
        for doc in docs:
            doc.pop("_id", None)
        return pd.json_normalize(docs)
    except:
        return None

def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode()
    except:
        return None

def get_crop_advisory(df):
    """Generate crop advisory based on weather conditions"""
    if df.empty:
        return html.Div()
    
    avg_moisture = df['avgsoilmoisture'].mean()
    avg_soil_temp = df['avgsoiltemp'].mean()
    avg_air_temp = df['avgairtemp'].mean()
    avg_humidity = df['avgairhumidity'].mean()
    
    # Build advisory messages
    advice = []
    warnings = []
    recommendations = []
    
    # Soil Moisture Analysis
    if avg_moisture < 30:
        warnings.append("⚠️ Low soil moisture - crops may experience water stress")
        recommendations.append("💧 Increase irrigation frequency")
    elif avg_moisture > 70:
        warnings.append("⚠️ High soil moisture - risk of root rot and fungal diseases")
        recommendations.append("🌳 Improve drainage, reduce watering")
    else:
        advice.append("✅ Optimal soil moisture for most crops")
    
    # Temperature Analysis
    if avg_soil_temp < 10:
        warnings.append("❄️ Cold soil temperature - slows nutrient uptake")
        recommendations.append("🌡️ Consider mulching to retain heat")
    elif avg_soil_temp > 35:
        warnings.append("🔥 Excessive soil temperature - risk of heat stress")
        recommendations.append("💨 Increase shading and irrigation")
    else:
        advice.append("✅ Ideal soil temperature range")
    
    # Air Temperature Analysis
    if avg_air_temp < 15:
        warnings.append("❄️ Cool air temperature - slower growth")
        recommendations.append("🏠 Monitor for frost risk, use frost protection if needed")
    elif avg_air_temp > 35:
        warnings.append("🔥 High air temperature - increased evapotranspiration")
        recommendations.append("💨 Increase irrigation, provide shade cloth if possible")
    else:
        advice.append("✅ Excellent temperature for crop growth")
    
    # Humidity Analysis
    if avg_humidity < 40:
        warnings.append("💨 Low humidity - increased water loss and heat stress")
        recommendations.append("💧 Increase irrigation, apply mulch")
    elif avg_humidity > 85:
        warnings.append("💧 High humidity - elevated disease pressure (fungal)")
        recommendations.append("🍃 Improve air circulation, monitor for diseases")
    else:
        advice.append("✅ Favorable humidity levels")
    
    # Determine most likely crop outcomes
    crop_scenarios = []
    
    if avg_moisture > 30 and avg_moisture < 70 and avg_soil_temp > 15 and avg_soil_temp < 30:
        if avg_air_temp > 20 and avg_air_temp < 28 and avg_humidity > 50 and avg_humidity < 80:
            crop_scenarios.append("🌾 **Excellent Growth Period** - Ideal conditions for vegetative growth and fruit development")
    
    if avg_humidity > 75 and avg_air_temp > 25:
        crop_scenarios.append("🦠 **Disease Risk** - High humidity + warm temperatures favor fungal and bacterial infections")
    
    if avg_moisture < 40 and avg_soil_temp > 30:
        crop_scenarios.append("🏜️ **Stress Conditions** - Dry soil + high temperature increases drought stress")
    
    if avg_air_temp < 18 and avg_soil_temp < 12:
        crop_scenarios.append("🌱 **Slow Growth** - Cool conditions may slow metabolic processes")
    
    if not crop_scenarios:
        crop_scenarios.append("📊 **Moderate Conditions** - Conditions are acceptable but not optimal")
    
    # Build the advisory card
    return dbc.Card([
        dbc.CardBody([
            html.H5("🌾 Crop Advisory & Weather Forecast", style={"color": "#2d5016", "marginTop": "0", "marginBottom": "20px", "fontWeight": "700"}),
            
            dbc.Row([
                dbc.Col([
                    html.H6("🌤️ Current Conditions Assessment", style={"color": "#558b2f", "marginBottom": "12px"}),
                    html.Div([
                        html.Div(a, style={"padding": "8px", "marginBottom": "6px", "backgroundColor": "#e8f5e9", 
                                          "borderLeft": "4px solid #7cb342", "borderRadius": "4px"})
                        for a in advice
                    ]) if advice else html.P("Monitor conditions closely", style={"color": "#999"})
                ], width=6),
                
                dbc.Col([
                    html.H6("⚠️ Alerts & Concerns", style={"color": "#d32f2f", "marginBottom": "12px"}),
                    html.Div([
                        html.Div(w, style={"padding": "8px", "marginBottom": "6px", "backgroundColor": "#ffebee", 
                                          "borderLeft": "4px solid #ff5252", "borderRadius": "4px"})
                        for w in warnings
                    ]) if warnings else html.P("No major concerns", style={"color": "#999"})
                ], width=6)
            ], style={"marginBottom": "20px"}),
            
            html.Hr(),
            
            dbc.Row([
                dbc.Col([
                    html.H6("💡 Recommendations", style={"color": "#1976d2", "marginBottom": "12px"}),
                    html.Ol([
                        html.Li(r, style={"marginBottom": "8px"})
                        for r in recommendations
                    ]) if recommendations else html.P("Current conditions are favorable", style={"color": "#999"})
                ], width=6),
                
                dbc.Col([
                    html.H6("🎯 Most Likely Crop Outcomes", style={"color": "#7b1fa2", "marginBottom": "12px"}),
                    html.Div([
                        html.Div(scenario, style={"padding": "12px", "marginBottom": "8px", "backgroundColor": "#f3e5f5", 
                                                 "borderLeft": "4px solid #7b1fa2", "borderRadius": "4px", "lineHeight": "1.5"})
                        for scenario in crop_scenarios
                    ])
                ], width=6)
            ])
        ])
    ], style={"borderLeft": "5px solid #7cb342", "backgroundColor": "#fafaf8", "marginTop": "20px"})

# ============= INITIALIZE DASH APP =============
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Smart Agri BigData"

# ============= CUSTOM CSS =============
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #fafaf8;
                color: #2c3e50;
            }
            .nav-link { color: #2c3e50 !important; font-weight: 500; transition: all 0.3s ease; }
            .nav-link:hover { color: #2d5016 !important; border-bottom: 3px solid #7cb342; }
            .card { border: none; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
            .btn-primary { background-color: #7cb342; border-color: #7cb342; font-weight: 600; }
            .btn-primary:hover { background-color: #558b2f; border-color: #558b2f; }
            .metric-card {
                background: linear-gradient(135deg, #f0f7f4 0%, #e8f5e9 100%);
                border-left: 5px solid #7cb342;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
            }
            .metric-value { font-size: 2.5em; font-weight: 700; color: #2d5016; margin: 10px 0; }
            .metric-label { font-size: 0.95em; color: #558b2f; font-weight: 600; }
            .section-title { color: #2d5016; font-weight: 700; border-bottom: 3px solid #7cb342; padding-bottom: 15px; margin-bottom: 25px; }
            .info-box {
                background: linear-gradient(135deg, #f0f7f4 0%, #e8f5e9 100%);
                border-left: 5px solid #7cb342;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .header-banner {
                background: linear-gradient(135deg, #2d5016 0%, #7cb342 100%);
                color: white;
                padding: 40px 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 4px 15px rgba(45, 80, 22, 0.2);
            }
            .header-banner h1 { margin: 0; font-size: 2.5em; font-weight: 700; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ============= LAYOUT =============
app.layout = dbc.Container([
    html.Div([
        html.H1("🌾 Smart Agri BigData", style={"margin": "0", "color": "white"}),
        html.P("Intelligent Agricultural Analytics Platform | Real-time IoT Monitoring & Batch Processing",
               style={"margin": "10px 0 0 0", "color": "rgba(255,255,255,0.95)", "fontSize": "1.1em"})
    ], className="header-banner"),
    
    # Main Tabs
    dbc.Tabs([
        # HOME TAB
        dbc.Tab(label="🏠 Home", tab_id="home", children=[
            dbc.Row([
                dbc.Col([
                    html.H2("Welcome to Smart Agri BigData", className="section-title"),
                    html.P(
                        "A complete end-to-end big data platform for agricultural IoT monitoring and analytics. "
                        "Process sensor data through Apache Spark, store in MongoDB, and visualize with advanced dashboards.",
                        style={"fontSize": "1.05em", "lineHeight": "1.6"}
                    ),
                ], width=8),
                dbc.Col([
                    dbc.Card([dbc.CardBody([
                        html.H5("⚡ Quick Start", style={"color": "#2d5016", "fontWeight": "700"}),
                        html.Ol([
                            html.Li("Go to Pipeline tab", style={"marginBottom": "8px"}),
                            html.Li("Click automation button", style={"marginBottom": "8px"}),
                            html.Li("View live charts", style={"marginBottom": "0"}),
                        ], style={"fontSize": "0.95em"})
                    ])], style={"borderLeft": "5px solid #7cb342", "background": "#f0f7f4"})
                ], width=4)
            ], style={"marginBottom": "30px"}),
            
            html.H3("Technology Stack", className="section-title"),
            dbc.Row([
                dbc.Col([dbc.Card([dbc.CardBody([
                    html.H4("🐘", style={"textAlign": "center", "fontSize": "3em"}),
                    html.H6("Hadoop", style={"textAlign": "center", "color": "#2d5016"}),
                    html.P("Distributed Storage", style={"textAlign": "center", "fontSize": "0.9em", "color": "#666"})
                ])])], width=3),
                dbc.Col([dbc.Card([dbc.CardBody([
                    html.H4("⚡", style={"textAlign": "center", "fontSize": "3em"}),
                    html.H6("Spark", style={"textAlign": "center", "color": "#2d5016"}),
                    html.P("Batch Processing", style={"textAlign": "center", "fontSize": "0.9em", "color": "#666"})
                ])])], width=3),
                dbc.Col([dbc.Card([dbc.CardBody([
                    html.H4("🗄️", style={"textAlign": "center", "fontSize": "3em"}),
                    html.H6("MongoDB", style={"textAlign": "center", "color": "#2d5016"}),
                    html.P("Analytics DB", style={"textAlign": "center", "fontSize": "0.9em", "color": "#666"})
                ])])], width=3),
                dbc.Col([dbc.Card([dbc.CardBody([
                    html.H4("📊", style={"textAlign": "center", "fontSize": "3em"}),
                    html.H6("Dash", style={"textAlign": "center", "color": "#2d5016"}),
                    html.P("Modern UI", style={"textAlign": "center", "fontSize": "0.9em", "color": "#666"})
                ])])], width=3)
            ]),
        ]),
        
        # PIPELINE TAB
        dbc.Tab(label="🚀 Pipeline", tab_id="pipeline", children=[
            html.H2("Data Pipeline Automation", className="section-title"),
            html.P(
                "Run the entire data processing pipeline with one click. "
                "Generate sensor data → Prepare metadata → Process through Spark → Store in MongoDB",
                style={"marginBottom": "20px"}
            ),
            
            html.Div(className="info-box", children=[
                html.H5("⚡ One-Click Execution", style={"color": "#2d5016", "marginTop": "0"}),
                html.P("Run all 5 pipeline steps automatically in ~1 minute.", style={"marginBottom": "0"})
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Button("🤖 Run Full Pipeline", id="run-btn", size="lg", color="primary",
                              style={"width": "100%", "fontWeight": "600", "padding": "15px"})
                ], width=6),
                dbc.Col([
                    dbc.Button("📋 Manual Steps", id="manual-btn", size="lg", outline=True, color="primary",
                              style={"width": "100%", "fontWeight": "600", "padding": "15px"})
                ], width=6)
            ], style={"marginBottom": "30px"}),
            
            html.Div(id="pipeline-output", style={"marginTop": "20px"}),
            
            html.Hr(),
            
            html.H3("Pipeline Overview", className="section-title"),
            dbc.Table.from_dataframe(
                pd.DataFrame({
                    "Step": ["1️⃣ Sensors", "2️⃣ Disease", "3️⃣ HDFS", "4️⃣ Spark", "5️⃣ MongoDB"],
                    "What": ["Generate data", "Prepare metadata", "Store distributed", "Process & aggregate", "Store analytics"],
                    "Time": ["~5s", "~2s", "~10s", "~30s", "~5s"]
                }),
                striped=True, bordered=True, hover=True
            )
        ]),
        
        # ANALYTICS TAB
        dbc.Tab(label="📈 Analytics", tab_id="analytics", children=[
            html.H2("Analytics Dashboard", className="section-title"),
            html.P("Real-time insights from your agricultural sensor data", style={"marginBottom": "20px"}),
            html.Div(id="analytics-container", children=[
                html.P("Loading analytics...", style={"textAlign": "center", "color": "#999"})
            ])
        ]),
        

        dbc.Tab(label="🌤️ Weather & Climate", tab_id="weather", children=[
            html.H2("Weather Forecast & Climate Analysis", className="section-title"),
            html.P("Real-time weather data from OpenWeatherMap API with 7-day forecasts and climate risk assessment",
                   style={"marginBottom": "30px", "color": "#666"}),
            
            # Current Weather Card
            html.Div(id="weather-card-container", children=[
                html.P("Loading weather data...", style={"textAlign": "center", "color": "#999"})
            ]),
            
            # Weather Forecast Charts
            html.H3("📊 7-Day Weather Forecast", className="section-title mt-5"),
            html.Div(id="forecast-chart-container"),
            
            # Climate Risk Analysis
            html.H3("🔍 Climate Risk Analysis", className="section-title mt-5"),
            html.Div(id="climate-risk-container"),
            
            # Irrigation Scheduling
            html.H3("💧 Irrigation Scheduling Forecast", className="section-title mt-5"),
            html.Div(id="irrigation-forecast-container")
        ], style={"padding": "20px"}),
        
        # COST-BENEFIT ANALYSIS TAB
        dbc.Tab(label="💰 Cost-Benefit Analysis", tab_id="economics", children=[
            html.H2("Farm Economics & Profitability Analysis", className="section-title"),
            html.P("Calculate ROI, compare crop profitability, and analyze market scenarios",
                   style={"marginBottom": "30px", "color": "#666"}),
            
            # Controls Row
            dbc.Row([
                dbc.Col([
                    dbc.Card([dbc.CardBody([
                        html.H5("Select Crop & Parameters", style={"color": "#2d5016", "marginBottom": "20px"}),
                        html.Label("Crop Type:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="crop-select",
                            options=[
                                {"label": "🌾 Wheat", "value": "wheat"},
                                {"label": "🍚 Rice", "value": "rice"},
                                {"label": "🌻 Cotton", "value": "cotton"},
                                {"label": "🎋 Sugarcane", "value": "sugarcane"},
                                {"label": "🌽 Maize", "value": "maize"},
                                {"label": "🥔 Potato", "value": "potato"},
                                {"label": "🧅 Onion", "value": "onion"},
                                {"label": "🍅 Tomato", "value": "tomato"},
                            ],
                            value="wheat",
                            style={"marginBottom": "15px"}
                        ),
                        html.Label("Farm Area (hectares):", style={"fontWeight": "bold"}),
                        dcc.Slider(
                            id="farm-area-slider",
                            min=0.5,
                            max=50,
                            step=0.5,
                            value=1,
                            marks={0.5: "0.5", 5: "5", 10: "10", 20: "20", 50: "50"},
                            tooltip={"placement": "bottom", "always_visible": True}
                        ),
                        html.P(id="farm-area-display", style={"marginTop": "10px", "color": "#2d5016", "fontWeight": "bold"})
                    ])], style={"borderLeft": "5px solid #ff9800", "backgroundColor": "#fffde7"})
                ], width=12, md=4)
            ], className="mb-4"),
            
            # Irrigation ROI Analysis
            html.H3("💧 Irrigation ROI Analysis", className="section-title"),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Current Rainfall (mm):", style={"fontWeight": "bold"}),
                            dcc.Slider(
                                id="rainfall-slider",
                                min=0,
                                max=500,
                                step=10,
                                value=150,
                                marks={0: "0", 100: "100", 200: "200", 300: "300", 500: "500"},
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ], width=12)
                    ])
                ], width=12, md=6),
                dbc.Col([
                    html.Div(id="irrigation-roi-container")
                ], width=12, md=6)
            ], className="mb-4"),
            
            html.Hr(),
            
            # Crop Profitability Analysis
            html.H3("🎯 Crop Profitability Metrics", className="section-title"),
            html.Div(id="profitability-metrics-container"),
            
            html.Hr(),
            
            # Crop Comparison
            html.H3("📊 Crop Comparison Chart", className="section-title"),
            html.Div(id="crop-comparison-container"),
            
            html.Hr(),
            
            # Cost Breakdown
            html.H3("💵 Cost Breakdown Analysis", className="section-title"),
            html.Div(id="cost-breakdown-container"),
            
            html.Hr(),
            
            # Price Scenario Analysis
            html.H3("📈 Market Price Scenario Analysis", className="section-title"),
            html.Div(id="price-scenario-container")
        ], style={"padding": "20px"}),

        # ARCHITECTURE TAB
        dbc.Tab(label="🏗️ Architecture", tab_id="architecture", children=[
            html.H2("System Architecture", className="section-title"),
            html.Div(id="arch-container"),
            
            html.Hr(style={"marginY": "40px"}),
            html.H2("Data Pipeline Flowchart", className="section-title"),
            html.Div(id="pipeline-flowchart-container"),
            
            html.Hr(style={"marginY": "40px"}),
            html.H3("Technology Stack", className="section-title"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([dbc.CardBody([
                        html.H5("Data Ingestion & Storage", style={"color": "#2d5016"}),
                        html.Ul([
                            html.Li("🐘 Hadoop HDFS - Distributed file storage"),
                            html.Li("📊 Apache Spark - Batch processing engine"),
                            html.Li("🗄️ MongoDB - NoSQL analytics database"),
                        ])
                    ])], style={"borderLeft": "5px solid #7cb342"})
                ], width=6),
                dbc.Col([
                    dbc.Card([dbc.CardBody([
                        html.H5("Application & Visualization", style={"color": "#2d5016"}),
                        html.Ul([
                            html.Li("🐍 Python 3.12 - Core language"),
                            html.Li("📊 Plotly/Dash - Modern dashboards"),
                            html.Li("🐳 Docker - Containerization"),
                        ])
                    ])], style={"borderLeft": "5px solid #7cb342"})
                ], width=6)
            ])
        ])
    ], id="main-tabs", active_tab="home"),
    
    html.Hr(style={"marginTop": "50px"}),
    html.P("🌾 Smart Agri BigData | Powered by Hadoop, Spark, MongoDB & Plotly/Dash",
           style={"textAlign": "center", "color": "#999"})
], fluid=True, style={"padding": "30px 20px", "maxWidth": "1400px"})

# ============= CALLBACKS =============

@callback(
    Output("pipeline-output", "children"),
    Input("run-btn", "n_clicks"),
    prevent_initial_call=True
)
def run_pipeline(n_clicks):
    try:
        result = subprocess.run(
            ["python", "app/scripts/run_full_pipeline.py"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            return dbc.Alert([
                html.H5("✅ Pipeline Success!", style={"marginTop": "0"}),
                html.P("MongoDB populated. Switch to Analytics tab!"),
                html.Pre(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout,
                        style={"backgroundColor": "#f5f5f5", "padding": "15px", "borderRadius": "5px", "fontSize": "0.8em"})
            ], color="success", style={"borderRadius": "10px"})
        else:
            return dbc.Alert("⚠️ Pipeline completed with warnings", color="warning", style={"borderRadius": "10px"})
    except Exception as e:
        return dbc.Alert(f"❌ Error: {str(e)}", color="danger", style={"borderRadius": "10px"})

@callback(
    Output("analytics-container", "children"),
    Input("main-tabs", "active_tab")
)
def update_analytics(active_tab):
    if active_tab != "analytics":
        return []
    
    df = load_analytics()
    
    if df is None:
        return dbc.Alert("❌ Could not connect to MongoDB.", color="danger")
    
    if df.empty:
        return dbc.Alert([
            html.H5("📊 MongoDB Connected but Empty"),
            html.Ol([html.Li("Go to Pipeline tab"), html.Li("Click automation button"), html.Li("Refresh here")])
        ], color="info")
    
    # Metrics
    metrics = [
        ("Avg Soil Moisture", f"{df['avgsoilmoisture'].mean():.2f}%", "🌱"),
        ("Avg Soil Temp", f"{df['avgsoiltemp'].mean():.1f}°C", "🌡️"),
        ("Avg Air Temp", f"{df['avgairtemp'].mean():.1f}°C", "🌡️"),
        ("Avg Humidity", f"{df['avgairhumidity'].mean():.1f}%", "💧"),
    ]
    
    metrics_row = dbc.Row([
        dbc.Col([html.Div([
            html.H5(m[2], style={"fontSize": "2em", "marginBottom": "5px"}),
            html.Div(m[1], style={"fontSize": "2em", "fontWeight": "700", "color": "#2d5016"}),
            html.Div(m[0], style={"fontSize": "0.9em", "color": "#666"})
        ], className="metric-card")], width=3) for m in metrics
    ], style={"marginBottom": "30px"})
    
    # Charts
    df_sorted = df.sort_values("date") if "date" in df.columns else df
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_sorted["date"], y=df_sorted["avgsoilmoisture"],
                              mode="lines+markers", name="Soil Moisture",
                              line=dict(color="#7cb342", width=3),
                              fill="tozeroy", fillcolor="rgba(123, 179, 66, 0.2)"))
    fig1.update_layout(title="Soil Moisture Over Time", template="plotly_white", height=400)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df_sorted["date"], y=df_sorted["avgsoiltemp"],
                              mode="lines+markers", name="Soil Temp", line=dict(color="#ff9800", width=2.5)))
    fig2.add_trace(go.Scatter(x=df_sorted["date"], y=df_sorted["avgairtemp"],
                              mode="lines+markers", name="Air Temp", line=dict(color="#ff5722", width=2.5)))
    fig2.update_layout(title="Temperature Comparison", template="plotly_white", height=400)
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_sorted["date"], y=df_sorted["avgairhumidity"],
                              mode="lines+markers", name="Humidity",
                              line=dict(color="#64b5f6", width=3),
                              fill="tozeroy", fillcolor="rgba(100, 181, 246, 0.2)"))
    fig3.update_layout(title="Humidity Trends", template="plotly_white", height=400)
    
    return html.Div([
        html.H5(f"✅ {len(df)} records found", style={"color": "#2d5016"}),
        html.Hr(),
        metrics_row,
        dbc.Row([dbc.Col([dcc.Graph(figure=fig1)], width=6), dbc.Col([dcc.Graph(figure=fig2)], width=6)]),
        dbc.Row([dbc.Col([dcc.Graph(figure=fig3)], width=6)]),
        get_crop_advisory(df)
    ])

@callback(
    Output("arch-container", "children"),
    Input("main-tabs", "active_tab")
)
def update_arch(active_tab):
    # Always load the image, regardless of tab
    img_path = os.path.join(IMAGE_DIR, "architecture_diagram.png")
    
    if os.path.exists(img_path):
        try:
            img_base64 = get_image_base64(img_path)
            if img_base64:
                return html.Img(
                    src=f"data:image/png;base64,{img_base64}",
                    style={
                        "width": "100%", 
                        "maxWidth": "1200px",
                        "height": "auto",
                        "borderRadius": "10px", 
                        "marginBottom": "30px", 
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                        "border": "1px solid #ddd"
                    }
                )
        except Exception as e:
            return dbc.Alert(f"Error loading image: {str(e)}", color="danger")
    
    return dbc.Alert([
        html.H5("⚠️ Architecture diagram not found"),
        html.P(f"Expected location: {img_path}"),
        html.P("Please regenerate it by running: python create_architecture_diagram.py")
    ], color="warning")

@callback(
    Output("pipeline-flowchart-container", "children"),
    Input("main-tabs", "active_tab")
)
def load_pipeline_flowchart(active_tab):
    """Load the pipeline flowchart diagram"""
    img_path = os.path.join(IMAGE_DIR, "pipeline_flowchart.png")
    
    if os.path.exists(img_path):
        try:
            img_base64 = get_image_base64(img_path)
            if img_base64:
                return html.Img(
                    src=f"data:image/png;base64,{img_base64}",
                    style={
                        "width": "100%", 
                        "maxWidth": "1400px",
                        "height": "auto",
                        "borderRadius": "10px", 
                        "marginBottom": "30px", 
                        "boxShadow": "0 4px 12px rgba(0,0,0,0.1)",
                        "border": "1px solid #ddd"
                    }
                )
        except Exception as e:
            return dbc.Alert(f"Error loading flowchart: {str(e)}", color="danger")
    
    return dbc.Alert([
        html.H5("⚠️ Pipeline flowchart not found"),
        html.P("Please regenerate it by running: python create_pipeline_flowchart.py")
    ], color="info")

# ============= WEATHER TAB CALLBACKS =============

@callback(
    [Output("weather-card-container", "children"),
     Output("forecast-chart-container", "children"),
     Output("climate-risk-container", "children"),
     Output("irrigation-forecast-container", "children")],
    Input("main-tabs", "active_tab")
)
def update_weather_data(active_tab):
    """Load and display weather data"""
    if active_tab != "weather":
        return "", "", "", ""
    
    try:
        weather_manager = WeatherManager()
        
        # Current weather
        current_weather = weather_manager.get_current_weather()
        weather_card = create_weather_card(current_weather)
        
        # Forecast
        forecast_df = weather_manager.get_forecast(days=7)
        forecast_chart = create_forecast_chart(forecast_df)
        
        # Climate risk analysis
        risks = weather_manager.get_climate_risk_analysis(forecast_df)
        climate_risk_card = create_climate_risk_card(risks)
        
        # Irrigation forecast
        irrigation_chart, daily_data = create_irrigation_forecast(forecast_df)
        
        return weather_card, forecast_chart, climate_risk_card, irrigation_chart
        
    except Exception as e:
        error_msg = dbc.Alert(f"Error loading weather data: {str(e)}", color="danger")
        return error_msg, error_msg, error_msg, error_msg

# ============= COST-BENEFIT ANALYSIS CALLBACKS =============

@callback(
    Output("farm-area-display", "children"),
    Input("farm-area-slider", "value")
)
def update_farm_area_display(farm_area):
    """Display selected farm area"""
    return f"Selected Area: {farm_area} hectares"

@callback(
    Output("irrigation-roi-container", "children"),
    [Input("crop-select", "value"),
     Input("rainfall-slider", "value"),
     Input("farm-area-slider", "value")]
)
def update_irrigation_roi(crop_type, rainfall, farm_area):
    """Update irrigation ROI analysis"""
    return create_irrigation_roi_card(rainfall, crop_type, farm_area)

@callback(
    Output("profitability-metrics-container", "children"),
    [Input("crop-select", "value"),
     Input("farm-area-slider", "value")]
)
def update_profitability(crop_type, farm_area):
    """Update crop profitability metrics"""
    return create_profitability_metrics(crop_type, farm_area)

@callback(
    Output("crop-comparison-container", "children"),
    Input("farm-area-slider", "value")
)
def update_crop_comparison(farm_area):
    """Update crop comparison chart"""
    return create_crop_profitability_chart(farm_area)

@callback(
    Output("cost-breakdown-container", "children"),
    [Input("crop-select", "value"),
     Input("farm-area-slider", "value")]
)
def update_cost_breakdown(crop_type, farm_area):
    """Update cost breakdown pie chart"""
    return create_cost_breakdown_card(crop_type, farm_area)

@callback(
    Output("price-scenario-container", "children"),
    [Input("crop-select", "value"),
     Input("farm-area-slider", "value")]
)
def update_price_scenario(crop_type, farm_area):
    """Update price scenario analysis"""
    return create_price_scenario_chart(crop_type, farm_area)

# ============= RUN =============
if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8055)
