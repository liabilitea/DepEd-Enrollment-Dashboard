import pandas as pd
import plotly.express as px
from dash import dcc, html

def generate_plot_school_enrollment_regression(df):
    """
    Generates a scatter plot with a linear regression line showing the
    relationship between the number of schools and the total number of
    enrollees per province. Styled to match the layout from insight6 (fig61).
    """
    df_processed = df.copy()

    # Sum all enrollment columns
    enrollment_columns = [col for col in df_processed.columns if 'male' in col or 'female' in col]
    df_processed['Total Enrollees'] = df_processed[enrollment_columns].sum(axis=1)

    # Aggregate the data by province
    province_summary = df_processed.groupby('province').agg(
        Number_of_Schools=('school_name', 'count'),
        Total_Enrollees=('Total Enrollees', 'sum')
    ).reset_index()

    # Custom Color Palette
    custom_colors = {
        "scatter_points": "#004080",     # Navy blue for data points
        "regression_line": "#FF0000",    # Red for regression line
        "confidence_band": "#E6F2FF",    # Light blue (if used for shading)
        "residuals": "#F7B267",          # Warm gold (optional)
        "background": "#FFFFFF",         # Background color
        "grid": "#E6E6E6"                # Grid line color
    }

    # Create the scatter plot with regression line
    fig = px.scatter(
        province_summary,
        x='Number_of_Schools',
        y='Total_Enrollees',
        trendline="ols",
        trendline_color_override=custom_colors["regression_line"],
        title="Regression Analysis: Relationship Between Number of Schools and Total Enrollees per Province",
        labels={'Number_of_Schools': 'Number of Schools', 'Total_Enrollees': 'Total Enrollees'},
        hover_name='province'
    )

    # Match layout and style with insight6 fig61
    fig.update_layout(
        height=500,
        width=400,
        margin=dict(t=90, l=0, r=0, b=10),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        title_font=dict(
            size=18, family='Poppins', color='#141D43', weight='bold'
        ),
        font=dict(
            size=10, family='Poppins'
        ),
        title_text="<span style='color:#444444; font-family:Poppins;'><b>Regression Analysis: Relationship<br>Between Number of Schools and<br>Total Enrollees per Province</b></span>",
        title_x=0.5,
        title_y=0.95
    )

    # Style the data points and hover
    fig.update_traces(
        marker=dict(size=6.5, color=custom_colors["scatter_points"]),
        hovertemplate="<b>%{hovertext}</b><br><b>Number of Schools:</b> %{x}<br><b>Total Enrollees:</b> %{y:,}",
        text=None
    )

    return fig
