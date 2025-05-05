import dash
from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from data.home_files.insight1 import fig1, enrollment_per_region_insights
from data.home_files.insight2 import fig2, shs_strand_region_insights
from data.home_files.insight4 import fig4, school_type_per_region_insights

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Function to generate the key findings and recommendations component
def create_insights_component(findings, recommendations):
    return html.Div([
        # Key Findings Section
        html.Div([
            html.Div("KEY FINDINGS", className="info-insights-heading"),
            html.Ul(findings, className="info-findings-list")
        ], className="info-key-findings-section"),
        
        # Recommendations Section
        html.Div([
            html.Div("RECOMMENDATIONS", className="info-insights-heading"),
            html.Ul(recommendations, className="info-recommendations-list")
        ], className="info-recommendations-section")
    ], className="info-insights-container")

def layout():
    # Load data and generate insights
    df_main = pd.read_csv("data/cleaned_data_v3.csv") 
    df_v1 = pd.read_csv("data/cleaned_data - cleaned_data.csv")

    fig1_findings, fig1_recommendations = enrollment_per_region_insights(df_v1)
    fig2_findings, fig2_recommendations = shs_strand_region_insights(df_main)
    fig4_findings, fig4_recommendations = school_type_per_region_insights(df_main)

    return html.Div([
        html.Div(html.H1("STUDENT INFORMATION"), className="info-div1"),

        html.Div([
            html.Div([
                html.Div("School Type Distribution", id="tab-1", className="nav-link active", n_clicks=0),
                html.Div("Grade Level Heatmap", id="tab-2", className="nav-link", n_clicks=0),
                html.Div("SHS Strand Analysis", id="tab-3", className="nav-link", n_clicks=0),
            ], className="info-top-nav"),

            html.Div([
                html.Div(id="info-content-container")
            ], className="info-content-container"),
        ], className="info-div2"),

        dcc.Store(id="active-info-tab", data="tab-1"),

        dcc.Store(id="info-insights-data", data={
            "tab-1": {
                "findings": [finding.children for finding in fig4_findings],
                "recommendations": [recommendation.children for recommendation in fig4_recommendations]
            },
            "tab-2": {
                "findings": [finding.children for finding in fig1_findings],
                "recommendations": [recommendation.children for recommendation in fig1_recommendations]
            },
            "tab-3": {
                "findings": [finding.children for finding in fig2_findings],
                "recommendations": [recommendation.children for recommendation in fig2_recommendations]
            }
        })
    ], className="info-parent")

@callback(
    [Output("tab-1", "className"),
     Output("tab-2", "className"),
     Output("tab-3", "className"),
     Output("active-info-tab", "data")],
    [Input("tab-1", "n_clicks"),
     Input("tab-2", "n_clicks"),
     Input("tab-3", "n_clicks")],
    [State("active-info-tab", "data")]
)
def update_active_info_tab(click1, click2, click3, current_tab):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "nav-link active", "nav-link", "nav-link", "tab-1"

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    tab_classes = ["nav-link", "nav-link", "nav-link"]

    if button_id == "tab-1":
        tab_classes[0] = "nav-link active"
        new_tab = "tab-1"
    elif button_id == "tab-2":
        tab_classes[1] = "nav-link active"
        new_tab = "tab-2"
    elif button_id == "tab-3":
        tab_classes[2] = "nav-link active"
        new_tab = "tab-3"
    else:
        tab_index = ["tab-1", "tab-2", "tab-3"].index(current_tab)
        tab_classes[tab_index] = "nav-link active"
        new_tab = current_tab

    return tab_classes[0], tab_classes[1], tab_classes[2], new_tab

@callback(
    Output("info-content-container", "children"),
    [Input("active-info-tab", "data"),
     Input("info-insights-data", "data")]
)
def update_info_content(active_tab, insights_data):
    tab_insights = insights_data[active_tab]
    findings_items = [html.Li(finding) for finding in tab_insights["findings"]]
    recommendations_items = [html.Li(recommendation) for recommendation in tab_insights["recommendations"]]

    if active_tab == "tab-1":
        return html.Div([
            dcc.Graph(figure=fig4),
            html.Div([
                create_insights_component(findings_items, recommendations_items)
            ], className="info-insights-wrapper")
        ], className="info-subnav-container", style={"gap": "50px"})

    elif active_tab == "tab-2":
        return html.Div([
            dcc.Graph(figure=fig1),
            html.Div([
                create_insights_component(findings_items, recommendations_items)
            ], className="info-insights-wrapper")
        ], className="info-subnav-container", style={"gap": "50px"})

    elif active_tab == "tab-3":
        return html.Div([
            dcc.Graph(figure=fig2),
            html.Div([
                create_insights_component(findings_items, recommendations_items)
            ], className="info-insights-wrapper")
        ], className="info-subnav-container", style={"gap": "50px"})

    return html.Div("No content available.")
