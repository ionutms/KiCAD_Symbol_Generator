"""
Connector Series Part Number Generator

Generates part numbers and specifications for connector series
with different pin counts.
Generates both individual series files and unified component database.
"""

import os
import csv
from typing import Final, List
from colorama import init, Fore, Style
import symbol_connector_generator as sym_con_gen
import kicad_connector_footprint_generator as kco_fg
import symbol_connectors_specs as sym_con_spec
import file_handler_utilities as utils

init(autoreset=True)


def print_success(message: str) -> None:
    """Print a success message in green."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Print an error message in red."""
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Print an info message in yellow."""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")


def generate_part_numbers(
        specs: sym_con_spec.SeriesSpec
) -> List[sym_con_spec.PartInfo]:
    """
    Generate all part numbers for the series.

    Args:
        specs: Series specifications

    Returns:
        List of PartInfo instances
    """
    return [
        sym_con_spec.create_part_info(pin_count, specs)
        for pin_count in specs.pin_counts
    ]


# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    'Symbol Name': lambda part: part.symbol_name,
    'Reference': lambda part: part.reference,
    'Value': lambda part: part.value,
    'Footprint': lambda part: part.footprint,
    'Datasheet': lambda part: part.datasheet,
    'Description': lambda part: part.description,
    'Manufacturer': lambda part: part.manufacturer,
    'MPN': lambda part: part.mpn,
    'Series': lambda part: part.series,
    'Trustedparts Search': lambda part: part.trustedparts_link,
    'Color': lambda part: part.color,
    'Pitch (mm)': lambda part: part.pitch,
    'Pin Count': lambda part: part.pin_count,
    'Mounting Angle': lambda part: part.mounting_angle,
    'Current Rating (A)': lambda part: part.current_rating,
    'Voltage Rating (V)': lambda part: part.voltage_rating,
    'Mounting Style': lambda part: part.mounting_style,
    'Contact Plating': lambda part: part.contact_plating
}


def generate_footprints_for_series(
        parts_list: List[sym_con_spec.PartInfo]
) -> None:
    """Generate footprint files for all parts in a series."""
    os.makedirs("connector_footprints.pretty", exist_ok=True)

    for part in parts_list:
        try:
            kco_fg.generate_footprint_file(part)
            print_success(
                f"Generated footprint file for {part.mpn}"
            )
        except ValueError as e:
            print_error(f"Error generating footprint: {e}")
        except IOError as e:
            print_error(f"I/O error generating footprint: {e}")


def generate_files_for_series(
    series_name: str,
    unified_parts_list: List[sym_con_spec.PartInfo]
) -> None:
    """
    Generate CSV and KiCad symbol files for specified series.

    Args:
        series_name: Name of the series to generate files for
        unified_parts_list: List to store generated parts for unified database
    """
    if series_name not in sym_con_spec.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = sym_con_spec.SERIES_SPECS[series_name]
    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"CONNECTORS_{specs.base_series}_DATA_BASE.kicad_sym"

    try:
        parts_list = generate_part_numbers(specs)
        utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
        print_success(
            f"Generated {len(parts_list)} part numbers "
            f"in '{csv_filename}'"
        )

        sym_con_gen.generate_kicad_symbol(
            f'data/{csv_filename}',
            f'series_kicad_sym/{symbol_filename}'
        )
        print_success(
            f"KiCad symbol file '{symbol_filename}' "
            "generated successfully."
        )
        generate_footprints_for_series(parts_list)

        # Add parts to unified list
        unified_parts_list.extend(parts_list)

    except FileNotFoundError as e:
        print_error(f"CSV file not found: {e}")
    except csv.Error as e:
        print_error(f"CSV processing error: {e}")
    except IOError as e:
        print_error(f"I/O error when generating files: {e}")


def generate_unified_files(
        all_parts: List[sym_con_spec.PartInfo],
        unified_csv: str,
        unified_symbol: str
) -> None:
    """
    Generate unified component database files containing all series.

    Creates:
    1. A unified CSV file containing all component specifications
    2. A unified KiCad symbol file containing all components

    Args:
        all_parts: List of all PartInfo instances across all series
        unified_csv: Name of the unified CSV file to generate
        unified_symbol: Name of the unified KiCad symbol file to generate
    """
    # Write unified CSV file
    utils.write_to_csv(all_parts, unified_csv, HEADER_MAPPING)
    print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        sym_con_gen.generate_kicad_symbol(
            f'data/{unified_csv}', f'symbols/{unified_symbol}')
        print_success("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as e:
        print_error(f"Unified CSV file not found: {e}")
    except csv.Error as e:
        print_error(f"CSV processing error for unified file: {e}")
    except IOError as e:
        print_error(
            f"I/O error when generating unified KiCad symbol file: {e}")


if __name__ == "__main__":
    try:
        unified_parts: List[sym_con_spec.PartInfo] = []

        for series in sym_con_spec.SERIES_SPECS:
            print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_CONNECTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_CONNECTORS_DATA_BASE.kicad_sym"
        print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (ValueError, csv.Error, IOError) as error:
        print_error(f"Error generating files: {error}")
