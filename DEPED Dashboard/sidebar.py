from dash import dcc, html
from dash_iconify import DashIconify

# Sidebar layout with collapsible content
sidebar = html.Div(
    [
        html.Div([
            # Sidebar header with logo, title and toggle button
            html.Div([
                # Toggle button is now inside the sidebar
                html.Img(
                    src="/assets/logos/logo.png", 
                    id="sidebar-logo", 
                    className="logo-small hidden",
                    style={'display': 'block'}  # Ensure visibility on mobile
                ),
                html.H2("DepEd", id="sidebar-title", className="sidebar-title hidden"),
                html.Button(
                    DashIconify(icon="mdi:menu", width=36),
                    id="sidebar-toggle",
                    className="toggle-button-collapsed",
                    style={'display': 'flex'}  # Ensure button is always visible
                ),
            ], className="sidebar-header"),
            
            html.Div([
                dcc.Link([
                    html.Div(DashIconify(icon="mdi:plus", width=24), className="nav-icon"),
                    html.Span("Upload CSV", id="link-text-upload-csv", className="link-text hidden")
                ], href="/upload_csv", className="nav-link"),
                dcc.Link([
                    html.Div(DashIconify(icon="mdi:home", width=24), className="nav-icon"),
                    html.Span("Dashboard", id="link-text-home", className="link-text hidden")
                ], href="/", className="nav-link"),
                dcc.Link([
                    html.Div(DashIconify(icon="mdi:map-marker", width=24), className="nav-icon"),
                    html.Span("Geographic Overview", id="link-text-page1", className="link-text hidden")
                ], href="/geo_overview", className="nav-link"),
                dcc.Link([
                    html.Div(DashIconify(icon="mdi:cloud", width=24), className="nav-icon"),
                    html.Span("Student Demographics", id="link-text-page2", className="link-text hidden")
                ], href="/student_demo", className="nav-link"),
                dcc.Link([
                    html.Div(DashIconify(icon="mdi:information", width=24), className="nav-icon"),
                    html.Span("School Information", id="link-text-page3", className="link-text hidden")
                ], href="/school_info", className="nav-link"),
                dcc.Link([
                    html.Div(DashIconify(icon="mdi:lightbulb", width=24), className="nav-icon"),
                    html.Span("Insights", id="link-text-page4", className="link-text hidden")
                ], href="/insights", className="nav-link"),
            ], className="nav-links"),
            
            # Documentation link at the bottom of the sidebar
            html.Div([
                html.A([
                    html.Div(DashIconify(icon="mdi:file-document", width=24), className="nav-icon"),
                    html.Span("Documentation", id="link-text-documentation", className="link-text hidden")
                ], href="https://colab.research.google.com/drive/1bf9frOkr3rhAnusELaSzxVLK6_d1Q-4Q?usp=sharing&fbclid=IwY2xjawJzPy9leHRuA2FlbQIxMAABHnGSpo7J7VKr2oCt6Z5gFzph6H9bZzp9FGmZ2TIi0GTy4JW75BmEAZ6lvtl__aem_gr5_cpa6KAo49s9e6e8SmQ#scrollTo=z_wZpOIrQEBq", target="_blank", className="nav-link")
            ], className="sidebar-footer")
        ], id="sidebar-content")
    ],
    id="sidebar",
    className="sidebar collapsed"  # Default to collapsed
)