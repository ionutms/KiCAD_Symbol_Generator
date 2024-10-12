"""
This module creates a Dash application that displays a static Plotly table.

The table is populated with data from a CSV file named 'resistor.csv'.
It includes styling for better readability and pagination for handling
large datasets. Column headers wrap their content, with each word
on a different row. The Description column has a percentage-based width,
while other columns adjust their width based on content. Cell contents
are center-aligned, and the Datasheet column contains clickable links
with the text "Link" centered in the cell using inline CSS.

The application can be run directly, and it will start a local server
for viewing the table.
"""

import pandas as pd
import dash
from dash import dash_table
from dash import html

resistor_dataframe = pd.read_csv('resistor.csv')

dash_app = dash.Dash(__name__)

CUSTOM_CSS = """
    .dash-table-container .dash-spreadsheet-container
    .dash-spreadsheet-inner td {
        text-align: center;
    }
    .dash-header .column-header-name {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        text-align: center !important;
        padding: 5px !important;
    }
"""

dash_app.css.append_css({"external_url": CUSTOM_CSS})


def create_column_definitions(dataframe):
    """Create column definitions for the DataTable."""
    return [
        {
            "name": "\n".join(column.split()),
            "id": column,
            "presentation": "markdown" if column == "Datasheet" else "input"
        } for column in dataframe.columns
    ]


def generate_centered_link(url_text):
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
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'fontSize': '14px',
            'height': 'auto',
            'whiteSpace': 'pre-wrap',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        cell_selectable=False,
        markdown_options={'html': True},
        page_size=8,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
    )
])

if __name__ == '__main__':
    dash_app.run_server(
        debug=True,
        dev_tools_ui=True,
        dev_tools_props_check=True
    )
