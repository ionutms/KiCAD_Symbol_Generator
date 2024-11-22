"""
KiCad Inductor Symbol Generator

This module provides functionality to generate KiCad symbol files from CSV
data for inductors. It creates symbol files with proper inductor properties
and graphical representation in horizontal layout.

The main function, generate_kicad_symbol, reads data from a CSV file and
produces a .kicad_sym file with the symbol definition, including properties
and graphical representation.

Usage:
    python kicad_inductor_symbol_generator.py

Or import and use the generate_kicad_symbol function in your own script.

Dependencies:
    - csv (Python standard library)
"""

import csv
from typing import List, Dict, TextIO
import symbol_utils as su


def generate_kicad_symbol(
        input_csv_file: str,
        output_symbol_file: str,
        encoding: str = 'utf-8'
) -> None:
    """
    Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.
        encoding (str, optional):
            Character encoding to use. Defaults to 'utf-8'.

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there's an error reading the CSV file.
        IOError: If there's an error writing to the output file.
    """
    component_data_list = read_csv_data(input_csv_file, encoding)
    all_properties = get_all_properties(component_data_list)

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def read_csv_data(
        input_csv_file: str,
        encoding: str
) -> List[Dict[str, str]]:
    """
    Read component data from a CSV file.

    Args:
        input_csv_file (str): Path to the input CSV file.
        encoding (str): Character encoding of the CSV file.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing component data.
    """
    with open(input_csv_file, 'r', encoding=encoding) as csv_file:
        return list(csv.DictReader(csv_file))


def get_all_properties(
        component_data_list: List[Dict[str, str]]
) -> set:
    """
    Get all unique properties from the component data.

    Args:
        component_data_list (List[Dict[str, str]]): List of component data.

    Returns:
        set: Set of all unique property names.
    """
    return set().union(
        *(component_data.keys() for component_data in component_data_list))


def write_header(
        symbol_file: TextIO
) -> None:
    """
    Write the header of the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
    """
    symbol_file.write("""
        (kicad_symbol_lib
            (version 20231120)
            (generator \"kicad_symbol_editor\")
            (generator_version \"8.0\")
        """)


def write_component(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """
    Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.
    """
    symbol_name = component_data.get('Symbol Name', '')
    su.write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write("\t)\n")


def write_properties(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """
    Write properties for a single symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.
    """
    property_configs = {
        "Reference": (0, 2.54, 1.27, False, False, "L"),
        "Value": (
            0, -2.54, 1.27, False, False,
            component_data.get('Inductance', '')),
        "Footprint": (0, -5.08, 1.27, True, True, None),
        "Datasheet": (0.254, -7.62, 1.27, True, True, None),
        "Description": (0, -10.16, 1.27, True, True, None)
    }

    y_offset = -12.7
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (0, y_offset, 1.27, True, True, None)
            )
            value = config[5] or component_data[prop_name]
            write_property(
                symbol_file,
                prop_name,
                value,
                *config[:5]
            )
            if prop_name not in property_configs:
                y_offset -= 2.54


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
                (font
                    (size {font_size} {font_size})
                )
                (justify left)
                {('(hide yes)' if hide else '')}
            )
        )
        """)


def write_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """
    Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    def write_arc(
            symbol_file: TextIO,
            start_x: float,
            mid_x: float,
            end_x: float
    ) -> None:
        """Write a single arc of the inductor symbol."""
        symbol_file.write(f"""
            (arc
                (start {start_x} 0.0056)
                (mid {mid_x} 1.27)
                (end {end_x} 0.0056)
                (stroke
                    (width 0.2032)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
            """)

    def write_pin(
            symbol_file: TextIO,
            x_pos: float,
            angle: int,
            number: str
    ) -> None:
        """Write a single pin of the inductor symbol."""
        symbol_file.write(f"""
            (pin unspecified line
                (at {x_pos} 0 {angle})
                (length 2.54)
                (name ""
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "{number}"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
            """)

    # Write symbol drawing section
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_1"\n')

    # Write arcs
    arc_params = [
        (-2.54, -3.81, -5.08),
        (0, -1.27, -2.54),
        (2.54, 1.27, 0),
        (5.08, 3.81, 2.54)
    ]
    for start_x, mid_x, end_x in arc_params:
        write_arc(symbol_file, start_x, mid_x, end_x)

    # Write pins
    write_pin(symbol_file, -7.62, 0, "1")
    write_pin(symbol_file, 7.62, 180, "2")

    symbol_file.write("\t\t)\n")
