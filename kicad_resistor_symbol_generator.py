"""
KiCad Symbol Generator

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

import csv


def generate_kicad_symbol(
        input_csv_file: str,
        output_symbol_file: str,
        encoding: str = 'utf-8') -> None:
    """
    Generate a KiCad symbol file from CSV data.

    This function reads component data from a CSV file and creates a KiCad
    symbol file (.kicad_sym) with the components' properties and graphical
    representations. It dynamically handles any properties present in the CSV.

    The function performs the following steps:
    1. Reads the CSV file and extracts component data.
    2. Determines all unique properties from the CSV.
    3. Generates a KiCad symbol file with:
       - Library version information
       - Symbol definitions for each component
       - Properties for each symbol (both visible and hidden)
       - Graphical representation of the symbol (resistor in this case)

    The generated symbols will have:
    - Hidden pin numbers
    - Visible property names for all properties (including hidden ones)
    - Hidden values for specific properties
        (e.g., Symbol Name, Footprint, Datasheet)
    - A simplified resistor symbol drawing

    Args:
        input_csv_file (str):
            Path to the input CSV file containing component data.
            The CSV should have headers matching the expected property names.
        output_symbol_file (str):
            Path where the output .kicad_sym file will be saved.
        encoding (str, optional):
            The character encoding to use for reading the CSV
            and writing the symbol file. Defaults to 'utf-8'.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input CSV file is not found.
        csv.Error: If there are issues reading the CSV file.
        IOError: If there are issues writing to the output file.
        UnicodeDecodeError:
            If there are encoding-related issues when reading the CSV file.
        UnicodeEncodeError:
            If there are encoding-related issues when writing the symbol file.

    Note:
        - The function assumes a specific set of common properties
            (Symbol Name, Reference, Value, Footprint, Datasheet)
            but can handle additional properties from the CSV.
        - The symbol drawing is currently set for a resistor and would
            need modification for other component types.
        - Property visibility is determined by the 'common_properties'
            list within the function.
    """
    with open(input_csv_file, 'r', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        component_data_list = list(csv_reader)

    # Get all unique property names from the CSV
    all_properties = set()
    for component_data in component_data_list:
        all_properties.update(component_data.keys())

    # Define the order and visibility of common properties
    common_properties = [
        ("Symbol Name", True),
        ("Reference", False),
        ("Value", False),
        ("Footprint", True),
        ("Datasheet", True),
    ]

    # Create a list of all properties in order, with common ones first
    property_order = [prop for prop, _ in common_properties] + \
        sorted(
            list(all_properties - set(prop for prop, _ in common_properties)))

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        symbol_file.write(
            '\n'.join([
                "(kicad_symbol_lib",
                "\t(version 20231120)",
                "\t(generator \"kicad_symbol_editor\")",
                "\t(generator_version \"8.0\")",
                ""
            ])
        )

        for component_data in component_data_list:
            symbol_name = component_data['Symbol Name']

            symbol_file.write(
                '\n'.join([
                    f"\t(symbol \"{symbol_name}\"",
                    "\t\t(pin_numbers hide)",
                    "\t\t(pin_names",
                    "\t\t\t(offset 0)",
                    "\t\t)",
                    "\t\t(exclude_from_sim no)",
                    "\t\t(in_bom yes)",
                    "\t\t(on_board yes)",
                    ""
                ])
            )

            # Generate properties
            y_offset = 1.27
            for property_name in property_order:
                if property_name in component_data:
                    property_value = component_data[property_name]
                    is_common = any(
                        prop == property_name for prop, _ in common_properties)
                    hidden = not is_common or any(
                        prop == property_name and hide for
                        prop, hide in common_properties)

                    symbol_file.write(
                        '\n'.join([
                            f"\t\t(property \"{property_name}\" " +
                            f"\"{property_value}\"",
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
                    y_offset += 2.54

            # Symbol drawing (simplified resistor symbol)
            symbol_file.write(
                '\n'.join([
                    f"\t\t(symbol \"{symbol_name}_0_1\"",
                    "\t\t\t(polyline",
                    "\t\t\t\t(pts",
                    "\t\t\t\t\t(xy 0 -2.286) (xy 0 -2.54)",
                    "\t\t\t\t)",
                    "\t\t\t\t(stroke (width 0) (type default))",
                    "\t\t\t\t(fill (type none))",
                    "\t\t\t)",
                    "\t\t\t(polyline",
                    "\t\t\t\t(pts",
                    "\t\t\t\t\t(xy 0 2.286) (xy 0 2.54)",
                    "\t\t\t\t)",
                    "\t\t\t\t(stroke (width 0) (type default))",
                    "\t\t\t\t(fill (type none))",
                    "\t\t\t)",
                    "\t\t\t(polyline",
                    "\t\t\t\t(pts",
                    "\t\t\t\t\t(xy 0 -0.762) (xy 1.016 -1.143) " +
                    "(xy 0 -1.524) (xy -1.016 -1.905) (xy 0 -2.286)",
                    "\t\t\t\t)",
                    "\t\t\t\t(stroke (width 0) (type default))",
                    "\t\t\t\t(fill (type none))",
                    "\t\t\t)",
                    "\t\t\t(polyline",
                    "\t\t\t\t(pts",
                    "\t\t\t\t\t(xy 0 0.762) (xy 1.016 0.381) (xy 0 0) " +
                    "(xy -1.016 -0.381) (xy 0 -0.762)",
                    "\t\t\t\t)",
                    "\t\t\t\t(stroke (width 0) (type default))",
                    "\t\t\t\t(fill (type none))",
                    "\t\t\t)",
                    "\t\t\t(polyline",
                    "\t\t\t\t(pts",
                    "\t\t\t\t\t(xy 0 2.286) (xy 1.016 1.905) (xy 0 1.524) "
                    + "(xy -1.016 1.143) (xy 0 0.762)",
                    "\t\t\t\t)",
                    "\t\t\t\t(stroke (width 0) (type default))",
                    "\t\t\t\t(fill (type none))",
                    "\t\t\t)",
                    "\t\t)",
                    f"\t\t(symbol \"{symbol_name}_1_1\"",
                    "\t\t\t(pin passive line (at 0 3.81 270) (length 1.27)",
                    "\t\t\t\t(name \"~\" (effects (font (size 1.27 1.27))))",
                    "\t\t\t\t(number \"1\" (effects (font (size 1.27 1.27))))",
                    "\t\t\t)",
                    "\t\t\t(pin passive line (at 0 -3.81 90) (length 1.27)",
                    "\t\t\t\t(name \"~\" (effects (font (size 1.27 1.27))))",
                    "\t\t\t\t(number \"2\" (effects (font (size 1.27 1.27))))",
                    "\t\t\t)",
                    "\t\t)",
                    "\t)",
                    ""
                ])
            )

        symbol_file.write(")")


if __name__ == "__main__":
    INPUT_CSV_FILE = 'resistor.csv'
    OUTPUT_SYMBOL_FILE = 'RESISTORS_DATA_BASE.kicad_sym'

    try:
        generate_kicad_symbol(INPUT_CSV_FILE, OUTPUT_SYMBOL_FILE)
        print("KiCad symbol file generated successfully.")
    except FileNotFoundError:
        print(f"Error: Input CSV file '{INPUT_CSV_FILE}' not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    except IOError as e:
        print(f"Error writing to output file: {e}")
