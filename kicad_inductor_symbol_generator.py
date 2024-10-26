"""
KiCad Inductor Symbol Generator

This module provides functionality to generate KiCad symbol files from CSV
data for inductors. It creates symbol files with proper inductor properties
and graphical representation, including both horizontal and vertical layouts.

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
    common_properties = [
        "Symbol Name", "Reference", "Value", "Footprint", "Datasheet",
        "Description", "ki_keywords"
    ]
    return common_properties + \
        sorted(list(all_properties - set(common_properties)))


def write_header(
        symbol_file: TextIO
) -> None:
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
    write_symbol_drawing_horizontal(symbol_file, symbol_name)
    write_symbol_drawing_vertical(symbol_file, symbol_name)
    symbol_file.write("\t)\n")


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
    symbol_file.write(
        '\n'.join([
            f"\t(symbol \"{symbol_name}\"",
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
    property_configs = {
        "Reference": (0, 2.54, 1.27, False, False),
        "Value": (0, -2.54, 1.524, False, False),
        "Footprint": (0, -5.08, 1.27, True, True),
        "Datasheet": (0.254, -7.62, 1.27, True, True),
        "Description": (0, -10.16, 1.27, True, True),
        "ki_keywords": (0, 0, 1.27, True, False)
    }

    for property_name in property_order:
        if property_name in component_data:
            config = property_configs.get(
                property_name,
                (0, 0, 1.27, True, False)
            )
            write_property(
                symbol_file,
                property_name,
                component_data[property_name],
                *config
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
    """
    Write a single property for a symbol in the KiCad symbol file.

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
    symbol_file.write(
        '\n'.join([
            f"\t\t(property \"{property_name}\" \"{property_value}\"",
            f"\t\t\t(at {x_offset} {y_offset} 0)",
            f"\t\t\t{('(show_name)' if show_name else '')}",
            "\t\t\t(effects",
            "\t\t\t\t(font",
            f"\t\t\t\t\t(size {font_size} {font_size})",
            "\t\t\t\t)",
            "\t\t\t\t(justify left)",
            f"\t\t\t\t{('(hide yes)' if hide else '')}",
            "\t\t\t)",
            "\t\t)",
            ""
        ])
    )


def write_symbol_drawing_horizontal(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """
    Write the horizontal graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(
        '\n'.join([
            f"\t\t(symbol \"{symbol_name}_1_1\"",
            "\t\t\t(arc",
            "\t\t\t\t(start -2.54 0.0056)",
            "\t\t\t\t(mid -3.81 1.27)",
            "\t\t\t\t(end -5.08 0.0056)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(arc",
            "\t\t\t\t(start 0 0.0056)",
            "\t\t\t\t(mid -1.27 1.27)",
            "\t\t\t\t(end -2.54 0.0056)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(arc",
            "\t\t\t\t(start 2.54 0.0056)",
            "\t\t\t\t(mid 1.27 1.27)",
            "\t\t\t\t(end 0 0.0056)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(arc",
            "\t\t\t\t(start 5.08 0.0056)",
            "\t\t\t\t(mid 3.81 1.27)",
            "\t\t\t\t(end 2.54 0.0056)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(pin unspecified line",
            "\t\t\t\t(at -7.62 0 0)",
            "\t\t\t\t(length 2.54)",
            "\t\t\t\t(name \"\"",
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
            "\t\t\t(pin unspecified line",
            "\t\t\t\t(at 7.62 0 180)",
            "\t\t\t\t(length 2.54)",
            "\t\t\t\t(name \"\"",
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
            ""
        ])
    )


def write_symbol_drawing_vertical(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """
    Write the vertical graphical representation of an inductor symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(
        '\n'.join([
            f"\t\t(symbol \"{symbol_name}_1_2\"",
            "\t\t\t(arc",
            "\t\t\t\t(start -1.27 5.08)",
            "\t\t\t\t(mid -2.5344 3.81)",
            "\t\t\t\t(end -1.27 2.54)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(arc",
            "\t\t\t\t(start -1.27 7.62)",
            "\t\t\t\t(mid -2.5344 6.35)",
            "\t\t\t\t(end -1.27 5.08)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(arc",
            "\t\t\t\t(start -1.27 10.16)",
            "\t\t\t\t(mid -2.5344 8.89)",
            "\t\t\t\t(end -1.27 7.62)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(arc",
            "\t\t\t\t(start -1.27 12.7)",
            "\t\t\t\t(mid -2.5344 11.43)",
            "\t\t\t\t(end -1.27 10.16)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy 0 2.54) (xy -1.27 2.54)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy 0 5.08) (xy -1.27 5.08)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy 0 7.62) (xy -1.27 7.62)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy 0 10.16) (xy -1.27 10.16)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(polyline",
            "\t\t\t\t(pts",
            "\t\t\t\t\t(xy 0 12.7) (xy -1.27 12.7)",
            "\t\t\t\t)",
            "\t\t\t\t(stroke",
            "\t\t\t\t\t(width 0.2032)",
            "\t\t\t\t\t(type default)",
            "\t\t\t\t)",
            "\t\t\t\t(fill",
            "\t\t\t\t\t(type none)",
            "\t\t\t\t)",
            "\t\t\t)",
            "\t\t\t(pin unspecified line",
            "\t\t\t\t(at 0 15.24 270)",
            "\t\t\t\t(length 2.54)",
            "\t\t\t\t(name \"1\"",
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
            "\t\t\t(pin unspecified line",
            "\t\t\t\t(at 0 0 90)",
            "\t\t\t\t(length 2.54)",
            "\t\t\t\t(name \"2\"",
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
        ])
    )


if __name__ == "__main__":
    file_pairs = [
        ('inductors.csv', 'INDUCTORS_DATA_BASE.kicad_sym'),
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
