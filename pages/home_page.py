"""Home page module for the Dash application.

This module defines the layout and callback for the home page of the Dash app.
It displays a title and dynamically generates links to other pages in the app.
"""

import io

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import requests
from dash import Input, Output, callback, dcc, html

import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

dash.register_page(__name__, name=link_name, path="/")

TITLE = "Home Page"

ABOUT = (
    "The Home page serves as the main entry point and "
    "navigation hub for the Dash application.",
    "It provides a centralized location for users to access "
    "all available pages within the application, "
    "offering a simple and intuitive navigation experience.",
)

features = [
    "Dynamic generation of links to other pages in the application",
    "Clean and simple interface for easy navigation",
    "Responsive layout using Dash Bootstrap Components",
]

usage_steps = [
    "View the list of available pages displayed as clickable links.",
    "Click on any link to navigate to the corresponding page.",
    "Use the browser's back button or navigation controls "
    "to return to the Home page.",
]

layout = dbc.Container([
    dbc.Row([dbc.Col([html.H3(
        f"{link_name.replace('_', ' ')}", style=styles.heading_3_style)])]),
    dbc.Row([dbc.Col([dcu.app_description(
        TITLE, ABOUT, features, usage_steps)], width=12)]),
    dbc.Row([
        dbc.Col([dcc.Loading([
            dcc.Graph(
                id=f"{module_name}_data_graph",
                config={"displaylogo": False})])], xs=12, md=8),

        dbc.Col([
            html.H4("Application Pages"),
            html.Div(id="links_display", style={
                "display": "flex", "flex-direction": "column", "gap": "10px",
            })], xs=12, md=4),
    ]),
], fluid=True)


@callback(
    Output("links_display", "children"),
    Input("links_store", "data"),
)
def display_links(links: list[dict] | None) -> html.Div | str:  # noqa: FA102
    """Generate and display links based on the provided data.

    This callback function creates a list of links to be displayed on the
    home page. It uses the data stored in the 'links_store' to dynamically
    generate these links.

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


@callback(
    Output(f"{module_name}_data_graph", "figure"),
    Input("theme_switch_value_store", "data"),
)
def update_graph_with_uploaded_file(
    theme_switch: bool,  # noqa: FBT001
) -> tuple[any, dict[str, str]]:
    """Update the graph with repository clone history data from GitHub."""
    github_csv_url = (
        "https://raw.githubusercontent.com/"
        "ionutms/KiCAD_Symbols_Generator/"
        "main/repo_traffic_data/clones_history.csv"
    )

    # User-Agent header to prevent potential 403 errors
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
    }

    try:
        # Fetch the CSV file from GitHub with User-Agent header
        response = requests.get(
            github_csv_url,
            headers=headers,
            timeout=10,
        )
        # Raise an exception for bad responses
        response.raise_for_status()

        # Read the CSV from the response content
        data_frame = pd.read_csv(io.StringIO(response.text))
        data_frame["clone_timestamp"] = pd.to_datetime(
            data_frame["clone_timestamp"])

    except requests.RequestException as requests_error_message:
        print(f"Error fetching CSV from GitHub: {requests_error_message}")
        # Create an empty DataFrame with the expected structure
        data_frame = pd.DataFrame({
            "clone_timestamp": pd.Series(dtype="datetime64[ns]"),
            "total_clones": pd.Series(dtype="int"),
            "unique_clones": pd.Series(dtype="int")})

    # Create figure layout
    figure_layout = {
        "xaxis": {
            "gridcolor": "#808080",
            "griddash": "dash",
            "zerolinecolor": "lightgray",
            "zeroline": False,
            "domain": (0.0, 1.0),
            "title": "Date",
            "showgrid": True,
            "range": [
                data_frame["clone_timestamp"].min(),
                data_frame["clone_timestamp"].max(),
            ],
            "type": "date",
        },
        "yaxis": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False, "tickangle": -90,
            "position": 0.0, "anchor": "free", "title": "Total Clones",
            "showgrid": False,
        },
        "yaxis2": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False, "tickangle": -90,
            "position": 1.0, "overlaying": "y", "side": "right",
            "title": "Unique Clones", "showgrid": False,
        },
        "title": {
            "text": "Repository Clone History", "x": 0.5, "xanchor": "center",
        },
        "showlegend": False,
    }

    # Create traces for total and unique clones
    total_clones_trace = go.Scatter(
        x=data_frame["clone_timestamp"], y=data_frame["total_clones"],
        mode="lines+markers", name="Total Clones",
        marker={"color": "#227b33", "size": 8},
        line={"color": "#227b33", "width": 2}, yaxis="y1")

    unique_clones_trace = go.Scatter(
        x=data_frame["clone_timestamp"], y=data_frame["unique_clones"],
        mode="lines+markers", name="Unique Clones",
        marker={"color": "#4187db", "size": 8},
        line={"color": "#4187db", "width": 2}, yaxis="y2")

    # Create figure
    figure = go.Figure(
        data=[total_clones_trace, unique_clones_trace], layout=figure_layout)

    # Update axis colors to match trace colors
    figure.update_layout(
        hovermode="x unified",
        yaxis={
            "tickcolor": "#227b33", "linecolor": "#227b33",
            "linewidth": 2, "title_font_color": "#227b33",
            "title_font_size": 14, "title_font_weight": "bold"},
        yaxis2={
            "tickcolor": "#4187db", "linecolor": "#4187db",
            "linewidth": 2, "title_font_color": "#4187db",
            "title_font_size": 14, "title_font_weight": "bold"},
    )

    # Theme configuration
    theme = {
        "template": "plotly" if theme_switch else "plotly_dark",
        "paper_bgcolor": "white" if theme_switch else "#222222",
        "plot_bgcolor": "white" if theme_switch else "#222222",
        "font_color": "black" if theme_switch else "white",
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50}}

    # Update figure layout with theme
    figure.update_layout(**theme, modebar={"remove": [
        "zoom", "pan", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d",
        "autoScale2d", "resetScale2d", "toImage"]})

    return figure
