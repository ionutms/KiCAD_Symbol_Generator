"""
KiCad Capacitor Symbol Generator

This module provides functionality to generate KiCad symbol files from CSV
data specifically for capacitors. It creates a symbol file (.kicad_sym) with
capacitor properties and graphical representations based on the input data.

The main function, generate_kicad_capacitor_symbol, reads capacitor data from
a CSV file and produces a .kicad_sym file with the symbol definitions,
including properties and graphical representations for each capacitor.

Usage:
    python kicad_capacitor_symbol_generator.py

Or import and use the generate_kicad_capacitor_symbol function in your script.

Dependencies:
    - csv (Python standard library)
"""

import csv
from typing import List, Tuple, Dict, TextIO


def generate_kicad_capacitor_symbol(
        input_csv_file: str,
        output_symbol_file: str,
        encoding: str = 'utf-8') -> None:
    """
    Generate a KiCad symbol file for capacitors from CSV data.

    This function reads capacitor data from a CSV file and creates a KiCad
    symbol file (.kicad_sym) with the capacitors' properties and graphical
    representations. It dynamically handles any properties present in the CSV.

    Args:
        input_csv_file (str):
            Path to the input CSV file containing capacitor data.
        output_symbol_file (str):
            Path where the output .kicad_sym file will be saved.
        encoding (str): The character encoding to use. Defaults to 'utf-8'.

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there are issues reading the CSV file.
        IOError: If there are issues writing to the output file.
    """
    component_data_list = read_csv_data(input_csv_file, encoding)
    all_properties = get_all_properties(component_data_list)
    property_order = get_property_order(all_properties)

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        write_header(symbol_file)
        for component_data in component_data_list:
            write_component(symbol_file, component_data, property_order)
        symbol_file.write(")")


def read_csv_data(input_csv_file: str, encoding: str) -> List[Dict[str, str]]:
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


def get_all_properties(component_data_list: List[Dict[str, str]]) -> set:
    """
    Get all unique properties from the component data.

    Args:
        component_data_list (List[Dict[str, str]]): List of component data.

    Returns:
        set: Set of all unique property names.
    """
    return set().union(
        *(component_data.keys() for component_data in component_data_list))


def get_property_order(all_properties: set) -> List[str]:
    """
    Determine the order of properties for symbol generation.

    Args:
        all_properties (set): Set of all unique property names.

    Returns:
        List[str]: Ordered list of property names.
    """
    common_properties = [
        "Symbol Name", "Reference", "Value", "Footprint", "Datasheet"
    ]
    return common_properties + \
        sorted(list(all_properties - set(common_properties)))


def write_header(symbol_file: TextIO) -> None:
    """
    Write the header of the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
    """
    symbol_file.write(
        '\n'.join([
            "(kicad_symbol_lib",
            "\t(version 20231120)",
            "\t(generator \"kicad_symbol_editor\")",
            "\t(generator_version \"8.0\")",
            ""
        ])
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
    symbol_name = component_data['Symbol Name']
    write_symbol_header(symbol_file, symbol_name)
    write_properties(symbol_file, component_data, property_order)
    write_symbol_drawing(symbol_file, symbol_name)


def write_symbol_header(symbol_file: TextIO, symbol_name: str) -> None:
    """
    Write the header for a single symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(
        '\n'.join([
            f"\t(symbol \"{symbol_name}\"",
            "\t\t(pin_numbers hide)",
            "\t\t(pin_names",
            "\t\t\t(offset 0.254)",
            "\t\t)",
            "\t\t(exclude_from_sim no)",
            "\t\t(in_bom yes)",
            "\t\t(on_board yes)",
            ""
        ])
    )


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
    common_properties = [
        ("Symbol Name", True),
        ("Reference", False),
        ("Value", False),
        ("Footprint", True),
        ("Datasheet", True),
    ]
    y_offset = 1.27
    for property_name in property_order:
        if property_name in component_data:
            write_property(
                symbol_file, property_name, component_data[property_name],
                y_offset, common_properties)
            y_offset += 2.54


def write_property(
    symbol_file: TextIO,
    property_name: str,
    property_value: str,
    y_offset: float,
    common_properties: List[Tuple[str, bool]]
) -> None:
    """
    Write a single property for a symbol in the KiCad symbol file.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        property_name (str): Name of the property.
        property_value (str): Value of the property.
        y_offset (float): Vertical offset for property placement.
        common_properties (List[Tuple[str, bool]]): List of common properties.
    """
    is_common = any(prop == property_name for prop, _ in common_properties)
    hidden = not is_common or any(
        prop == property_name and hide for prop, hide in common_properties)
    symbol_file.write(
        '\n'.join([
            f"\t\t(property \"{property_name}\" \"{property_value}\"",
            f"\t\t\t(at 2.54 {-y_offset} 0)",
            "\t\t\t(effects",
            "\t\t\t\t(font",
            "\t\t\t\t\t(size 1.27 1.27)",
            "\t\t\t\t)",
            "\t\t\t\t(justify left)",
            f"\t\t\t\t{('(hide yes)' if hidden else '')}",
            "\t\t\t)",
            f"\t\t\t(show_name {'yes' if hidden else 'no'})",
            "\t\t)",
            ""
        ])
    )


def write_symbol_drawing(symbol_file: TextIO, symbol_name: str) -> None:
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


if __name__ == "__main__":
    INPUT_CSV_FILE = 'capacitor.csv'
    OUTPUT_SYMBOL_FILE = 'CAPACITORS_DATA_BASE.kicad_sym'

    try:
        generate_kicad_capacitor_symbol(INPUT_CSV_FILE, OUTPUT_SYMBOL_FILE)
        print("KiCad capacitor symbol file generated successfully.")
    except FileNotFoundError:
        print(f"Error: Input CSV file '{INPUT_CSV_FILE}' not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    except IOError as e:
        print(f"Error writing to output file: {e}")
