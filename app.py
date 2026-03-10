import os
import threading
import webbrowser

import dash

from backend.FitFileProcessor import FitFileProcessor
from dashboard.layout import create_layout
import dashboard.callbacks  # noqa: F401 - registers tab router
import dashboard.tabs  # noqa: F401 - registers tab-specific callbacks

# Process any new FIT files on startup (skipped on Plotly Cloud where source folder doesn't exist)
_fp = FitFileProcessor()
if os.path.isdir(_fp.source_folder):
    _fp.run()

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Tyler's Activities"
app.layout = create_layout()

server = app.server  # required for Plotly Cloud / gunicorn

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        threading.Timer(1.5, webbrowser.open, args=["http://localhost:8050"]).start()
    app.run(debug=True, port=8050)
