import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.layout import create_layout
from dashboard.callbacks import register_callbacks
from dash import Dash

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Advanced Network Traffic Dashboard"

# Layout & callbacks
app.layout = create_layout(app)
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)