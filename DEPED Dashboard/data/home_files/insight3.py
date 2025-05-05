import pandas as pd
import json
import plotly.graph_objects as go
import re
from dash import html

# Load your data and geojsons
df = pd.read_csv("data/cleaned_data_v3.csv")
with open("data/json_files/Regions.json", "r", encoding="latin1") as f1:
    geojson_regions = json.load(f1)
with open("data/json_files/world_countries_geojson.geojson", "r", encoding="latin1") as f2:
    geojson_countries = json.load(f2)

# Clean REGION names in GeoJSON to match CSV
for feature in geojson_regions["features"]:
    region_full = feature["properties"].get("REGION", "")
    if "MIMAROPA" in region_full:
        feature["properties"]["REGION"] = "MIMAROPA"
    elif "Caraga" in region_full:
        feature["properties"]["REGION"] = "CARAGA"
    elif "ARMM" in region_full:
        feature["properties"]["REGION"] = "BARMM"
    elif "Metropolitan Manila" in region_full:
        feature["properties"]["REGION"] = "NCR"
    else:
        match = re.search(r"\((.*?)\)", region_full)
        if match:
            feature["properties"]["REGION"] = match.group(1)

# Clean country names in world_countries_geojson
for feature in geojson_countries["features"]:
    countries_full = feature["properties"].get("sovereignt", "")
    if "Bahrain" in countries_full:
        feature["properties"]["sovereignt"] = "Kingdom of Bahrain"
    elif "Saudi Arabia" in countries_full:
        feature["properties"]["sovereignt"] = "Kingdom of Saudi Arabia"
    elif "Qatar" in countries_full:
        feature["properties"]["sovereignt"] = "Qatar"
    elif "United Arab Emirates" in countries_full:
        feature["properties"]["sovereignt"] = "United Arab Emirates"
    elif "East Timor" in countries_full:
        feature["properties"]["sovereignt"] = "East Timor"
    elif "Italy" in countries_full:
        feature["properties"]["sovereignt"] = "Italy"
    elif "Oman" in countries_full:
        feature["properties"]["sovereignt"] = "Sultanate of Oman"
    elif "Kuwait" in countries_full:
        feature["properties"]["sovereignt"] = "State of Kuwait"
    elif "Greece" in countries_full:
        feature["properties"]["sovereignt"] = "Greece"
    else:
        match = re.search(r"\((.*?)\)", countries_full)
        if match:
            feature["properties"]["sovereignt"] = match.group(1)

# Get all unique modified_coc values
coc_list = df["modified_coc"].dropna().unique().tolist()
coc_list.append("SNED")

# Generate traces and visibility map
traces = []
visibility = []
buttons = []
all_region_buttons = []
pso_buttons = []

ph_center = {"lat": 12.8797, "lon": 121.7740}
ph_zoom = 4.5
pso_center = {"lat": 30, "lon": 30}
pso_zoom = 3.0
custom_color = ["#013A63", "#184C71", "#7F9FB8", "#B3C9DC", "#E6F2FF", "#EDB6C0", "#F37980", "#F93D40", "#FF0000"]

for i, coc in enumerate(coc_list):
    if coc == "SNED":
        # Apply SNED logic
        filtered_df = df[
            (df["elem_ng_male"].fillna(0) > 0) |
            (df["elem_ng_female"].fillna(0) > 0) |
            (df["jhs_ng_male"].fillna(0) > 0) |
            (df["jhs_ng_female"].fillna(0) > 0)
        ]
        color_column = "SNED School Count"
    else:
        filtered_df = df[df["modified_coc"].str.contains(coc, na=False, case=False)]
        color_column = "School<br>Count"

    grouped_regions = filtered_df.groupby('region').size().reset_index(name=color_column)
    grouped_countries = filtered_df[~filtered_df['division'].str.contains('El Salvador', na=False, case=False)].groupby('division').size().reset_index(name=color_column)

    # Region trace
    traces.append(go.Choroplethmapbox(
        geojson=geojson_regions,
        locations=grouped_regions["region"],
        z=grouped_regions[color_column],
        featureidkey="properties.REGION",
        colorscale=custom_color,
        colorbar_title=color_column,
        name=f"All Regions - {coc}",
        visible=(i == 0),  # Only first trace visible by default
        hovertemplate=f'COC: {coc}<br>Region: %{{customdata[0]}}<br>{color_column}: %{{z}}<extra></extra>',
        customdata=grouped_regions[["region"]].values
    ))

    # PSO trace
    traces.append(go.Choroplethmapbox(
        geojson=geojson_countries,
        locations=grouped_countries["division"],
        z=grouped_countries[color_column],
        featureidkey="properties.sovereignt",
        colorscale=custom_color,
        colorbar_title=color_column,
        name=f"PSO - {coc}",
        hovertemplate=f'COC: {coc}<br>Country: %{{customdata[0]}}<br>{color_column}: %{{z}}<extra></extra>',
        customdata=grouped_countries[["division"]].values,
        visible=False
    ))

    # Button logic
    visibility_map = [False] * (2 * len(coc_list))
    visibility_map[2 * i] = True
    all_region_buttons.append(dict(
        label=f"{coc} (All Regions)",
        method="update",
        args=[{"visible": visibility_map},
              {"mapbox.center": ph_center, "mapbox.zoom": ph_zoom}]
    ))

    visibility_map_pso = [False] * (2 * len(coc_list))
    visibility_map_pso[2 * i + 1] = True
    pso_buttons.append(dict(
        label=f"{coc} (PSO)",
        method="update",
        args=[{"visible": visibility_map_pso},
              {"mapbox.center": pso_center, "mapbox.zoom": pso_zoom}]
    ))

buttons=all_region_buttons+pso_buttons

# Create figure and add all traces
fig3 = go.Figure(data=traces)

# Layout
fig3.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(center=ph_center, zoom=ph_zoom),
    title=dict(text="Distribution of Schools by Modified COC", font=dict(size=18, family='Poppins', color='#444444', weight='bold')),
    title_x=0.5, title_y=0.98,
    height=1000,
    width=450,
    margin={"r": 0, "t": 110, "l": 0, "b": 100},
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)',
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.6,
            xanchor="center",
            y=1.07,
            yanchor="top",
            bgcolor="white"
        )
    ],
)

# Create figure and add all traces
fig32 = go.Figure(data=traces)

# Layout
fig32.update_layout(
    mapbox_style="carto-positron",
    mapbox=dict(center=ph_center, zoom=ph_zoom),
    title=dict(text="Distribution of Schools by Modified COC", font=dict(size=18, family='Poppins', color='#444444', weight='bold')),
    title_x=0.5, title_y=0.98,
    height=800,
    width=1400,
    margin={"r": 0, "t": 110, "l": 0, "b": 100},
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)',
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.54,
            xanchor="center",
            y=1.1,
            yanchor="top",
            bgcolor="white"
        )
    ],
)

def school_count_coc_insights(df):

    df = df.copy()

    # Get the most coc count across all regions
    most_count_coc = df['modified_coc'].value_counts().idxmax()
    most_count_coc_count = df['modified_coc'].value_counts().max()

    # Get the region that has the most_count_coc
    region_with_most_count = df[df['modified_coc'] == most_count_coc]['region'].value_counts().idxmax()
    region_with_most_count_of_coc_count = df[df['modified_coc'] == most_count_coc]['region'].value_counts().max()

    # Get the coc that is most offered in PSO
    pso_df = df[df['region'].str.contains('PSO', na=False)].copy()

    pso_most_prevalent_coc = None
    pso_most_prevalent_coc_count = 0

    if not pso_df.empty:
        # Get the value counts of 'modified_coc' within the PSO DataFrame
        pso_coc_counts = pso_df['modified_coc'].value_counts()

        if not pso_coc_counts.empty:
            # Get the most frequent 'modified_coc' in PSO
            pso_most_prevalent_coc = pso_coc_counts.idxmax()
            pso_most_prevalent_coc_count = pso_coc_counts.max()

    # Get the least coc count across all regions
    least_count_coc = df['modified_coc'].value_counts().idxmin()
    least_count_coc_count = df['modified_coc'].value_counts().min()

    # Get the region with the least_count_coc
    region_with_least_count = df[df['modified_coc'] == least_count_coc]['region'].value_counts().idxmin()
    region_with_least_count_of_coc_count = df[df['modified_coc'] == least_count_coc]['region'].value_counts().min()

    # Get the region count that offers "All Offering"
    all_offering_non_pso_df = df[
            (df['modified_coc'] == "All Offering") &
            (~df['region'].str.contains('PSO', na=False))
        ]
    max_region_all_offering = all_offering_non_pso_df['region'].value_counts().idxmax() if not all_offering_non_pso_df.empty else None
    min_region_all_offering = all_offering_non_pso_df['region'].value_counts().idxmin() if not all_offering_non_pso_df.empty else None


    # Get the region count that offers "Purely SHS"
    shs_non_pso_df = df[
            (df['modified_coc'] == "Purely SHS") &
            (~df['region'].str.contains('PSO', na=False))
        ]
    max_region_shs = shs_non_pso_df['region'].value_counts().idxmax() if not shs_non_pso_df.empty else None
    min_region_shs = shs_non_pso_df['region'].value_counts().idxmin() if not shs_non_pso_df.empty else None

    # Get the region with highest/lowest SNED school count
    sned_df = df[
        (df["elem_ng_male"].fillna(0) > 0) |
        (df["elem_ng_female"].fillna(0) > 0) |
        (df["jhs_ng_male"].fillna(0) > 0) |
        (df["jhs_ng_female"].fillna(0) > 0)
    ].copy()

    sned_count = len(sned_df)
    region_with_most_sned = sned_df['region'].value_counts().idxmax() if not sned_df.empty else None
    region_with_least_sned = sned_df['region'].value_counts().idxmin() if not sned_df.empty else None

    region_with_most_sned_count = sned_df['region'].value_counts().max() if not sned_df.empty else None
    region_with_least_sned_count = sned_df['region'].value_counts().min() if not sned_df.empty else None

    # Get the percentage of schools offering 'All Offering'
    total_schools = len(df)
    total_all_offering_schools = len(df[df['modified_coc'] == "All Offering"])
    percentage_all_offering = (total_all_offering_schools / total_schools) * 100 if total_schools > 0 else 0

    key_findings = [
        html.Li(f"The most common curriculum offered is '{most_count_coc}' while '{least_count_coc}' is the least offered."),
        html.Li(f"'All Offering' curriculum is most prevalent in '{max_region_all_offering}' and the least in '{min_region_all_offering}'."),
        html.Li(f"The most common curriculum offered by PSO is '{pso_most_prevalent_coc}'."),
        html.Li(f"Only {percentage_all_offering:.2f}% of total schools offers a complete 'All Offering' curriculum."),
        html.Li(f"'SNED' is least offered in '{region_with_least_sned}' with only {region_with_least_sned_count} school count.")
    ]

    recommendations = [
        html.Li(f"Strengthen the support for SNED in '{region_with_least_sned}' for equal opportunities."),
        html.Li(f"Allocate resources in '{min_region_all_offering}' to expand schools that offers complete range of curriculum."),
        html.Li(f"Understand the factors that hinders curriculum expansion in rural areas."),
        html.Li(f"Ensure equitable resource distribution to regions with low educational coverage."),

    ]

    return key_findings, recommendations