"""
KiCad Connector Symbol Generator
Generates KiCad symbol files for connectors from CSV data.
Modified to match specific pin and field positioning requirements.
"""

import csv
from typing import List, Dict, TextIO


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
    component_data_list = read_csv_data(input_csv_file, encoding)
    all_properties = get_all_properties(component_data_list)
    property_order = get_property_order(all_properties)

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, property_order)
        symbol_file.write(")")


def read_csv_data(
        input_csv_file: str,
        encoding: str
) -> List[Dict[str, str]]:
    """Read component data from a CSV file."""
    with open(input_csv_file, 'r', encoding=encoding) as csv_file:
        return list(csv.DictReader(csv_file))


def get_all_properties(
        component_data_list: List[Dict[str, str]]
) -> set:
    """Get all unique properties from the component data."""
    return set().union(
        *(component_data.keys() for component_data in component_data_list))


def get_property_order(
        all_properties: set
) -> List[str]:
    """Define the standard order of properties."""
    common_properties = [
        "Symbol Name",
        "Reference",
        "Value",
        "Footprint",
        "Datasheet",
        "Description"
    ]
    remaining_props = sorted(list(all_properties - set(common_properties)))
    return common_properties + remaining_props


def write_header(
        symbol_file: TextIO
) -> None:
    """Write the KiCad symbol file header."""
    symbol_file.write(
        "(kicad_symbol_lib\n"
        "\t(version 20231120)\n"
        "\t(generator \"kicad_symbol_editor\")\n"
        "\t(generator_version \"8.0\")\n"
    )


def write_component(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """Write a complete component definition."""
    symbol_name = component_data.get('Symbol Name', '')
    write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name, component_data)
    symbol_file.write("\t)\n")


def write_symbol_header(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """Write the symbol header section."""
    header_lines = [
        f'\t(symbol "{symbol_name}"',
        "\t\t(pin_names",
        "\t\t\t(offset 1.016)",
        "\t\t)",
        "\t\t(exclude_from_sim no)",
        "\t\t(in_bom yes)",
        "\t\t(on_board yes)"
    ]
    symbol_file.write('\n'.join(header_lines) + '\n')


def write_properties(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """Write symbol properties with specific positioning."""
    property_configs = {
        "Reference": (0, 5.08, 1.27, False, False, "J"),
        "Value": (3.81, 2.54, 1.27, True, True, None),
        "Footprint": (3.81, 0, 1.27, True, True, None),
        "Datasheet": (3.81, -2.54, 1.27, True, True, None),
        "Description": (3.81, -5.08, 1.27, True, True, None),
    }

    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(prop_name)
            if config:
                value = config[5] or component_data[prop_name]
                write_property(
                    symbol_file,
                    prop_name,
                    value,
                    *config[:5]
                )


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
    """Write a property definition with specific formatting."""
    justify = "left bottom" if property_name == "Reference" else "left"

    property_lines = [
        f'\t\t(property "{property_name}" "{property_value}"',
        f"\t\t\t(at {x_offset} {y_offset} 0)",
        f"\t\t\t{('(show_name)' if show_name else '')}",
        "\t\t\t(effects",
        "\t\t\t\t(font",
        f"\t\t\t\t\t(size {font_size} {font_size})",
        "\t\t\t\t)",
        f"\t\t\t\t(justify {justify})",
        f"\t\t\t\t{('(hide yes)' if hide else '')}",
        "\t\t\t)",
        "\t\t)"
    ]
    symbol_file.write('\n'.join(property_lines) + '\n')


def write_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
        component_data: Dict[str, str]
) -> None:
    """Write the symbol drawing with specific dimensions."""
    num_pins = int(component_data.get('Pins', '2'))
    pin_spacing = 2.54  # Standard pin spacing in mm
    # Dynamic height based on pins
    rectangle_height = max(7.62, (num_pins * pin_spacing) + 2.54)

    # Write pins section
    symbol_file.write(f'\t\t(symbol "{symbol_name}_0_0"\n')

    # Calculate starting position for first pin
    start_y = (num_pins - 1) * pin_spacing / 2

    for pin_num in range(1, num_pins + 1):
        y_pos = start_y - (pin_num - 1) * pin_spacing
        write_pin(symbol_file, -5.08, y_pos, str(pin_num))

    symbol_file.write("\t\t)\n")

    # Write rectangle section
    symbol_file.write(f'\t\t(symbol "{symbol_name}_1_0"\n')
    write_rectangle(symbol_file, -2.54, rectangle_height /
                    2, 2.54, -rectangle_height/2)
    symbol_file.write("\t\t)\n")


def write_pin(
        file: TextIO,
        x_pos: float,
        y_pos: float,
        number: str
) -> None:
    """Write a pin definition with specific formatting."""
    pin_lines = [
        "\t\t\t(pin passive line",
        f"\t\t\t\t(at {x_pos} {y_pos} 0)",
        "\t\t\t\t(length 2.54)",
        f'\t\t\t\t(name "{number}"',
        "\t\t\t\t\t(effects",
        "\t\t\t\t\t\t(font",
        "\t\t\t\t\t\t\t(size 1.016 1.016)",
        "\t\t\t\t\t\t)",
        "\t\t\t\t\t)",
        "\t\t\t\t)",
        f'\t\t\t\t(number "{number}"',
        "\t\t\t\t\t(effects",
        "\t\t\t\t\t\t(font",
        "\t\t\t\t\t\t\t(size 1.016 1.016)",
        "\t\t\t\t\t\t)",
        "\t\t\t\t\t)",
        "\t\t\t\t)",
        "\t\t\t)"
    ]
    file.write('\n'.join(pin_lines) + '\n')


def write_rectangle(
        file: TextIO,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float
) -> None:
    """Write a rectangle definition with specific formatting."""
    rectangle_lines = [
        "\t\t\t(rectangle",
        f"\t\t\t\t(start {start_x} {start_y})",
        f"\t\t\t\t(end {end_x} {end_y})",
        "\t\t\t\t(stroke",
        "\t\t\t\t\t(width 0.254)",
        "\t\t\t\t\t(type solid)",
        "\t\t\t\t)",
        "\t\t\t\t(fill",
        "\t\t\t\t\t(type none)",
        "\t\t\t\t)",
        "\t\t\t)"
    ]
    file.write('\n'.join(rectangle_lines) + '\n')


if __name__ == "__main__":
    file_pairs = [
        ('connectors.csv', 'CONNECTORS_DATA_BASE.kicad_sym'),
    ]

    for input_csv, output_symbol in file_pairs:
        try:
            generate_kicad_symbol(input_csv, output_symbol)
            print(
                f"KiCad symbol file '{output_symbol}' generated successfully.")
        except FileNotFoundError:
            print(f"Error: Input CSV file '{input_csv}' not found.")
        except csv.Error as e:
            print(f"Error reading CSV file '{input_csv}': {e}")
        except IOError as e:
            print(f"Error writing to output file '{output_symbol}': {e}")
