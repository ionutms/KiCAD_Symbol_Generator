"""
KiCad Connector Symbol Generator
Generates KiCad symbol files for connectors from CSV data.
Modified to match specific pin and field positioning requirements.
"""

import re
from typing import List, Dict, TextIO
import symbol_utils as su
import file_handler_utilities as fhu


def generate_kicad_symbol(
        input_csv_file: str,
        output_symbol_file: str,
        encoding: str = 'utf-8'
) -> None:
    """
    Generate a KiCad symbol file from CSV data for connectors.

    Args:
        input_csv_file (str): Path to the input CSV file with component data.
        output_symbol_file (str): Path for the output .kicad_sym file.
        encoding (str, optional):
            Character encoding to use. Defaults to 'utf-8'.
    """
    component_data_list = fhu.read_csv_data(input_csv_file, encoding)
    all_properties = su.get_all_properties(component_data_list)

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        su.write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, all_properties)
        symbol_file.write(")")


def write_component(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """Write a complete component definition."""
    symbol_name = component_data.get('Symbol Name', '')
    su.write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name, component_data)
    symbol_file.write("\t)\n")


def write_properties(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """
    Write all symbol properties with positions adjusted for variable pin count.
    """
    property_configs = {
        "Reference": (0, 7.62, 1.27, False, False, "J"),
        "Value": (5.08, 5.08, 1.27, True, True, component_data.get('MPN', '')),
        "Footprint": (5.08, 2.54, 1.27, True, True, None),
        "Datasheet": (5.08, 0, 1.27, True, True, None),
        "Description": (5.08, -2.54, 1.27, True, True, None),
    }

    y_offset = -5.08
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (5.08, y_offset, 1.27, True, True, None)
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
        component_data: Dict[str, str]
) -> None:
    """Write the symbol drawing with dimensions adjusted for pin count."""
    # Extract pin count using regex
    value = component_data.get('Value', '')
    pin_count_match = re.search(r'-(\d+)BE', value)
    pin_count = int(pin_count_match.group(1)) if pin_count_match else 2

    pin_spacing = 2.54  # Standard pin spacing in mm

    # Calculate rectangle dimensions based on pin count
    min_height = 7.62  # Minimum rectangle height
    calculated_height = (pin_count * pin_spacing) + 2.54  # Add margin
    rectangle_height = max(min_height, calculated_height)

    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    start_y = (pin_count - 1) * pin_spacing / 2

    for pin_num in range(1, pin_count + 1):
        y_pos = start_y - (pin_num - 1) * pin_spacing
        su.write_pin(symbol_file, -5.08, y_pos, 0, str(pin_num))

    symbol_file.write("\t\t)\n")

    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    write_rectangle(
        symbol_file, -2.54, rectangle_height / 2, 2.54, -rectangle_height/2)
    symbol_file.write("\t\t)\n")


def write_rectangle(
        symbol_file: TextIO,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float
) -> None:
    """Write a rectangle definition with specific formatting."""
    symbol_file.write(f"""
        (rectangle
            (start {start_x} {start_y})
            (end {end_x} {end_y})
            (stroke (width 0.254) (type solid) )
            (fill (type none) )
        )
        """)
