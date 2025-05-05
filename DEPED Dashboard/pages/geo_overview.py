import dash
from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from data.home_files.insight3 import fig32, school_count_coc_insights
from data.home_files.insight6 import fig62, regression_schools_enrollment_insights, province_summary

# Function to generate the key findings and recommendations component
def create_insights_component(findings, recommendations):
    return html.Div([
        # Key Findings Section
        html.Div([
            html.Div("KEY FINDINGS", className="insights-heading"),
            html.Ul(findings, className="geo-findings-list")
        ], className="key-findings-section"),
        
        # Recommendations Section
        html.Div([
            html.Div("RECOMMENDATIONS", className="insights-heading"),
            html.Ul(recommendations, className="geo-recommendations-list")
        ], className="recommendations-section")
    ], className="insights-container")

# Define layout
def layout():

    # Load data and generate insights
    df_v1 = pd.read_csv("data/cleaned_data - cleaned_data.csv")
    df_main = pd.read_csv("data/cleaned_data_v3.csv") 
    fig3_findings, fig3_recommendations = school_count_coc_insights(df_main)
    fig6_findings, fig6_recommendations = regression_schools_enrollment_insights(province_summary)

    return html.Div([
        # Header
        html.Div(html.H1("GEOGRAPHIC OVERVIEW"), className="geo-div1"),
        
        # Main content div
        html.Div([
            # Top navigation - Add n_clicks and ids to each tab
            html.Div([
                html.Div("School Map Distribution", id="tab-geo-overview", className="nav-link active", n_clicks=0),
                html.Div("Regression Analysis", id="tab-graph2", className="nav-link", n_clicks=0),
            ], className="geo-top-nav"),
            
            # Content container
            html.Div([
                # This div will be updated based on the active tab
                html.Div(id="geo-content-container")
            ], className="geo-content-container"),
        ], className="geo-div2"),
        
        # store component to keep track of the active tab
        dcc.Store(id="active-geo-tab", data="tab-geo-overview"),

        # Store the findings and recommendations to pass to the callback
        dcc.Store(id="insights-data", data={
            "tab-geo-overview": {
                "findings": [finding.children for finding in fig3_findings],
                "recommendations": [recommendation.children for recommendation in fig3_recommendations]},
            "tab-graph2": {
                "findings": [finding.children for finding in fig6_findings],
                "recommendations": [recommendation.children for recommendation in fig6_recommendations]},
        })
    ], className="geo-parent")


# Callback to update active tab styling
@callback(
    [Output("tab-geo-overview", "className"),
     Output("tab-graph2", "className"),
     Output("active-geo-tab", "data")],
    [Input("tab-geo-overview", "n_clicks"),
     Input("tab-graph2", "n_clicks")],
    [State("active-geo-tab", "data")]
)
def update_active_geo_tab(click1, click2, current_tab):
    # Find which tab was clicked
    ctx = dash.callback_context
    
    if not ctx.triggered:
        # No clicks yet, return default
        return "nav-link active", "nav-link", "tab-geo-overview"
    
    # Get the id of the component that triggered the callback
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Set all tabs to default class
    tab_classes = ["nav-link", "nav-link"]
    
    # Set the active tab
    if button_id == "tab-geo-overview":
        tab_classes[0] = "nav-link active"
        new_tab = "tab-geo-overview"
    elif button_id == "tab-graph2":
        tab_classes[1] = "nav-link active"
        new_tab = "tab-graph2"
    else:
        # If no match, keep current state
        tab_index = ["tab-geo-overview", "tab-graph2"].index(current_tab)
        tab_classes[tab_index] = "nav-link active"
        new_tab = current_tab
        
    return tab_classes[0], tab_classes[1], new_tab

# Callback to update content based on active tab
@callback(
    Output("geo-content-container", "children"),
    [Input("active-geo-tab", "data"),
    Input("insights-data", "data")]
)

def update_geo_content(active_tab, insights_data):
    # Create the key findings and recommendations components
    tab_insights = insights_data[active_tab]
    findings_items = [html.Li(finding) for finding in tab_insights["findings"]]
    recommendations_items = [html.Li(recommendation) for recommendation in tab_insights["recommendations"]]

    if active_tab == "tab-geo-overview":
        # Return the graph and insights components
        return html.Div([
            dcc.Graph(figure=fig32),
            # Add the insights component with findings and recommendations
            html.Div([
                create_insights_component(findings_items, recommendations_items)
            ], className="insights-wrapper")
        ], className="geo-subnav-container")
    
    elif active_tab == "tab-graph2":
        return html.Div([
            dcc.Graph(figure=fig62),
            html.Div([
                create_insights_component(findings_items, recommendations_items)
            ], className="insights-wrapper")
        ], className="geo-subnav-container", style={"gap": "70px"})