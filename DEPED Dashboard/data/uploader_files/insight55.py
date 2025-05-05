import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

def generate_plot_gender_distribution(df):
    levels = {
        "Elementary School": {
            "Kindergarten": ["k_male", "k_female"],
            "Grade 1": ["g1_male", "g1_female"],
            "Grade 2": ["g2_male", "g2_female"],
            "Grade 3": ["g3_male", "g3_female"],
            "Grade 4": ["g4_male", "g4_female"],
            "Grade 5": ["g5_male", "g5_female"],
            "Grade 6": ["g6_male", "g6_female"],
            "Non-graded": ["elem_ng_male", "elem_ng_female"]
        },
        "Junior High School": {
            "Grade 7": ["g7_male", "g7_female"],
            "Grade 8": ["g8_male", "g8_female"],
            "Grade 9": ["g9_male", "g9_female"],
            "Grade 10": ["g10_male", "g10_female"],
            "Non-graded": ["jhs_ng_male", "jhs_ng_female"]
        },
        "Senior High School": {
            "HUMSS": ["g11_acad_-_humss_male", "g11_acad_-_humss_female", "g12_acad_-_humss_male", "g12_acad_-_humss_female"],
            "ABM": ["g11_acad_-_abm_male", "g11_acad_-_abm_female", "g12_acad_-_abm_male", "g12_acad_-_abm_female"],
            "STEM": ["g11_acad_stem_male", "g11_acad_stem_female", "g12_acad_stem_male", "g12_acad_stem_female"],
            "GAS": ["g11_acad_gas_male", "g11_acad_gas_female", "g12_acad_gas_male", "g12_acad_gas_female"],
            "TVL": ["g11_tvl_male", "g11_tvl_female", "g12_tvl_male", "g12_tvl_female"],
            "SPORTS": ["g11_sports_male", "g11_sports_female", "g12_sports_male", "g12_sports_female"],
            "ARTS": ["g11_arts_male", "g11_arts_female", "g12_arts_male", "g12_arts_female"],
            "PBM": ["g11_acad_pbm_male", "g11_acad_pbm_female", "g12_acad_pbm_male", "g12_acad_pbm_female"]
        }
    }

    fig = go.Figure()
    menu_buttons = []

    for level, categories in levels.items():
        totals = {}
        for category, columns in categories.items():
            if len(columns) == 2:
                male_total = df[columns[0]].sum()
                female_total = df[columns[1]].sum()
            else:
                male_total = df[columns[0]].sum() + df[columns[2]].sum()
                female_total = df[columns[1]].sum() + df[columns[3]].sum()
            totals[category] = {"Male": male_total, "Female": female_total, "Total": male_total + female_total}

        labels = list(categories.keys()) + ["Male", "Female", level]
        male_index = labels.index("Male")
        female_index = labels.index("Female")
        level_index = labels.index(level)

        source, target, values, link_tooltips, node_tooltips = [], [], [], [], []

        for category, counts in totals.items():
            node_tooltips.append(f"{category}: {counts['Total']}")
        node_tooltips.append(f"Total Male: {sum(totals[cat]['Male'] for cat in totals)}")
        node_tooltips.append(f"Total Female: {sum(totals[cat]['Female'] for cat in totals)}")
        node_tooltips.append(f"Overall Population in {level}: {sum(totals[cat]['Total'] for cat in totals)}")

        for category, counts in totals.items():
            category_index = labels.index(category)
            source.extend([category_index, category_index])
            target.extend([male_index, female_index])
            values.extend([counts["Male"], counts["Female"]])
            link_tooltips.append(f"Males in {category}: {counts['Male']}")
            link_tooltips.append(f"Females in {category}: {counts['Female']}")

        source.extend([male_index, female_index])
        target.extend([level_index, level_index])
        values.extend([
            sum(totals[cat]["Male"] for cat in totals),
            sum(totals[cat]["Female"] for cat in totals),
        ])
        link_tooltips.append(f"Total Count : {values[-2]}")
        link_tooltips.append(f"Total Count : {values[-1]}")

        fig.add_trace(go.Sankey(
            visible=(level == "Elementary School"),
            node=dict(
                pad=50,
                thickness=100,
                line=dict(color="black", width=1.5),
                label=labels,
                color=(["#e6f2ff"] * len(categories)) + ["#013A63", "#ff0000", "#e6f2ff"],
                customdata=node_tooltips,
                hovertemplate='%{customdata}<extra></extra>'
            ),
            link=dict(
                source=source,
                target=target,
                value=values,
                color=["#013A63" if i % 2 == 0 else "#ff0000" for i in range(len(values))],
                customdata=link_tooltips,
                hovertemplate='%{customdata}<extra></extra>'
            )
        ))

        menu_buttons.append(dict(
            label=level,
            method="update",
            args=[{"visible": [level == l for l in levels] + [False]}]
        ))

    # Overall Distribution
    total_male = df.filter(like='_male').sum().sum()
    total_female = df.filter(like='_female').sum().sum()
    total_students = total_male + total_female

    labels_overall = ["Male Students", "Female Students", "Total Students"]
    source_overall, target_overall, values_overall = [0, 1], [2, 2], [total_male, total_female]

    node_tooltips_overall = [
        f"Overall Male Population: {total_male}",
        f"Overall Female Population: {total_female}",
        f"Overall Student Population: {total_students}"
    ]
    link_tooltips_overall = [
        f"Male Students Count: {total_male}",
        f"Female Students Count: {total_female}"
    ]

    fig.add_trace(go.Sankey(
        visible=False,
        node=dict(
            pad=50,
            thickness=100,
            line=dict(color="black", width=1.5),
            label=labels_overall,
            color=["#013A63", "#ff0000", "#e6f2ff"],
            customdata=node_tooltips_overall,
            hovertemplate='%{customdata}<extra></extra>'
        ),
        link=dict(
            source=source_overall,
            target=target_overall,
            value=values_overall,
            color=["#013A63", "#ff0000"],
            customdata=link_tooltips_overall,
            hovertemplate='%{customdata}<extra></extra>'
        )
    ))

    # Add dropdown for "Overall"
    menu_buttons.append(dict(
        label="Overall Distribution",
        method="update",
        args=[{"visible": [False] * len(levels) + [True]}]
    ))

    # Updated Layout (match insight5)
    fig.update_layout(
        title_text="Gender-Based Student Enrollment per Curriculum Level",
        title_x=0.5,
        height=550,
        width=1100,
        font=dict(family="Poppins", size=12, color="#444444"),
        title_font=dict(family="Poppins", size=18, color="#444444", weight="bold"),
        margin=dict(l=100, r=60, t=80, b=50),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        updatemenus=[dict(
            buttons=menu_buttons,
            direction="down",
            showactive=True,
            x=0.5,
            y=1.07,
            xanchor="center",
            yanchor="top",
            bgcolor='white'
        )]
    )

    return fig
