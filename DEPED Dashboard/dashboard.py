import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import traceback
from pages import home, insights, geo_overview, student_demo, school_info, upload_csv
from sidebar import sidebar

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "DEPED Dashboard"
# Define the main layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="sidebar-state", data={"is_collapsed": True}),  # Default to collapsed
    sidebar,

    # Main content container
    html.Div(children=[
        html.Div(children=[  
            # Header
            html.Img(src="/assets/logos/deped-logo-with-text.png", className="header-logo1"),
            html.Img(src="/assets/logos/DepED-Logo.png", className="header-logo2")
        ], className="header"),

        # Dynamic content area
        html.Div(id="page-content", className="content") 
    ], id="main-content", className="main-content expanded")  # Default expanded
], className="app-container")

# Callback to update sidebar state
@app.callback(
    [Output("sidebar", "className"),
     Output("main-content", "className"),
     Output("sidebar-state", "data"),
     Output("link-text-upload-csv", "className"),
     Output("link-text-home", "className"),
     Output("link-text-page1", "className"),
     Output("link-text-page2", "className"),
     Output("link-text-page3", "className"),
     Output("link-text-page4", "className"),
     Output("sidebar-title", "className"),
     Output("sidebar-toggle", "className"),
     Output("sidebar-logo", "className"),
     Output("link-text-documentation", "className")],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar-state", "data")]
)
def toggle_sidebar(n_clicks, sidebar_state):
    if n_clicks is None:
        # On initial load, maintain the default collapsed state
        is_collapsed = True
    else:
        is_collapsed = not sidebar_state["is_collapsed"]
    
    # Styles based on collapse state
    if is_collapsed:
        sidebar_class = "sidebar collapsed"
        content_class = "main-content expanded"
        link_text_class = "link-text hidden"
        title_class = "sidebar-title hidden"
        toggle_class = "toggle-button-collapsed"
        logo_class = "logo-small hidden"  # Hide logo when collapsed
    else:
        sidebar_class = "sidebar"
        content_class = "main-content"
        link_text_class = "link-text"
        title_class = "sidebar-title"
        toggle_class = "toggle-button-expanded"
        logo_class = "logo-small"  # Show logo when expanded
    
    # Update the sidebar state
    return sidebar_class, content_class, {"is_collapsed": is_collapsed}, link_text_class, link_text_class, link_text_class, link_text_class, link_text_class, link_text_class, title_class, toggle_class, logo_class, link_text_class

# Callback to update page content with error handling
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    try:
        if pathname == "/" or pathname == "":
            return home.layout()
        elif pathname == "/upload_csv":
            return upload_csv.layout()
        elif pathname == "/geo_overview":
            return geo_overview.layout()
        elif pathname == "/student_demo":
            return student_demo.layout()
        elif pathname == "/school_info":
            return school_info.layout()
        elif pathname == "/insights":
            return insights.layout()
        else:
            # Add a 404 page or redirect to home
            return html.Div([
                html.H1("404 - Page not found", className="page-header"),
                html.P("The page you requested does not exist."),
                html.A("Return to Home", href="/", className="link-button")
            ])
    except Exception as e:
        # Log the error
        print(f"Error loading page {pathname}: {str(e)}")
        print(traceback.format_exc())
        
        # Return an error message to the user
        return html.Div([
            html.H1("Error Loading Page", className="page-header"),
            html.P(f"An error occurred while loading this page: {str(e)}"),
            html.Pre(traceback.format_exc(), style={"whiteSpace": "pre-wrap", "backgroundColor": "#f8f9fa", "padding": "15px", "borderRadius": "5px"}),
            html.A("Return to Home", href="/", className="link-button")
        ])

if __name__ == "__main__":
    app.run(debug=True)