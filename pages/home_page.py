"""Home page module for the Dash application.

This module defines the layout and callback for the home page of the Dash app.
It displays a title and dynamically generates links to other pages in the app.
"""
from __future__ import annotations

from typing import Any

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
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
        dbc.Col([
            dcc.Loading([dcc.Graph(
                id=f"{module_name}_repo_clones_graph",
                config={"displaylogo": False}),
                ], delay_show=700, delay_hide=500),
            dcc.Loading([dcc.Graph(
                id=f"{module_name}_repo_visitors_graph",
                config={"displaylogo": False}),
                ], delay_show=700, delay_hide=500),
            ], xs=12, md=8),

        dbc.Col([
            html.H4("Application Pages"),
            html.Div(id="links_display", style={
                "display": "flex", "flex-direction": "column", "gap": "10px",
            })], xs=12, md=4),
    ]),
], fluid=True)


def create_figure(
    theme_switch: bool,  # noqa: FBT001
    data_frame: pd.DataFrame,
    trace_colors: tuple[str, str],
    titles: tuple[str, str],
    relayout_data: dict[str, Any] | None = None,
) -> go.Figure:
    """Create a figure with dynamic x-axis range handling."""
    # Determine the x-axis range
    min_timestamp = data_frame["clone_timestamp"].min()
    max_timestamp = data_frame["clone_timestamp"].max()

    # Determine x-axis range based on relayout data
    x_range = [min_timestamp, max_timestamp]
    if (relayout_data and "xaxis.range[0]" in relayout_data):
        x_range = [
            pd.to_datetime(relayout_data["xaxis.range[0]"]),
            pd.to_datetime(relayout_data["xaxis.range[1]"]),
        ]

    # Existing figure layout configuration
    figure_layout = {
        "xaxis": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False,
            "domain": (0.0, 1.0), "title": "Date", "showgrid": True,
            "range": x_range,
            "type": "date",
        },
        "yaxis": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False,
            "tickangle": -90, "position": 0.0,
            "title": titles[1], "showgrid": False,
            "anchor": "free",
        },
        "yaxis2": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False,
            "tickangle": -90, "position": 1.0,
            "title": titles[2], "showgrid": False,
            "overlaying": "y", "side": "right",
        },
        "title": {
            "text": titles[0], "x": 0.5, "xanchor": "center",
        },
        "showlegend": False,
    }

    total_trace = go.Scatter(
        x=data_frame["clone_timestamp"], y=data_frame["total_clones"],
        mode="lines+markers", name=titles[1],
        marker={"color": trace_colors[0], "size": 8},
        line={"color": trace_colors[0], "width": 2}, yaxis="y1")

    unique_trace = go.Scatter(
        x=data_frame["clone_timestamp"], y=data_frame["unique_clones"],
        mode="lines+markers", name=titles[2],
        marker={"color": trace_colors[1], "size": 8},
        line={"color": trace_colors[1], "width": 2}, yaxis="y2")

    figure = go.Figure(
        data=[total_trace, unique_trace], layout=figure_layout)

    figure.update_layout(
        height=300,
        hovermode="x unified",
        yaxis={
            "tickcolor": trace_colors[0], "linecolor": trace_colors[0],
            "linewidth": 2, "title_font_color": trace_colors[0],
            "title_font_size": 14, "title_font_weight": "bold",
        },
        yaxis2={
            "tickcolor": trace_colors[1], "linecolor": trace_colors[1],
            "linewidth": 2, "title_font_color": trace_colors[1],
            "title_font_size": 14, "title_font_weight": "bold",
        },
    )

    # Theme configuration
    theme = {
        "template": "plotly" if theme_switch else "plotly_dark",
        "paper_bgcolor": "white" if theme_switch else "#222222",
        "plot_bgcolor": "white" if theme_switch else "#222222",
        "font_color": "black" if theme_switch else "white",
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
    }

    figure.update_layout(**theme, modebar={"remove": [
        "zoom", "pan", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d",
        "autoScale2d", "resetScale2d", "toImage",
    ]})

    return figure


@callback(
    Output("links_display", "children"),
    Input("links_store", "data"),
)
def display_links(links: list[dict] | None) -> html.Div | str:
    """Generate and display links based on the provided data."""
    if not links:
        return "Loading links..."

    return html.Div([
        html.Div(dcc.Link(link["name"], href=link["path"]))
        for link in links
    ][:-1])


@callback(
    Output(f"{module_name}_repo_clones_graph", "figure"),
    Output(f"{module_name}_repo_visitors_graph", "figure"),
    Input("theme_switch_value_store", "data"),
    Input(f"{module_name}_repo_clones_graph", "relayoutData"),
    Input(f"{module_name}_repo_visitors_graph", "relayoutData"),
)
def update_graph_with_uploaded_file(
    theme_switch: bool,  # noqa: FBT001
    clones_relayout: dict[str, Any] | None = None,
    visitors_relayout: dict[str, Any] | None = None,
) -> tuple[Any, dict[str, Any]]:
    """Read CSV data and update the repository graphs."""
    def load_traffic_data(
        github_url: str,
        local_file: str,
        rename_columns: dict[str, str] | None = None,
    ) -> pd.DataFrame:
        """Load traffic data from GitHub, fallback to local file if needed.

        Args:
            github_url: URL of the CSV file on GitHub
            local_file: Path to local CSV file
            rename_columns: Optional dictionary to rename columns

        Returns:
            DataFrame with traffic data

        """
        try:
            # Try loading from GitHub
            data_frame = pd.read_csv(github_url)
        except (pd.errors.ParserError, pd.errors.EmptyDataError, OSError):
            try:
                # Fallback to local file
                data_frame = pd.read_csv(local_file)
            except (
                FileNotFoundError,
                pd.errors.ParserError, pd.errors.EmptyDataError):
                # Return empty DataFrame if both attempts fail
                return pd.DataFrame({
                    "clone_timestamp": pd.Series(dtype="datetime64[ns, UTC]"),
                    "total_clones": pd.Series(dtype="int"),
                    "unique_clones": pd.Series(dtype="int"),
                })

        # Rename columns if specified
        if rename_columns:
            data_frame = data_frame.rename(columns=rename_columns)

        # Convert timestamp to datetime
        data_frame["clone_timestamp"] = pd.to_datetime(
            data_frame["clone_timestamp"], utc=True)

        return data_frame

    # Define data sources
    clones_sources = {
        "github_url": (
            "https://raw.githubusercontent.com/ionutms/KiCAD_Symbols_Generator/"
            "main/repo_traffic_data/clones_history.csv"
        ),
        "local_file": "repo_traffic_data/clones_history.csv",
        "rename_columns": None,
    }

    visitors_sources = {
        "github_url": (
            "https://raw.githubusercontent.com/ionutms/KiCAD_Symbols_Generator/"
            "main/repo_traffic_data/visitors_history.csv"
        ),
        "local_file": "repo_traffic_data/visitors_history.csv",
        "rename_columns": {
            "visitor_timestamp": "clone_timestamp",
            "total_visitors": "total_clones",
            "unique_visitors": "unique_clones",
        },
    }

    # Load data
    data_frame_clones = load_traffic_data(**clones_sources)
    data_frame_visitors = load_traffic_data(**visitors_sources)

    # Create figures with specific color schemes
    repo_clones_figure = create_figure(
        theme_switch, data_frame_clones, ("#227b33", "#4187db"),
        ("Git clones", "Clones", "Unique Clones"), clones_relayout)

    repo_visitors_figure = create_figure(
        theme_switch, data_frame_visitors, ("#227b33", "#4187db"),
        ("Visitors", "Views", "Unique Views"), visitors_relayout)

    return repo_clones_figure, repo_visitors_figure
