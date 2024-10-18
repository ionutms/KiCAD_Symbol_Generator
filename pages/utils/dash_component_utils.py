"""TODO
"""

from typing import Any, List, Dict, Tuple
from dash import html, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import pandas as pd

import pages.utils.style_utils as styles


def app_description(
    title: str,
    about: Tuple[str],
    features: Tuple[str],
    usage_steps: Tuple[str]
) -> html.Div:
    """Create a description component for any app page.

    Args:
        title (str): The title of the page.
        about (Tuple[str]): A brief description of the page's purpose.
        features (Tuple[str]): A tuple of key features of the page.
        usage_steps (Tuple[str]):
            A tuple of steps describing how to use the page.

    Returns:
        html.Div: A Div component containing the formatted app description.
    """
    left_column_content: dbc.Col = dbc.Col([
        html.H4("Key Features:"),
        html.Ul([html.Li(feature) for feature in features])
    ], xs=12, md=6)

    right_column_content: dbc.Col = dbc.Col([
        html.H4("How to Use:"),
        html.Ol([html.Li(step) for step in usage_steps])
    ], xs=12, md=6)

    description: html.Div = html.Div([
        html.Hr(),
        html.H3(f"About the {title}"), *[
            html.Div(content) if len(about) > 1
            else html.Div(content) for content in about],
        html.Hr(),
        dbc.Row([left_column_content, right_column_content]),
        html.Hr()])
    return description


def callback_update_table_style_and_visibility(
    table_id: str
) -> None:
    """Create a callback function to update DataTable styles based on theme.

    This is a factory function that generates a callback for updating the
    visual styles of a Dash DataTable component in response to theme changes.
    The callback updates multiple style properties to ensure consistent
    theming across the table's various elements.

    The generated callback will:
    - Update data cell styles based on theme
    - Update header styles based on theme
    - Apply conditional styles for alternating rows
    - Set theme-independent table layout properties
    - Configure cell styling properties
    - Update filter row styling
    - Apply theme-specific CSS rules

    Args:
        table_id (str): The ID of the DataTable component for which to create
            the callback. This ID will be used to target the specific table's
            style properties.

    Returns:
        None:
            This function registers a callback with Dash and
            doesn't return a value directly.
    """
    @callback(
        Output(table_id, "style_data"),
        Output(table_id, "style_header"),
        Output(table_id, "style_data_conditional"),
        Output(table_id, "style_table"),
        Output(table_id, "style_cell"),
        Output(table_id, "style_filter"),
        Output(table_id, "css"),
        Input("theme_switch_value_store", "data"),
    )
    def update_table_style_and_visibility(
        switch: bool
    ) -> Tuple[
        Dict[str, str],
        Dict[str, str],
        List[Dict[str, str]],
        Dict[str, str],
        Dict[str, str],
        Dict[str, str],
        List[Dict[str, str]]
    ]:
        """Update the styles of the DataTable based on the theme switch value.

        Args:
            switch: The state of the theme switch. True for light theme, False
                for dark theme.

        Returns:
            A tuple containing seven style-related elements:
                1. Style for data cells (Dict[str, str])
                2. Style for header cells (Dict[str, str])
                3. Conditional styles for alternating rows
                    (List[Dict[str, str]])
                4. Table style (Dict[str, str])
                5. Cell style (Dict[str, str])
                6. Filter row style (Dict[str, str])
                7. CSS rules (List[Dict[str, str]])
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


def callback_update_visible_columns(
    table_id: str,
    checklist_id: str,
    dataframe: pd.DataFrame
) -> None:
    """Create a callback function to update DataTable columns visibility.

    This is a factory function that generates a callback for managing visible
    columns in a Dash DataTable component. The callback responds to changes in
    a checklist component that controls column visibility.

    The generated callback will:
    - Filter column definitions based on selected visibility options
    - Update the table data to include only visible columns
    - Update the DataTable component with new column definitions and data

    Args:
        table_id (str):
            The ID of the DataTable component to update.
            This ID will be used to target the table's columns and
            data properties.
        checklist_id (str):
            The ID of the Checklist component that controls column visibility.
            This component should have column names as its options.
        dataframe (pd.DataFrame):
            The source DataFrame containing all possible columns and data.
            Used to filter and format data based on selected columns.

    Returns:
        None:
            This function registers a callback with Dash and doesn't return
            a value directly.
    """
    @callback(
        Output(table_id, "columns"),
        Output(table_id, "data"),
        Input(checklist_id, "value"),
    )
    def update_visible_columns(visible_columns):
        """Update the visible columns based on the checklist selection.

        Args:
            visible_columns:
                List of column names that should be displayed in the table.

        Returns:
            A tuple containing:
                - List of column definitions for the visible columns
                - List of dictionaries containing the filtered data records
        """
        columns = create_column_definitions(dataframe, visible_columns)
        filtered_data = dataframe[visible_columns].to_dict('records')
        return columns, filtered_data


def create_column_definitions(
        dataframe: pd.DataFrame,
        visible_columns: List[str] = None
) -> List[Dict[str, Any]]:
    """Create column definitions for the Dash DataTable.

    Generates a list of column specifications for the DataTable component,
    with support for selective column visibility and special handling for
    datasheet links.

    Args:
        dataframe: The pandas DataFrame containing the resistor data.
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
