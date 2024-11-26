"""Generator for diode component files.

This module generates KiCad-compatible files for diode components including:
- CSV files with component specifications
- KiCad symbol files
- KiCad footprint files
- Unified component database
"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_diode_generator as ftp_diode_gen
import symbol_diode_generator as sym_diode_gen
import symbol_diode_specs as sym_diode_spec
from utilities import file_handler_utilities as utils
from utilities import print_message_utilities as pmu


def create_description(specs: sym_diode_spec.SeriesSpec) -> str:
    """Create a formatted description string from series specifications.

    Args:
        specs: Series specifications containing component details.

    Returns:
        Formatted description combining key specifications.

    """
    parts = [
        specs.description,
        f"{specs.voltage_rating}",
        f"{specs.current_rating}",
        specs.package,
    ]
    return " ".join(parts)


def create_part_info(
        specs: sym_diode_spec.SeriesSpec,
) -> sym_diode_spec.PartInfo:
    """Create a complete part information instance from specifications.

    Args:
        specs: Series specifications containing all component details.

    Returns:
        PartInfo instance with complete component specifications.

    """
    trustedparts_link = f"{specs.trustedparts_link}/{specs.base_series}"
    return sym_diode_spec.PartInfo(
        symbol_name=f"D_{specs.base_series}",
        reference="D",
        value=specs.base_series,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(specs),
        diode_type=specs.diode_type,
        manufacturer=specs.manufacturer,
        mpn=specs.base_series,
        voltage_rating=specs.voltage_rating,
        current_rating=specs.current_rating,
        package=specs.package,
        trustedparts_link=trustedparts_link,
    )


HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: part.value,
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Diode Type": lambda part: part.diode_type,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Voltage Rating": lambda part: part.voltage_rating,
    "Current Rating": lambda part: part.current_rating,
    "Package": lambda part: part.package,
    "Trustedparts Search": lambda part: part.trustedparts_link,
}


def generate_files_for_series(
    series_name: str, unified_parts_list: list[sym_diode_spec.PartInfo],
) -> None:
    """Generate all required files for a diode series.

    Creates CSV, KiCad symbol, and footprint files for the specified series
    and adds the part information to the unified component list.

    Args:
        series_name: Series identifier that must exist in SERIES_SPECS.
        unified_parts_list: List to append generated parts to.

    Raises:
        ValueError: If series_name is not found in SERIES_SPECS.
        FileNotFoundError: If CSV file creation fails.
        csv.Error: If CSV processing fails.
        IOError: If file operations fail.

    """
    if series_name not in sym_diode_spec.SERIES_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = sym_diode_spec.SERIES_SPECS[series_name]

    # Ensure required directories exist
    utils.ensure_directory_exists("data")
    utils.ensure_directory_exists("series_kicad_sym")
    utils.ensure_directory_exists("symbols")
    utils.ensure_directory_exists("footprints")
    footprint_dir = "footprints/diode_footprints.pretty"
    utils.ensure_directory_exists(footprint_dir)

    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"DIODES_{specs.base_series}_DATA_BASE.kicad_sym"

    try:
        part_info = create_part_info(specs)
        utils.write_to_csv([part_info], csv_filename, HEADER_MAPPING)
        pmu.print_success(f"Generated part number in '{csv_filename}'")

        # Generate KiCad symbol file
        sym_diode_gen.generate_kicad_symbol(
            f"data/{csv_filename}", f"series_kicad_sym/{symbol_filename}")
        pmu.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.")

        # Generate KiCad footprint files
        try:
            ftp_diode_gen.generate_footprint_file(part_info, footprint_dir)
            pmu.print_success(f"Generated footprint file for {part_info.mpn}")
        except ValueError as footprint_error:
            pmu.print_error(f"Error generating footprint: {footprint_error}")
        except OSError as io_error:
            pmu.print_error(f"I/O error generating footprint: {io_error}")

        # Add part to unified list
        unified_parts_list.append(part_info)

    except FileNotFoundError as file_error:
        pmu.print_error(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        pmu.print_error(f"CSV processing error: {csv_error}")
    except OSError as io_error:
        pmu.print_error(f"I/O error when generating files: {io_error}")


def generate_unified_files(
    all_parts: list[sym_diode_spec.PartInfo],
    unified_csv: str,
    unified_symbol: str,
) -> None:
    """Generate unified component database files.

    Creates a combined CSV file and KiCad symbol file containing all
    components across all series.

    Args:
        all_parts: List of all PartInfo instances across all series.
        unified_csv: Name of the unified CSV file to generate.
        unified_symbol: Name of the unified KiCad symbol file to generate.

    """
    # Write unified CSV file
    utils.write_to_csv(all_parts, unified_csv, HEADER_MAPPING)
    pmu.print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        sym_diode_gen.generate_kicad_symbol(
            f"data/{unified_csv}", f"symbols/{unified_symbol}",
        )
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
        unified_parts: list[sym_diode_spec.PartInfo] = []

        for series in sym_diode_spec.SERIES_SPECS:
            pmu.print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_DIODES_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_DIODES_DATA_BASE.kicad_sym"
        pmu.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, ValueError, csv.Error) as error:
        pmu.print_error(f"Error generating files: {error}")
