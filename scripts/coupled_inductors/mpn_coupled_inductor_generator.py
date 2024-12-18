"""Coilcraft Inductor Series Part Number Generator.

Generates part numbers and specifications for Coilcraft inductor series
with custom inductance values.
Supports both standard and AEC-Q200 qualified parts.
Generates both individual series files and unified component database.
"""

import csv
import os
import sys
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_coupled_inductor_generator
import symbol_coupled_inductor_generator
import symbol_coupled_inductors_specs
from utilities import file_handler_utilities, print_message_utilities


def format_inductance_value(inductance: float) -> str:
    """Format inductance value with appropriate unit.

    Shows integer values where possible (no decimal places needed).

    Args:
        inductance: Value in µH

    Returns:
        Formatted string with unit

    """
    if inductance < 1:
        return f"{int(inductance * 1000)} nH"
    if inductance.is_integer():
        return f"{int(inductance)} µH"
    return f"{inductance:.1f} µH"


def generate_value_code(
    inductance: float,
    value_suffix: str,
) -> str:
    """Generate Coilcraft value code for inductance values.

    The value code consists of:
    1. Two digits representing the significant figures of the inductance value
    2. A decimal position indicator (0-4)
    3. Optional AEC qualification suffix

    Decimal position indicators:
    - 4: Multiply by 10 µH (100.0-999.99 µH)
    - 3: Value is in µH (10.0-99.99 µH)
    - 2: Divide by 10 µH (1.0-9.99 µH)
    - 1: Divide by 100 µH (0.1-0.99 µH)
    - 0: Divide by 1000 µH (0.01-0.099 µH)

    Args:
        inductance:
            Value in µH (microhenries), must be between 0.01 and 999.99
        value_suffix: AEC qualification suffix to append when is_aec is True

    Returns:
        str: Value code string.

    Raises:
        ValueError: If inductance is outside the valid range (0.01-9999.99 µH)

    """
    if not 0.01 <= inductance <= 9999.99:  # noqa: PLR2004
        msg = f"Invalid inductance: {inductance}µH (0.01-9999.99)"
        raise ValueError(msg)

    if inductance >= 1000.0:  # noqa: PLR2004
        value = round(inductance / 100)
        base_code = f"{value:02d}5"
        return f"{base_code}{value_suffix}"

    if inductance >= 100.0:  # noqa: PLR2004
        value = round(inductance / 10)
        base_code = f"{value:02d}4"
        return f"{base_code}{value_suffix}"

    if inductance >= 10.0:  # noqa: PLR2004
        value = round(inductance)
        base_code = f"{value:02d}3"
        return f"{base_code}{value_suffix}"

    if inductance >= 1.0:
        value = round(inductance * 10)
        base_code = f"{value:02d}2"
        return f"{base_code}{value_suffix}"

    if inductance >= 0.1:  # noqa: PLR2004
        value = round(inductance * 100)
        base_code = f"{value:02d}1"
        return f"{base_code}{value_suffix}"

    value = round(inductance * 1000)
    base_code = f"{value:02d}0"
    return f"{base_code}{value_suffix}"


def create_description(
    inductance: float,
    specs: symbol_coupled_inductors_specs.SeriesSpec,
) -> str:
    """Create component description.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, add AEC-Q200 qualification

    Returns:
        Formatted description string

    """
    parts = [
        "COUPLED INDUCTOR SMD",
        format_inductance_value(inductance), specs.tolerance]

    return " ".join(parts)


def create_part_info(
    inductance: float,
    specs: symbol_coupled_inductors_specs.SeriesSpec,
) -> symbol_coupled_inductors_specs.PartInfo:
    """Create complete part information.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, create AEC-Q200 qualified part

    Returns:
        PartInfo instance with all specifications

    """
    value_code = generate_value_code(inductance, specs.value_suffix)
    mpn = f"{specs.base_series}-{value_code}"
    trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

    try:
        index = specs.inductance_values.index(inductance)
        max_dc_current = float(specs.max_dc_current[index])
        max_dc_resistance = float(specs.max_dc_resistance[index])
    except ValueError:
        print_message_utilities.print_error(
            f"Error: Inductance value {inductance} µH "
            f"not found in series {specs.base_series}")
        max_dc_current = 0.0
        max_dc_resistance = 0.0
    except IndexError:
        print_message_utilities.print_error(
            "Error: No DC specifications found for inductance "
            f"{inductance} µH in series {specs.base_series}")
        max_dc_current = 0.0
        max_dc_resistance = 0.0

    return symbol_coupled_inductors_specs.PartInfo(
        symbol_name=f"{specs.reference}_{mpn}",
        reference=specs.reference,
        value=inductance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(inductance, specs),
        manufacturer=specs.manufacturer,
        mpn=mpn,
        tolerance=specs.tolerance,
        series=specs.base_series,
        trustedparts_link=trustedparts_link,
        max_dc_current=max_dc_current,
        max_dc_resistance=max_dc_resistance,
    )


def generate_part_numbers(
    specs: symbol_coupled_inductors_specs.SeriesSpec,
) -> list[symbol_coupled_inductors_specs.PartInfo]:
    """Generate all part numbers for the series.

    Args:
        specs: Series specifications
        is_aec: If True, generate AEC-Q200 qualified parts

    Returns:
        List of PartInfo instances

    """
    return [
        create_part_info(value, specs) for value in specs.inductance_values]


# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: format_inductance_value(part.value),
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Tolerance": lambda part: part.tolerance,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
    "Maximum DC Current (A)": lambda part: f"{part.max_dc_current:.1f}",
    "Maximum DC Resistance (Ω)": lambda part: f"{part.max_dc_resistance:.3f}",
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_coupled_inductors_specs.PartInfo],
) -> None:
    """Generate CSV, KiCad symbol, and footprint files for a specific series.

    Args:
        series_name: Series identifier (must exist in SYMBOLS_SPECS)
        is_aec: If True, generate AEC-Q200 qualified parts
        unified_parts_list: List to append generated parts to

    Raises:
        ValueError: If series_name is not found in SYMBOLS_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Generated files are saved in 'data/', 'series_kicad_sym/', and
        'coupled_inductor_footprints.pretty/' directories.

    """
    if series_name not in symbol_coupled_inductors_specs.SYMBOLS_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_coupled_inductors_specs.SYMBOLS_SPECS[series_name]

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists("data")
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/coupled_inductor_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = (
        f"COUPLED_INDUCTORS_{specs.base_series}_DATA_BASE.kicad_sym")

    # Generate part numbers and write to CSV
    try:
        parts_list = generate_part_numbers(specs)
        file_handler_utilities.write_to_csv(
            parts_list, csv_filename, HEADER_MAPPING)
        print_message_utilities.print_success(
            f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

        # Generate KiCad symbol file
        symbol_coupled_inductor_generator.generate_kicad_symbol(
            f"data/{csv_filename}", f"series_kicad_sym/{symbol_filename}")
        print_message_utilities.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.")

        # Generate KiCad footprint files
        try:
            for part in parts_list:
                footprint_coupled_inductor_generator.generate_footprint_file(
                    part, footprint_dir)
                print_message_utilities.print_success(
                    f"Generated footprint file for {part.mpn}")
        except ValueError as footprint_error:
            print_message_utilities.print_error(
                f"Error generating footprint: {footprint_error}",
            )
        except OSError as io_error:
            print_message_utilities.print_error(
                f"I/O error generating footprint: {io_error}")

        # Add parts to unified list
        unified_parts_list.extend(parts_list)

    except FileNotFoundError as file_error:
        print_message_utilities.print_error(
            f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print_message_utilities.print_error(
            f"CSV processing error: {csv_error}")
    except OSError as io_error:
        print_message_utilities.print_error(
            f"I/O error when generating files: {io_error}")
    except ValueError as val_error:
        print_message_utilities.print_error(
            f"Error generating part numbers: {val_error}")


def generate_unified_files(
    all_parts: list[symbol_coupled_inductors_specs.PartInfo],
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
    file_handler_utilities.write_to_csv(
        all_parts, unified_csv, HEADER_MAPPING)
    print_message_utilities.print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        symbol_coupled_inductor_generator.generate_kicad_symbol(
            f"data/{unified_csv}", f"symbols/{unified_symbol}")
        print_message_utilities.print_success(
            "Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as e:
        print_message_utilities.print_error(
            f"Unified CSV file not found: {e}")
    except csv.Error as e:
        print_message_utilities.print_error(
            f"CSV processing error for unified file: {e}")
    except OSError as e:
        print_message_utilities.print_error(
            f"I/O error when generating unified KiCad symbol file: {e}")


if __name__ == "__main__":
    try:
        unified_parts: list[symbol_coupled_inductors_specs.PartInfo] = []

        for series in symbol_coupled_inductors_specs.SYMBOLS_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_COUPLED_INDUCTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_COUPLED_INDUCTORS_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, ValueError, csv.Error) as error:
        print_message_utilities.print_error(
            f"Error generating files: {error}")
