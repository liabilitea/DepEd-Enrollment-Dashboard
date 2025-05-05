import pandas as pd
import json
import plotly.graph_objects as go
import re

def create_school_distribution_map(df):
    """
    Returns:
        plotly.graph_objects.Figure: The generated Plotly figure.
    """
    df = df.copy()

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

    coc_list = df["modified_coc"].dropna().unique().tolist()
    coc_list.append("SNED")

    custom_color = ["#013A63", "#184C71", "#7F9FB8", "#B3C9DC", "#E6F2FF", "#EDB6C0", "#F37980", "#F93D40", "#FF0000"]

    traces = []
    all_region_buttons = []
    pso_buttons = []

    ph_center = {"lat": 12.8797, "lon": 121.7740}
    ph_zoom = 4.5
    pso_center = {"lat": 30, "lon": 30}
    pso_zoom = 3.0

    for i, coc in enumerate(coc_list):
        if coc == "SNED":
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
            visible=(i == 0),
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

    fig = go.Figure(data=traces)

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(center=ph_center, zoom=ph_zoom),
        title=dict(
            text="Distribution of Schools by Modified COC",
            font=dict(size=18, family='Poppins', color='#444444', weight='bold')
        ),
        title_x=0.5,
        title_y=0.98,
        height=1000,
        width=450,
        margin={"r": 0, "t": 110, "l": 0, "b": 100},
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        updatemenus=[
            dict(
                buttons=all_region_buttons + pso_buttons,
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

    return fig
