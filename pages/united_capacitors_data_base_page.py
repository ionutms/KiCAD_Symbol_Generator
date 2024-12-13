"""Capacitors Database Page.

This module provides a Dash page for viewing and interacting with capacitor
specifications. It allows users to browse, search, and filter through a
database of capacitors, with features for customizing the view and accessing
detailed information.

Key features:
- Interactive DataTable displaying capacitor specifications
- Column visibility controls for customizing the view
- Dynamic filtering and multi-column sorting capabilities
- Pagination with customizable page size
- Theme-aware styling with light/dark mode support
- Direct links to capacitor datasheets
- Responsive design for various screen sizes

The module uses Dash components and callbacks to create an interactive
interface for data visualization and exploration. It integrates with
Bootstrap components for a polished user interface and includes
comprehensive styling support for both light and dark themes.
"""

from typing import Any

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback, dash_table, dcc, html, register_page

import pages.utils.dash_component_utils as dcu
import pages.utils.style_utils as styles

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=1)

dataframe: pd.DataFrame = pd.read_csv("data/UNITED_CAPACITORS_DATA_BASE.csv")
total_rows = len(dataframe)

TITLE = "Capacitors Database"
ABOUT = (
    "The Capacitors Database is an interactive web application that "
    "provides a comprehensive view of capacitor specifications.",
    "It allows users to easily browse, search, and filter "
    f"through a database of {total_rows:,} capacitors, "
    "providing quick access to important information and datasheets.",
)

features = [
    "Interactive data table displaying capacitor specifications",
    "Dynamic filtering and multi-column sorting capabilities",
    "Customizable pagination with adjustable items per page",
    "Direct links to capacitor datasheets",
    "Responsive design adapting to light and dark themes",
    "Easy-to-use interface for exploring capacitor data",
    "Customizable column visibility",
]

usage_steps = [
    "Navigate to the Capacitors Database page",
    "Use the table's built-in search functionality "
    "to find specific capacitors",
    "Click on column headers to sort the data",
    "Use the filter action to narrow down the displayed results",
    "Toggle column visibility using the checkboxes above the table",
    "Adjust the number of items per page using the dropdown menu",
    "Navigate through pages using the pagination controls at "
    "the bottom of the table",
    "Access capacitor datasheets by clicking on the provided links in the "
    "'Datasheet' column",
    "Switch between light and dark themes for comfortable viewing in "
    "different environments",
]

hidden_columns = [
    "Reference",
    "Case Code - mm",
    "Case Code - in",
    "Series",
    "Dielectric",
    "Tolerance",
    "Voltage Rating",
]

visible_columns = [
    col for col in dataframe.columns if col not in hidden_columns]

try:
    dataframe["Datasheet"] = dataframe["Datasheet"].apply(
        lambda url_text: dcu.generate_centered_link(url_text, "Datasheet"))

    dataframe["Trustedparts Search"] = dataframe["Trustedparts Search"].apply(
        lambda url_text: dcu.generate_centered_link(url_text, "Search"))
except KeyError:
    pass

layout = dbc.Container([html.Div([
    dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
    dbc.Row([dbc.Col([html.H3(
        f"{link_name.replace('_', ' ')} ({total_rows:,} items)",
        style=styles.heading_3_style)])]),
    dbc.Row([dcu.app_description(TITLE, ABOUT, features, usage_steps)]),

    dbc.Row([dcc.Loading([dcc.Graph(
        id=f"{module_name}_bar_graph",
        config={"displaylogo": False}),
        ], delay_show=100, delay_hide=100),
    ]),

    dcu.table_controls_row(module_name, dataframe, visible_columns),

    dash_table.DataTable(
        id=f"{module_name}_table",
        columns=dcu.create_column_definitions(dataframe, visible_columns),
        data=dataframe[visible_columns].to_dict("records"),
        cell_selectable=False,
        markdown_options={"html": True},
        page_size=10,
        filter_action="native",
        sort_action="native",
        sort_mode="multi"),

], style=styles.GLOBAL_STYLE),
], fluid=True)


dcu.callback_update_visible_columns(
    f"{module_name}_table",
    f"{module_name}_column_toggle",
    dataframe)

dcu.callback_update_table_style_and_visibility(f"{module_name}_table")

dcu.callback_update_page_size(
    f"{module_name}_table", f"{module_name}_page_size")

dcu.callback_update_dropdown_style(f"{module_name}_page_size")


def get_unique_values_with_repetitions(input_list):  # noqa: ANN001, ANN201
    """TODO."""
    if not input_list:
        return []

    unique_counts = []
    current_value = input_list[0]
    current_count = 1

    for item in input_list[1:]:
        if item == current_value:
            current_count += 1
        else:
            unique_counts.append((current_value, current_count))
            current_value = item
            current_count = 1

    unique_counts.append((current_value, current_count))

    unique_values, counts = zip(*unique_counts)

    return list(unique_values), list(counts)


@callback(
    Output(f"{module_name}_bar_graph", "figure"),
    Input("theme_switch_value_store", "data"),
)
def update_distribution_graph(
    theme_switch: bool,  # noqa: FBT001
) -> tuple[Any, dict[str, Any]]:
    """Create a bar graph showing the distribution of capacitance values.

    Args:
        theme_switch (bool): Indicates the current theme (light/dark).

    Returns:
        Plotly figure with capacitance distribution visualization.

    """
    values, counts = \
        get_unique_values_with_repetitions(dataframe["Value"].to_list())
    # Existing figure layout configuration
    figure_layout = {
        "xaxis": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False,
            "domain": (0.0, 1.0), "showgrid": True,
            "title": {"text": "Capacitance Value", "standoff": 10},
            "title_font_weight": "bold", "tickmode": "array",
            "tickangle": -30,
            "tickfont": {"color": "#808080", "weight": "bold"},
            "titlefont": {"color": "#808080"},
        },
        "yaxis": {
            "gridcolor": "#808080", "griddash": "dash",
            "zerolinecolor": "lightgray", "zeroline": False,
            "tickangle": -30, "position": 0.0,
            "title": "Number of Capacitors",
            "tickfont": {"color": "#808080", "weight": "bold"},
            "titlefont": {"color": "#808080"}, "showgrid": True,
            "anchor": "free", "autorange": True, "tickformat": ".0f",
        },
        "title": {
            "text":
                "Capacitance Value Distribution",
                "x": 0.5, "xanchor": "center",
        },
        "showlegend": False,
    }

    # Create the figure
    figure = go.Figure(
        data=[go.Bar(
            x=values, y=counts, textposition="auto", text=counts,
            hovertemplate=(
                "Capacitance: %{x}<br>"
                "Number of Capacitors: %{y}<extra></extra>"),
        )],
        layout=figure_layout)

    # Define theme settings
    theme = {
        "template": "plotly" if theme_switch else "plotly_dark",
        "paper_bgcolor": "white" if theme_switch else "#222222",
        "plot_bgcolor": "white" if theme_switch else "#222222",
        "font_color": "black" if theme_switch else "white",
        "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
        "xaxis": {"tickangle": -45},
    }

    # Update figure layout with theme and remove unnecessary modebar options
    figure.update_layout(
        **theme,
        modebar={"remove": [
            "zoom", "pan", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d",
            "autoScale2d", "resetScale2d", "toImage",
        ]},
    )

    return figure
