import dash
import dash_bootstrap_components as dbc
import os

from utils.callbacks import register_callbacks
from utils.layout import create_layout

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set layout
app.layout = create_layout(app)

# Register all callbacks
register_callbacks(app)

if __name__ == "__main__":
    # Get host and port from environment variables for Docker compatibility
    host = os.getenv('DASH_HOST', '127.0.0.1')
    port = int(os.getenv('DASH_PORT', 8050))
    app.run(host=host, port=port, debug=False)