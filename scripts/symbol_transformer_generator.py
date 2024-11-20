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


def get_property_order(
        all_properties: set
) -> List[str]:
    """
    Determine the order of properties for symbol generation.

    Args:
        all_properties (set): Set of all unique property names.

    Returns:
        List[str]: Ordered list of property names.
    """
    # Define the order of common properties
    common_properties = [
        "Symbol Name",
        "Reference",
        "Value",
        "Footprint",
        "Datasheet",
        "Description",
        "Octopart Search",
        "MPN",
        "Manufacturer",
        "DCR Max",
        "Series",
        "Height",
        "Tolerance",
        "Idc Rated",
        "Idc Saturated",
        "Inductance"
    ]
    # Return ordered properties list
    remaining_props = sorted(list(all_properties - set(common_properties)))
    return common_properties + remaining_props


def write_header(
        symbol_file: TextIO
) -> None:
    """
    Write the header of the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
    """
    symbol_file.write(
        "(kicad_symbol_lib\n"
        "    (version 20231120)\n"
        "    (generator \"kicad_symbol_editor\")\n"
        "    (generator_version \"8.0\")\n"
    )


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
    write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name)
    symbol_file.write("    )\n")


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
    header_lines = [
        f'    (symbol "{symbol_name}"',
        "        (pin_names",
        "            (offset 0.254)",
        "        )",
        "        (exclude_from_sim no)",
        "        (in_bom yes)",
        "        (on_board yes)"
    ]
    symbol_file.write('\n'.join(header_lines) + '\n')


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
        "Value": (
            0, -7.62, 1.524, False, False,
            component_data.get('Inductance', '')
            ),
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
    property_lines = [
        f'        (property "{property_name}" "{property_value}"',
        f"            (at {x_offset} {y_offset} 0)",
        f"            {('(show_name)' if show_name else '')}",
        "            (effects",
        "                (font",
        f"                    (size {font_size} {font_size})",
        "                )",
        "                (justify left)",
        f"                {('(hide yes)' if hide else '')}",
        "            )",
        "        )"
    ]
    symbol_file.write('\n'.join(property_lines) + '\n')


def write_symbol_drawing(
        symbol_file: TextIO,
        symbol_name: str,
        pin_config: dict = None
) -> None:
    """
    Write the horizontal graphical representation of a transformer symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
        pin_config (dict, optional): Dictionary defining pin configuration.
    """
    # Default 8-pin configuration if none provided
    if pin_config is None:
        pin_config = {
            "left": [
                {"number": "1", "y_pos": 5.08, "type": "unspecified"},
                {"number": "2", "y_pos": 2.54, "type": "no_connect",
                 "hide": True},
                {"number": "3", "y_pos": -2.54, "type": "no_connect",
                 "hide": True},
                {"number": "4", "y_pos": -5.08, "type": "unspecified"}
            ],
            "right": [
                {"number": "5", "y_pos": 5.08, "type": "unspecified"},
                {"number": "6", "y_pos": 2.54, "type": "no_connect",
                 "hide": True},
                {"number": "7", "y_pos": -2.54, "type": "no_connect",
                 "hide": True},
                {"number": "8", "y_pos": -5.08, "type": "unspecified"}
            ]
        }

    def write_pin(
            file: TextIO,
            x_pos: float,
            y_pos: float,
            angle: int,
            number: str,
            pin_type: str = "unspecified",
            hide: bool = False,
            length: float = 2.54
    ) -> None:
        """Write a single pin of the transformer symbol."""
        pin_lines = [
            f"            (pin {pin_type} line",
            f"                (at {x_pos} {y_pos} {angle})",
            f"                (length {length})",
            '                (name ""',
            "                    (effects",
            "                        (font",
            "                            (size 1.27 1.27)",
            "                        )",
            "                    )",
            "                )",
            f'                (number "{number}"',
            "                    (effects",
            "                        (font",
            "                            (size 1.27 1.27)",
            "                        )",
            "                    )",
            "                )",
            f"                {('hide' if hide else '')}",
            "            )"
        ]
        file.write('\n'.join(pin_lines) + '\n')

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
        symbol_file.write(
            '            (arc'
            f'                (start -2.54 {-5.08 + (y_start * 2.54)})'
            f'                (mid -1.27 {-3.81 + (y_start * 2.54)})'
            f'                (end -2.54 {-2.54 + (y_start * 2.54)})'
            '                (stroke'
            '                    (width 0)'
            '                    (type default)'
            '                )'
            '                (fill'
            '                    (type none)'
            '                )'
            '            )'
        )

    # Write right inductor arcs
    for y_start in range(0, 4):
        symbol_file.write(f"""
            (arc
                (start 2.54 {5.08 - (y_start * 2.54)})
                (mid 1.27 {3.81 - (y_start * 2.54)})
                (end 2.54 {2.54 - (y_start * 2.54)})
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )""")

    # Write polarity dots
    for x, y in [(-2.54, 3.81), (2.54, -3.81)]:
        symbol_file.write(f"""
            (circle
                (center {x} {y})
                (radius 0.508)
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )""")

    # Write coupling lines
    for x in [-0.254, 0.254]:
        symbol_file.write(f"""
            (polyline
                (pts
                    (xy {x} {max_y}) (xy {x} {min_y})
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )""")

    # Write connection lines for active pins
    active_pins = {
        "left": [p for p in pin_config["left"] if p["type"] == "unspecified"],
        "right": [p for p in pin_config["right"] if p["type"] == "unspecified"]
    }

    for side, pins in active_pins.items():
        x1, x2 = (-2.54, -5.08) if side == "left" else (2.54, 5.08)
        for pin in pins:
            symbol_file.write(f"""
                (polyline
                    (pts
                        (xy {x1} {pin["y_pos"]}) (xy {x2} {pin["y_pos"]})
                    )
                    (stroke
                        (width 0)
                        (type default)
                    )
                    (fill
                        (type none)
                    )
                )""")

    symbol_file.write("        )\n")

    # Write second unit with pins
    symbol_file.write(f'        (symbol "{symbol_name}_1_1"\n')

    # Write left side pins
    for pin in pin_config["left"]:
        write_pin(
            symbol_file,
            -7.62,
            pin["y_pos"],
            0,
            pin["number"],
            pin["type"],
            pin.get("hide", False)
        )

    # Write right side pins
    for pin in pin_config["right"]:
        write_pin(
            symbol_file,
            7.62,
            pin["y_pos"],
            180,
            pin["number"],
            pin["type"],
            pin.get("hide", False)
        )

    symbol_file.write("        )\n")
