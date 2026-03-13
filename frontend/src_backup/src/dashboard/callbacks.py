from dash import Input, Output, dash_table
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

CSV_PATH = "../../data/processed/network_features.csv"

def register_callbacks(app):

    @app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value'),
        Input('interval-component', 'n_intervals')
    )
    def update_tab(tab, n_intervals):
        # Load CSV dynamically to simulate real-time updates
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)
        else:
            df = pd.DataFrame(columns=["flow_duration","avg_packet_size","attack_type"])

        if tab == 'tab-overview':
            fig = px.scatter(df, x="flow_duration", y="avg_packet_size",
                             color="attack_type", size_max=15,
                             title="Flow Duration vs Avg Packet Size")
            return html.Div([
                dcc.Graph(figure=fig)
            ])

        elif tab == 'tab-attacks':
            fig = px.histogram(df, x="attack_type", color="attack_type",
                               title="Packets per Attack Type")
            table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'center', 'padding': '5px'},
                style_data_conditional=[
                    {'if': {'filter_query': '{attack_type} = "Attack"'},
                     'backgroundColor': '#FF4136', 'color': 'white'},
                    {'if': {'filter_query': '{attack_type} = "Normal"'},
                     'backgroundColor': '#2ECC40', 'color': 'white'}
                ],
                page_size=10
            )
            return html.Div([
                dcc.Graph(figure=fig),
                html.Hr(),
                table
            ])

        elif tab == 'tab-alerts':
            attacks = df[df['attack_type'] == 'Attack']
            alerts_list = [
                html.Div(f"⚠ Packet {row.name} detected as ATTACK",
                         style={'color': 'red', 'fontWeight': 'bold'})
                for _, row in attacks.iterrows()
            ]
            if len(alerts_list) == 0:
                alerts_list = [html.Div("No attacks detected.", style={'color': 'green'})]
            return html.Div(alerts_list)