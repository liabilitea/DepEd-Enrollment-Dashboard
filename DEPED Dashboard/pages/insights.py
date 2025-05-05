import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html
from data.home_files.insight1 import fig1
from data.home_files.insight2 import fig2
from data.home_files.insight3 import fig3
from data.home_files.insight4 import fig4
from data.home_files.insight5 import fig5
from data.home_files.insight6 import fig61

# Create Dash application
app = dash.Dash(__name__, suppress_callback_exceptions=True)

df = pd.read_csv("data/cleaned_data - cleaned_data.csv")

# Page 1 Layout
def layout():
    return html.Div(children=[
        # Title and Key Metrics
        html.Div(html.H1("INSIGHTS"), className="insights-div1"),
        
        # Key Statistics Cards
        html.Div([
            dcc.Graph(figure=fig1),
            html.Div(children=
                [
                    html.P("The enrollment data shows a significantly higher student enrollment count in Region IV-A (CALABARZON), followed by NCR (National Capital Region), and Region III (Central Luzon) across all grade levels, likely due to their large populations and well-developed school infrastructures. While smaller regions such as CAR (Cordillera Administrative Region) and BARMM (Bangsamoro Autonomous Region in Muslim Mindanao) show considerably lower enrollments, which may be attributed to smaller student populations, geographic challenges, or limited school availability."),
                    html.P("The number of enrollees in urban regions such as NCR and Region IV-A tend to be more consistent across all grade levels, while rural areas (i.e. BARMM, CAR, CARAGA, and MIMAROPA) indicate a relatively steady distribution in early education but experience a decline in higher grades. This suggests dropout possibilities due to economic factors or students moving out to urban areas to pursue higher education. In addition, the Non-graded category has significantly fewer enrollees, which includes students in special education. While PSO indicates the number of enrollees outside the country."),
                    html.P("Regions that show a decline of enrollees in higher grade levels may require more infrastructures to support higher education. The enrollment data shows rural areas need to have more accessible schools that offer senior high school programs. While the more concentrated areas, mainly NCR and Region IV-A, call for additional resources and subsidiaries to ensure quality education."),
                ], style={'width': '75%', 'text-align': 'justify'}
            )
        ], className="insights-div2"), 
        
        html.Div([dcc.Graph(figure=fig2),
            html.Div(children=
                [
                    html.P("The enrollment data highlights that Region IV-A CALABARZON has the highest number of Senior High School enrollees in both Grade 11 and Grade 12 with HUMSS being the most preferred strand. Following closely is NCR, where STEM has the highest number of enrollees among the strands."),
                    html.P("Moreover, HUMSS appears to be the most chosen strand across almost all regions, making it the dominant preference for Senior High School students. Given its popularity, the government should further strengthen this strand by improving resources and building more infrastructure to support its growth."),
                    html.P("On the other hand, SPORTS is the least enrolled strand in Senior High School. This suggests that DepEd should promote this strand more actively and invest in better facilities to encourage students to consider it as an option."),
                    html.P("The data emphasizes the need for targeted improvements in Senior High School education. With HUMSS leading in enrollment, enhancing its facilities and support systems should be a priority. Meanwhile, efforts should be made to increase awareness and accessibility of under-enrolled strands like SPORTS to provide students with more balanced opportunities across different fields."),
                ], style={'width': '75%', 'text-align': 'justify'}
            )
        ], className="insights-div3"), 
        
        html.Div([dcc.Graph(figure=fig3),
            html.Div(children=
                [
                    html.P("In this map plot, upon seeing the default option of schools offering “Purely ES” in the national regions, Region VI shows the most number of schools, indicating that rural areas tend to build institutions limitied to elementary students only, probably due to limited resources. On the contrary, NCR has the least amount of schools, showing how urbanized areas have limited spaces, hence, majority of them offer a complete K-12 program to maximize land use."),
                    html.P("As for the schools that completely offer the K-12 program, Region IV-A shows the highest count, showing that institutions have better access to resources to accommodate the population density of the area. Whereas, rural regions like CAR and MIMAROPA have the least number of schools, indicating that these areas face challenges such as limited infrastructure and fewer opportunities. For the PSO, Saudi Arabia has the most schools that provide the complete offering for Filipino students abroad."),
                    html.P("For the data that shows the areas that cater to the special needs, there is a significant number of schools in Region IX that implement the curriculum designed for these students. While BARMM has the fewest schools, this indicates that it poses a serious challenge for individuals with special needs, as it may prevent them from receiving the support they need."),
                    html.P("This data shows how fewer educational institutions remain one of the factors that limit Filipino students from receiving the proper education they need. With rural areas receiving the least support from the government due to a lack of infrastructure, people in these areas are also more likely to suffer from the lack of access to quality education, limiting their opportunities for academic and professional growth."),
                ], style={'width': '75%', 'text-align': 'justify'}
            )
        ], className="insights-div4"), 
        
        html.Div([
            dcc.Graph(figure=fig4),
            html.Div(children=
                [
                    html.P("The enrollment data shows that Public Schools have the highest number of students in most regions, making them the primary choice for education. Region IV-A (CALABARZON) has the highest total enrollments across all school types, likely due to its large population and urban centers. In contrast, CAR (Cordillera Administrative Region) and CARAGA have the lowest enrollment numbers, which may indicate a smaller student population or limited school availability."),
                    html.P("Among school types, Public Schools consistently have the highest number of enrollees, especially in regions like Region IV-A and Region III (Central Luzon). Private Schools are more concentrated in urban areas, particularly in NCR (National Capital Region), where families have more options for education. State or Local Universities and Colleges (UCs) have significantly fewer enrollments than Public Schools, with BARMM (Bangsamoro Autonomous Region in Muslim Mindanao) having the highest number of State or Local UCs enrollees, while CARAGA has the least."),
                    html.P("Regions with lower enrollments, like CAR and CARAGA, may require additional resources, such as more schools or improved access to education. On the other hand, highly populated regions like Region IV-A and NCR may need better infrastructure and funding to accommodate the large number of students. The data highlights the importance of balancing school distribution to ensure that education is accessible to all students across different regions.")
                ], style={'width': '75%', 'text-align': 'justify'}
            )
        ], className="insights-div5"), 
        
        html.Div([
            dcc.Graph(figure=fig5),
            html.Div(children=
                [
                    html.P("The Sankey diagram offers a clear, visual representation of how students are distributed across different educational curriculum—Elementary, Junior High School, and Senior High School—and breaks it down further by gender. It shows the decline in enrollment as students move up through the educational levels. The data also highlights which academic tracks are most popular, with the Technical-Vocational-Livelihood (TVL) strand leading in Senior High School enrollment, followed by the STEM (Science, Technology, Engineering, and Mathematics) track. Gender differences also stand out, with Female students generally enrolling more in academic strands like HUMSS (Humanities and Social Sciences) and ABM (Accountancy, Business, and Management), while Male students tend to dominate the STEM and TVL strands."),
                    html.P("Overall, this data provides a clear overview of student distribution across grade levels, academic preferences, and gender, offering valuable insights into current enrollment trends and the choices students are making in their educational journeys."),    
                ], style={'width': '75%', 'text-align': 'justify'}
            )
        ], className="insights-div6"),
        
        html.Div([
            dcc.Graph(figure=fig61),
            html.Div(children=
                [
                    html.P("Based on the scatter plot, it shows that as the number of school increases in a province, student enrollment also tends to increase. Thus, on average, each new/additional school rise enrollment by 523 students."),
                    html.P("The high variation (70.7%) in enrollment tells that the number of schools is a significant predictor of student enrollment however it is not the only factor at play as enrollment can also be affected by population growth, education policies, economic condition, and school accessibility."),
                    html.P("Therefore, expanding or building more schools is an effective way to increase the number of students, however the Department of Education should also address other factors such as population growth, and economic conditions to ensure the sustainable growth in enrollment.")
                ], style={'width': '75%', 'text-align': 'justify'}
            )
        ], className="insights-div7"),
        
    ], className="insights-parent")

