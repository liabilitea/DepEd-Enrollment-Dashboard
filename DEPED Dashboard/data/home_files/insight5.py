import pandas as pd
import plotly.graph_objects as go
from dash import html
import re

df = pd.read_csv("data/cleaned_data - cleaned_data.csv")

# Define categories
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


fig5 = go.Figure()
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

    fig5.add_trace(go.Sankey(
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

# Add Overall Distribution
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

fig5.add_trace(go.Sankey(
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

# Add dropdown option for Overall Distribution
menu_buttons.append(dict(
    label="Overall Distribution",
    method="update",
    args=[{"visible": [False] * len(levels) + [True]}]
))

fig5.update_layout(
    title_text="Gender-Based Student Distribution per Curriculum",
    title_x=0.5,
    font=dict(
        family="Poppins",
        size=14,
        color="#444444"
    ),
    title_font=dict(
        family="Poppins",
        size=20,
        color="#444444",
        weight="bold"
    ),
    height=500, width=1300,
    margin=dict(l=150, r=150, t=120, b=50),
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    updatemenus=[dict(
        buttons=menu_buttons,
        direction="down",
        showactive=True,
        x=0.50,
        y=1.1,
        xanchor="center",
        yanchor="top", 
        bgcolor='white', 
        font=dict(size=14)
    )]
)


def format_grade_name(grade_code):
    if grade_code.startswith('g'):
        try:
            grade_num = int(grade_code[1:])
            return f"Grade {grade_num}"
        except ValueError:
            return grade_code.upper()
    elif grade_code == 'k':
        return "Kindergarten"
    else:
        return grade_code.upper()

def gender_level_insights(df):
    grade_totals = {}
    grade_regex = re.compile(r'^g\d+_male$|^g\d+_female$|^k_male$|^k_female$')
    for col in df.columns:
        if grade_regex.match(col):
            grade = col.split('_')[0]
            if grade not in grade_totals:
                grade_totals[grade] = 0
            grade_totals[grade] += df[col].sum()

    highest_grade_code = max(grade_totals, key=grade_totals.get)
    highest_grade = format_grade_name(highest_grade_code)
    highest_grade_enrollment = grade_totals[highest_grade_code]
    lowest_grade_code = min(grade_totals, key=grade_totals.get)
    lowest_grade = format_grade_name(lowest_grade_code)
    lowest_grade_enrollment = grade_totals[lowest_grade_code]

    strand_columns = {
        "HUMSS": ['g11_acad_-_humss_male', 'g11_acad_-_humss_female', 'g12_acad_-_humss_male', 'g12_acad_-_humss_female'],
        "ABM": ['g11_acad_-_abm_male', 'g11_acad_-_abm_female', 'g12_acad_-_abm_male', 'g12_acad_-_abm_female'],
        "STEM": ['g11_acad_stem_male', 'g11_acad_stem_female', 'g12_acad_stem_male', 'g12_acad_stem_female'],
        "GAS": ['g11_acad_gas_male', 'g11_acad_gas_female', 'g12_acad_gas_male', 'g12_acad_gas_female'],
        "TVL": ['g11_tvl_male', 'g11_tvl_female', 'g12_tvl_male', 'g12_tvl_female'],
        "SPORTS": ['g11_sports_male', 'g11_sports_female', 'g12_sports_male', 'g12_sports_female'],
        "ARTS": ['g11_arts_male', 'g11_arts_female', 'g12_arts_male', 'g12_arts_female'],
        "PBM": ['g11_acad_pbm_male', 'g11_acad_pbm_female', 'g12_acad_pbm_male', 'g12_acad_pbm_female']
    }

    strand_gender_ratios = {}
    for strand, cols in strand_columns.items():
        male_sum = df[[c for c in cols if c.endswith('_male')]].sum().sum()
        female_sum = df[[c for c in cols if c.endswith('_female')]].sum().sum()
        if female_sum == 0:
            strand_gender_ratios[strand] = "All Male"
        else:
            strand_gender_ratios[strand] = male_sum / female_sum

    non_graded_totals = {}
    non_graded_regex = re.compile(r'elem_ng|jhs_ng')
    for col in df.columns:
        if non_graded_regex.search(col):
            level = 'Elementary' if 'elem' in col else 'Junior High School'
            if level not in non_graded_totals:
                non_graded_totals[level] = 0
            non_graded_totals[level] += df[col].sum()

    non_graded_highest_level = max(non_graded_totals, key=non_graded_totals.get)

    level_totals = {
        "Elementary": df.filter(regex='^g[1-6]_male$|^k_male$|^elem_ng_male$').sum().sum() + df.filter(regex='^g[1-6]_female$|^k_female$|^elem_ng_female$').sum().sum(),
        "Junior High School": df.filter(regex='^g(7|8|9|10)_male$|^jhs_ng_male$').sum().sum() + df.filter(regex='^g(7|8|9|10)_female$|^jhs_ng_female$').sum().sum(),
        "Senior High School": df.filter(like='_male').filter(regex='^g1[1-2]|^g12').sum().sum() + df.filter(like='_female').filter(regex='^g1[1-2]|^g12').sum().sum()
    }
    total_elem = level_totals["Elementary"]
    total_jhs = level_totals["Junior High School"]

    level_enrollment_trend = "increase" if total_jhs > total_elem else "decrease"

    strand_percentages = {}
    total_shs_enrollment = sum(level_totals.values())
    for strand, cols in strand_columns.items():
        strand_total = df[cols].sum().sum()
        strand_percentages[strand] = (strand_total / total_shs_enrollment) * 100

    most_popular_strands = sorted(strand_percentages, key=strand_percentages.get, reverse=True)[:2]
    least_popular_strand = min(strand_percentages, key=strand_percentages.get)

    # Key Findings
    key_findings = [
        html.Li(f"{highest_grade} shows the highest enrollment among individual grades."),
        html.Li(f"{lowest_grade} has the lowest enrollment."),
        html.Li(f"The {most_popular_strands[0]} and {most_popular_strands[1]} strands are the most popular, accounting for {strand_percentages[most_popular_strands[0]] + strand_percentages[most_popular_strands[1]]:.2f}% of the SHS population."),
        html.Li(f"The {least_popular_strand} strand has the lowest enrollment."),
        html.Li(f"The {non_graded_highest_level} level has the highest number of non-graded students."),
        html.Li(f"There is an {level_enrollment_trend} in overall enrollment from Elementary to Junior High School."),
    ]

    # Recommendations
    recommendations = [
        html.Li(f"Investigate the reasons for the high enrollment in {highest_grade} and prepare resources accordingly."),
        html.Li(f"Develop strategies to increase enrollment in {lowest_grade}."),
        html.Li(f"Capitalize on the popularity of the {most_popular_strands[0]} and {most_popular_strands[1]} strands with enhanced resources and programs."),
        html.Li(f"Promote the {least_popular_strand} strand through targeted campaigns and resource allocation."),
        html.Li(f"Provide specialized support and resources for non-graded students, especially in the {non_graded_highest_level} level."),
        html.Li(f"Analyze the causes for the {level_enrollment_trend} from Elementary to Junior High School and implement appropriate interventions."),
    ]

    return key_findings, recommendations