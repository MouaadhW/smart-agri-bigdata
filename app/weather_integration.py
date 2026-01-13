"""
Weather API Integration Module
Connects to OpenWeatherMap API for real-time weather data and 7-day forecasts
Includes rainfall prediction and climate risk analysis
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

# OpenWeatherMap API Configuration
API_KEY = "15a44ead0fdab06857de34c49cbb242f"
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Default coordinates (Tunisia - Tunis)
DEFAULT_LAT = 33.8869  # Tunisia latitude
DEFAULT_LON = 9.5375   # Tunisia longitude

class WeatherManager:
    """Manage weather data from OpenWeatherMap API"""
    
    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.lat = DEFAULT_LAT
        self.lon = DEFAULT_LON
    
    def set_location(self, lat, lon):
        """Set custom location (latitude, longitude)"""
        self.lat = lat
        self.lon = lon
    
    def get_current_weather(self):
        """Fetch current weather data"""
        try:
            url = f"{BASE_URL}/weather"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "clouds": data["clouds"]["all"],
                    "rain": data.get("rain", {}).get("1h", 0),
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"],
                    "timestamp": datetime.fromtimestamp(data["dt"])
                }
            return None
        except Exception as e:
            print(f"Error fetching current weather: {e}")
            return None
    
    def get_forecast(self, days=7):
        """Fetch 7-day forecast"""
        try:
            url = f"{BASE_URL}/forecast"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                
                for item in data["list"]:
                    forecasts.append({
                        "datetime": datetime.fromtimestamp(item["dt"]),
                        "date": datetime.fromtimestamp(item["dt"]).date(),
                        "temp": item["main"]["temp"],
                        "humidity": item["main"]["humidity"],
                        "rain_prob": item.get("pop", 0) * 100,  # Probability of precipitation
                        "rain_amount": item.get("rain", {}).get("3h", 0),
                        "wind_speed": item["wind"]["speed"],
                        "clouds": item["clouds"]["all"],
                        "description": item["weather"][0]["description"].title()
                    })
                
                return pd.DataFrame(forecasts)
            return None
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    def get_climate_risk_analysis(self, forecast_df):
        """Analyze climate risks for crop planning"""
        if forecast_df is None or forecast_df.empty:
            return {}
        
        # Group by date and aggregate
        daily = forecast_df.groupby("date").agg({
            "temp": ["min", "max", "mean"],
            "humidity": "mean",
            "rain_prob": "max",
            "rain_amount": "sum",
            "wind_speed": "max"
        }).round(2)
        
        risks = {
            "frost_risk": False,
            "heat_stress": False,
            "excessive_rainfall": False,
            "drought_risk": False,
            "wind_damage_risk": False,
            "disease_risk": False,
            "summary": []
        }
        
        # Frost risk (temp < 0°C)
        if (daily[("temp", "min")] < 0).any():
            risks["frost_risk"] = True
            risks["summary"].append("❄️ Frost risk detected - Protect sensitive crops")
        
        # Heat stress (temp > 35°C)
        if (daily[("temp", "max")] > 35).any():
            risks["heat_stress"] = True
            risks["summary"].append("🔥 Heat stress risk - Increase irrigation")
        
        # Excessive rainfall (>50mm)
        if (daily[("rain_amount", "sum")] > 50).any():
            risks["excessive_rainfall"] = True
            risks["summary"].append("🌊 Heavy rainfall expected - Risk of crop damage")
        
        # Drought risk (low rainfall for 3+ days)
        low_rain_days = (daily[("rain_prob", "max")] < 20).sum()
        if low_rain_days >= 3:
            risks["drought_risk"] = True
            risks["summary"].append("☀️ Drought risk - Plan irrigation schedule")
        
        # Wind damage (wind > 30 km/h)
        if (daily[("wind_speed", "max")] > 8.33).any():  # 30 km/h = 8.33 m/s
            risks["wind_damage_risk"] = True
            risks["summary"].append("💨 Strong winds expected - Stake tall crops")
        
        # Disease risk (high humidity + moderate temp)
        humid_warm = (
            (daily[("humidity", "mean")] > 70) & 
            (daily[("temp", "mean")] > 20) & 
            (daily[("temp", "mean")] < 28)
        ).any()
        if humid_warm:
            risks["disease_risk"] = True
            risks["summary"].append("🦠 Fungal disease risk - Monitor leaf moisture")
        
        risks["daily_stats"] = daily
        return risks


def create_weather_card(weather_data):
    """Create current weather display card"""
    if not weather_data:
        return html.Div(
            "⚠️ Unable to fetch weather data. Check API key and internet connection.",
            className="alert alert-warning"
        )
    
    temp = weather_data["temperature"]
    feels_like = weather_data["feels_like"]
    humidity = weather_data["humidity"]
    wind = weather_data["wind_speed"]
    rain = weather_data["rain"]
    description = weather_data["description"]
    
    return dbc.Card(
        dbc.CardBody([
            html.H4("🌤️ Current Weather Conditions", className="card-title mb-4"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2(f"{temp}°C", style={"color": "#2ecc71", "fontWeight": "bold"}),
                        html.P(f"Feels like {feels_like}°C", className="text-muted")
                    ], style={"textAlign": "center"})
                ], md=3),
                dbc.Col([
                    html.Div([
                        html.P([html.B("💧 Humidity: "), f"{humidity}%"]),
                        html.P([html.B("💨 Wind Speed: "), f"{wind} m/s"]),
                        html.P([html.B("🌧️ Rain (1h): "), f"{rain} mm"])
                    ])
                ], md=3),
                dbc.Col([
                    html.Div([
                        html.P([html.B("📋 Conditions: "), description]),
                        html.P([html.B("⏰ Updated: "), weather_data["timestamp"].strftime("%H:%M")]),
                        html.P([html.B("📍 Location: "), f"Lat {DEFAULT_LAT:.2f}°, Lon {DEFAULT_LON:.2f}°"])
                    ])
                ], md=6)
            ], className="g-3")
        ]),
        className="border-0 shadow-sm mb-4",
        style={"backgroundColor": "#f8f9fa"}
    )


def create_forecast_chart(forecast_df):
    """Create 7-day forecast visualization"""
    if forecast_df is None or forecast_df.empty:
        return dcc.Graph(figure=go.Figure().add_annotation(text="No forecast data available"))
    
    # Aggregate by date
    daily = forecast_df.groupby("date").agg({
        "temp": ["min", "max", "mean"],
        "rain_prob": "max",
        "rain_amount": "sum",
        "wind_speed": "max"
    }).reset_index()
    daily.columns = ["date", "temp_min", "temp_max", "temp_avg", "rain_prob", "rain_amount", "wind_max"]
    
    fig = go.Figure()
    
    # Temperature range
    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["temp_max"],
        fill=None,
        mode='lines',
        line=dict(color='rgba(255, 127, 14, 0)'),
        showlegend=False,
        name='Max Temp'
    ))
    
    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["temp_min"],
        fill='tonexty',
        mode='lines',
        line=dict(color='rgba(255, 127, 14, 0)'),
        name='Temperature Range',
        fillcolor='rgba(255, 127, 14, 0.2)',
        hovertemplate='<b>%{x}</b><br>Temp: %{y}°C<extra></extra>'
    ))
    
    # Average temperature
    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["temp_avg"],
        mode='lines+markers',
        name='Avg Temperature',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x}</b><br>Avg: %{y:.1f}°C<extra></extra>'
    ))
    
    # Rainfall probability
    fig.add_trace(go.Bar(
        x=daily["date"],
        y=daily["rain_prob"],
        name='Rain Probability (%)',
        marker=dict(color='#1f77b4', opacity=0.6),
        yaxis='y2',
        hovertemplate='<b>%{x}</b><br>Rain Prob: %{y:.0f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title="7-Day Weather Forecast & Rainfall Probability",
        hovermode='x unified',
        template='plotly_white',
        yaxis=dict(title="Temperature (°C)", side='left'),
        yaxis2=dict(title="Rainfall Probability (%)", side='right', overlaying='y', range=[0, 100]),
        xaxis_title="Date",
        height=400,
        margin=dict(l=80, r=80, t=60, b=60)
    )
    
    return dcc.Graph(figure=fig)


def create_climate_risk_card(risks):
    """Create climate risk analysis card"""
    if not risks:
        return html.Div("No risk analysis available", className="alert alert-info")
    
    risk_items = []
    
    # Risk indicators
    risk_indicators = [
        ("frost_risk", "❄️ Frost Risk"),
        ("heat_stress", "🔥 Heat Stress"),
        ("excessive_rainfall", "🌊 Heavy Rain"),
        ("drought_risk", "☀️ Drought"),
        ("wind_damage_risk", "💨 Wind Damage"),
        ("disease_risk", "🦠 Disease Risk")
    ]
    
    for risk_key, risk_label in risk_indicators:
        is_risk = risks.get(risk_key, False)
        badge_color = "danger" if is_risk else "success"
        badge_text = "⚠️ HIGH RISK" if is_risk else "✅ OK"
        
        risk_items.append(
            dbc.Row([
                dbc.Col(html.Span(risk_label), md=6),
                dbc.Col(dbc.Badge(badge_text, color=badge_color, pill=True), md=6)
            ], className="mb-2")
        )
    
    # Recommendations
    summary = risks.get("summary", [])
    recommendations = []
    if summary:
        for rec in summary:
            recommendations.append(html.Li(rec, className="mb-2"))
    
    return dbc.Card(
        dbc.CardBody([
            html.H4("🔍 Climate Risk Analysis", className="card-title mb-3"),
            html.Hr(),
            html.Div(risk_items),
            html.Hr(),
            html.H6("📋 Recommendations:", className="mt-4 mb-2"),
            html.Ul(recommendations) if recommendations else html.P("No specific risks detected", className="text-muted")
        ]),
        className="border-0 shadow-sm",
        style={"backgroundColor": "#f8f9fa"}
    )


def create_irrigation_forecast(forecast_df):
    """Create irrigation scheduling forecast"""
    if forecast_df is None or forecast_df.empty:
        return dcc.Graph(figure=go.Figure().add_annotation(text="No data available"))
    
    # Aggregate by date
    daily = forecast_df.groupby("date").agg({
        "rain_amount": "sum",
        "temp": "mean",
        "humidity": "mean"
    }).reset_index()
    
    # Calculate irrigation need (simplified model)
    daily["irrigation_need"] = (
        100 - daily["humidity"] + 
        (daily["temp"] / 10) - 
        (daily["rain_amount"] * 2)  # Reduce need if rain expected
    ).clip(lower=0)
    
    daily["recommendation"] = daily["irrigation_need"].apply(
        lambda x: "High - Irrigate immediately" if x > 70 else 
                  "Medium - Schedule irrigation" if x > 40 else 
                  "Low - Rain expected, monitor" if x > 20 else 
                  "None - Sufficient moisture"
    )
    
    fig = go.Figure()
    
    # Irrigation need bar
    colors = ['#d9534f' if x > 70 else '#f0ad4e' if x > 40 else '#5cb85c' 
              for x in daily["irrigation_need"]]
    
    fig.add_trace(go.Bar(
        x=daily["date"],
        y=daily["irrigation_need"],
        marker=dict(color=colors),
        hovertemplate='<b>%{x}</b><br>Irrigation Need: %{y:.0f}%<extra></extra>',
        name='Irrigation Need (%)'
    ))
    
    fig.update_layout(
        title="Irrigation Scheduling Forecast (Next 7 Days)",
        xaxis_title="Date",
        yaxis_title="Irrigation Need (%)",
        template='plotly_white',
        height=350,
        margin=dict(l=60, r=60, t=60, b=60),
        showlegend=False
    )
    
    return dcc.Graph(figure=fig), daily


if __name__ == "__main__":
    # Test the module
    manager = WeatherManager()
    weather = manager.get_current_weather()
    if weather:
        print("Current Weather:", weather)
    
    forecast = manager.get_forecast(days=7)
    if forecast is not None:
        print("\nForecast Data:")
        print(forecast.head())
        
        risks = manager.get_climate_risk_analysis(forecast)
        print("\nClimate Risks:")
        print(risks["summary"])
