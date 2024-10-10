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


def generate_kicad_capacitor_symbol(
        input_csv_file: str,
        output_symbol_file: str,
        encoding: str = 'utf-8') -> None:
    """
    Generate a KiCad symbol file for capacitors from CSV data.

    This function reads capacitor data from a CSV file and creates a KiCad
    symbol file (.kicad_sym) with the capacitors' properties and graphical
    representations.

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
    with open(input_csv_file, 'r', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        component_data_list = list(csv_reader)

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
                    "\t\t\t(offset 0.254)",
                    "\t\t)",
                    "\t\t(exclude_from_sim no)",
                    "\t\t(in_bom yes)",
                    "\t\t(on_board yes)",
                    ""
                ])
            )

            # Generate properties
            property_list = [
                ("Reference",
                 component_data['Reference'], "2.54 1.27",
                 "left", False),
                ("Value", component_data['Value'], "2.54 -1.27",
                 "left", False),
                ("Footprint", component_data['Footprint'], "2.54 -8.89",
                 "left", True),
                ("Datasheet", component_data['Datasheet'], "2.54 -3.81",
                 "left", True),
                ("Description", component_data['Description'], "2.54 -6.35",
                 "left", True),
                ("MPN", component_data['MPN'], "2.54 -11.43", "left", True),
                ("Voltage Rating DC", component_data['Voltage Rating DC'],
                 "2.54 -13.97", "left", True),
                ("Tolerance", component_data['Tolerance'], "2.54 -16.51",
                 "left", True),
            ]

            for property_name, property_value, position, justification, \
                    hidden in property_list:
                symbol_file.write(
                    '\n'.join([
                        f"\t\t(property \"{property_name}\" " +
                        f"\"{property_value}\"",
                        f"\t\t\t(at {position} 0)",
                        f"\t\t\t{('(show_name)' if hidden else '')}",
                        "\t\t\t(effects",
                        "\t\t\t\t(font",
                        "\t\t\t\t\t(size 1.27 1.27)",
                        "\t\t\t\t)",
                        f"\t\t\t\t(justify {justification})",
                        f"\t\t\t\t{('(hide yes)' if hidden else '')}",
                        "\t\t\t)",
                        "\t\t)",
                        ""
                    ])
                )

            # Symbol drawing (capacitor symbol)
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

        symbol_file.write(")")


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
