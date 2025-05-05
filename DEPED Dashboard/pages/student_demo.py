import dash
from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from data.home_files.insight5 import fig5, gender_level_insights

# Create Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Function to generate the key findings and recommendations component
def create_insights_component(findings, recommendations):
    return html.Div([
        # Key Findings Section
        html.Div([
            html.Div("KEY FINDINGS", className="demo-insights-heading"),
            html.Ul(findings, className="demo-findings-list")
        ], className="demo-key-findings-section"),
        
        # Recommendations Section
        html.Div([
            html.Div("RECOMMENDATIONS", className="demo-insights-heading"),
            html.Ul(recommendations, className="demo-recommendations-list")
        ], className="demo-recommendations-section")
    ], className="demo-insights-container")

# Define layout
def layout():

    # Load data and generate insights
    df_main = pd.read_csv("data/cleaned_data_v3.csv") 
    fig5_findings, fig5_recommendations = gender_level_insights(df_main) 

    return html.Div([
        # Header
        html.Div(html.H1("STUDENT DEMOGRAPHICS"), className="demo-div1"),
        
        # Main content div
        html.Div([
            # Top navigation - simplified to just one tab
            html.Div([
                html.Div("Demographic Overview", id="tab-demo-overview", className="nav-link active", n_clicks=0),
            ], className="demo-top-nav"),
            
            # Content container
            html.Div([
                # This div will be updated based on the active tab
                html.Div(id="demo-content-container")
            ], className="demo-content-container"),
        ], className="demo-div2"),
        
        # Store the active tab (simplified to just one tab)
        dcc.Store(id="active-demo-tab", data="tab-demo-overview"),
        # Store the findings and recommendations to pass to the callback
        dcc.Store(id="insights-data", data={
            "tab-demo-overview": {
                "findings": [finding.children for finding in fig5_findings],
                "recommendations": [recommendation.children for recommendation in fig5_recommendations]
            }
        })
    ], className="demo-parent")

# Callback to update active tab styling (simplified)
@callback(
    [Output("tab-demo-overview", "className"),
     Output("active-demo-tab", "data")],
    [Input("tab-demo-overview", "n_clicks")],
    [State("active-demo-tab", "data")]
)
def update_active_demo_tab(click1, current_tab):
    # Since there's only one tab now, always keep it active
    return "nav-link active", "tab-demo-overview"

# Callback to update content based on active tab
@callback(
    Output("demo-content-container", "children"),
    [Input("active-demo-tab", "data"),
    Input("insights-data", "data")]
)
def update_demo_content(active_tab, insights_data):
    # Create the key findings and recommendations components
    tab_insights = insights_data[active_tab]
    findings_items = [html.Li(finding) for finding in tab_insights["findings"]]
    recommendations_items = [html.Li(recommendation) for recommendation in tab_insights["recommendations"]]

    # Now there's only one tab option: tab-demo-overview
    return html.Div([
        dcc.Graph(figure=fig5),
        # Add the insights component with findings and recommendations
        html.Div([
            create_insights_component(findings_items, recommendations_items)
        ], className="demo-insights-wrapper")
    ], className="demo-subnav-container", style={"gap": "50px"})