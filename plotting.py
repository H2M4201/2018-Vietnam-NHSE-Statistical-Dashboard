import plotly.graph_objects as go
from dash import dcc, html
from util import *

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
        height=180
    )

    fig.update_traces(
        textinfo='percent'
    )
    
    return fig

def create_bar_chart(province_score_distribution, subject):
    categories = province_score_distribution[subject]['score']
    values = province_score_distribution[subject]['count']

    # Create the bar chart
    fig = go.Figure(data=[
        go.Bar(name='score_distribution', x=categories, y=values)
    ])

    # Customize the layout
    fig.update_layout(
        title={
            'text': 'Phổ điểm môn ' + name_conversion[subject] + ' ',
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Điểm số',
        yaxis_title='Số lượng thí sinh',
        font=dict(
            family="Arial",
            size=14,
            color="Black"
        ),
        title_font=dict(
            size=20
        ),
        margin=dict(
            l=20,  # Adjust left margin
            r=20,  # Adjust right margin
            t=60,  # Adjust top margin
            b=20   # Adjust bottom margin
        ),
        width=440,  # Adjust width
        height=400,  # Adjust height
        paper_bgcolor="#d0d0e1",  # Match the background color of the gray box
        plot_bgcolor="#f2f2f2",
    )

    return fig

def create_score_distribution_figures_and_summary(pCode):
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