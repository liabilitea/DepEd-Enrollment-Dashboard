import plotly.express as px
import pandas as pd
from dash import dcc, html
import plotly.graph_objs as go

def generate_plot_sector_enrollment(df):
    """
    Generates a grouped bar chart of total student enrollment by region and sector
    with updated layout to match the dashboard version used in insight4.
    """
    # Work on a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Data Cleaning
    if 'sector' in df.columns:
        df['sector'] = df['sector'].replace({'SUCsLUCs': 'State or Local UCs'})
        df = df[df['sector'] != 'PSO']

    # Calculate total enrollment if columns exist
    if 'k_male' in df.columns and 'g12_arts_female' in df.columns:
        enrollment_cols = df.loc[:, 'k_male':'g12_arts_female'].columns
        df['total_enrollment'] = df[enrollment_cols].sum(axis=1)

    # Group by region and sector
    enrollment_summary = df.groupby(['region', 'sector'], as_index=False)['total_enrollment'].sum()

    # Define consistent custom colors for sectors (matching insight4)
    custom_colors = {
        "Public": "#004080",
        "Private": "#ff0000",
        "State or Local UCs": "#f0b50d"
    }

    # Create bar chart
    fig = px.bar(
        enrollment_summary,
        x='region',
        y='total_enrollment',
        color='sector',
        barmode='group',
        title='Enrollments in Public, Private, and State or Local UCs Schools',
        color_discrete_map=custom_colors,
        custom_data=['sector']  
    )

    # For hover template
    fig.update_traces(
        hovertemplate='<b>Sector:</b> %{customdata[0]}<br><b>Region:</b> %{x}<br><b>Total Enrollment:</b> %{y:,}<extra></extra>'
    )

    # Update layout to exactly match insight4
    fig.update_layout(
        width=850,
        title=dict(
            text='Enrollments in Public, Private, and State or Local UCs Schools',
            font=dict(size=18, family='Poppins', color='#444444', weight='bold'),
            x=0.5, y=0.95
        ),
        legend_title=dict(
            text='School Type',
            font=dict(size=14, family='Poppins', color='#444444', weight='bold')
        ),
        legend=dict(
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
        yaxis=dict(
            title=dict(
                text="Total Enrollment",
                font=dict(size=14, family='Poppins', color='#444444', weight='bold')
            ),
            autorange=True
        ),
        xaxis=dict(
            title=dict(
                text="Regions",
                font=dict(size=14, family='Poppins', color='#444444', weight='bold')
            ),
            autorange=True
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 100},
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
    )

    return fig
