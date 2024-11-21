"""
KiCad Symbol Generator

This module provides functionality to generate KiCad symbol files from CSV
data. It creates a symbol for electronic components, specifically tailored
for capacitors in this version, but can be extended for other components.

The main function, generate_kicad_symbol, reads data from a CSV file and
produces a .kicad_sym file with the symbol definition, including properties
and graphical representation.

Usage:
    python kicad_capacitor_symbol_generator.py

Or import and use the kicad_capacitor_symbol_generator
function in your own script.

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
    Generate a KiCad symbol file from CSV data.

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

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there's an error reading the CSV file.
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
    symbol_name = component_data['Symbol Name']
    write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name)


def write_symbol_header(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """
    Write the header for a single symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(f"""
        (symbol "{symbol_name}"
            (pin_names
                (offset 0.254)
            )
            (exclude_from_sim no)
            (in_bom yes)
            (on_board yes)
        """)


def write_properties(
        symbol_file: TextIO,
        component_data: Dict[str, str],
        property_order: List[str]
) -> None:
    """
    Write properties for a single symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        component_data (Dict[str, str]): Data for a single component.
        property_order (List[str]): Ordered list of property names.
    """
    property_configs = {
        "Reference": (2.54, 2.54, 1.27, False, False, "C"),
        "Value": (
            2.54, 0, 1.27, False, False,
            component_data.get('Resistance', '')),
        "Footprint": (2.54, -2.54, 1.27, True, True, None),
        "Datasheet": (2.54, -5.08, 1.27, True, True, None),
        "Description": (2.54, -7.62, 1.27, True, True, None)
    }

    y_offset = -10.16
    for prop_name in property_order:
        if prop_name in component_data:
            config = property_configs.get(
                prop_name,
                (2.54, y_offset, 1.27, True, True, None)
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
    Write the graphical representation of a symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(
        '\n'.join([
            f"\t\t(symbol \"{symbol_name}_0_1\"",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy -2.032 -0.762) (xy 2.032 -0.762)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.508)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy -2.032 0.762) (xy 2.032 0.762)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.508)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t)",
            f"\t\t(symbol \"{symbol_name}_1_1\"",
            "\t\t\t(pin passive line",
            "\t\t\t\t(at 0 3.81 270)",
            "\t\t\t\t(length 2.794)",
            "\t\t\t\t(name \"~\"",
            "\t\t\t\t\t(effects",
            "\t\t\t\t\t\t(font",
            "\t\t\t\t\t\t\t(size 1.27 1.27)",
            "\t\t\t\t\t\t)",
            "\t\t\t\t\t)",
            "\t\t\t\t)",
            "\t\t\t\t(number \"1\"",
            "\t\t\t\t\t(effects",
            "\t\t\t\t\t\t(font",
            "\t\t\t\t\t\t\t(size 1.27 1.27)",
            "\t\t\t\t\t\t)",
            "\t\t\t\t\t)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(pin passive line",
            "\t\t\t\t(at 0 -3.81 90)",
            "\t\t\t\t(length 2.794)",
            "\t\t\t\t(name \"~\"",
            "\t\t\t\t\t(effects",
            "\t\t\t\t\t\t(font",
            "\t\t\t\t\t\t\t(size 1.27 1.27)",
            "\t\t\t\t\t\t)",
            "\t\t\t\t\t)",
            "\t\t\t\t)",
            "\t\t\t\t(number \"2\"",
            "\t\t\t\t\t(effects",
            "\t\t\t\t\t\t(font",
            "\t\t\t\t\t\t\t(size 1.27 1.27)",
            "\t\t\t\t\t\t)",
            "\t\t\t\t\t)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t)",
            "\t)",
            ""
        ])
    )
