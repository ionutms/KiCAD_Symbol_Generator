"""Capacitors Database Page

This module provides a Dash page for displaying and interacting with a
database of capacitors. It allows users to view, search, filter, and sort
capacitor specifications.
The page includes an interactive DataTable for displaying the capacitor data.

The module uses Dash components and callbacks to create an interactive
interface for data visualization and exploration.
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

register_page(__name__, name=link_name, order=2)


TITLE = "Capacitors Database"
ABOUT = (
    "The Capacitors Database is an interactive web application that "
    "provides a comprehensive view of capacitor specifications.",
    "It allows users to easily browse, search, and filter "
    "through a database of capacitors, "
    "providing quick access to important information and datasheets."
)

features = [
    "Interactive data table displaying capacitor specifications",
    "Dynamic filtering and multi-column sorting capabilities",
    "Pagination for efficient browsing of large datasets",
    "Direct links to capacitor datasheets",
    "Responsive design adapting to light and dark themes",
    "Easy-to-use interface for exploring capacitor data"
]

usage_steps = [
    "Navigate to the Capacitors Database page",
    "Use the table's built-in search functionality "
    "to find specific capacitors",
    "Click on column headers to sort the data",
    "Use the filter action to narrow down the displayed results",
    "Navigate through pages using the pagination controls at "
    "the bottom of the table",
    "Access capacitor datasheets by clicking on the provided links in the "
    "'Datasheet' column",
    "Switch between light and dark themes for comfortable viewing in "
    "different environments"
]


capacitor_dataframe: pd.DataFrame = pd.read_csv('capacitor.csv')


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


capacitor_dataframe['Datasheet'] = capacitor_dataframe['Datasheet'].apply(
    generate_centered_link
)


layout = dbc.Container([html.Div([
    dbc.Row([dbc.Col([dcc.Link("Go back Home", href="/")])]),
    dbc.Row([dbc.Col([html.H3(
        f"{link_name.replace('_', ' ')}", style=styles.heading_3_style)])]),
    dbc.Row([dcu.app_description(TITLE, ABOUT, features, usage_steps)]),

    dash_table.DataTable(
        id=f'{module_name}_table',
        columns=create_column_definitions(capacitor_dataframe),
        data=capacitor_dataframe.to_dict('records'),
        cell_selectable=False,
        markdown_options={'html': True},
        page_size=8,
        filter_action="native",
        sort_action="native",
        sort_mode="multi"),

], style=styles.GLOBAL_STYLE)
], fluid=True)


@callback(
    Output(f'{module_name}_table', "style_data"),
    Output(f'{module_name}_table', "style_header"),
    Output(f'{module_name}_table', "style_data_conditional"),
    Output(f'{module_name}_table', "style_table"),
    Output(f'{module_name}_table', "style_cell"),
    Output(f'{module_name}_table', "style_filter"),
    Output(f'{module_name}_table', "css"),
    Input("theme_switch_value_store", "data"),
)
def update_table_style_and_visibility(
    switch: bool
) -> Tuple[Dict, Dict, List[Dict], Dict, Dict, Dict, List[Dict]]:
    """
    Update the styles of the DataTable based on the theme switch value.

    This function changes the appearance of the DataTable, including
    data cells, header, filter row, and alternating row colors,
    depending on the selected theme (light or dark). The function
    applies the Roboto font to all elements within the DataTable.

    Args:
        switch (bool):
            The state of the theme switch.
            True for light theme, False for dark theme.

    Returns:
        Tuple[Dict, Dict, List[Dict], Dict, Dict, Dict, List[Dict]]:
            Styles for data cells, header cells, conditional styles
            for alternating rows, table style, cell style, filter style,
            and CSS rules.
    """
    style_data = {
        "backgroundColor":
            styles.TABLE_GLOBAL_STYLES["light_background"]
            if switch else
            styles.TABLE_GLOBAL_STYLES["dark_background"],
        "color":
            styles.TABLE_GLOBAL_STYLES["light_color"]
            if switch else
            styles.TABLE_GLOBAL_STYLES["dark_color"],
        "fontWeight": styles.TABLE_GLOBAL_STYLES["font_weight_normal"],
        "whiteSpace": styles.TABLE_GLOBAL_STYLES["white_space_normal"],
        "height": styles.TABLE_GLOBAL_STYLES["height_auto"],
        "font-family": styles.TABLE_GLOBAL_STYLES["font_family"]
    }

    style_header = {
        "backgroundColor":
            styles.TABLE_GLOBAL_STYLES["header_background_light"]
            if switch else
            styles.TABLE_GLOBAL_STYLES["header_background_dark"],
        "fontSize": styles.TABLE_GLOBAL_STYLES["header_font_size"],
        "textAlign": styles.TABLE_GLOBAL_STYLES["text_align_center"],
        "height": styles.TABLE_GLOBAL_STYLES["height_auto"],
        "whiteSpace": styles.TABLE_GLOBAL_STYLES["white_space_pre_wrap"],
        "fontWeight": styles.TABLE_GLOBAL_STYLES["font_weight_bold"],
        "color":
            styles.TABLE_GLOBAL_STYLES["light_color"]
            if switch else
            styles.TABLE_GLOBAL_STYLES["dark_color"],
        "font-family": styles.TABLE_GLOBAL_STYLES["font_family"]
    }

    style_data_conditional = (
        [{"if": {"row_index": "odd"},
            "backgroundColor":
                styles.TABLE_GLOBAL_STYLES["filter_background_light"]}]
        if switch else
        [{"if": {"row_index": "odd"},
            "backgroundColor":
                styles.TABLE_GLOBAL_STYLES["filter_background_dark"]}]
    )

    style_table = {
        "overflowX": styles.TABLE_GLOBAL_STYLES["overflow_x_auto"],
        "minWidth": styles.TABLE_GLOBAL_STYLES["min_width_100"],
        "width": styles.TABLE_GLOBAL_STYLES["width_100"],
        "maxWidth": styles.TABLE_GLOBAL_STYLES["max_width_100"],
        "height": styles.TABLE_GLOBAL_STYLES["height_auto"],
        "overflowY": styles.TABLE_GLOBAL_STYLES["overflow_y_auto"],
        "font-family": styles.TABLE_GLOBAL_STYLES["font_family"]
    }

    style_cell = {
        "textAlign": styles.TABLE_GLOBAL_STYLES["text_align_center"],
        "overflow": styles.TABLE_GLOBAL_STYLES["overflow_hidden"],
        "textOverflow": styles.TABLE_GLOBAL_STYLES["text_overflow_ellipsis"],
        "fontSize": styles.TABLE_GLOBAL_STYLES["cell_font_size"],
        "padding": styles.TABLE_GLOBAL_STYLES["cell_padding"],
        "font-family": styles.TABLE_GLOBAL_STYLES["font_family"],
        "whiteSpace": styles.TABLE_GLOBAL_STYLES["white_space_normal"],
        "height": styles.TABLE_GLOBAL_STYLES["height_auto"]
    }

    style_filter = {
        "backgroundColor":
            styles.TABLE_GLOBAL_STYLES["filter_background_light"]
            if switch else
            styles.TABLE_GLOBAL_STYLES["filter_background_dark"]
    }

    return (
        style_data,
        style_header,
        style_data_conditional,
        style_table,
        style_cell,
        style_filter,
        styles.generate_css(switch)
    )
