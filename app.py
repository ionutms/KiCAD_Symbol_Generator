"""
Main application module for a Dash web application.

This module sets up the Dash application, defines the layout, and includes
callbacks for theme switching and link generation. It uses Dash Bootstrap
Components for styling and implements a theme switcher.

The application uses Dash's multi-page functionality and sets up a container
for page content. It also includes components for storing theme preference
and page links.

Usage:
    Run this script directly to start the Dash server.

Environment Variables:
    PORT: The port number on which to run the server (default: 8050)
"""

import os
from dash import Dash, html, dcc, Input, Output, callback
import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            ThemeSwitchAIO(
                aio_id="theme",
                themes=[dbc.themes.CERULEAN, dbc.themes.DARKLY],
                switch_props={"persistence": False, "value": 0}),
        ])
    ], id='theme_switch', style={"display": ''}),

    dcc.Store(id='theme_switch_value_store', data=[]),

    # Interval component for triggering the callback once
    dcc.Interval(id='interval_component', interval=1*100, max_intervals=1),

    # Store component to hold the links
    dcc.Store(id='links_store'),

    dash.page_container,
], fluid=True)


@app.callback(
    Output('theme_switch_value_store', 'data'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def update_graph_theme(switch):
    """Update graph theme."""
    return switch


@callback(
    Output('links_store', 'data'),
    Input('interval_component', 'n_intervals')
)
def update_links_store(interval_component):
    """Update links store."""
    if interval_component is None:
        raise PreventUpdate

    links = [
        {'name': page['name'], 'path': page['relative_path']}
        for page in dash.page_registry.values()
    ]
    return links


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(
        port=port,
        debug=True, dev_tools_ui=True, dev_tools_props_check=True
    )
