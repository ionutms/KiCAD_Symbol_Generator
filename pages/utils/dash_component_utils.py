"""TODO
"""

from typing import Tuple

from dash import html
import dash_bootstrap_components as dbc


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
