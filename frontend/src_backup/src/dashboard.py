# src/dashboard.py
import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
from ml_service import load_demo_dataset, predict_attack

df = load_demo_dataset()
df["prediction"] = predict_attack(df.drop(columns="label"))

app = dash.Dash(__name__)

# Table
table = dash_table.DataTable(
    columns=[{"name": c, "id": c} for c in df.columns],
    data=df.to_dict("records"),
    page_size=10,
)

# Chart
fig = px.histogram(df, x="prediction", title="Predicted Attacks vs Normal")

app.layout = html.Div([
    html.H1("Network Traffic Analysis Dashboard"),
    table,
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)