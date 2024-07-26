import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import json
from dash import html
import plotly.graph_objects as go
from dash import dash_table
from plotting import *
from layout import dashboard_layout
from callback import *

attendant_stat = './caching/attendant_stat.csv'

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# load caching data
provinces, attendant_stat,score_distribution_stat = load_caching_information()

# load layout
app.layout = dashboard_layout()

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
        Output('participation-category', 'figure'),
        Output('bar-charts-container', 'children')
    ],
    Input('submit-button', 'n_clicks'),
    State('select-province', 'value')
)

def update_attendant_stat_by_province(n_clicks, selected_province):
    expected_attendants = update_expected_participation_by_province(n_clicks, selected_province)
    actual_attendants = update_actual_participation_by_province(n_clicks, selected_province)
    attendant_percentage = update_participation_percentage_by_province(n_clicks, selected_province)
    attendant_category = update_participation_category(n_clicks, selected_province)
    score_distribution = create_score_distribution_figures_and_summary(selected_province)
    
    return expected_attendants, actual_attendants, attendant_percentage, \
        attendant_category, score_distribution

#---------------------------------------------


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
