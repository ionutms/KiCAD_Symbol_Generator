"""TODO."""

from typing import TextIO


def write_header(
        symbol_file: TextIO,
) -> None:
    """Write the header of the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.

    """
    symbol_file.write("""
        (kicad_symbol_lib
            (version 20231120)
            (generator kicad_symbol_editor)
            (generator_version 8.0)
        """)


def write_symbol_header(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the header for a single symbol.

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


def get_all_properties(
        component_data_list: list[dict[str, str]],
) -> set:
    """Get all unique properties from the component data.

    Args:
        component_data_list (List[Dict[str, str]]): List of component data.

    Returns:
        set: Set of all unique property names.

    """
    return set().union(
        *(component_data.keys() for component_data in component_data_list))


def write_property(  # noqa: PLR0913
    symbol_file: TextIO,
    property_name: str,
    property_value: str,
    x_offset: float,
    y_offset: float,
    font_size: float,
    show_name: bool,  # noqa: FBT001
    hide: bool,  # noqa: FBT001
) -> None:
    """Write a single property for a symbol.

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


def write_pin(  # noqa: PLR0913
        symbol_file: TextIO,
        x_pos: float,
        y_pos: float,
        angle: int,
        number: str,
        pin_type: str = "unspecified",
        hide: bool = False,  # noqa: FBT001, FBT002
        length: float = 2.54,
) -> None:
    """Write a single pin of the transformer symbol."""
    symbol_file.write(f"""
        (pin {pin_type} line
            (at {x_pos} {y_pos} {angle})
            (length {length})
            (name ""(effects(font(size 1.27 1.27))))
            (number "{number}"(effects(font(size 1.27 1.27))))
            {('hide' if hide else '')}
        )
        """)
