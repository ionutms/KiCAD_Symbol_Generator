"""KiCad Symbol Generator.

This module provides functionality to generate KiCad symbol files from CSV
data. It creates a symbol for electronic components, specifically tailored
for resistors in this version, but can be extended for other components.

The main function, generate_kicad_symbol, reads data from a CSV file and
produces a .kicad_sym file with the symbol definition, including properties
and graphical representation.

Usage:
    python kicad_symbol_generator.py

Or import and use the generate_kicad_symbol function in your own script.

Dependencies:
    - csv (Python standard library)
"""

from pathlib import Path
from typing import TextIO

from utilities import file_handler_utilities as fhu
from utilities import symbol_utils as su


def generate_kicad_symbol(
    input_csv_file: str, output_symbol_file: str, encoding: str = "utf-8",
) -> None:
    """Generate a KiCad symbol file from CSV data.

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
    component_data_list = fhu.read_csv_data(input_csv_file, encoding)
    all_properties = su.get_all_properties(component_data_list)

    with Path.open(output_symbol_file, "w", encoding=encoding) as symbol_file:
        su.write_header(symbol_file)
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
    symbol_name = component_data["Symbol Name"]
    su.write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write("    )")


def write_properties(
    symbol_file: TextIO,
    component_data: dict[str, str],
    property_order: list[str],
) -> None:
    """Write properties for a single symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.

    """
    property_configs = {
        "Reference": (0, 2.54, 1.27, False, False, "R"),
        "Value": (
            0, -2.54, 1.27, False, False,
            component_data.get("Resistance", "")),
        "Footprint": (0, -5.08, 1.27, True, True, None),
        "Datasheet": (0, -7.62, 1.27, True, True, None),
        "Description": (0, -10.16, 1.27, True, True, None),
    }

    y_offset = -12.7
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name, (0, y_offset, 1.27, True, True, None))
            value = config[5] or component_data[prop_name]
            su.write_property(symbol_file, prop_name, value, *config[:5])
            if prop_name not in property_configs:
                y_offset -= 2.54


def write_symbol_drawing(symbol_file: TextIO, symbol_name: str) -> None:
    """Write the graphical representation of a symbol in the KiCad file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.

    """
    symbol_file.write(f"""
        (symbol "{symbol_name}_0_1"
            (polyline
                (pts (xy 2.286 0) (xy 2.54 0))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts (xy -2.286 0) (xy -2.54 0))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy 0.762 0) (xy 1.143 1.016) (xy 1.524 0)
                    (xy 1.905 -1.016) (xy 2.286 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy -0.762 0) (xy -0.381 1.016) (xy 0 0)
                    (xy 0.381 -1.016) (xy 0.762 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
            (polyline
                (pts
                    (xy -2.286 0) (xy -1.905 1.016) (xy -1.524 0)
                    (xy -1.143 -1.016) (xy -0.762 0)
                )
                (stroke (width 0) (type default))
                (fill (type none))
            )
        )
        """)

    # Write pins
    su.write_pin(symbol_file, -5.08, 0, 0, "1")
    su.write_pin(symbol_file, 5.08, 0, 180, "2")
