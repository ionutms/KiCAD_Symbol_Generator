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

from symbol_transformer_specs import SERIES_SPECS, SidePinConfig
from utilities import file_handler_utilities, symbol_utils


def generate_kicad_symbol(
        input_csv_file: str,
        output_symbol_file: str,
) -> None:
    """Generate a KiCad symbol file from CSV data for inductors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.

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


def convert_pin_config(
        spec_config: SidePinConfig,
) -> dict[str, list[dict[str, float | bool]]]:  # noqa: FA102
    """Convert a SidePinConfig from specs.

    Args:
        spec_config: Optional[SidePinConfig] from SERIES_SPECS

    Returns:
        Optional[Dict]:
            Pin configuration in the format expected by
            write_transformer_symbol_drawing.

    """
    return {
        "left": [{
            "number": pin.number,
            "y_pos": pin.y_pos,
            "pin_type": pin.pin_type,
            "lenght": pin.lenght,
            "hide": pin.hide} for pin in spec_config.left],
        "right": [{
            "number": pin.number,
            "y_pos": pin.y_pos,
            "pin_type": pin.pin_type,
            "lenght": pin.lenght,
            "hide": pin.hide} for pin in spec_config.right],
    }


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
    series = component_data.get("Series", "")

    # Get pin configuration from SERIES_SPECS if available
    series_spec = SERIES_SPECS.get(series)
    pin_config = convert_pin_config(series_spec.pin_config)

    symbol_utils.write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    symbol_utils.write_transformer_symbol_drawing(
        symbol_file, symbol_name, pin_config)
    symbol_file.write("    )\n")


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
        "Reference": (0, 7.62, 1.27, False, False, "T"),
        "Value": (
            0, -7.62, 1.27, False, False, component_data.get("MPN", "")),
        "Footprint": (0, -10.16, 1.27, True, True, None),
        "Datasheet": (0.254, -12.7, 1.27, True, True, None),
        "Description": (0, -15.24, 1.27, True, True, None),
    }

    y_offset = -17.78
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name, (0, y_offset, 1.27, True, True, None))
            value = config[5] or component_data[prop_name]
            symbol_utils.write_property(
                symbol_file, prop_name, value, *config[:5])
            if prop_name not in property_configs:
                y_offset -= 2.54
