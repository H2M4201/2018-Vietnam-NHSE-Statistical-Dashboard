import plotly.graph_objects as go
from dash import dcc, html
from util import *

subject_name_conversion = {
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

key_index_name_conversion = {
    'total': 'Tổng số bài thi',
    'average': 'Điểm trung bình',
    'mode': 'Mức điểm có nhiều thí sinh đạt được nhất',
    'sub_standard_count': 'Số bài thi bị điểm liệt (<= 1)',
    'under_average_count': 'Số bài thi dưới trung bình',
    'under_average_percentage': 'Tỷ lệ dưới trung bình (%)',
    'above_excellent_count': 'Số bài thi từ 9 điểm trở lên',
    'above_excellent_percentage': 'Tỷ lệ từ 9 điểm trở lên (%)'
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

# function to create bar chart
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
            'text': 'Phổ điểm môn ' + subject_name_conversion[subject] + ' ',
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
        height=405,  # Adjust height
        paper_bgcolor="#d0d0e1",  # Match the background color of the gray box
        plot_bgcolor="#f2f2f2",
    )

    return fig

def create_summary_table(province_score_distribution, subject):
    # Define table header and cell values
    header_values = ['Thông số', 'Giá trị']
    cell_values = [
        list(key_index_name_conversion.values()),
        [province_score_distribution[subject][key] for key in list(key_index_name_conversion.keys())]

    ]

    # Create the table
    fig = go.Figure(data=[go.Table(
        header=dict(values=header_values,
                     fill_color='#8080ff',
                     line_color='darkslategray',
                    align='center',
                    font=dict(size=14),
                    height=30),
        cells=dict(values=cell_values,
                   fill_color='white',
                   line_color='darkslategray',
                   align='center'))
    ])
    
    # Customize layout
    fig.update_layout(
        width=440,
        height=270,
        margin=dict(
            l=0,  # Adjust left margin
            r=0,  # Adjust right margin
            t=20,  # Adjust top margin
            b=0   # Adjust bottom margin
        ),
        paper_bgcolor="#d0d0e1"
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
                'height': '60%', 
                'background-color': '#d0d0e1', 
                'border-radius': '30px',
                'padding': '0', 
                'margin': '0'}
                ),
                dcc.Graph(
                id=f"{subjects[i]}_summary_table_{pCode}",
                figure=create_summary_table(score_distribution, subjects[i]),
                config={'responsive': False},
                style={
                    'width': '100%', 
                    'height': '30%', 
                    'background-color': '#d0d0e1', 
                    'border-radius': '30px',
                    'padding': '0'}
            ),

            ],  style={'display': 'inline-block', 'width': '31%', 'margin': '1%'})
        )

    return charts