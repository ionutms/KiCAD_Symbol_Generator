"""Home page module for the Dash application.

This module defines the layout and callback for the home page of the Dash app.
It displays a title and dynamically generates links to other pages in the app.
"""

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pages.utils.style_utils as styles
import pages.utils.dash_component_utils as dcu

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()

dash.register_page(__name__, name=link_name, path="/")

TITLE = "Home Page"
ABOUT = (
    "The Home page serves as the main entry point and "
    "navigation hub for the Dash application.",
    "It provides a centralized location for users to access "
    "all available pages within the application, "
    "offering a simple and intuitive navigation experience."
)
features = [
    "Dynamic generation of links to other pages in the application",
    "Clean and simple interface for easy navigation",
    "Responsive layout using Dash Bootstrap Components"
]
usage_steps = [
    "View the list of available pages displayed as clickable links.",
    "Click on any link to navigate to the corresponding page.",
    "Use the browser's back button or navigation controls "
    "to return to the Home page."
]


layout = dbc.Container([html.Div([
    dbc.Row([dbc.Col([html.H3(
        f"{link_name.replace('_', ' ')}", style=styles.heading_3_style)])]),
    dbc.Row([dcu.app_description(TITLE, ABOUT, features, usage_steps)]),
    html.Div(id="links_display"),
], style=styles.GLOBAL_STYLE)
], fluid=True)


@callback(
    Output("links_display", "children"),
    Input("links_store", "data")
)
def display_links(links: list[dict] | None) -> html.Div | str:
    """
    Generate and display links based on the provided data.

    This callback function creates a list of links to be displayed on the home
    page. It uses the data stored in the 'links_store' to dynamically generate
    these links.

    Args:
        links (list[dict] | None): A list of dictionaries containing link
            information. Each dictionary should have 'name' and 'path' keys.
            If None, a loading message is returned.

    Returns:
        html.Div | str: A Div containing Link components for each link in the
        input, or a string with a loading message if no links are provided.

    Note:
        The function excludes the last link in the list when creating the Div.
    """
    if not links:
        return "Loading links..."

    return html.Div([
        html.Div(dcc.Link(link["name"], href=link["path"]))
        for link in links
    ][:-1])
