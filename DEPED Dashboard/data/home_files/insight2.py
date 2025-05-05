import pandas as pd
import plotly.graph_objects as go
from dash import html

df = pd.read_csv("data/cleaned_data_v3.csv")

# DataFrame
df["G11_ABM"] = df["g11_acad_-_abm_male"] + df["g11_acad_-_abm_female"]
df["G11_HUMSS"] = df["g11_acad_-_humss_male"] + df["g11_acad_-_humss_female"]
df["G11_STEM"] = df["g11_acad_stem_male"] + df["g11_acad_stem_female"]
df["G11_GAS"] = df["g11_acad_gas_male"] + df["g11_acad_gas_female"]
df["G11_TVL"] = df["g11_tvl_male"] + df["g11_tvl_female"]
df["G11_SPORTS"] = df["g11_sports_male"] + df["g11_sports_female"]
df["G11_ARTS"] = df["g11_arts_male"] + df["g11_arts_female"]

df["G12_ABM"] = df["g12_acad_-_abm_male"] + df["g12_acad_-_abm_female"]
df["G12_HUMSS"] = df["g12_acad_-_humss_male"] + df["g12_acad_-_humss_female"]
df["G12_STEM"] = df["g12_acad_stem_male"] + df["g12_acad_stem_female"]
df["G12_GAS"] = df["g12_acad_gas_male"] + df["g12_acad_gas_female"]
df["G12_TVL"] = df["g12_tvl_male"] + df["g12_tvl_female"]
df["G12_SPORTS"] = df["g12_sports_male"] + df["g12_sports_female"]
df["G12_ARTS"] = df["g12_arts_male"] + df["g12_arts_female"]

df["ABM"] = df["G11_ABM"] + df["G12_ABM"]
df["HUMSS"] = df["G11_HUMSS"] + df["G12_HUMSS"]
df["STEM"] = df["G11_STEM"] + df["G12_STEM"]
df["GAS"] = df["G11_GAS"] + df["G12_GAS"]
df["TVL"] = df["G11_TVL"] + df["G12_TVL"]
df["SPORTS"] = df["G11_SPORTS"] + df["G12_SPORTS"]
df["ARTS"] = df["G11_ARTS"] + df["G12_ARTS"]

# Group and melt
region_totals = {
    "G11": df.groupby("region")[["G11_ABM", "G11_HUMSS", "G11_STEM", "G11_GAS", "G11_TVL", "G11_SPORTS", "G11_ARTS"]].sum().reset_index().rename(columns=lambda x: x.replace("G11_", "")),
    "G12": df.groupby("region")[["G12_ABM", "G12_HUMSS", "G12_STEM", "G12_GAS", "G12_TVL", "G12_SPORTS", "G12_ARTS"]].sum().reset_index().rename(columns=lambda x: x.replace("G12_", "")),
    "TOTAL": df.groupby("region")[["ABM", "HUMSS", "STEM", "GAS", "TVL", "SPORTS", "ARTS"]].sum().reset_index()
}

# Color scheme
colors = {
    "ABM": "#013A63",
    "HUMSS": "#004080",
    "STEM": "#0074A5",
    "GAS": "#E7331A",
    "TVL": "#FF0000",
    "SPORTS": "#F26A16",
    "ARTS": "#F0B50D"
}

# Prepare traces per view
data = {}
for key, rdf in region_totals.items():
    melted = rdf.melt(id_vars="region", var_name="Strand", value_name="Enrollees")
    traces = []
    for strand in melted["Strand"].unique():
        strand_data = melted[melted["Strand"] == strand]
        traces.append(go.Bar(
            x=strand_data["Enrollees"],
            y=strand_data["region"],
            name=strand,
            orientation="h",
            marker=dict(color=colors[strand]),
            visible=True if key == "TOTAL" else False
        ))
    data[key] = traces

# Combine all traces
all_traces = data["G11"] + data["G12"] + data["TOTAL"]

# Visibility logic
visibility = {
    "G11": [True]*7 + [False]*7 + [False]*7,
    "G12": [False]*7 + [True]*7 + [False]*7,
    "TOTAL": [False]*7 + [False]*7 + [True]*7
}


layout = go.Layout(
    title=dict(
        text="<b>Senior High School Enrollment by Strand per Region</b>",
        x=0.5, y =0.95,
        font=dict(family="Poppins", size=18, color="#444444")
    ),
    barmode="stack",
    xaxis=dict(
        title=dict(
            text="<b>Number of Enrollees</b>",
            font=dict(family="Poppins", size=12, color="#444444")
        )
    ),
    yaxis=dict(
        title=dict(
            text="<b>Region</b>",
            font=dict(family="Poppins", size=12, color="#444444")
        )
    ),
    height=600, width=900,
    margin={"r": 0, "t": 100, "l": 0, "b": 70},  # Adjusted top margin for title spacing
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font=dict(family="Poppins", size=10, color="#444444"),
    legend=dict(
        font=dict(family="Poppins", size=10, color="#444444"),
        title=dict(text="<b>Strand</b>")
    ),
    updatemenus=[dict(
        type="dropdown",
        buttons=[
            dict(label="Total SHS Enrollment", method="update", args=[{"visible": visibility["TOTAL"]}]),
            dict(label="Grade 11", method="update", args=[{"visible": visibility["G11"]}]),
            dict(label="Grade 12", method="update", args=[{"visible": visibility["G12"]}])
        ],
        showactive=True,
        x=0.4,
        y=1.1,
        xanchor="left",
        yanchor="top", bgcolor="white"
    )]
)


# Plot figure
fig2 = go.Figure(data=all_traces, layout=layout)

def shs_strand_region_insights(df):
    if "ABM" not in df.columns:
        # Create G11 strand columns if they don't exist
        if "G11_ABM" not in df.columns:
            df["G11_ABM"] = df["g11_acad_-_abm_male"] + df["g11_acad_-_abm_female"]
            df["G11_HUMSS"] = df["g11_acad_-_humss_male"] + df["g11_acad_-_humss_female"]
            df["G11_STEM"] = df["g11_acad_stem_male"] + df["g11_acad_stem_female"]
            df["G11_GAS"] = df["g11_acad_gas_male"] + df["g11_acad_gas_female"]
            df["G11_TVL"] = df["g11_tvl_male"] + df["g11_tvl_female"]
            df["G11_SPORTS"] = df["g11_sports_male"] + df["g11_sports_female"]
            df["G11_ARTS"] = df["g11_arts_male"] + df["g11_arts_female"]
        
        # Create G12 strand columns if they don't exist
        if "G12_ABM" not in df.columns:
            df["G12_ABM"] = df["g12_acad_-_abm_male"] + df["g12_acad_-_abm_female"]
            df["G12_HUMSS"] = df["g12_acad_-_humss_male"] + df["g12_acad_-_humss_female"]
            df["G12_STEM"] = df["g12_acad_stem_male"] + df["g12_acad_stem_female"]
            df["G12_GAS"] = df["g12_acad_gas_male"] + df["g12_acad_gas_female"]
            df["G12_TVL"] = df["g12_tvl_male"] + df["g12_tvl_female"]
            df["G12_SPORTS"] = df["g12_sports_male"] + df["g12_sports_female"]
            df["G12_ARTS"] = df["g12_arts_male"] + df["g12_arts_female"]
        
        # Create total strand columns
        df["ABM"] = df["G11_ABM"] + df["G12_ABM"]
        df["HUMSS"] = df["G11_HUMSS"] + df["G12_HUMSS"]
        df["STEM"] = df["G11_STEM"] + df["G12_STEM"]
        df["GAS"] = df["G11_GAS"] + df["G12_GAS"]
        df["TVL"] = df["G11_TVL"] + df["G12_TVL"]
        df["SPORTS"] = df["G11_SPORTS"] + df["G12_SPORTS"]
        df["ARTS"] = df["G11_ARTS"] + df["G12_ARTS"]

    # Total enrollees by region
    region_totals = df.groupby("region")[["ABM", "HUMSS", "STEM", "GAS", "TVL", "SPORTS", "ARTS"]].sum()
    region_totals["Total"] = region_totals.sum(axis=1)

    # Find most and least enrolled region
    most_region = region_totals["Total"].idxmax()
    least_region = region_totals["Total"].idxmin()

    # Total enrollees by strand
    strand_totals = df[["ABM", "HUMSS", "STEM", "GAS", "TVL", "SPORTS", "ARTS"]].sum()
    most_strand = strand_totals.idxmax()
    least_strand = strand_totals.idxmin()

    # Key insights
    most_region_enrollments = region_totals.loc[most_region, "Total"]
    least_region_enrollments = region_totals.loc[least_region, "Total"]
    most_strand_enrollments = strand_totals[most_strand]
    least_strand_enrollments = strand_totals[least_strand]

    insights = [
        html.Li(f"{most_region} has the highest number of Senior High School enrollees in both Grade 11 and Grade 12, totaling {most_region_enrollments} students."),
        html.Li(f"{most_strand} is the most preferred strand with {most_strand_enrollments} enrollees."),
        html.Li(f"{least_region} has the lowest number of Senior High School enrollees, totaling {least_region_enrollments} students."),
        html.Li(f"{least_strand} is the least enrolled strand, with {least_strand_enrollments} enrollees."),
    ]

    recommendations = [
        html.Li(f"{most_strand} is the most chosen strand across almost all regions, making it the dominant preference."),
        html.Li(f"The government should strengthen {most_strand} by improving resources and infrastructure to support its growth."),
        html.Li(f"For {least_strand}, there's a need for promotion and better facilities to encourage students to choose it."),
    ]

    return insights, recommendations