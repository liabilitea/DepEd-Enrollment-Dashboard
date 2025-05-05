from dash import dcc, html, Input, Output, State, callback
import base64
import io
import pandas as pd
import re
from google.cloud import storage
import os
import dash_bootstrap_components as dbc
import dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

from data.uploader_files.insight11 import generate_plot as gen_plot1
from data.uploader_files.insight22 import create_enrollment_figure as gen_plot2
from data.uploader_files.insight33 import create_school_distribution_map as gen_plot3
from data.uploader_files.insight44 import generate_plot_sector_enrollment as gen_plot4
from data.uploader_files.insight55 import generate_plot_gender_distribution as gen_plot5
from data.uploader_files.insight66 import generate_plot_school_enrollment_regression as gen_plot6
from data.uploader_files.insight77 import gen_retention_graph as gen_retention

# For Google Cloud Storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "data/json_files/key.json"
PROJECT_ID = 'bda-storage'
BUCKET_NAME = 'bda_grp5'
storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)

def identify_metadata_row(df, max_rows=10):
    """
    Identify the row that contains actual headers in a dataframe.
    Scans the first few rows and finds the row where most values appear to be valid string headers.
    """
    for i in range(min(max_rows, len(df))):
        row = df.iloc[i]
        valid_str_count = row.apply(lambda x: isinstance(x, str) and bool(re.search(r'[A-Za-z]', str(x))))
        if valid_str_count.sum() > len(row) // 2:
            return i
    return 0  # Default to the first row if no better match is found


def clean_metadata_rows(df):
    # Dynamically detect the metadata/header row
    header_row_index = identify_metadata_row(df)

    # Slice the data starting from the row after the header, and set headers properly
    df_cleaned = df.iloc[header_row_index + 1:].reset_index(drop=True)
    df_cleaned.columns = df.iloc[header_row_index]
    df_cleaned = df_cleaned.reset_index(drop=True)

    # Drop completely empty rows and columns
    df_cleaned = df_cleaned.dropna(axis=1, how='all')
    df_cleaned = df_cleaned.dropna(how='all')

    return df_cleaned

def clean_column_names(df):
    # Convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    return df

def clean_division(value):
    if isinstance(value, str):
        if value.lower().startswith("city of "):
            return value[8:] + " City"
        if " - " in value:
            value = value.replace(" - ", " ")
        if value.lower() == "samar (western samar)":
            return "Western Samar"
    return value

def clean_street_address(address):
    if not isinstance(address, str):
        return "Not provided"
    address = address.strip()
    address = address.replace('"', '').replace("'", "").strip()
    missing_values = {"0", "0.0", "not applicable", "Not Applicable",
                      "not available", "Not Available", "-none",
                      "none", "n/a", "N/A", "N / A", "n / a",
                      "_ _ _ _", "______", "-----", "------"}
    if address.lower() in missing_values:
        return "Not provided"
    if re.fullmatch(r"0+", address):
        return "Not provided"
    address = re.sub(r"^[\s,._-]+", "", address)
    address = re.sub(r"@nd", "2nd", address, flags=re.IGNORECASE)
    if len(address) < 5:
        return "Not provided"
    return address

def clean_district(value):
    if isinstance(value, str):
        value = value.strip()
        value = value.replace(" - ", "-")
    return value

def trim_whitespace(value):
    if isinstance(value, str):
        return " ".join(value.split())
    return value

def capitalize_properly(value):
    if isinstance(value, str):
        return re.sub(r"(\b[a-z])|(?<=\(|-)[a-z]", lambda x: x.group().upper(), value.lower())
    return value

def my_cleaning_function(df):
    df_cleaned = df.copy()
    df_cleaned.columns = df_cleaned.columns.str.lower().str.replace(" ", "_")
    if 'street_address' in df_cleaned.columns:
        df_cleaned['street_address'] = df_cleaned['street_address'].apply(clean_street_address)
    if 'barangay' in df_cleaned.columns:
        df_cleaned['barangay'] = df_cleaned['barangay'].fillna("Not provided").apply(capitalize_properly)
    if 'street_address' in df_cleaned.columns:
        df_cleaned['street_address'] = df_cleaned['street_address'].fillna("Not provided").replace(
            to_replace=r'^\s*["\']?(0+|N/A|None|none|n/a|not available|not applicable)["\']?\s*$',
            value="Not provided",
            regex=True
        )
    for col in df_cleaned.columns[:14]:
        if df_cleaned[col].dtype == "object":
            df_cleaned[col] = df_cleaned[col].apply(trim_whitespace)
    if 'division' in df_cleaned.columns:
        df_cleaned['division'] = df_cleaned['division'].apply(clean_division)
    if 'district' in df_cleaned.columns:
        df_cleaned['district'] = df_cleaned['district'].apply(clean_district)
    if 'province' in df_cleaned.columns:
        df_cleaned['province'] = df_cleaned['province'].apply(capitalize_properly)
    if 'municipality' in df_cleaned.columns:
        df_cleaned['municipality'] = df_cleaned['municipality'].apply(capitalize_properly)
    if 'barangay' in df_cleaned.columns:
        df_cleaned['barangay'] = df_cleaned['barangay'].apply(capitalize_properly)
    return df_cleaned

# Modified upload_to_gcs
def upload_to_gcs(contents, filename):
    try:
        blob = bucket.blob(f'uploads/{filename}')
        if blob.exists():
            return f'gs://{BUCKET_NAME}/uploads/{filename}', True  # Already exists

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        blob.upload_from_file(io.BytesIO(decoded), content_type=content_type)
        return f'gs://{BUCKET_NAME}/uploads/{filename}', False  # Newly uploaded

    except Exception as e:
        print(f"Error uploading to GCS: {e}")
        return None, False

def read_dataframe_from_gcs(gcs_url):
    try:
        blob_name = '/'.join(gcs_url.split('/')[3:])
        blob = bucket.blob(blob_name)
        file_obj = io.BytesIO(blob.download_as_bytes())
        filename = blob_name.split('/')[-1]
        if filename.endswith('.csv'):
            df = pd.read_csv(file_obj)
        elif filename.endswith('.xlsx'):
            df = pd.read_excel(file_obj)
        return df
    except Exception as e:
        print(f"Error reading from GCS: {e}")
        return None

# Modified get_uploaded_dataframe
def get_uploaded_dataframe(contents, filename):
    gcs_url, already_exists = upload_to_gcs(contents, filename)
    if gcs_url:
        df = read_dataframe_from_gcs(gcs_url)
        return df, already_exists
    return None, False

# Utility to dynamically find column name from a list of options
def get_column_name(df, options):
    df_cols = df.columns.str.lower()
    for col in options:
        col_clean = col.lower().replace(" ", "_")
        if col_clean in df_cols.values:
            return col_clean
    return None

# Layout
def layout():
    return html.Div([
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload File', style={
                    'backgroundColor': 'white', 'color': '#004080',
                    'border': 'none', 'padding': '10px 20px',
                    'borderRadius': '6px', 'cursor': 'pointer',
                    'fontFamily': 'Poppins'
                }),
                multiple=False
            ),
            html.Div(id='output-message', style={'marginTop': '10px'}),
        ], className="upload-div1"),

        html.Div([
            dcc.Loading(
                id="loading-graphs",
                type="default",
                color="#004080",
                children=html.Div(id="output-message", children="Please upload your data file.")
            )
        ], className="upload-div2"),

        html.Div([
            dcc.Graph(id='retention-plot'),
        ], className="upload-div-retention", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([dcc.Graph(id='insight-plot-4'),
        ], className="upload-div3", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([dcc.Graph(id='insight-plot-1'),
        ], className="upload-div4", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([dcc.Graph(id='insight-plot-3'),
        ], className="upload-div5", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([dcc.Graph(id='insight-plot-5'),
        ], className="upload-div6", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([dcc.Graph(id='insight-plot-2'),
        ], className="upload-div7", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

        html.Div([dcc.Graph(id='insight-plot-6'),
        ], className="upload-div8", style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),

    ], className="upload-parent")

# Callback
@callback(
    Output('insight-plot-1', 'figure'),
    Output('insight-plot-2', 'figure'),
    Output('insight-plot-3', 'figure'),
    Output('insight-plot-4', 'figure'),
    Output('insight-plot-5', 'figure'),
    Output('insight-plot-6', 'figure'),
    Output('retention-plot', 'figure'),
    Output('output-message', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'), allow_duplicate=True
)
def update_dashboard(contents, filename):
    if contents is not None:
        try:
            df, already_exists = get_uploaded_dataframe(contents, filename)
            if df is not None:
                cleaned_df = my_cleaning_function(df)
                fig1 = gen_plot1(cleaned_df)
                fig2 = gen_plot2(cleaned_df)
                fig3 = gen_plot3(cleaned_df)
                fig4 = gen_plot4(cleaned_df)
                fig5 = gen_plot5(cleaned_df)
                fig6 = gen_plot6(cleaned_df)
                fig7 = gen_retention(cleaned_df)

                # Generate dynamic province_summary from the cleaned_df
                # Dynamically get column names
                province_col = get_column_name(cleaned_df, ["province"])
                school_col = get_column_name(cleaned_df, ["school_id", "school_name", "School ID", "School Name"])
                enrollees_col = get_column_name(cleaned_df, ["total_enrollees", "Total Enrollees", "enrollees", "Enrollment"])

                # Build dynamic province summary
                if province_col and school_col and enrollees_col:
                    province_summary_dynamic = (
                        cleaned_df.groupby(province_col)
                        .agg(
                            number_of_schools=(school_col, "nunique"),
                            total_enrollees=(enrollees_col, "sum")
                        )
                        .reset_index()
                    )
                else:
                    print("Warning: Required columns not found for province summary.")
                    province_summary_dynamic = pd.DataFrame(columns=["province", "number_of_schools", "total_enrollees"])

                # Rename to match expected column names in the insight function
                province_summary_dynamic = province_summary_dynamic.rename(columns={
                    "number_of_schools": "Number_of_Schools",
                    "total_enrollees": "Total_Enrollees"
                })

                message = f"File '{filename}' was uploaded successfully!" if already_exists else f"File '{filename}' uploaded successfully."
                return fig1, fig2, fig3, fig4, fig5, fig6, fig7, html.Div(message, style={'color': 'green', 'fontWeight': 'bold', 'font':' Poppins'})

            else:
                return {}, {}, {}, {}, {}, {}, {}, html.Div("Error processing the uploaded file from Google Cloud Storage.", style={'color': 'red', 'font':' Poppins'})

        except ValueError as e:
            return {}, {}, {}, {}, {}, {}, {}, html.Div(str(e), style={'color': 'red', 'font':' Poppins'})

    return {}, {}, {}, {}, {}, {}, {}, html.Div("Upload your data file.", style={'color': 'gray'})

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
