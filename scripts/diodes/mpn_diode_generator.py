"""
Diode Part Number Generator

Generates part numbers and specifications for diode series.
Supports various package types and configurations.
Generates both individual series files and unified component database.
"""
import sys
import os
import csv
from typing import Final, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import symbol_diode_generator as sym_diode_gen
import footprint_diode_generator as ftp_diode_gen
import symbol_diode_specs as sym_diode_spec

from utilities import print_message_utilities as pmu
from utilities import file_handler_utilities as utils


def create_description(specs: sym_diode_spec.SeriesSpec) -> str:
    """
    Create component description.

    Args:
        specs: Series specifications

    Returns:
        Formatted description string
    """
    parts = [
        specs.description,
        f"{specs.voltage_rating}",
        f"{specs.current_rating}",
        specs.package
    ]
    return " ".join(parts)


def create_part_info(
    specs: sym_diode_spec.SeriesSpec,
    variant: str = ""
) -> sym_diode_spec.PartInfo:
    """
    Create complete part information.

    Args:
        specs: Series specifications
        variant: Optional variant suffix (e.g., "-7" for tape and reel)

    Returns:
        PartInfo instance with all specifications
    """
    mpn = f"{specs.base_series}{'Q' if specs.has_thermal_pad else ''}{variant}"
    trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

    return sym_diode_spec.PartInfo(
        symbol_name=f"D_{mpn}",
        reference="D",
        value=mpn,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(specs),
        manufacturer=specs.manufacturer,
        mpn=mpn,
        voltage_rating=specs.voltage_rating,
        current_rating=specs.current_rating,
        package=specs.package,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(
    specs: sym_diode_spec.SeriesSpec,
    variants: List[str] = ["-7"]  # Default to tape and reel variant
) -> List[sym_diode_spec.PartInfo]:
    """
    Generate all part numbers for the series.

    Args:
        specs: Series specifications
        variants: List of variant suffixes to generate

    Returns:
        List of PartInfo instances
    """
    return [
        create_part_info(specs, variant)
        for variant in variants
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
    'Voltage Rating': lambda part: part.voltage_rating,
    'Current Rating': lambda part: part.current_rating,
    'Package': lambda part: part.package,
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: List[sym_diode_spec.PartInfo]
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a specific series.

    Args:
        series_name: Series identifier (must exist in SERIES_SPECS)
        unified_parts_list: List to append generated parts to

    Raises:
        ValueError: If series_name is not found in SERIES_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails
        IOError: If file operations fail
    """
    if series_name not in sym_diode_spec.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = sym_diode_spec.SERIES_SPECS[series_name]

    # Ensure required directories exist
    utils.ensure_directory_exists('data')
    utils.ensure_directory_exists('series_kicad_sym')
    utils.ensure_directory_exists('symbols')
    footprint_dir = "diode_footprints.pretty"
    utils.ensure_directory_exists(footprint_dir)

    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"DIODES_{specs.base_series}_DATA_BASE.kicad_sym"

    try:
        parts_list = generate_part_numbers(specs)
        utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
        pmu.print_success(
            f"Generated {len(parts_list)} part numbers in '{csv_filename}'"
        )

        # Generate KiCad symbol file
        sym_diode_gen.generate_kicad_symbol(
            f'data/{csv_filename}',
            f'series_kicad_sym/{symbol_filename}'
        )
        pmu.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully."
        )

        # Generate KiCad footprint files
        for part in parts_list:
            try:
                ftp_diode_gen.generate_footprint_file(part, footprint_dir)
                pmu.print_success(
                    f"Generated footprint file for {part.mpn}"
                )
            except ValueError as footprint_error:
                pmu.print_error(f"Error generating footprint: {footprint_error}")
            except IOError as io_error:
                pmu.print_error(
                    f"I/O error generating footprint: {io_error}"
                )

        # Add parts to unified list
        unified_parts_list.extend(parts_list)

    except FileNotFoundError as file_error:
        pmu.print_error(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        pmu.print_error(f"CSV processing error: {csv_error}")
    except IOError as io_error:
        pmu.print_error(f"I/O error when generating files: {io_error}")
    except ValueError as val_error:
        pmu.print_error(f"Error generating part numbers: {val_error}")


def generate_unified_files(
        all_parts: List[sym_diode_spec.PartInfo],
        unified_csv: str,
        unified_symbol: str
) -> None:
    """
    Generate unified component database files containing all series.

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
        sym_diode_gen.generate_kicad_symbol(
            f'data/{unified_csv}', f'symbols/{unified_symbol}')
        pmu.print_success("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as e:
        pmu.print_error(f"Unified CSV file not found: {e}")
    except csv.Error as e:
        pmu.print_error(f"CSV processing error for unified file: {e}")
    except IOError as e:
        pmu.print_error(
            f"I/O error when generating unified KiCad symbol file: {e}")


if __name__ == "__main__":
    try:
        unified_parts: List[sym_diode_spec.PartInfo] = []

        for series in sym_diode_spec.SERIES_SPECS:
            pmu.print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_DIODES_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_DIODES_DATA_BASE.kicad_sym"
        pmu.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (ValueError, csv.Error, IOError) as error:
        pmu.print_error(f"Error generating files: {error}")
