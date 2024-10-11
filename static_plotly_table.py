"""
This module creates a Dash application that displays a static Plotly table.

The table is populated with data from a CSV file named 'resistor.csv'.
It includes styling for better readability and pagination for handling
large datasets.

The application can be run directly, and it will start a local server for
viewing the table.
"""

import pandas as pd
import dash
from dash import dash_table
from dash import html

# Read the CSV file
dataframe = pd.read_csv('resistor.csv')

# Initialize the Dash app
app = dash.Dash(__name__)


def create_column_definitions(df):
    """Create column definitions for the DataTable."""
    return [{"name": column, "id": column} for column in df.columns]


# Create the layout
app.layout = html.Div([
    dash_table.DataTable(
        id='resistor_table',
        columns=create_column_definitions(dataframe),
        data=dataframe.to_dict('records'),
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_table={
            'overflowX': 'auto',
            'minWidth': '100%',
            'width': '100%',
            'maxWidth': '100%',
            'height': '400px',
            'overflowY': 'auto',
        },
        style_cell={
            'textAlign': 'left',
            'minWidth': '100px',
            'width': '150px',
            'maxWidth': '300px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        page_size=10,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
    )
])

if __name__ == '__main__':
    # Run the app and save the HTML
    app.run_server(debug=True, dev_tools_ui=True, dev_tools_props_check=True)
