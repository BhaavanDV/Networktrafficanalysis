from dash import dcc, html, dash_table
import pandas as pd

def create_layout(app):
    # Load initial dataset
    df = pd.read_csv(r"C:\Users\bhaav\Downloads\Networktrafficanalysis\network_data.csv")

    return html.Div([
        html.H1("🔥 Advanced Network Traffic Dashboard", style={'textAlign': 'center'}),
        dcc.Tabs(id="tabs", value='tab-overview', children=[
            dcc.Tab(label='Overview', value='tab-overview'),
            dcc.Tab(label='Attack Types', value='tab-attacks'),
            dcc.Tab(label='Alerts', value='tab-alerts')
        ]),
        html.Div(id='tabs-content'),

        # Hidden Interval for live updates
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
    ])