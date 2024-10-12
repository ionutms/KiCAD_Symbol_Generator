"""Signal Data Generator Page

This module provides a Dash page for generating and downloading sample data.
It allows users to specify parameters such as number of channels, frames,
records, and sample interval. The page includes interactive controls for
data generation and a DataTable for displaying the generated data. Users can
also download the generated data as a CSV file.

The module uses Dash components and callbacks to create an interactive
interface for data generation and visualization.
"""

from typing import List, Dict, Any, Tuple
import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
from dash import dash_table, callback
from dash.dependencies import Input, Output
import pandas as pd

import pages.utils.style_utils as styles
import pages.utils.dash_component_utils as dcu

link_name = __name__.rsplit(".", maxsplit=1)[-1].replace("_page", "").title()
module_name = __name__.rsplit(".", maxsplit=1)[-1]

register_page(__name__, name=link_name, order=1)


TITLE = "Resistors Database"
ABOUT = (
    "The ...", ""
)
features = [
    "TODO"
]
usage_steps = [
    "TODO"
]


resistor_dataframe: pd.DataFrame = pd.read_csv('resistor.csv')


def create_column_definitions(
        dataframe: pd.DataFrame
) -> List[Dict[str, Any]]:
    """Create column definitions for the DataTable."""
    return [
        {
            "name": "\n".join(column.split()),
            "id": column,
            "presentation": "markdown" if column == "Datasheet" else "input"
        } for column in dataframe.columns
    ]


def generate_centered_link(
        url_text: Any
) -> str:
    """Generate a centered link with inline CSS."""
    if pd.notna(url_text):
        return (
            f'<div style="width:100%;text-align:center;">'
            f'<a href="{url_text}" target="_blank" '
            f'style="display:inline-block;">Link</a></div>'
        )
    return ''


resistor_dataframe['Datasheet'] = resistor_dataframe['Datasheet'].apply(
    generate_centered_link
)


layout = dbc.Container([html.Div([
    dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
    dbc.Row([dbc.Col([html.H3(
        f"{link_name.replace('_', ' ')}", style=styles.heading_3_style)])]),
    dbc.Row([dcu.app_description(TITLE, ABOUT, features, usage_steps)]),

    dash_table.DataTable(
        id='resistor_table',
        columns=create_column_definitions(resistor_dataframe),
        data=resistor_dataframe.to_dict('records'),
        cell_selectable=False,
        markdown_options={'html': True},
        page_size=8,
        filter_action="native",
        sort_action="native",
        sort_mode="multi"),

], style=styles.GLOBAL_STYLE)
], fluid=True)


@callback(
    Output("resistor_table", "style_data"),
    Output("resistor_table", "style_header"),
    Output("resistor_table", "style_data_conditional"),
    Output("resistor_table", "style_table"),
    Output("resistor_table", "style_cell"),
    Input("theme_switch_value_store", "data"),
)
def update_table_style_and_visibility(
        switch: bool
) -> Tuple[Dict, Dict, List[Dict]]:
    """
    Update the DataTable styles based on the theme switch value.

    This function changes the appearance of the DataTable,
    including data cells, header, and alternating row colors,
    depending on the selected theme.

    Args:
        switch (bool):
            The state of the theme switch.
            True for light theme, False for dark theme.

    Returns:
        Tuple[Dict, Dict, List[Dict]]:
            Styles for data cells, header cells,
            and conditional styles for alternating rows.
    """
    style_data = {
        "backgroundColor": "white" if switch else "#666666",
        "color": "black" if switch else "white",
        "fontWeight": "bold",
        "whiteSpace": "normal",
        "height": "auto"
    }

    style_header = {
        "backgroundColor": "#DDDDDD" if switch else "#111111",
        "fontSize": "16px",
        "textAlign": "center",
        "height": "auto",
        "whiteSpace": "pre-wrap",
        "fontWeight": "bold",
        "color": "black" if switch else "white"
    }

    style_data_conditional = (
        [{"if": {"row_index": "odd"}, "backgroundColor": "#DDDDDD"}]
        if switch else
        [{"if": {"row_index": "odd"}, "backgroundColor": "#555555"}]
    )

    style_table = {
        'overflowX': 'auto',
        'minWidth': '100%',
        'width': '100%',
        'maxWidth': '100%',
        'height': 'auto',
        'overflowY': 'auto',
    }

    style_cell = {
        'textAlign': 'center',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'fontSize': '14px',
    }

    return (
        style_data,
        style_header,
        style_data_conditional,
        style_table,
        style_cell
    )
