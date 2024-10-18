"""Capacitors Database Page

This module provides a Dash page for viewing and interacting with capacitor
specifications. It allows users to browse, search, and filter through a
database of capacitors, with features for customizing the view and accessing
detailed information.

Key features:
- Interactive DataTable displaying capacitor specifications
- Column visibility controls for customizing the view
- Dynamic filtering and multi-column sorting capabilities
- Pagination for efficient browsing of large datasets
- Theme-aware styling with light/dark mode support
- Direct links to capacitor datasheets
- Responsive design for various screen sizes

The module uses Dash components and callbacks to create an interactive
interface for data visualization and exploration. It integrates with
Bootstrap components for a polished user interface and includes
comprehensive styling support for both light and dark themes.
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
    "Easy-to-use interface for exploring capacitor data",
    "Customizable column visibility"
]

usage_steps = [
    "Navigate to the Capacitors Database page",
    "Use the table's built-in search functionality "
    "to find specific capacitors",
    "Click on column headers to sort the data",
    "Use the filter action to narrow down the displayed results",
    "Toggle column visibility using the checkboxes above the table",
    "Navigate through pages using the pagination controls at "
    "the bottom of the table",
    "Access capacitor datasheets by clicking on the provided links in the "
    "'Datasheet' column",
    "Switch between light and dark themes for comfortable viewing in "
    "different environments"
]

capacitor_dataframe: pd.DataFrame = pd.read_csv('capacitor.csv')


def create_column_definitions(
        dataframe: pd.DataFrame,
        visible_columns: List[str] = None
) -> List[Dict[str, Any]]:
    """Create column definitions for the Dash DataTable.

    Generates a list of column specifications for the DataTable component,
    with support for selective column visibility and special handling for
    datasheet links.

    Args:
        dataframe: The pandas DataFrame containing the capacitor data.
        visible_columns:
            Optional list of column names to include in the table.
            If None, all columns will be visible.

    Returns:
        A list of dictionaries, each containing the configuration for a
        single column. Each dictionary includes:
            - name:
                The display name of the column (with newlines for wrapping)
            - id: The column identifier matching the DataFrame column name
            - presentation:
                The column's display type (markdown for datasheet links)
    """
    if visible_columns is None:
        visible_columns = dataframe.columns.tolist()

    return [
        {
            "name": "\n".join(column.split()),
            "id": column,
            "presentation": "markdown" if column == "Datasheet" else "input"
        } for column in dataframe.columns if column in visible_columns
    ]


def generate_centered_link(
        url_text: Any
) -> str:
    """Generate a centered HTML link with consistent styling.

    Creates an HTML div containing a centered link for the datasheet URLs.
    Returns an empty string for null/NaN values to handle missing links
    gracefully.

    Args:
        url_text:
            The URL to convert into a centered link. Can be any type,
            as the function handles null/NaN values.

    Returns:
        A string containing HTML for a centered link, or an empty string if
        the input is null/NaN.
    """
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

    dbc.Row([
        dbc.Col([
            html.H6("Show/Hide Columns:", className="mb-2"),
            dbc.Checklist(
                id=f'{module_name}_column_toggle',
                options=[
                    {"label": " ".join(col.split()), "value": col}
                    for col in capacitor_dataframe.columns
                ],
                value=capacitor_dataframe.columns.tolist(),
                inline=True,
                style={"marginBottom": "1rem"}
            )
        ])
    ]),

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
    Output(f'{module_name}_table', "columns"),
    Output(f'{module_name}_table', "data"),
    Input(f'{module_name}_column_toggle', "value"),
)
def update_visible_columns(visible_columns):
    """Update the visible columns based on the checklist selection.

    Filters both the column definitions and data based on the selected
    columns from the visibility toggle checklist.

    Args:
        visible_columns:
            List of column names that should be displayed in the table.

    Returns:
        A tuple containing:
            - List of column definitions for the visible columns
            - List of dictionaries containing the filtered data records
    """
    columns = create_column_definitions(capacitor_dataframe, visible_columns)
    filtered_data = capacitor_dataframe[visible_columns].to_dict('records')
    return columns, filtered_data


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
    """Update the styles of the DataTable based on the theme switch value.

    This function changes the appearance of the DataTable, including data
    cells, header, filter row, and alternating row colors, depending on the
    selected theme (light or dark). The function applies styles defined in
    the style_utils module to all elements within the DataTable.

    Args:
        switch: The state of the theme switch. True for light theme, False
            for dark theme.

    Returns:
        A tuple containing seven style-related elements:
            1. Style for data cells
            2. Style for header cells
            3. Conditional styles for alternating rows
            4. Table style (theme-independent)
            5. Cell style (theme-independent)
            6. Filter row style
            7. CSS rules
    """
    return (
        styles.generate_style_data(switch),
        styles.generate_style_header(switch),
        styles.generate_style_data_conditional(switch),
        styles.generate_style_table(),
        styles.generate_style_cell(),
        styles.generate_style_filter(switch),
        styles.generate_css(switch)
    )
