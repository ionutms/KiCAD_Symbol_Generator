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
    symbol file (.kicad_sym) with the component's properties and graphical
    representation.

    Args:
        input_csv_file (str):
            Path to the input CSV file containing component data.
            The CSV should have headers matching the expected property names.
        output_symbol_file (str):
            Path where the output .kicad_sym file will be saved.
        encoding (str):
            The character encoding to use for reading the CSV and
            writing the symbol file. Defaults to 'utf-8'.

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
        This function assumes the CSV file contains data for a single
        component and uses only the first data row.
    """
    with open(input_csv_file, 'r', encoding=encoding) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        component_data = next(csv_reader)  # Assume processing one row

    symbol_name = component_data['Symbol Name']

    with open(output_symbol_file, 'w', encoding=encoding) as symbol_file:
        symbol_file.write(
            f"""(kicad_symbol_lib
\t(version 20231120)
\t(generator "kicad_symbol_editor")
\t(generator_version "8.0")
\t(symbol "{symbol_name}"
\t\t(pin_numbers hide)
\t\t(pin_names
\t\t\t(offset 0)
\t\t)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
""")

        # Generate properties
        property_list = [
            ("Reference", component_data['Reference'], "2.54 1.27", "left",
             False),
            ("Value", component_data['Value'], "2.54 -1.27", "left", False),
            ("Footprint", component_data['Footprint'], "2.54 -8.89", "left",
             True),
            ("Datasheet", component_data['Datasheet'], "2.54 -3.81", "left",
             True),
            ("Description", component_data['Description'], "2.54 -6.35",
             "left", True),
            ("Manufacturer", component_data['Manufacturer'], "2.54 -11.43",
             "left", True),
            ("MPN", component_data['MPN'], "2.54 -13.97", "left", True),
            ("Tolerance", component_data['Tolerance'], "2.794 -16.51", "left",
             True),
            ("Voltage Rating", component_data['Voltage Rating'],
             "2.54 -19.05", "left", True),
        ]

        for property_name, property_value, position, justification, hidden \
                in property_list:
            symbol_file.write(
                f"""\t\t(property "{property_name}" "{property_value}"
\t\t\t(at {position} 0)
\t\t\t{"(show_name)" if hidden else ""}
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify {justification})
\t\t\t\t{"(hide yes)" if hidden else ""}
\t\t\t)
\t\t)
""")

        # Symbol drawing (simplified resistor symbol)
        symbol_file.write(
            f"""\t\t(symbol "{symbol_name}_0_1"
\t\t\t(polyline
\t\t\t\t(pts
\t\t\t\t\t(xy 0 -2.286) (xy 0 -2.54)
\t\t\t\t)
\t\t\t\t(stroke
\t\t\t\t\t(width 0)
\t\t\t\t\t(type default)
\t\t\t\t)
\t\t\t\t(fill
\t\t\t\t\t(type none)
\t\t\t\t)
\t\t\t)
\t\t\t(polyline
\t\t\t\t(pts
\t\t\t\t\t(xy 0 2.286) (xy 0 2.54)
\t\t\t\t)
\t\t\t\t(stroke
\t\t\t\t\t(width 0)
\t\t\t\t\t(type default)
\t\t\t\t)
\t\t\t\t(fill
\t\t\t\t\t(type none)
\t\t\t\t)
\t\t\t)
\t\t\t(polyline
\t\t\t\t(pts
\t\t\t\t\t(xy 0 -0.762) (xy 1.016 -1.143) (xy 0 -1.524) \
(xy -1.016 -1.905) (xy 0 -2.286)
\t\t\t\t)
\t\t\t\t(stroke
\t\t\t\t\t(width 0)
\t\t\t\t\t(type default)
\t\t\t\t)
\t\t\t\t(fill
\t\t\t\t\t(type none)
\t\t\t\t)
\t\t\t)
\t\t\t(polyline
\t\t\t\t(pts
\t\t\t\t\t(xy 0 0.762) (xy 1.016 0.381) (xy 0 0) (xy -1.016 -0.381) \
(xy 0 -0.762)
\t\t\t\t)
\t\t\t\t(stroke
\t\t\t\t\t(width 0)
\t\t\t\t\t(type default)
\t\t\t\t)
\t\t\t\t(fill
\t\t\t\t\t(type none)
\t\t\t\t)
\t\t\t)
\t\t\t(polyline
\t\t\t\t(pts
\t\t\t\t\t(xy 0 2.286) (xy 1.016 1.905) (xy 0 1.524) \
(xy -1.016 1.143) (xy 0 0.762)
\t\t\t\t)
\t\t\t\t(stroke
\t\t\t\t\t(width 0)
\t\t\t\t\t(type default)
\t\t\t\t)
\t\t\t\t(fill
\t\t\t\t\t(type none)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(symbol "{symbol_name}_1_1"
\t\t\t(pin passive line
\t\t\t\t(at 0 3.81 270)
\t\t\t\t(length 1.27)
\t\t\t\t(name "~"
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(number "1"
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t\t(pin passive line
\t\t\t\t(at 0 -3.81 90)
\t\t\t\t(length 1.27)
\t\t\t\t(name "~"
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t\t(number "2"
\t\t\t\t\t(effects
\t\t\t\t\t\t(font
\t\t\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t\t)
\t\t\t\t\t)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
)
""")


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
