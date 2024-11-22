"""TODO"""

from typing import TextIO


def write_symbol_header(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """
    Write the header for a single symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(f"""
        (symbol "{symbol_name}"
            (pin_names(offset 0.254))
            (exclude_from_sim no)
            (in_bom yes)
            (on_board yes)
        """)


def write_property(
    symbol_file: TextIO,
    property_name: str,
    property_value: str,
    x_offset: float,
    y_offset: float,
    font_size: float,
    show_name: bool,
    hide: bool
) -> None:
    """
    Write a single property for a symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        property_name (str): Name of the property.
        property_value (str): Value of the property.
        x_offset (float): Horizontal offset for property placement.
        y_offset (float): Vertical offset for property placement.
        font_size (float): Size of the font.
        show_name (bool): Whether to show the property name.
        hide (bool): Whether to hide the property.
    """
    symbol_file.write(f"""
        (property "{property_name}" "{property_value}"
            (at {x_offset} {y_offset} 0)
            {('(show_name)' if show_name else '')}
            (effects
                (font(size {font_size} {font_size}))
                (justify left)
                {('(hide yes)' if hide else '')}
            )
        )
        """)
