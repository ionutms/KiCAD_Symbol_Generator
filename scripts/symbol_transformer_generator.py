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

from typing import List, Dict, TextIO
from symbol_transformer_specs import SERIES_SPECS, SidePinConfig
import symbol_utils as su
import file_handler_utilities as fhu


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
    component_data_list = fhu.read_csv_data(input_csv_file, encoding)
    all_properties = su.get_all_properties(component_data_list)

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        su.write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def convert_pin_config(
        spec_config: SidePinConfig
) -> Dict[str, List[Dict[str, float | bool]]]:
    """
    Convert a SidePinConfig from specs into the format expected
    by the symbol generator.

    Args:
        spec_config: Optional[SidePinConfig] from SERIES_SPECS

    Returns:
        Optional[Dict]:
            Pin configuration in the format expected by write_symbol_drawing
    """
    return {
        "left": [{
            "number": pin.number,
            "y_pos": pin.y_pos,
            "pin_type": pin.pin_type,
            "lenght": pin.lenght,
            "hide": pin.hide
        } for pin in spec_config.left],
        "right": [{
            "number": pin.number,
            "y_pos": pin.y_pos,
            "pin_type": pin.pin_type,
            "lenght": pin.lenght,
            "hide": pin.hide
        } for pin in spec_config.right]
    }


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
    series = component_data.get('Series', '')

    # Get pin configuration from SERIES_SPECS if available
    series_spec = SERIES_SPECS.get(series)
    pin_config = convert_pin_config(series_spec.pin_config)

    su.write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name, pin_config)
    symbol_file.write("    )\n")


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
        "Reference": (0, 7.62, 1.27, False, False, "T"),
        "Value": (0, -7.62, 1.27, False, False, component_data.get('MPN', '')),
        "Footprint": (0, -10.16, 1.27, True, True, None),
        "Datasheet": (0.254, -12.7, 1.27, True, True, None),
        "Description": (0, -15.24, 1.27, True, True, None)
    }

    y_offset = -17.78
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (0, y_offset, 1.27, True, True, None)
            )
            value = config[5] or component_data[prop_name]
            su.write_property(
                symbol_file,
                prop_name,
                value,
                *config[:5]
            )
            if prop_name not in property_configs:
                y_offset -= 2.54


def write_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
        pin_config: dict
) -> None:
    """
    Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.
    """
    def get_symbol_bounds(pin_config):
        """Calculate symbol bounds based on pin configuration."""
        y_positions = (
            [pin["y_pos"] for pin in pin_config["left"]] +
            [pin["y_pos"] for pin in pin_config["right"]]
        )
        max_y = max(y_positions)
        min_y = min(y_positions)
        return min_y, max_y

    # Calculate symbol bounds
    min_y, max_y = get_symbol_bounds(pin_config)

    # Write symbol drawing section - split into two units
    symbol_file.write(f'        (symbol "{symbol_name}_0_1"\n')

    # Write left inductor arcs
    for y_start in range(0, 4):
        symbol_file.write(f"""
            (arc
                (start -2.54 {-5.08 + (y_start * 2.54)})
                (mid -1.27 {-3.81 + (y_start * 2.54)})
                (end -2.54 {-2.54 + (y_start * 2.54)})
                (stroke (width 0) (type default) )
                (fill (type none) )
            )
            """)

    # Write right inductor arcs
    for y_start in range(0, 4):
        symbol_file.write(f"""
            (arc
                (start 2.54 {5.08 - (y_start * 2.54)})
                (mid 1.27 {3.81 - (y_start * 2.54)})
                (end 2.54 {2.54 - (y_start * 2.54)})
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write polarity dots
    for x, y in [(-2.54, 3.81), (2.54, -3.81)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts (xy {x} {max_y}) (xy {x} {min_y}))
                (stroke (width 0) (type default))
                (fill (type none))
            )
            """)

    # Write left side pins
    for pin in pin_config["left"]:
        su.write_pin(
            symbol_file, -7.62, pin["y_pos"], 0, pin["number"],
            pin["pin_type"], pin.get("hide", False), pin["lenght"])

    # Write right side pins
    for pin in pin_config["right"]:
        su.write_pin(
            symbol_file, 7.62, pin["y_pos"], 180, pin["number"],
            pin["pin_type"], pin.get("hide", False), pin["lenght"])

    symbol_file.write("        )\n")
