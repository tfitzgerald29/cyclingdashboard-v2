import dash
import dash_mantine_components as dmc

from dashboard.layout import create_layout
import dashboard.callbacks  # noqa: F401


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=dmc.styles.ALL,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Tyler's Activities"
app.layout = dmc.MantineProvider(
    children=create_layout(),
    forceColorScheme="dark",
)

server = app.server
