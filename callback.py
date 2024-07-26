from dash import callback, Input, Output, State
from util import *
from plotting import *

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