import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import date

prognoses = pd.read_excel('prognoses_test.xlsx')
prognoses = pd.DataFrame(prognoses)

prognoses['Date'] = pd.to_datetime(prognoses['Date'], format='%Y-%m-%d') # convert to datetime object so we can work with dates
prognoses['Date'] = prognoses['Date'].dt.to_period('M') # convert to year and month to later use for group by
prognoses = prognoses.rename(columns={'Date':'year_month'}) # rename columns for better visualisation

def period_to_str(series):
    """"
    This function sets te date column to format YYYY-MM
    """
    if type(series) != type(""):
        return series.strftime('%Y-%m')
    return series

prognoses['year_month'] = prognoses.year_month.apply(period_to_str)

# print(prognoses)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.DatePickerRange(
        id='date_picker_cash',
        min_date_allowed = prognoses['year_month'].min(),  # minimum date allowed on the DatePickerRange component
        max_date_allowed = prognoses['year_month'].max(),  # maximum date allowed on the DatePickerRange component
        initial_visible_month = date.today(),  # the month initially presented when the user opens the calendar
        start_date = prognoses.iloc[12, 0],
        end_date = prognoses.iloc[0, 0],
        with_portal = True,
        display_format='MMM Do, YYYY',
    ),

    dcc.Graph(id='graph_outgoing_cash', figure={})

])


@app.callback(
    Output(component_id='graph_outgoing_cash', component_property='figure'),
    Input(component_id='date_picker_cash', component_property='start_date'), 
    Input(component_id='date_picker_cash', component_property='end_date')
)
    
def update_graph_incoming_cash(start_date, end_date):
    dff2 = prognoses
    dff2 = dff2[(dff2['year_month'] >= start_date) & (dff2['year_month'] <= end_date)]
    fig = px.bar(
        data_frame = dff2,
        x = 'year_month',
        y = ['Expected incoming cash', 'True incoming cash'],
        barmode = 'group',
        height = 400,
        labels={    
            'value':'Amount in EUR'
        },
    )

    return fig


if __name__ == '__main__':
    app.run_server()