import plotly.express as px
import pandas as pd
from dash import html

df = pd.read_csv('data/cleaned_data_v3.csv', dtype={'beis_school_id': str})
enrollee_columns = [col for col in df.columns if "_male" in col or "_female" in col]
df["total_enrollment"] = df[enrollee_columns].sum(axis=1)

# Additional Cleaning
df['sector'] = df['sector'].replace({'SUCsLUCs': 'State or Local UCs'})

# Filter out PSO rows
df = df[df['sector'] != 'PSO']

# Enrollment Calculation
enrollment_cols = df.loc[:, 'k_male':'g12_arts_female'].columns
df['total_enrollment'] = df[enrollment_cols].sum(axis=1)

# Group data
grouped_df = df.groupby(['region', 'sector'])['total_enrollment'].sum().reset_index()
enrollment_summary = df.groupby(['region', 'sector'])['total_enrollment'].sum().reset_index()

# Filter out PSO
filtered_enrollment_summary = enrollment_summary[
    ~enrollment_summary['sector'].str.contains("PSO", case=False, na=False)
]

# ITO PO ANG GAMITIN DAHIL NAKA DROP NA ANG PSO

# Custom colors
custom_colors = {
    "Public": "#004080",
    "Private": "#ff0000",
    "State or Local UCs": "#f0b50d"
}

# Filter out PSO
filtered_enrollment_summary = enrollment_summary[
    ~enrollment_summary['sector'].str.contains("PSO", case=False, na=False)
]

# Add custom data for hover
fig4 = px.bar(
    filtered_enrollment_summary,
    x='region',
    y='total_enrollment',
    color='sector',
    barmode='group',
    title='Enrollments in Public, Private, and State or Local UCs Schools',
    color_discrete_map=custom_colors,
    custom_data=['sector']  
)

# For hover template
fig4.update_traces(
    hovertemplate='<b>Sector:</b> %{customdata[0]}<br><b>Region:</b> %{x}<br><b>Total Enrollment:</b> %{y:,}<extra></extra>'
)

fig4.update_layout(
    width=850,
    title_x=0.46, title_y=0.95,
    title=dict(text='Enrollments in Public, Private, and State or Local UCs Schools',
               font=dict(size=18, family='Poppins', color='#444444', weight='bold')),
    legend_title=dict(text='School Type',
                      font=dict(size=14, family='Poppins', color='#444444', weight='bold')),
    legend=dict(itemclick="toggle", itemdoubleclick="toggleothers"),
    yaxis=dict(title=dict(text="Total Enrollment",
                          font=dict(size=14, family='Poppins', color='#444444', weight='bold')),
               autorange=True),
    xaxis=dict(title=dict(text="Regions",
                          font=dict(size=14, family='Poppins', color='#444444', weight='bold')),
               autorange=True),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)'
)


def school_type_per_region_insights(cleaned_df):
    if 'total_enrollment' not in cleaned_df.columns:
        enrollment_cols = cleaned_df.loc[:, 'k_male':'g12_arts_female'].columns
        cleaned_df['total_enrollment'] = cleaned_df[enrollment_cols].sum(axis=1)

    cleaned_df = cleaned_df[~cleaned_df['sector'].str.contains("PSO", case=False, na=False)]

    if 'sector' in cleaned_df.columns and 'region' in cleaned_df.columns:
        # Most and least common sector
        top_sector = cleaned_df['sector'].value_counts().idxmax()
        bottom_sector = cleaned_df['sector'].value_counts().idxmin()

        # Most and least populated region by total enrollment
        region_totals = cleaned_df.groupby('region')['total_enrollment'].sum()
        top_region = region_totals.idxmax()
        bottom_region = region_totals.idxmin()

        # UCs specifically
        uc_df = cleaned_df[cleaned_df['sector'].str.lower().str.contains("uc")]
        uc_region_max = uc_df.groupby('region')['total_enrollment'].sum().idxmax() if not uc_df.empty else "N/A"
        uc_region_min = uc_df.groupby('region')['total_enrollment'].sum().idxmin() if not uc_df.empty else "N/A"

        # Key Findings
        key_findings = [
            html.Li(f"{top_sector} schools have the highest enrollment across regions."),
            html.Li(f"{top_region} has the most students enrolled."),
            html.Li(f"{bottom_sector} has the fewest enrollments."),
            html.Li("Private schools are more concentrated in urban regions like NCR."),
            html.Li(f"State or Local UCs have the most enrollees in {uc_region_max}, and the fewest in {uc_region_min}."),
        ]

        # Recommendations
        recommendations = [
            html.Li(f"Expand infrastructure in {top_region} to support high enrollment."),
            html.Li(f"Allocate more resources to {bottom_region} to improve access."),
            html.Li(f"Support {top_sector} schools with funding and capacity-building."),
            html.Li(f"Investigate issues affecting {bottom_sector} schools and address them."),
            html.Li("Encourage public-private partnerships to enhance education reach."),
        ]

        return key_findings, recommendations

    return [], []
