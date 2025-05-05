import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

def generate_plot(df):
    df_processed = df.copy()
    df_processed.drop(['street_address', 'barangay'], axis='columns', inplace=True, errors='ignore')

    # Create columns with combined enrollee count of each grade level
    df_processed['Kindergarten'] = df_processed.get('k_male', 0) + df_processed.get('k_female', 0)
    df_processed['Grade 1'] = df_processed.get('g1_male', 0) + df_processed.get('g1_female', 0)
    df_processed['Grade 2'] = df_processed.get('g2_male', 0) + df_processed.get('g2_female', 0)
    df_processed['Grade 3'] = df_processed.get('g3_male', 0) + df_processed.get('g3_female', 0)
    df_processed['Grade 4'] = df_processed.get('g4_male', 0) + df_processed.get('g4_female', 0)
    df_processed['Grade 5'] = df_processed.get('g5_male', 0) + df_processed.get('g5_female', 0)
    df_processed['Grade 6'] = df_processed.get('g6_male', 0) + df_processed.get('g6_female', 0)
    df_processed['Grade 7'] = df_processed.get('g7_male', 0) + df_processed.get('g7_female', 0)
    df_processed['Grade 8'] = df_processed.get('g8_male', 0) + df_processed.get('g8_female', 0)
    df_processed['Grade 9'] = df_processed.get('g9_male', 0) + df_processed.get('g9_female', 0)
    df_processed['Grade 10'] = df_processed.get('g10_male', 0) + df_processed.get('g10_female', 0)
    df_processed['Grade 11'] = df_processed.get('g11_acad_-_abm_male', 0) + df_processed.get('g11_acad_-_abm_female', 0) + \
                               df_processed.get('g11_acad_-_humss_male', 0) + df_processed.get('g11_acad_-_humss_female', 0) + \
                               df_processed.get('g11_acad_stem_male', 0) + df_processed.get('g11_acad_stem_female', 0) + \
                               df_processed.get('g11_acad_gas_male', 0) + df_processed.get('g11_acad_gas_female', 0) + \
                               df_processed.get('g11_acad_pbm_male', 0) + df_processed.get('g11_acad_pbm_female', 0) + \
                               df_processed.get('g11_tvl_male', 0) + df_processed.get('g11_tvl_female', 0) + \
                               df_processed.get('g11_sports_male', 0) + df_processed.get('g11_sports_female', 0) + \
                               df_processed.get('g11_arts_male', 0) + df_processed.get('g11_arts_female', 0)
    df_processed['Grade 12'] = df_processed.get('g12_acad_-_abm_male', 0) + df_processed.get('g12_acad_-_abm_female', 0) + \
                               df_processed.get('g12_acad_-_humss_male', 0) + df_processed.get('g12_acad_-_humss_female', 0) + \
                               df_processed.get('g12_acad_stem_male', 0) + df_processed.get('g12_acad_stem_female', 0) + \
                               df_processed.get('g12_acad_gas_male', 0) + df_processed.get('g12_acad_gas_female', 0) + \
                               df_processed.get('g12_acad_pbm_male', 0) + df_processed.get('g12_acad_pbm_female', 0) + \
                               df_processed.get('g12_tvl_male', 0) + df_processed.get('g12_tvl_female', 0) + \
                               df_processed.get('g12_sports_male', 0) + df_processed.get('g12_sports_female', 0) + \
                               df_processed.get('g12_arts_male', 0) + df_processed.get('g12_arts_female', 0)
    df_processed['Non-graded'] = df_processed.get('elem_ng_male', 0) + df_processed.get('elem_ng_female', 0) + \
                                 df_processed.get('jhs_ng_male', 0) + df_processed.get('jhs_ng_female', 0)

    grade_lvl = ['Kindergarten', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5',
                 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11',
                 'Grade 12', 'Non-graded']

    regions = ['All Regions'] + sorted(df_processed['region'].unique().tolist())

    buttons = []
    grouped_data = df_processed.groupby('region')[grade_lvl].sum()

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

    data, y_values = get_data('All Regions')

    custom_colors = [
        "#013A63", "#004080", "#3A7F97", "#7FB3D5", "#E6F2FF",
        "#FFD6D6", "#FF9999", "#FF4C4C", "#FF0000"
    ]

    fig = px.imshow(data, aspect="auto", color_continuous_scale=custom_colors)

    fig.update_layout(
        title=dict(
            text='Student Enrollment by Region and Grade Level',
            font=dict(size=18, family='Poppins', color='#444444', weight='bold')
        ),
        title_x=0.5,
        title_y=0.95,
        height=550,
        width=900,
        margin=dict(l=100, r=100, t=100, b=100),
        coloraxis_colorbar=dict(
            title="Number of<br>Enrollees",
            len=0.8,
            y=0.5,
            yanchor="middle",
            thickness=4
        ),
        font=dict(size=10, family='Poppins'),
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

    fig.update_xaxes(title_text="<b>Grade Level</b>")
    fig.update_yaxes(title_text="<b>Region</b>")
    fig.update_traces(
        hovertemplate="Grade Level: %{x}<br>Region: %{y}<br>Number of Enrollees: %{z}<extra></extra>"
    )

    return fig
