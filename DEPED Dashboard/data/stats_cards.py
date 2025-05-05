from dash import html
from dash_iconify import DashIconify
import pandas as pd

# Load data
df_main = pd.read_csv("data/cleaned_data_v3.csv")

# Handle missing values in student count columns
student_columns = [col for col in df_main.columns if 'male' in col or 'female' in col]
df_main[student_columns] = df_main[student_columns].fillna(0)

# Clean and group sector types
df_main['sector'] = df_main['sector'].str.strip().str.title()
public_schools = df_main[df_main['sector'] == 'Public']
private_schools = df_main[df_main['sector'] == 'Private']

# Metrics
total_students = int(df_main[student_columns].sum().sum())
total_schools = int(df_main['beis_school_id'].nunique())
total_public_students = int(public_schools[student_columns].sum().sum())
total_private_students = int(private_schools[student_columns].sum().sum())

# Individual stat card generators
def stat_card_total_students():
    return html.Div([
        DashIconify(icon="mdi:account-group", width=40, style={'color': '#004080'}),
        html.Span("|", style={'margin': '0 10px', 'color': '#cccccc'}),
        html.Div([
            html.H3("Total Students"),
            html.H1(f"{total_students:,}", style={'margin': '0', 'color': '#004080', 'fontSize': '24px'})
        ])
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})

def stat_card_total_schools():
    return html.Div([
        DashIconify(icon="mdi:domain", width=40, style={'color': '#004080'}),
        html.Span("|", style={'margin': '0 10px', 'color': '#cccccc'}),
        html.Div([
            html.H3("Total Schools"),
            html.H1(f"{total_schools:,}", style={'margin': '0', 'color': '#004080', 'fontSize': '24px'})
        ])
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})

def stat_card_public_students():
    return html.Div([
        DashIconify(icon="mdi:account-multiple", width=40, style={'color': '#004080'}),
        html.Span("|", style={'margin': '0 10px', 'color': '#cccccc'}),
        html.Div([
            html.H3("Public School Students"),
            html.H1(f"{total_public_students:,}", style={'margin': '0', 'color': '#004080', 'fontSize': '24px'})
        ])
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})

def stat_card_private_students():
    return html.Div([
        DashIconify(icon="mdi:account-multiple", width=40, style={'color': '#004080'}),
        html.Span("|", style={'margin': '0 10px', 'color': '#cccccc'}),
        html.Div([
            html.H3("Private School Students"),
            html.H1(f"{total_private_students:,}", style={'margin': '0', 'color': '#004080', 'fontSize': '24px'})
        ])
    ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
