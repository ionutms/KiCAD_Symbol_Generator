"""
Style Utilities for Dash Components

This module defines styles and styling functions for various Dash components.
It includes predefined styles for headings, accordion items, radio buttons,
popovers, and centering elements. It also provides a function for styling
accordion item titles.

Styles:
    heading_style: Style for headings.
    accordionitem_style: Style for accordion items.
    accordion_style: Style for accordions.
    radioitems_style: Style for radio button groups.

Constants:
    CENTER_DIV_CONTENT: Class for centering div content.
    CENTER_CLASS_NAME: Class for centering elements.
    CENTER_BOTTOM_CLASS_NAME: Class for centering elements at the bottom.

Functions:
    style_accordionitem_title: Create a styled accordion item title.
"""

from dash import html

heading_3_style = {"font-size": "30px", "font-weight": "bold"}

accordionitem_style = {"border": "2px solid #abc", "border-radius": "5px"}

accordion_style = {"width": "100%", "margin": "5px auto"}

radioitems_style = {"max-height": "400px", "overflow-y": "auto"}

CENTER_DIV_CONTENT = \
    "d-flex flex-column justify-content-center align-items-center h-100"

CENTER_CLASS_NAME = "w-100 d-flex justify-content-center align-items-center"

CENTER_BOTTOM_CLASS_NAME = "d-flex justify-content-center align-items-end"

GLOBAL_STYLE = {"font-family": "Roboto"}

FLEX_CENTER_COLUMN = \
    "d-flex flex-column justify-content-center align-items-center"

RESPONSIVE_CENTER_BUTTON_CLASS = \
    "w-100 d-flex justify-content-center align-items-center mb-2 mb-md-0"

CENTER_CONTENT_CLASS = \
    "w-100 d-flex justify-content-center align-items-center"


def style_accordionitem_title(title: str, font_size: int = 24):
    """Style accordionitem title."""
    style_accordionitem_title_params = {
        "font-size": f"{font_size}px", "font-weight": "bold",
        "font-family": "Roboto", "text-align": "center",
        "width": "100%", "margin": "0px auto", "padding": "0px"}
    return html.H1(title, style=style_accordionitem_title_params)
