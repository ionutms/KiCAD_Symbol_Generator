"""
This module creates a Dash application that displays a static Plotly table.

The table is populated with data from a CSV file named 'resistor.csv'.
It includes styling for better readability and pagination for handling
large datasets. All columns are set to adjust their width based on content,
both column titles and cell contents are center-aligned, and the Datasheet
column contains clickable links with consistent text size.

The application can be run directly, and it will start a local server for
viewing the table.
"""

import pandas as pd
import dash
from dash import dash_table
from dash import html

resistor_dataframe = pd.read_csv('resistor.csv')

dash_app = dash.Dash(__name__)

CUSTOM_CSS = """
    .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner
    td a {
        font-size: inherit;
        color: inherit;
        text-decoration: underline;
    }
"""

dash_app.css.append_css({"external_url": CUSTOM_CSS})


def create_column_definitions(dataframe):
    """Create column definitions for the DataTable."""
    return [
        {
            "name": column,
            "id": column,
            "presentation": "markdown" if column == "Datasheet" else "input"
        } for column in dataframe.columns
    ]


resistor_dataframe['Datasheet'] = resistor_dataframe['Datasheet'].apply(
    lambda x: f'[{x}]({x})' if pd.notna(x) else ''
)

dash_app.layout = html.Div([
    dash_table.DataTable(
        id='resistor_table',
        columns=create_column_definitions(resistor_dataframe),
        data=resistor_dataframe.to_dict('records'),
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_table={
            'overflowX': 'auto',
            'minWidth': '100%',
            'width': '100%',
            'maxWidth': '100%',
            'height': 'auto',
            'overflowY': 'auto',
        },
        style_cell={
            'textAlign': 'center',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'fontSize': '14px',
        },
        style_cell_conditional=[
            {
                'if': {'column_id': column},
                'width': 'auto',
                'minWidth': 'unset',
                'maxWidth': 'unset',
            } for column in resistor_dataframe.columns
        ],
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'fontSize': '14px',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        markdown_options={'html': True},
        page_size=10,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
    )
])

if __name__ == '__main__':
    dash_app.run_server(
        debug=True, dev_tools_ui=True, dev_tools_props_check=True)
