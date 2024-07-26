import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import json
from dash import html
import plotly.graph_objects as go


attendant_stat = './caching/attendant_stat.csv'

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# ________________________________________________________
#                                                         |
#                   DATA PREPERATION SECTION              |
# ________________________________________________________|

# load provinces 
with open('./caching/province.json', 'r', encoding='utf-8') as json_file:
    provinces = json.load(json_file)
json_file.close()
provinces['00'] = 'Cả nước'

# load caching stat about participation
with open('./caching/attendant_stat.json', 'r', encoding='utf-8') as json_file:
    attendant_stat = json.load(json_file)
json_file.close()

# load caching stat score distribution
with open('./caching/score_distribution_stat.json', 'r', encoding='utf-8') as json_file:
    score_distribution_stat = json.load(json_file)
json_file.close()


# ________________________________________________________
#                                                         |
#          SUPPORT FUNCTION AND VARIABLES SECTION         |
# ________________________________________________________|
def find_attendant_stat_by_province(province_code):
    result = next((item for item in attendant_stat if item['province_code'] == province_code), None)
    return result

def find_score_distribution_stat_by_province(province_code):
    result = next((item for item in score_distribution_stat if item['province_code'] == province_code), None)
    return result

name_conversion = {
    'toan': 'Toán',
    'van': 'Ngữ Văn',
    'ngoaiNgu': 'Ngoại Ngữ',
    'vatLy': 'Vật Lý',
    'hoaHoc': 'Hóa Học',
    'sinhHoc': 'Sinh Học',
    'lichSu': 'Lịch Sử',
    'diaLy': 'Địa Lý',
    'gdcd': 'Giáo dục Công dân'
}

# ________________________________________________________
#                                                         |
#                   GRAPH PLOTTING SECTION                |
# ________________________________________________________|

# function to create donut chart
def create_donut_chart(province_code):
    attendant_stat = find_attendant_stat_by_province(province_code)
    labels = ['KHTN', 'KHXH', 'Cả 2 tổ hợp', 'Thí sinh tự do']
    values = [attendant_stat['science'], attendant_stat['social'], attendant_stat['both'], \
        attendant_stat['independent']]
           
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(
        showlegend=True,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#d0d0e1',
        height=200
    )

    fig.update_traces(
        textinfo='percent'
    )
    
    return fig

def create_bar_chart(province_score_distribution, subject):
    province_code = province_score_distribution['province_code']
    categories = province_score_distribution[subject]['score']
    values = province_score_distribution[subject]['count']

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(name='score_distribution', x=categories, y=values)
    ])

    # Customize the layout
    fig.update_layout(
        title='Phổ điểm môn ' + name_conversion[subject] + ' ' + \
            provinces[province_code],
        xaxis_title='Điểm số',
        yaxis_title='Số lượng thí sinh'
    )

    return fig

def create_score_distribution_figures(pCode):
    score_distribution = find_score_distribution_stat_by_province(pCode)
    subjects = [k for k in score_distribution_stat[0].keys() if k != 'province_code']
    charts = []
    for i in range(9):
        charts.append(
            html.Div([
                dcc.Graph(
                    id=f"{subjects[i]}_score_distribution_{pCode}",
                    figure=create_bar_chart(score_distribution, subjects[i]),
                    config={'responsive': False},
                    style={
                        'width': '100%', 
                        'height': '400px', 
                        'background-color': '#d0d0e1', 
                        'border-radius': '30px',
                        'padding': '0', 
                        'margin': '0'}
                ),
            ], style={'width': '33.33%', 'padding': '10px', 'box-sizing': 'border-box'})
        )

    return charts


# ________________________________________________________
# |                                                       |
# |                 CSS LAYOUT SECTION                    |
# |_______________________________________________________|
attendant_stat_layout = {
            'display': 'inline-block', 
            'width': '23%', 
            'height': '250px',
            'background-color': '#d0d0e1', 
            'padding': '10px', 
            'border-radius': '30px',
            'margin': '10px',
            'margin-top': '0px'
        }

attendant_key_index_layout = {
                'text-align': 'center', 
                'vertical-align': 'middle',
                'horizontal-align': 'middle',
                'color': 'red',
                'font-family': 'Arial',  
                'font-size': '60px',
                'padding-bottom': '10px',
                'margin-top': '20px'  # Adjusted position
            }

attendant_title_layout = {
    'text-align': 'center', 
                'vertical-align': 'middle',
                'color': 'black',
                'font-family': 'Arial',  
                'font-size': '25px'
}

# ________________________________________________________
#                                                         |
#            APPLICATION (HTML) LAYOUT SECTION            |
# ________________________________________________________|

app.layout = html.Div([
    # Title
    html.H1("Thống kê kỳ thi THPT 2018".upper(), style={
        'text-align': 'center', 
        'color': 'white', 
        'font-family': 'Arial', 
        'background-color': '#3498db', 
        'font-size': '50px',
        'padding': '20px', 
        'margin': '10px',
        'border-radius': '20px'
    }),

    # Search box
    html.Div([
        dcc.Dropdown(
            id='select-province',
            options=[{'label': v, 'value': k} for k, v in provinces.items()],
            placeholder='Chọn địa phương',
            style={
                'display': 'inline-block',
                'width': '100%',  # Increased width
                'margin-right': '10px',
                'height': '40px'
            }
        ),
        html.Button('🔍', id='submit-button', n_clicks=0, style={
            'display': 'inline-block',
            'vertical-align': 'right',
            'height': '38px',
            'width': '38px',
            'border-radius': '5px',
            'background-color': '#3498db',
            'color': 'white',
            'border': 'none',
            'cursor': 'pointer'
        }),

        # province display box
        html.H3(children="Cả nước", id='province-name', style={
            'display': 'inline-block',
            'text-align': 'center',
            'margin-left': '10px',
            'vertical-align': 'middle',
            'background-color': '#8080ff', 
            'font-family': 'Arial',
            'font-size': '25px',
            'padding': '15px', 
            'margin': '10px',
            'border-radius': '20px',
            'color': 'white',
            'width': '60%'  # Adjusted width
        }),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),
    html.Div(id='selected-value', style={'margin-top': '10px'}),
    
    # Attendance statistic boxes
    html.Div([
        # Show expected participants
        html.Div([  
            html.H2("Tổng số thí sinh đăng ký".upper(), style=attendant_title_layout),
            html.H3(id="expect_attendants", 
                    children=str(find_attendant_stat_by_province('00')['expected']),
                    style=attendant_key_index_layout),
        ], style=attendant_stat_layout),

        # Show actual participants
        html.Div([
            html.H2(["Tổng số bài thi".upper(), html.Br(), "ghi nhận".upper()], style=attendant_title_layout),
            html.H3(id="actual_attendants", 
                    children=find_attendant_stat_by_province('00')['actual'], 
                    style=attendant_key_index_layout),
        ], style=attendant_stat_layout),

        # Show participation rate
        html.Div([
            html.H2("Tỷ lệ tham dự".upper(), style=attendant_title_layout),
            html.H3(id="participation_percentage", 
                    children=find_attendant_stat_by_province('00')['participation_percentage'], 
                    style={**attendant_key_index_layout, 'margin-top': '50px'}),
        ], style=attendant_stat_layout),

        # Category
        html.Div([
            html.H2("Phân loại".upper(), style=attendant_title_layout),
            dcc.Graph(
                id="participation-category",
                figure=create_donut_chart('00'),
                style={
                    'width': '100%', 
                    'height': '70%', 
                    'background-color': '#d0d0e1', 
                    'padding': '0', 
                    'margin': '0'}
            ),
        ], style={            
            'display': 'inline-block', 
            'width': '41%', 
            'height': '250px',
            'background-color': '#d0d0e1', 
            'padding': '10px', 
            'border-radius': '30px',
            'margin': '10px',
            'margin-top': '0px'})
    ], style={'display': 'flex', 'justify-content': 'center', \
              'align-items': 'flex-middle', 'background-color': '#2c3e50', \
              'padding': '10px', 'margin-top': '10px'}),

    # Score distribution by subject
    html.Div([
        html.Div(create_score_distribution_figures('00'), \
                 style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'}),
    ], style={}), 

    dcc.Interval(
        id='interval-component',
        interval=1*40000000,  # in milliseconds
        n_intervals=0
    )
], style={'background-color': '#2c3e50', 'padding': '10px'})

# ________________________________________________________
#                                                         |
#                   API CALLBACK SECTION                  |
# ________________________________________________________|


# update province
@app.callback(
    Output('province-name', 'children'),
    Input('submit-button', 'n_clicks'),
    State('select-province', 'value')
)

def update_province_name(n_clicks, selected_province):
    if n_clicks > 0:
        if selected_province:
            return provinces.get(selected_province, 'Cả nước')
    return 'Cả nước'


# callbacks to update participation stat by province
@app.callback(
    [
        Output('expect_attendants', 'children'),
        Output('actual_attendants', 'children'),
        Output('participation_percentage', 'children'),
        Output('participation-category', 'figure')
        
    ],
    Input('submit-button', 'n_clicks'),
    State('select-province', 'value')
)

def update_attendant_stat_by_province(n_clicks, selected_province):
    expected_attendants = update_expected_participation_by_province(n_clicks, selected_province)
    actual_attendants = update_actual_participation_by_province(n_clicks, selected_province)
    attendant_percentage = update_participation_percentage_by_province(n_clicks, selected_province)
    attendant_category = update_participation_category(n_clicks, selected_province)
    
    return expected_attendants, actual_attendants, attendant_percentage, attendant_category


# update expected participants
def update_expected_participation_by_province(n_clicks, selected_province):
    expected_attendants = find_attendant_stat_by_province('00')['expected']
    if n_clicks > 0:
        if selected_province:
            expected_attendants = find_attendant_stat_by_province(selected_province)['expected']
    return [expected_attendants]


# update actual participation by province
def update_actual_participation_by_province(n_clicks, selected_province):
    actual_attendants = find_attendant_stat_by_province('00')['actual']
    if n_clicks > 0:
        if selected_province:
            actual_attendants = find_attendant_stat_by_province(selected_province)['actual']
    return [actual_attendants]


# update participation percentage
def update_participation_percentage_by_province(n_clicks, selected_province):
    participation_percentage = \
        str(find_attendant_stat_by_province('00')['participation_percentage']) + '%'
    
    if n_clicks > 0:
        if selected_province:
            participation_percentage = str(find_attendant_stat_by_province(selected_province) \
                                           ['participation_percentage']) + '%'
    return [participation_percentage]

def update_participation_category(n_clicks, province_code):
    if n_clicks > 0:
        return create_donut_chart(province_code)
    return create_donut_chart('00')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
