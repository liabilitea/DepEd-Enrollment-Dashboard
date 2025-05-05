import pandas as pd
import plotly.express as px
import statsmodels.api as sm
from dash import html

# --- Load and preprocess data ---
df = pd.read_csv("data/cleaned_data_v3.csv")

# Sum all enrollment columns
enrollment_columns = [col for col in df.columns if 'male' in col or 'female' in col]
df['Total Enrollees'] = df[enrollment_columns].sum(axis=1)

# Group by province
province_summary = df.groupby('province').agg(
    Number_of_Schools=('school_name', 'count'),
    Total_Enrollees=('Total Enrollees', 'sum')
).reset_index()

# 🔧 Ensure numeric data types
province_summary["Number_of_Schools"] = pd.to_numeric(province_summary["Number_of_Schools"], errors="coerce")
province_summary["Total_Enrollees"] = pd.to_numeric(province_summary["Total_Enrollees"], errors="coerce")

# Remove rows with missing or invalid data
province_summary.dropna(subset=["Number_of_Schools", "Total_Enrollees"], inplace=True)

# --- Custom Colors ---
custom_colors = {
    "scatter_points": "#004080",
    "regression_line": "#FF0000",
    "confidence_band": "#E6F2FF",
    "residuals": "#F7B267",
    "background": "#FFFFFF",
    "grid": "#E6E6E6"
}

# --- FIG6: Compact version ---
fig6 = px.scatter(
    province_summary,
    x='Number_of_Schools',
    y='Total_Enrollees',
    trendline="ols",
    trendline_color_override=custom_colors["regression_line"],
    # Remove title from here
    labels={'Number_of_Schools': 'Number of Schools', 'Total_Enrollees': 'Total Enrollees'},
    hover_name='province'
)

fig6.update_layout(
    height=500, width=400,
    margin=dict(t=90, l=0, r=0, b=70),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title_x=0.5, title_y=0.95,
    # Set the title and its formatting properly
    title_text="Regression Analysis: Relationship<br>Number of Schools and Total Enrollees",
    title_font=dict(family="Poppins", size=18, color="#444444", weight="bold"),
    font=dict(family="Poppins")
)

fig6.update_traces(
    marker=dict(size=6.5, color=custom_colors["scatter_points"]),
    hovertemplate="<b>%{hovertext}</b><br>Number of Schools: %{x}<br>Total Enrollees: %{y:,}"
)

# --- FIG61: Mid-sized version ---
fig61 = px.scatter(
    province_summary, x='Number_of_Schools', y='Total_Enrollees',
    trendline="ols", trendline_color_override=custom_colors["regression_line"],
    labels={'Number_of_Schools': 'Number of Schools', 'Total_Enrollees': 'Total Enrollees'},
    hover_name='province'
)

fig61.update_layout(
    height=400, width=600,
    margin=dict(t=90, l=0, r=0, b=10),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    title_font=dict(size=18, family='Poppins', color='#141D43', weight='bold'),
    font=dict(size=10),
    title_text="<span style='color:#444444; font-family:Poppins;'><b>Regression Analysis: Relationship<br>Between Number of Schools and<br>Total Enrollees per Province</b></span>",
    title_x=0.5, title_y=0.95
)

fig61.update_traces(
    marker=dict(size=6.5, color=custom_colors["scatter_points"]),
    hovertemplate="<b>%{hovertext}</b><br><b>Number of Schools:</b> %{x}<br><b>Total Enrollees:</b> %{y:,}",
    text=None
)

# --- FIG62: mid Compact version ---
fig62 = px.scatter(
    province_summary,
    x='Number_of_Schools',
    y='Total_Enrollees',
    trendline="ols",
    trendline_color_override=custom_colors["regression_line"],
    title="Regression Analysis: Relationship Between Number of Schools and Total Enrollees per Province",
    labels={'Number_of_Schools': 'Number of Schools', 'Total_Enrollees': 'Total Enrollees'},
    hover_name='province'
)

fig62.update_layout(
    height=700, width=900,
    margin=dict(t=90, l=0, r=0, b=70),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title_x=0.5, title_y=0.95,
    title_font=dict(family="Poppins", size=18, color="#444444", weight="bold"),
    font=dict(family="Poppins"),
)

fig62.update_traces(
    marker=dict(size=6.5, color=custom_colors["scatter_points"]),
    hovertemplate="<b>%{hovertext}</b><br>Number of Schools: %{x}<br>Total Enrollees: %{y:,}"
)

# --- Insights Function ---
def regression_schools_enrollment_insights(province_summary):
    # Ensure data is numeric and clean
    province_summary = province_summary.copy()
    province_summary["Number_of_Schools"] = pd.to_numeric(province_summary["Number_of_Schools"], errors="coerce")
    province_summary["Total_Enrollees"] = pd.to_numeric(province_summary["Total_Enrollees"], errors="coerce")
    province_summary.dropna(subset=["Number_of_Schools", "Total_Enrollees"], inplace=True)

    # Check if data is empty
    if province_summary.empty:
        return (
            [html.Li("No data available for regression analysis.")],
            [html.Li("Please check your dataset for missing or invalid values.")]
        )

    # Proceed with regression analysis
    X = sm.add_constant(province_summary['Number_of_Schools'])
    y = province_summary['Total_Enrollees']
    model = sm.OLS(y, X).fit()

    slope = model.params['Number_of_Schools']
    intercept = model.params['const']
    r_squared = model.rsquared
    p_value = model.pvalues['Number_of_Schools']

    max_enroll = province_summary.loc[province_summary['Total_Enrollees'].idxmax()]
    min_enroll = province_summary.loc[province_summary['Total_Enrollees'].idxmin()]
    max_province = max_enroll.get('province', 'Unknown Province')
    min_province = min_enroll.get('province', 'Unknown Province')

    if r_squared >= 0.7:
        strength = "a very strong predictor"
        policy_implication = "School construction should be a primary focus for enrollment growth."
    elif r_squared >= 0.5:
        strength = "a moderately strong predictor"
        policy_implication = "School construction is important but should be combined with other initiatives."
    elif r_squared >= 0.3:
        strength = "a weak predictor"
        policy_implication = "School construction should be considered alongside other more impactful factors."
    else:
        strength = "a very weak predictor"
        policy_implication = "Other factors beyond school count should be prioritized in education planning."

    if slope > 1000:
        enrollment_impact = "dramatically increases"
        expansion_recommendation = "aggressive school construction"
    elif slope > 500:
        enrollment_impact = "significantly increases"
        expansion_recommendation = "substantial school expansion"
    elif slope > 200:
        enrollment_impact = "moderately increases"
        expansion_recommendation = "measured school expansion"
    else:
        enrollment_impact = "slightly increases"
        expansion_recommendation = "targeted school additions"

    findings = [
        html.Li(f"{max_province} has the highest enrollment with {max_enroll['Total_Enrollees']:,} students across {max_enroll['Number_of_Schools']} schools."),
        html.Li(f"{min_province} has the lowest enrollment with {min_enroll['Total_Enrollees']:,} students across {min_enroll['Number_of_Schools']} schools."),
        html.Li(f"Each additional school {enrollment_impact} enrollment by approximately {slope:.0f} students."),
        html.Li(f"The number of schools explains {r_squared:.1%} of enrollment variation, making it {strength} of enrollment numbers."),
        html.Li(f"The relationship is statistically {'significant' if p_value < 0.05 else 'not significant'} (p = {p_value:.3f}).")
    ]

    recommendations = [
        html.Li(f"{policy_implication}"),
        html.Li(f"Consider {expansion_recommendation} in provinces with growing populations."),
        html.Li(f"In high-enrollment provinces like {max_province}, focus on optimizing existing school capacity."),
        html.Li(f"In low-enrollment provinces like {min_province}, investigate other barriers to education access."),
        html.Li("Monitor other factors like population growth, economic conditions, and education quality that may affect enrollment.")
    ]

    return findings, recommendations
