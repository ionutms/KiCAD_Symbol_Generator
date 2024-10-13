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

from typing import List, Dict


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

TABLE_GLOBAL_STYLES = {
    "font_family": "'Roboto', sans-serif",
    "light_background": "white",
    "dark_background": "#666666",
    "light_color": "black",
    "dark_color": "white",
    "header_background_light": "#DDDDDD",
    "header_background_dark": "#111111",
    "filter_background_light": "#F8F8F8",
    "filter_background_dark": "#555555",
    "placeholder_color_light": "#AAAAAA",
    "placeholder_color_dark": "#CCCCCC",
    "input_text_color_light": "#555555",
    "input_text_color_dark": "#E0E0E0",
    "cell_padding": "10px",
    "filter_padding": "5px",
    "cell_font_size": "14px",
    "header_font_size": "16px",
    "filter_font_size": "16px",
    "placeholder_font_size": "14px",
    "font_weight_normal": "normal",
    "font_weight_bold": "bold",
    "font_style_normal": "normal",
    "font_style_bold": "bold",
    "white_space_normal": "normal",
    "white_space_pre_wrap": "pre-wrap",
    "height_auto": "auto",
    "text_align_center": "center",
    "overflow_x_auto": "auto",
    "overflow_y_auto": "auto",
    "min_width_100": "100%",
    "width_100": "100%",
    "max_width_100": "100%",
    "overflow_hidden": "hidden",
    "text_overflow_ellipsis": "ellipsis"
}


def generate_css(switch: bool) -> List[Dict[str, str]]:
    """
    Generate CSS rules for the DataTable based on the theme switch value.

    Args:
        switch (bool):
            The state of the theme switch.
            True for light theme, False for dark theme.

    Returns:
        List[Dict[str, str]]: A list of CSS rule dictionaries.
    """
    input_color = \
        TABLE_GLOBAL_STYLES["input_text_color_light"] \
        if switch else \
        TABLE_GLOBAL_STYLES["input_text_color_dark"]
    placeholder_color = \
        TABLE_GLOBAL_STYLES["placeholder_color_light"] \
        if switch else \
        TABLE_GLOBAL_STYLES["placeholder_color_dark"]

    return [
        {
            'selector': '.dash-filter input',
            'rule': f'''
                text-align:
                    {TABLE_GLOBAL_STYLES["text_align_center"]} !important;
                font-size:
                    {TABLE_GLOBAL_STYLES["filter_font_size"]} !important;
                padding:
                    {TABLE_GLOBAL_STYLES["filter_padding"]} !important;
                color: {input_color} !important;
                font-family:
                    {TABLE_GLOBAL_STYLES["font_family"]} !important;
            '''
        },
        {
            'selector': '.dash-filter input::placeholder',
            'rule': f'''
                color: {placeholder_color} !important;
                font-size:
                    {TABLE_GLOBAL_STYLES["placeholder_font_size"]} !important;
                text-align:
                    {TABLE_GLOBAL_STYLES["text_align_center"]} !important;
                font-style:
                    {TABLE_GLOBAL_STYLES["font_style_bold"]} !important;
                font-family:
                    {TABLE_GLOBAL_STYLES["font_family"]} !important;
            '''
        }
    ]


def style_accordionitem_title(title: str, font_size: int = 24):
    """Style accordionitem title."""
    style_accordionitem_title_params = {
        "font-size": f"{font_size}px", "font-weight": "bold",
        "font-family": "Roboto", "text-align": "center",
        "width": "100%", "margin": "0px auto", "padding": "0px"}
    return html.H1(title, style=style_accordionitem_title_params)
