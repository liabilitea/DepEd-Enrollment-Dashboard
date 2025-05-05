# data/uploader_files/insight77.py

import pandas as pd
import plotly.express as px
from google.cloud import storage
import io


def clean_column_names(df):
    """
    Standardize and clean column names, rename kindergarten fields, convert to uppercase
    """
    df_cleaned = df.copy()
    df_cleaned.columns = df_cleaned.columns.str.lower().str.replace(" ", "_")
    new_columns = []
    for col in df_cleaned.columns:
        if col.startswith("k_"):
            col = col.replace("k_", "kinder_", 1)
        new_columns.append(col.upper())
    df_cleaned.columns = new_columns
    return df_cleaned


def load_reference_data():
    """
    Load reference data from Google Cloud Storage (GCS) and clean it
    """
    try:
        project_id = 'bda-storage'
        bucket_name = 'bda_grp5'
        blob_path = 'cleaned_data_v3.csv'

        storage_client = storage.Client(project=project_id)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        content = blob.download_as_bytes()
        df = pd.read_csv(io.BytesIO(content))
        return clean_reference_data(df)
    except Exception as e:
        print(f"[Error loading reference data from GCS]: {e}")
        return pd.DataFrame()


def clean_reference_data(df):
    """
    Clean reference data consistently with uploaded data
    """
    df_cleaned = clean_column_names(df)
    df_cleaned = df_cleaned.drop(columns=['STREET_ADDRESS', 'BARANGAY'], errors='ignore')
    return df_cleaned


# Load the reference (existing) dataset from cloud
try:
    df_2023 = load_reference_data()
except Exception as e:
    print(f"[Error loading 2023 data]: {e}")
    df_2023 = pd.DataFrame()


def get_grade_totals(df, school_year):
    """
    Compute total enrollment per grade level from gender-based columns
    """
    grade_levels = set(col.replace('_MALE', '').replace('_FEMALE', '')
                       for col in df.columns if '_MALE' in col or '_FEMALE' in col)

    records = []
    for grade in sorted(grade_levels):
        male_col = f"{grade}_MALE"
        female_col = f"{grade}_FEMALE"
        if male_col in df.columns and female_col in df.columns:
            total = df[male_col].sum() + df[female_col].sum()
            records.append({
                "GRADE_LEVEL": grade.replace("_", " ").upper(),
                "TOTAL_ENROLLEES": total,
                "SCHOOL_YEAR": school_year
            })
    return pd.DataFrame(records)


def grade_sort_key(grade):
    """
    Sorting function for grade levels (supports Nursery, Kinder, G1-G12, SPED)
    """
    grade = grade.upper()
    if "NURSERY" in grade: return -3
    if "PRE" in grade: return -2
    if "KINDER" in grade: return -1
    if "SPED" in grade: return 99
    return int(''.join(filter(str.isdigit, grade)) or 0)


def gen_retention_graph(df_upload):
    """
    Generate a line plot comparing enrollment counts by grade level across two school years:
    - df_2023: reference data (2023-2024)
    - df_upload: newly uploaded data (2024-2025 or user-defined)
    """
    if df_upload is None or df_upload.empty:
        print("[No uploaded data provided]")
        return None

    # Clean uploaded data
    df_upload_cleaned = clean_column_names(df_upload)
    df_upload_cleaned = df_upload_cleaned.drop(columns=['STREET_ADDRESS', 'BARANGAY'], errors='ignore')

    # Get totals
    df_2023_totals = get_grade_totals(df_2023, "2023-2024")
    df_upload_totals = get_grade_totals(df_upload_cleaned, "Your Data File")

    # Combine both years
    combined_df = pd.concat([df_2023_totals, df_upload_totals], ignore_index=True)

    # Sort grade levels properly
    combined_df["GRADE_LEVEL"] = pd.Categorical(
        combined_df["GRADE_LEVEL"],
        categories=sorted(combined_df["GRADE_LEVEL"].unique(), key=grade_sort_key),
        ordered=True
    )
    combined_df = combined_df.sort_values("GRADE_LEVEL")

    # Create the line chart
    fig = px.line(
        combined_df,
        x="GRADE_LEVEL",
        y="TOTAL_ENROLLEES",
        color="SCHOOL_YEAR",
        markers=True,
        title="Enrollment Trends by Grade Level",
        labels={
            "GRADE_LEVEL": "Grade Level",
            "TOTAL_ENROLLEES": "Total Enrollees",
            "SCHOOL_YEAR": "School Year"
        },
        color_discrete_map={
            "2023-2024": "#004080",
            "Your Data File": "#ff0000",
        }
    )

    fig.update_layout(
        title=dict(
            text="Enrollment Trends by Grade Level",
            font=dict(size=16, family='Poppins', color='#444444', weight='bold'),
            x=0.5
        ),
        xaxis=dict(
            title=dict(text="Grade Level", font=dict(size=14, family='Poppins')),
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="Total Enrollees", font=dict(size=14, family='Poppins'))
        ),
        legend_title=dict(
            text="School Year",
            font=dict(size=14, family='Poppins')
        ),
        legend=dict(
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
        hovermode="x unified",
        width=1300,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    return fig
