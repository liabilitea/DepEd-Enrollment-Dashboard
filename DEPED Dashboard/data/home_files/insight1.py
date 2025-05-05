import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("data/cleaned_data - cleaned_data.csv")

df.drop(['street_address', 'barangay'], axis='columns', inplace=True)

# Create columns with combined enrollee count of each grade level
df['Kindergarten'] = df['k_male'] + df['k_female']
df['Grade 1'] = df['g1_male'] + df['g1_female']
df['Grade 2'] = df['g2_male'] + df['g2_female']
df['Grade 3'] = df['g3_male'] + df['g3_female']
df['Grade 4'] = df['g4_male'] + df['g4_female']
df['Grade 5'] = df['g5_male'] + df['g5_female']
df['Grade 6'] = df['g6_male'] + df['g6_female']
df['Grade 7'] = df['g7_male'] + df['g7_female']
df['Grade 8'] = df['g8_male'] + df['g8_female']
df['Grade 9'] = df['g9_male'] + df['g9_female']
df['Grade 10'] = df['g10_male'] + df['g10_female']
df['Grade 11'] = df['g11_acad_-_abm_male'] + df['g11_acad_-_abm_female'] + df['g11_acad_-_humss_male'] + df['g11_acad_-_humss_female'] + df['g11_acad_stem_male'] + df['g11_acad_stem_female'] + df['g11_acad_gas_male'] + df['g11_acad_gas_female'] + df['g11_acad_pbm_male'] + df['g11_acad_pbm_female'] + df['g11_tvl_male'] + df['g11_tvl_female'] + df['g11_sports_male'] + df['g11_sports_female'] + df['g11_arts_male'] + df['g11_arts_female']
df['Grade 12'] = df['g12_acad_-_abm_male'] + df['g12_acad_-_abm_female'] + df['g12_acad_-_humss_male'] + df['g12_acad_-_humss_female'] + df['g12_acad_stem_male'] + df['g12_acad_stem_female'] + df['g12_acad_gas_male'] + df['g12_acad_gas_female'] + df['g12_acad_pbm_male'] + df['g12_acad_pbm_female'] + df['g12_tvl_male'] + df['g12_tvl_female'] + df['g12_sports_male'] + df['g12_sports_female'] + df['g12_arts_male'] + df['g12_arts_female']
df['Non-graded'] = df['elem_ng_male'] + df['elem_ng_female'] + df['jhs_ng_male'] + df['jhs_ng_female']

region = df['region']
grade_lvl = ['Kindergarten', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
       'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12', 'Non-graded']

regions = ['All Regions'] + sorted(df['region'].unique().tolist())

# Adding interactivity by creating a dropdown menu for selecting a region
buttons = []
grouped_data = df.groupby('region')[grade_lvl].sum() # Enrollment calculation

def get_data(region):
    if region == 'All Regions':
        return grouped_data, grouped_data.index.tolist()
    else:
        return grouped_data.loc[[region]], [region]

for region in regions:
    data, y_values = get_data(region)
    buttons.append({
        'label': region,
        'method': 'update',
        'args': [{'z': [data.values], 'y': [y_values]},
                 {'title': f"Student Enrollment by Grade Level ({region})"}]
    })

custom_colors = [
    "#013A63",  # Deep navy blue
    "#004080",  # Dark blue
    "#3A7F97",  # Muted teal
    "#7FB3D5",  # Medium-light blue
    "#E6F2FF",  # Light blue (midpoint)
    "#FFD6D6",  # Soft pink
    "#FF9999",  # Light red
    "#FF4C4C",  # Bright red-orange
    "#FF0000"   # Bold red (max intensity)
]

# Initial figure to show all regions
data, y_values = get_data('All Regions')
fig1 = px.imshow(data, aspect="auto", color_continuous_scale=custom_colors)

# Chart layout
fig1.update_layout( 
    title=dict(text='Student Enrollment by Region and Grade Level', 
               font=dict(size=18, family='Poppins', color='#444444', weight='bold')),
    title_x=0.5, title_y=0.95,
    height=550,
    width=900,  # Added margin control
    margin=dict(l=100, r=100, t=100, b=100),
    coloraxis_colorbar=dict(
        title="Number of<br>Enrollees",
        len=0.8,  # Make colorbar shorter
        y=0.5,    # Center colorbar
        yanchor="middle",
        thickness = 4
    ), 
    font=dict(
        size=10, family='Poppins'
    ),
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        "x": 0.5,
        "xanchor": "center",
        "y": 1.13,  # Adjusted dropdown position
        "yanchor": "top",
        'bgcolor': "white"
    }], 
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)'
)

fig1.update_xaxes(title_text="<b>Grade Level</b>")
fig1.update_yaxes(title_text="<b>Region</b>")
fig1.update_traces(hovertemplate="Grade Level: %{x}<br>Region: %{y}<br>Number of Enrollees: %{z}<extra></extra>")

# For school information
fig12 = px.imshow(data, aspect="auto", color_continuous_scale=px.colors.sequential.tempo)
fig12.update_layout(
    title=dict(
        text='Student Enrollment by Region and Grade Level',
        font=dict(size=18, family='Poppins', color='#444444', weight='bold')
    ),
    title_x=0.5,
    title_y=0.95,
    height=600,
    width=900,
    margin=dict(l=100, r=100, t=100, b=100),
    coloraxis_colorbar=dict(
        title="Number of<br>Enrollees",
        len=0.8,
        y=0.5,
        yanchor="middle",
        thickness=4
    ),
    font=dict(
        size=10, family='Poppins'
    ),
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'showactive': True,
        "x": 0.5,
        "xanchor": "center",
        "y": 1.13,
        "yanchor": "top",
        'bgcolor': "white"
    }],
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)'
)

# Update axes and hover
fig12.update_xaxes(title_text="<b>Grade Level</b>")
fig12.update_yaxes(title_text="<b>Region</b>")
fig12.update_traces(
    hovertemplate="Grade Level: %{x}<br>Region: %{y}<br>Number of Enrollees: %{z}<extra></extra>"
)
    
def enrollment_per_region_insights(df):
    if 'region' in df.columns:
        # Check if grade level columns exist, create them if they don't
        if 'Kindergarten' not in df.columns:
            df['Kindergarten'] = df['k_male'] + df['k_female']
            df['Grade 1'] = df['g1_male'] + df['g1_female']
            df['Grade 2'] = df['g2_male'] + df['g2_female']
            df['Grade 3'] = df['g3_male'] + df['g3_female']
            df['Grade 4'] = df['g4_male'] + df['g4_female']
            df['Grade 5'] = df['g5_male'] + df['g5_female']
            df['Grade 6'] = df['g6_male'] + df['g6_female']
            df['Grade 7'] = df['g7_male'] + df['g7_female']
            df['Grade 8'] = df['g8_male'] + df['g8_female']
            df['Grade 9'] = df['g9_male'] + df['g9_female']
            df['Grade 10'] = df['g10_male'] + df['g10_female']
            df['Grade 11'] = df['g11_acad_-_abm_male'] + df['g11_acad_-_abm_female'] + df['g11_acad_-_humss_male'] + df['g11_acad_-_humss_female'] + df['g11_acad_stem_male'] + df['g11_acad_stem_female'] + df['g11_acad_gas_male'] + df['g11_acad_gas_female'] + df['g11_acad_pbm_male'] + df['g11_acad_pbm_female'] + df['g11_tvl_male'] + df['g11_tvl_female'] + df['g11_sports_male'] + df['g11_sports_female'] + df['g11_arts_male'] + df['g11_arts_female']
            df['Grade 12'] = df['g12_acad_-_abm_male'] + df['g12_acad_-_abm_female'] + df['g12_acad_-_humss_male'] + df['g12_acad_-_humss_female'] + df['g12_acad_stem_male'] + df['g12_acad_stem_female'] + df['g12_acad_gas_male'] + df['g12_acad_gas_female'] + df['g12_acad_pbm_male'] + df['g12_acad_pbm_female'] + df['g12_tvl_male'] + df['g12_tvl_female'] + df['g12_sports_male'] + df['g12_sports_female'] + df['g12_arts_male'] + df['g12_arts_female']
            df['Non-graded'] = df['elem_ng_male'] + df['elem_ng_female'] + df['jhs_ng_male'] + df['jhs_ng_female']

        grouped = df.groupby('region')[
            ['Kindergarten', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5',
             'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11',
             'Grade 12', 'Non-graded']
        ].sum()

        # Total enrollment per region
        total_enrollment = grouped.sum(axis=1)

        # Exclude PSO from insights
        filtered_enrollment = total_enrollment[total_enrollment.index != 'PSO']

        top_region = filtered_enrollment.idxmax()
        bottom_region = filtered_enrollment.idxmin()

        # Check dropout patterns from early to senior high school
        dropout_region = grouped.apply(
            lambda row: row['Kindergarten'] + row['Grade 1'] - row['Grade 11'] - row['Grade 12'], axis=1
        )
        dropout_region = dropout_region.drop(labels='PSO', errors='ignore')
        highest_dropout_region = dropout_region.idxmax()

        key_findings = [
            html.Li(f"{top_region} has the highest student enrollment across all grade levels."),
            html.Li(f"{bottom_region} has the fewest students enrolled."),
            html.Li(f"{highest_dropout_region} shows a noticeable drop in enrollment from early to senior high school."),
            html.Li(f"'Non-graded' enrollment remains low, reflecting the need for more inclusive education.")
        ]

        recommendations = [
            html.Li(f"Expand senior high access in {highest_dropout_region} to reduce dropouts."),
            html.Li(f"Provide more access to basic education in {bottom_region}."),
            html.Li(f"Expand educational programs and support in {top_region} to meet growing demand."),
            html.Li("Prioritize support and inclusion for 'Non-graded' learners."),
        ]

        return key_findings, recommendations
    else:
        return [], []