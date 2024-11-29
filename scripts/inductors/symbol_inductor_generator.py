"""KiCad Inductor Symbol Generator.

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

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
    input_csv_file: str,
    output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.

    """
    component_data_list = file_handler_utilities.read_csv_data(input_csv_file)
    all_properties = symbol_utils.get_all_properties(component_data_list)

    with Path.open(output_symbol_file, "w", encoding="utf-8") as symbol_file:
        symbol_utils.write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def write_component(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write a single component to the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    """
    symbol_name = component_data.get("Symbol Name", "")
    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write("\t)\n")


def write_properties(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write properties for a single symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    """
    property_configs = {
        "Reference": (0, 2.54, 1.27, False, False, "L"),
        "Value": (
            0, -2.54, 1.27, False, False,
            component_data.get("Inductance", "")),
        "Footprint": (0, -5.08, 1.27, True, True, None),
        "Datasheet": (0.254, -7.62, 1.27, True, True, None),
        "Description": (0, -10.16, 1.27, True, True, None),
    }

    y_offset = -12.7
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name, (0, y_offset, 1.27, True, True, None))
            value = config[5] or component_data[prop_name]
            symbol_utils.write_property(
                symbol_file, prop_name, value, *config[:5])
            if prop_name not in property_configs:
                y_offset -= 2.54


def write_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
) -> None:
    """Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """

    def write_arc(
        symbol_file: TextIO,
        start_x: float,
        mid_x: float,
        end_x: float,
    ) -> None:
        """Write a single arc of the inductor symbol."""
        symbol_file.write(f"""
            (arc
                (start {start_x} 0.0056)
                (mid {mid_x} 1.27)
                (end {end_x} 0.0056)
                (stroke (width 0.2032) (type default))
                (fill (type none))
            )
            """)

    # Write symbol drawing section
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_1"\n')

    # Write arcs
    arc_params = [
        (-2.54, -3.81, -5.08),
        (0, -1.27, -2.54),
        (2.54, 1.27, 0),
        (5.08, 3.81, 2.54),
    ]
    for start_x, mid_x, end_x in arc_params:
        write_arc(symbol_file, start_x, mid_x, end_x)

    # Write pins
    symbol_utils.write_pin(symbol_file, -7.62, 0, 0, "1")
    symbol_utils.write_pin(symbol_file, 7.62, 0, 180, "2")

    symbol_file.write("\t\t)\n")
