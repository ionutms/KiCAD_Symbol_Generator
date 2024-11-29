"""KiCad Diode Symbol Generator.

This module provides functionality to generate KiCad symbol files from CSV
data for diodes. It creates symbol files with proper diode properties
and graphical representation in both horizontal and vertical layouts.

The main function, generate_kicad_symbol, reads data from a CSV file and
produces a .kicad_sym file with the symbol definition, including properties
and graphical representation.

Usage:
    python kicad_diode_symbol_generator.py

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
        encoding (str, optional):
            Character encoding to use. Defaults to 'utf-8'.

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there's an error reading the CSV file.
        IOError: If there's an error writing to the output file.

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
    if component_data.get("Diode Type") == "Schottky":
        symbol_utils.write_schottky_symbol_drawing(symbol_file, symbol_name)
    symbol_utils.write_zener_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write("\t)\n")


def write_properties(
        symbol_file: TextIO,
        component_data: dict[str, str],
        property_order: list[str],
) -> None:
    """Write properties for a single diode symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    """
    property_configs = {
        "Reference": (0, 2.54*2, 1.27, False, False, "D"),
        "Value": (0, -2.54*2, 1.27, True, True, None),
        "Footprint": (0, -2.54*3, 1.27, True, True, None),
        "Datasheet": (0, -2.54*4, 1.27, True, True, None),
        "Description": (0, -2.54*5, 1.27, True, True, None),
    }

    y_offset = -2.54*6
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (0, y_offset, 1.27, True, True, None))
            value = config[5] or component_data[prop_name]
            symbol_utils.write_property(
                symbol_file, prop_name, value, *config[:5])
            if prop_name not in property_configs:
                y_offset -= 2.54
