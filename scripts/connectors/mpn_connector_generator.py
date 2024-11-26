"""Connector Series Part Number Generator.

Generates part numbers and specifications for connector series
with different pin counts.
Generates both individual series files and unified component database.
"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_connector_generator as ftp_con_gen
import symbol_connector_generator as sym_con_gen
import symbol_connectors_specs as sym_con_spec
from utilities import file_handler_utilities as utils
from utilities import print_message_utilities as pmu


def generate_part_numbers(
    specs: sym_con_spec.SeriesSpec,
) -> list[sym_con_spec.PartInfo]:
    """Generate all part numbers for the series.

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
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: part.value,
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "Color": lambda part: part.color,
    "Pitch (mm)": lambda part: part.pitch,
    "Pin Count": lambda part: part.pin_count,
    "Mounting Angle": lambda part: part.mounting_angle,
    "Current Rating (A)": lambda part: part.current_rating,
    "Voltage Rating (V)": lambda part: part.voltage_rating,
    "Mounting Style": lambda part: part.mounting_style,
    "Contact Plating": lambda part: part.contact_plating,
}


def generate_files_for_series(
    series_name: str, unified_parts_list: list[sym_con_spec.PartInfo],
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a specific series.

    Args:
        series_name: Series identifier (must exist in SERIES_SPECS)
        unified_parts_list: List to append generated parts to

    Raises:
        ValueError: If series_name is not found in SERIES_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Generated files are saved in 'data/', 'series_kicad_sym/', and
        'connector_footprints.pretty/' directories.

    """
    if series_name not in sym_con_spec.SERIES_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = sym_con_spec.SERIES_SPECS[series_name]
    series_code = specs.base_series

    # Ensure required directories exist
    utils.ensure_directory_exists("data")
    utils.ensure_directory_exists("series_kicad_sym")
    utils.ensure_directory_exists("symbols")
    utils.ensure_directory_exists("footprints")
    footprint_dir = "footprints/connector_footprints.pretty"
    utils.ensure_directory_exists(footprint_dir)

    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"CONNECTORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
    pmu.print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        sym_con_gen.generate_kicad_symbol(
            f"data/{csv_filename}", f"series_kicad_sym/{symbol_filename}")
        pmu.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError as file_error:
        pmu.print_error(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        pmu.print_error(f"CSV processing error: {csv_error}")
    except OSError as io_error:
        pmu.print_error(
            f"I/O error when generating KiCad symbol file: {io_error}")

    # Generate KiCad footprint files
    try:
        for part in parts_list:
            ftp_con_gen.generate_footprint_file(part)
            footprint_name = f"{part.mpn}.kicad_mod"
            pmu.print_success(
                "KiCad footprint file "
                f"{footprint_name}' generated successfully.")
    except ValueError as val_error:
        pmu.print_error(f"Invalid connector specification: {val_error}")
    except OSError as io_error:
        pmu.print_error(
            f"I/O error when generating footprint file: {io_error}")

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
    all_parts: list[sym_con_spec.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files containing all series.

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
    pmu.print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        sym_con_gen.generate_kicad_symbol(
            f"data/{unified_csv}", f"symbols/{unified_symbol}")
        pmu.print_success("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as e:
        pmu.print_error(f"Unified CSV file not found: {e}")
    except csv.Error as e:
        pmu.print_error(f"CSV processing error for unified file: {e}")
    except OSError as e:
        pmu.print_error(
            f"I/O error when generating unified KiCad symbol file: {e}")


if __name__ == "__main__":
    try:
        unified_parts: list[sym_con_spec.PartInfo] = []

        for series in sym_con_spec.SERIES_SPECS:
            pmu.print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_CONNECTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_CONNECTORS_DATA_BASE.kicad_sym"
        pmu.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, ValueError, csv.Error) as error:
        pmu.print_error(f"Error generating files: {error}")
