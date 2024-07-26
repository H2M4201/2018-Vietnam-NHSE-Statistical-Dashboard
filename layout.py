from dash import html, dcc
from plotting import load_caching_information
from util import *
from plotting import *


def dashboard_layout():
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

    provinces, attendant_stat, score_distribution_stat = load_caching_information()


    layout = html.Div([
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
                    children=str(find_attendant_stat_by_province('00')['participation_percentage']) + '%', 
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
        html.Div(id='bar-charts-container', children= create_score_distribution_figures_and_summary('00'),\
                 style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center'}),
    ], style={}),


    dcc.Interval(
        id='interval-component',
        interval=1*40000000,  # in milliseconds
        n_intervals=0
    )
], style={'background-color': "#2c3e50", 'padding': '10px'})
    
    return layout