"""
Cost-Benefit Analysis Module
Calculate ROI for irrigation decisions, crop profitability, and farm economics
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

class CostBenefitAnalyzer:
    """Analyze farm economics and profitability"""
    
    # Default cost structure (Tunisia/USD-based, per hectare)
    DEFAULT_COSTS = {
        "water": {"rate": 0.06, "unit": "$/1000L"},  # $0.06 per 1000 liters
        "fertilizer": {"rate": 145, "unit": "$/ton"},
        "labor": {"rate": 3, "unit": "$/day"},
        "seeds": {"rate": 24, "unit": "$/kg"},
        "pesticide": {"rate": 3.6, "unit": "$/liter"},
        "electricity": {"rate": 0.10, "unit": "$/kWh"}
    }
    
    # Crop yield and market prices (per hectare, USD)
    CROP_DATA = {
        "wheat": {
            "yield": 50,  # quintals per hectare
            "market_price": 30,  # $ per quintal
            "water_needed": 400,  # mm
            "growing_period": 120,  # days
            "labor_days": 20
        },
        "rice": {
            "yield": 55,
            "market_price": 23,
            "water_needed": 1200,
            "growing_period": 130,
            "labor_days": 25
        },
        "cotton": {
            "yield": 18,
            "market_price": 66,
            "water_needed": 600,
            "growing_period": 150,
            "labor_days": 35
        },
        "sugarcane": {
            "yield": 70,
            "market_price": 3.6,
            "water_needed": 2000,
            "growing_period": 365,
            "labor_days": 60
        },
        "maize": {
            "yield": 40,
            "market_price": 22,
            "water_needed": 500,
            "growing_period": 100,
            "labor_days": 18
        },
        "potato": {
            "yield": 25,
            "market_price": 14,
            "water_needed": 400,
            "growing_period": 90,
            "labor_days": 15
        },
        "onion": {
            "yield": 20,
            "market_price": 24,
            "water_needed": 300,
            "growing_period": 120,
            "labor_days": 30
        },
        "tomato": {
            "yield": 35,
            "market_price": 18,
            "water_needed": 350,
            "growing_period": 110,
            "labor_days": 40
        }
    }
    
    def __init__(self):
        self.costs = self.DEFAULT_COSTS.copy()
        self.crops = self.CROP_DATA.copy()
    
    def calculate_irrigation_roi(self, current_rainfall_mm, crop_type, farm_area_ha=1):
        """
        Calculate ROI for irrigation decision
        
        Args:
            current_rainfall_mm: Current rainfall in mm
            crop_type: Type of crop
            farm_area_ha: Farm area in hectares
        
        Returns:
            Dictionary with ROI analysis
        """
        if crop_type not in self.crops:
            return {"error": f"Crop {crop_type} not found"}
        
        crop = self.crops[crop_type]
        water_needed = crop["water_needed"]
        irrigation_needed = max(0, water_needed - current_rainfall_mm)
        
        # Cost of irrigation ($/hectare)
        irrigation_cost = (irrigation_needed / 1000) * self.costs["water"]["rate"] * farm_area_ha
        
        # Additional yield due to optimal irrigation (assume 15-25% boost)
        yield_boost_percentage = 20
        additional_yield = (crop["yield"] * farm_area_ha) * (yield_boost_percentage / 100)
        
        # Revenue from additional yield
        additional_revenue = additional_yield * crop["market_price"]
        
        # ROI calculation
        roi = ((additional_revenue - irrigation_cost) / irrigation_cost * 100) if irrigation_cost > 0 else 0
        payback_days = (irrigation_cost / (additional_revenue / crop["growing_period"])) if additional_revenue > 0 else 0
        
        return {
            "crop": crop_type,
            "irrigation_needed_mm": irrigation_needed,
            "irrigation_cost_inr": round(irrigation_cost, 2),
            "additional_yield": round(additional_yield, 2),
            "additional_revenue_inr": round(additional_revenue, 2),
            "roi_percentage": round(roi, 2),
            "payback_days": round(max(0, payback_days), 1),
            "recommendation": "Irrigate" if roi > 30 else "Monitor" if roi > 0 else "No irrigation needed"
        }
    
    def calculate_crop_profitability(self, crop_type, farm_area_ha=1, actual_yield_boost=1.0):
        """
        Calculate complete profitability of a crop
        
        Args:
            crop_type: Type of crop
            farm_area_ha: Farm area in hectares
            actual_yield_boost: Multiplier for actual yield (1.0 = baseline)
        
        Returns:
            Dictionary with profitability breakdown
        """
        if crop_type not in self.crops:
            return {"error": f"Crop {crop_type} not found"}
        
        crop = self.crops[crop_type]
        
        # Revenue calculation
        actual_yield = crop["yield"] * farm_area_ha * actual_yield_boost
        total_revenue = actual_yield * crop["market_price"]
        
        # Cost breakdown (per hectare)
        costs = {
            "water": (crop["water_needed"] / 1000) * self.costs["water"]["rate"] * farm_area_ha,
            "fertilizer": 181 * farm_area_ha,  # Assumed fertilizer cost in USD
            "labor": crop["labor_days"] * self.costs["labor"]["rate"] * farm_area_ha,
            "seeds": self.costs["seeds"]["rate"] * farm_area_ha,
            "pesticide": 60 * farm_area_ha,  # Assumed pesticide cost in USD
            "electricity": crop["water_needed"] * 0.8 * 0.10 * 0.001 * farm_area_ha,  # Irrigation pumping
            "miscellaneous": 60 * farm_area_ha  # Transport, tools, etc.
        }
        
        total_cost = sum(costs.values())
        net_profit = total_revenue - total_cost
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            "crop": crop_type,
            "farm_area_ha": farm_area_ha,
            "actual_yield": round(actual_yield, 2),
            "total_revenue_inr": round(total_revenue, 2),
            "costs_breakdown": {k: round(v, 2) for k, v in costs.items()},
            "total_cost_inr": round(total_cost, 2),
            "net_profit_inr": round(net_profit, 2),
            "profit_margin_percent": round(profit_margin, 2),
            "roi_percent": round((net_profit / total_cost * 100) if total_cost > 0 else 0, 2),
            "profit_per_day": round(net_profit / crop["growing_period"], 2)
        }
    
    def compare_crops(self, farm_area_ha=1):
        """Compare profitability of all crops"""
        results = []
        for crop in self.crops.keys():
            analysis = self.calculate_crop_profitability(crop, farm_area_ha)
            results.append(analysis)
        
        df = pd.DataFrame(results)
        df = df.sort_values("net_profit_inr", ascending=False)
        return df
    
    def break_even_analysis(self, crop_type, farm_area_ha=1):
        """
        Calculate break-even point
        
        Args:
            crop_type: Type of crop
            farm_area_ha: Farm area in hectares
        
        Returns:
            Break-even analysis
        """
        if crop_type not in self.crops:
            return {"error": f"Crop {crop_type} not found"}
        
        crop = self.crops[crop_type]
        analysis = self.calculate_crop_profitability(crop_type, farm_area_ha)
        
        # Calculate break-even yield
        total_cost = analysis["total_cost_inr"]
        market_price = crop["market_price"]
        break_even_yield_units = total_cost / market_price
        break_even_yield_percentage = (break_even_yield_units / analysis["actual_yield"] * 100)
        
        return {
            "crop": crop_type,
            "total_cost_inr": total_cost,
            "market_price": market_price,
            "break_even_yield": round(break_even_yield_units, 2),
            "break_even_percentage": round(break_even_yield_percentage, 2),
            "safety_margin": round(100 - break_even_yield_percentage, 2),
            "recommendation": "Good" if break_even_yield_percentage < 70 else "Risky" if break_even_yield_percentage < 90 else "Very Risky"
        }
    
    def seasonal_profitability(self, crop_type, farm_area_ha=1, price_variance=0.1):
        """
        Analyze seasonal profitability with market price variations
        
        Args:
            crop_type: Type of crop
            farm_area_ha: Farm area in hectares
            price_variance: Market price variation range (10% = 0.1)
        
        Returns:
            Seasonal profitability analysis
        """
        if crop_type not in self.crops:
            return {"error": f"Crop {crop_type} not found"}
        
        crop = self.crops[crop_type]
        base_analysis = self.calculate_crop_profitability(crop_type, farm_area_ha)
        
        # Price scenarios
        scenarios = []
        for variation in [-price_variance, -price_variance/2, 0, price_variance/2, price_variance]:
            modified_price = crop["market_price"] * (1 + variation)
            scenario_yield = base_analysis["actual_yield"]
            scenario_revenue = scenario_yield * modified_price
            scenario_profit = scenario_revenue - base_analysis["total_cost_inr"]
            
            scenarios.append({
                "scenario": f"{variation*100:+.0f}% Price",
                "market_price": round(modified_price, 0),
                "revenue": round(scenario_revenue, 0),
                "profit": round(scenario_profit, 0),
                "roi_percent": round((scenario_profit / base_analysis["total_cost_inr"] * 100) if base_analysis["total_cost_inr"] > 0 else 0, 1)
            })
        
        return {
            "crop": crop_type,
            "scenarios": scenarios,
            "base_profit": base_analysis["net_profit_inr"],
            "worst_case_profit": scenarios[0]["profit"],
            "best_case_profit": scenarios[-1]["profit"]
        }


# Dashboard UI Components

def create_irrigation_roi_card(rainfall_mm, crop_type="wheat", farm_area=1):
    """Create irrigation ROI analysis card"""
    analyzer = CostBenefitAnalyzer()
    roi_data = analyzer.calculate_irrigation_roi(rainfall_mm, crop_type, farm_area)
    
    if "error" in roi_data:
        return dbc.Card(
            dbc.CardBody([
                html.P(roi_data["error"], className="text-danger")
            ]),
            className="border-0"
        )
    
    # Color based on recommendation
    rec_color = "#2ecc71" if roi_data["recommendation"] == "Irrigate" else "#f39c12"
    
    return dbc.Card(
        dbc.CardBody([
            html.H5("💧 Irrigation ROI Analysis", className="card-title text-primary mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Water Deficit", className="text-muted small"),
                        html.H4(f"{roi_data['irrigation_needed_mm']:.0f} mm", className="text-info"),
                    ])
                ], md=4),
                dbc.Col([
                    html.Div([
                        html.P("Irrigation Cost", className="text-muted small"),
                        html.H4(f"${roi_data['irrigation_cost_inr']:,.0f}", className="text-warning"),
                    ])
                ], md=4),
                dbc.Col([
                    html.Div([
                        html.P("Expected ROI", className="text-muted small"),
                        html.H4(f"{roi_data['roi_percentage']:.1f}%", className="text-success"),
                    ])
                ], md=4)
            ], className="mb-3"),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.P([html.B("Additional Revenue: "), f"${roi_data['additional_revenue_inr']:,.0f}"])
                ], md=6),
                dbc.Col([
                    html.P([html.B("Payback Period: "), f"{roi_data['payback_days']:.0f} days"])
                ], md=6)
            ]),
            html.Hr(),
            dbc.Alert([
                html.B("📊 Recommendation: "),
                html.Span(roi_data["recommendation"], style={"color": rec_color, "fontWeight": "bold", "fontSize": "1.1em"})
            ], color="light", className="mt-3")
        ]),
        className="border-0 shadow-sm",
        style={"backgroundColor": "#f8f9fa"}
    )


def create_crop_profitability_chart(farm_area=1):
    """Create crop comparison profitability chart"""
    analyzer = CostBenefitAnalyzer()
    df = analyzer.compare_crops(farm_area)
    
    fig = px.bar(
        df,
        x="crop",
        y="net_profit_inr",
        title="Crop Profitability Comparison",
        labels={"net_profit_inr": "Net Profit ($)", "crop": "Crop Type"},
        color="net_profit_inr",
        color_continuous_scale=["#ff6b6b", "#ffd93d", "#6bcf7f"]
    )
    
    fig.update_layout(
        template="plotly_white",
        height=400,
        hovermode="x unified",
        coloraxis_colorbar=dict(title="Profit ($)")
    )
    
    return dcc.Graph(figure=fig)


def create_cost_breakdown_card(crop_type="wheat", farm_area=1):
    """Create cost breakdown pie chart"""
    analyzer = CostBenefitAnalyzer()
    analysis = analyzer.calculate_crop_profitability(crop_type, farm_area)
    
    if "error" in analysis:
        return html.P(analysis["error"], className="text-danger")
    
    costs = analysis["costs_breakdown"]
    
    fig = go.Figure(data=[go.Pie(
        labels=list(costs.keys()),
        values=list(costs.values()),
        marker=dict(colors=["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#ffeaa7", "#dfe6e9", "#a8edea"])
    )])
    
    fig.update_layout(
        title=f"Cost Breakdown for {crop_type.title()} ({farm_area}ha)",
        template="plotly_white",
        height=400
    )
    
    return dcc.Graph(figure=fig)


def create_profitability_metrics(crop_type="wheat", farm_area=1):
    """Create profitability metrics display"""
    analyzer = CostBenefitAnalyzer()
    analysis = analyzer.calculate_crop_profitability(crop_type, farm_area)
    be_analysis = analyzer.break_even_analysis(crop_type, farm_area)
    
    if "error" in analysis:
        return html.P(analysis["error"], className="text-danger")
    
    # Color scheme based on profit margin
    profit_margin = analysis["profit_margin_percent"]
    margin_color = "#2ecc71" if profit_margin > 30 else "#f39c12" if profit_margin > 15 else "#e74c3c"
    roi_color = "#2ecc71" if analysis["roi_percent"] > 50 else "#f39c12" if analysis["roi_percent"] > 20 else "#e74c3c"
    
    return dbc.Card(
        dbc.CardBody([
            html.H5(f"💰 {crop_type.title()} Profitability Analysis", className="card-title text-primary mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H6("Total Revenue", className="text-muted"),
                            html.H4(f"${analysis['total_revenue_inr']:,.0f}", className="text-info mb-2"),
                            html.Small(f"Yield: {analysis['actual_yield']:.1f} units", className="text-muted")
                        ]),
                        className="border-0 shadow-sm text-center"
                    )
                ], md=4, className="mb-3"),
                
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H6("Total Cost", className="text-muted"),
                            html.H4(f"${analysis['total_cost_inr']:,.0f}", className="text-warning mb-2"),
                            html.Small(f"Per hectare", className="text-muted")
                        ]),
                        className="border-0 shadow-sm text-center"
                    )
                ], md=4, className="mb-3"),
                
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H6("Net Profit", className="text-muted"),
                            html.H4(f"${analysis['net_profit_inr']:,.0f}", className="text-success mb-2"),
                            html.Small(f"Per {farm_area}ha", className="text-muted")
                        ]),
                        className="border-0 shadow-sm text-center"
                    )
                ], md=4, className="mb-3")
            ]),
            
            html.Hr(),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.P("Profit Margin", className="text-muted small"),
                        html.H4(f"{profit_margin:.1f}%", style={"color": margin_color}, className="mb-2"),
                        html.P("Range: 15-40% is good", className="small text-muted")
                    ])
                ], md=4),
                
                dbc.Col([
                    html.Div([
                        html.P("Return on Investment", className="text-muted small"),
                        html.H4(f"{analysis['roi_percent']:.1f}%", style={"color": roi_color}, className="mb-2"),
                        html.P("Annual ROI", className="small text-muted")
                    ])
                ], md=4),
                
                dbc.Col([
                    html.Div([
                        html.P("Break-Even Safety", className="text-muted small"),
                        html.H4(f"{be_analysis['safety_margin']:.1f}%", className="text-success mb-2"),
                        html.P(f"Status: {be_analysis['recommendation']}", className="small text-muted")
                    ])
                ], md=4)
            ])
        ]),
        className="border-0 shadow-sm",
        style={"backgroundColor": "#f8f9fa"}
    )


def create_price_scenario_chart(crop_type="wheat", farm_area=1):
    """Create price scenario analysis chart"""
    analyzer = CostBenefitAnalyzer()
    seasonal = analyzer.seasonal_profitability(crop_type, farm_area)
    
    if "error" in seasonal:
        return html.P(seasonal["error"], className="text-danger")
    
    df = pd.DataFrame(seasonal["scenarios"])
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["scenario"],
        y=df["profit"],
        name="Profit",
        marker=dict(color=df["profit"], colorscale="RdYlGn", showscale=False),
        hovertemplate="<b>%{x}</b><br>Profit: $%{y:,.0f}<extra></extra>"
    ))
    
    fig.update_layout(
        title=f"Market Price Scenario Analysis - {crop_type.title()}",
        xaxis_title="Market Price Scenario",
        yaxis_title="Net Profit ($)",
        template="plotly_white",
        height=350,
        showlegend=False,
        hovermode="x unified"
    )
    
    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    # Test the module
    analyzer = CostBenefitAnalyzer()
    
    # Test irrigation ROI
    print("=== Irrigation ROI Analysis ===")
    roi = analyzer.calculate_irrigation_roi(150, "wheat", farm_area_ha=1)
    print(roi)
    
    # Test crop profitability
    print("\n=== Crop Profitability ===")
    prof = analyzer.calculate_crop_profitability("wheat", 1)
    print(f"Net Profit: ${prof['net_profit_inr']}")
    
    # Test crop comparison
    print("\n=== Crop Comparison ===")
    comparison = analyzer.compare_crops(1)
    print(comparison[["crop", "net_profit_inr", "profit_margin_percent"]])
