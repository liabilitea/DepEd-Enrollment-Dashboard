import dash
from dash import dcc, html, callback, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc

# Load figures and insight functions
from data.stats_cards import stat_card_total_students, stat_card_total_schools, stat_card_public_students, stat_card_private_students
from data.home_files.insight1 import fig1, enrollment_per_region_insights
from data.home_files.insight2 import fig2, shs_strand_region_insights
from data.home_files.insight3 import fig3, school_count_coc_insights
from data.home_files.insight4 import fig4, school_type_per_region_insights
from data.home_files.insight5 import fig5, gender_level_insights
from data.home_files.insight6 import fig6, regression_schools_enrollment_insights, province_summary

# Create Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
df_main = pd.read_csv("data/cleaned_data_v3.csv") 
df_v1 = pd.read_csv("data/cleaned_data - cleaned_data.csv")
fig1_findings, fig1_recommendations = enrollment_per_region_insights(df_v1) # Modal data for insight 1
fig2_findings, fig2_recommendations = shs_strand_region_insights(df_main) # Modal data for insight 2
fig3_findings, fig3_recommendations = school_count_coc_insights(df_main) # Modal data for insight 3
fig4_findings, fig4_recommendations = school_type_per_region_insights(df_main) # Modal data for insight 4
fig5_findings, fig5_recommendations = gender_level_insights(df_main) # Modal data for insight 5
fig6_findings, fig6_recommendations = regression_schools_enrollment_insights(province_summary) # Modal data for insight 6

# Create a reusable modal component
def create_insight_modal(modal_id, title, findings, recommendations):
    return dbc.Modal([
        dbc.ModalHeader([
            html.H5(title, className="modal-title"),
            html.Button("×", id=f"close-{modal_id}", className="modal-close-btn")
        ], className="modal-header", close_button=False),
        dbc.ModalBody([
            html.H4("Key Findings", className="modal-body-heading"),
            html.Ul(findings, className="findings-list"),
            html.H4("Recommendations", className="modal-body-heading"),
            html.Ul(recommendations, className="recommendations-list")
        ], className="modal-body")
    ], id=modal_id, 
       is_open=False, 
       centered=True, 
       backdrop="static",  # Prevents closing when clicking outside
       keyboard=False,     # Prevents closing with Escape key
       className="modal-container", 
       scrollable=True,    # Enables scrolling within the modal
       style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "zIndex": 1060}
    )

# Layout
def layout():
    return html.Div(children=[
        html.Div(id="modal-state-div", style={"display": "none"}),
        html.Div(html.H1("DEPED DATA ANALYTICS"), className="home-div1"),

        # STATS CARDS
        html.Div(stat_card_total_students(), className="home-div2 stat-card"),
        html.Div(stat_card_total_schools(), className="home-div3 stat-card"),
        html.Div(stat_card_public_students(), className="home-div4 stat-card"),
        html.Div(stat_card_private_students(), className="home-div5 stat-card"),

        html.Div([
            dcc.Graph(figure=fig4),
            html.Button("CLICK TO VIEW INSIGHTS", id="fig4-open-modal", n_clicks=0,
                style={'margin': '10px', 'backgroundColor': '#004080', 'color': '#fff',
                       'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none'}),
            create_insight_modal("modal_fig4", "School Type by Region", fig4_findings, fig4_recommendations)
        ], className="home-div6", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([
            dcc.Graph(figure=fig1),
            html.Button("CLICK TO VIEW INSIGHTS", id="fig1-open-modal", n_clicks=0,
                style={'margin': '10px', 'backgroundColor': '#004080', 'color': '#fff',
                       'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none'}),
            create_insight_modal("modal_fig1", "Student Enrollment by Region and Grade Level", 
                               fig1_findings, fig1_recommendations)
        ], className="home-div7", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([
            dcc.Graph(figure=fig3),
            html.Button("CLICK TO VIEW INSIGHTS", id="fig3-open-modal", n_clicks=0,
                style={'margin': '10px', 'backgroundColor': '#004080', 'color': '#fff',
                       'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none'}),
            create_insight_modal("modal_fig3", "Distribution of Schools by Modified COC", 
                               fig3_findings, fig3_recommendations)
        ], className="home-div8", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([
            dcc.Graph(figure=fig5),
            html.Button("CLICK TO VIEW INSIGHTS", id="fig5-open-modal", n_clicks=0,
                style={'margin': '10px', 'backgroundColor': '#004080', 'color': '#fff',
                       'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none'}),
            create_insight_modal("modal_fig5", "Gender-Based Student Distribution per Curriculum", 
                               fig5_findings, fig5_recommendations)
        ], className="home-div9", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([
            dcc.Graph(figure=fig2),
            html.Button("CLICK TO VIEW INSIGHTS", id="fig2-open-modal", n_clicks=0,
                style={'margin': '10px', 'backgroundColor': '#004080', 'color': '#fff',
                       'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none'}),
            create_insight_modal("modal_fig2", "Senior High School Enrollment by Strand per Region", 
                               fig2_findings, fig2_recommendations)
        ],className="home-div10", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([
            dcc.Graph(figure=fig6),
            html.Button("CLICK TO VIEW INSIGHTS", id="fig6-open-modal", n_clicks=0,
                style={'margin': '10px', 'backgroundColor': '#004080', 'color': '#fff',
                       'padding': '10px 20px', 'borderRadius': '5px', 'border': 'none'}),
            create_insight_modal("modal_fig6", "Relationship Between Number of Schools and Total Enrollees per Province", 
                               fig6_findings, fig6_recommendations)
        ], className="home-div11", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    ], className="parent")

def toggle_modal(modal_id, open_button_id, close_button_id, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == open_button_id:
        return True
    elif triggered_id == close_button_id:
        return False
    return is_open

# Now you can use the same function for all your modals:
@callback(
    Output("modal_fig1", "is_open"),
    [Input("fig1-open-modal", "n_clicks"),
     Input("close-modal_fig1", "n_clicks")],
    [State("modal_fig1", "is_open")]
)
def toggle_fig1_modal(open_clicks, close_clicks, is_open):
    return toggle_modal("modal_fig1", "fig1-open-modal", "close-modal_fig1", is_open)

@callback(
    Output("modal_fig2", "is_open"),
    [Input("fig2-open-modal", "n_clicks"),
     Input("close-modal_fig2", "n_clicks")],
    [State("modal_fig2", "is_open")]
)
def toggle_fig2_modal(open_clicks, close_clicks, is_open):
    return toggle_modal("modal_fig2", "fig2-open-modal", "close-modal_fig2", is_open)

@callback(
    Output("modal_fig3", "is_open"),
    [Input("fig3-open-modal", "n_clicks"),
     Input("close-modal_fig3", "n_clicks")],
    [State("modal_fig3", "is_open")]
)
def toggle_fig3_modal(open_clicks, close_clicks, is_open):
    return toggle_modal("modal_fig3", "fig3-open-modal", "close-modal_fig3", is_open)

@callback(
    Output("modal_fig4", "is_open"),
    [Input("fig4-open-modal", "n_clicks"),
     Input("close-modal_fig4", "n_clicks")],
    [State("modal_fig4", "is_open")]
)
def toggle_fig4_modal(open_clicks, close_clicks, is_open):
    return toggle_modal("modal_fig4", "fig4-open-modal", "close-modal_fig4", is_open)

@callback(
    Output("modal_fig5", "is_open"),
    [Input("fig5-open-modal", "n_clicks"),
     Input("close-modal_fig5", "n_clicks")],
    [State("modal_fig5", "is_open")]
)
def toggle_fig5_modal(open_clicks, close_clicks, is_open):
    return toggle_modal("modal_fig5", "fig5-open-modal", "close-modal_fig5", is_open)

@callback(
    Output("modal_fig6", "is_open"),
    [Input("fig6-open-modal", "n_clicks"),
     Input("close-modal_fig6", "n_clicks")],
    [State("modal_fig6", "is_open")]
)
def toggle_fig6_modal(open_clicks, close_clicks, is_open):
    return toggle_modal("modal_fig6", "fig6-open-modal", "close-modal_fig6", is_open)


# Clientside callback to manage body scrolling when modals are open
# In your layout

# Then in your callback
app.clientside_callback(
    """
    function(is_open1, is_open2, is_open3, is_open4, is_open5, is_open6) {
        const anyModalOpen = is_open1 || is_open2 || is_open3 || is_open4 || is_open5 || is_open6;
        
        if(anyModalOpen) {
            document.body.classList.add('modal-open');
        } else {
            document.body.classList.remove('modal-open');
        }
        
        // Return something for the hidden div
        return "";
    }
    """,
    Output("modal-state-div", "children"),
    [
        Input("modal_fig1", "is_open"),
        Input("modal_fig2", "is_open"),
        Input("modal_fig3", "is_open"),
        Input("modal_fig4", "is_open"),
        Input("modal_fig5", "is_open"),
        Input("modal_fig6", "is_open")
    ],
    prevent_initial_call=True
)
