"""
Coilcraft Inductor Series Part Number Generator

Generates part numbers and specifications for Coilcraft inductor series
with custom inductance values.
Supports both standard and AEC-Q200 qualified parts.
Generates both individual series files and unified component database.
"""

import os
import csv
from typing import Final, List
from colorama import init, Fore, Style
import kicad_inductor_symbol_generator as ki_isg
import kicad_inductor_footprint_generator as ki_ifg
import series_specs_inductors as ssi
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


def format_inductance_value(inductance: float) -> str:
    """
    Format inductance value with appropriate unit.
    Shows integer values where possible (no decimal places needed).

    Args:
        inductance: Value in µH

    Returns:
        Formatted string with unit
    """
    if inductance < 1:
        return f"{int(inductance*1000)} nH"
    if inductance.is_integer():
        return f"{int(inductance)} µH"
    return f"{inductance:.1f} µH"


def generate_value_code(
    inductance: float,
    value_suffix: str,
    is_aec: bool = True,
) -> str:
    """
    Generate Coilcraft value code for inductance values according
    to their part numbering system.

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
        inductance: Value in µH (microhenries), must be between 0.01 and 999.99
        is_aec: If True, append AEC qualification suffix to the value code
        value_suffix: AEC qualification suffix to append when is_aec is True

    Returns:
        str: Value code string.

    Raises:
        ValueError: If inductance is outside the valid range (0.01-999.99 µH)
    """
    if not 0.01 <= inductance <= 999.99:
        raise ValueError(
            f"Invalid inductance: {inductance}µH (0.01-999.99)"
        )

    if inductance >= 100.0:
        value = round(inductance / 10)
        base_code = f"{value:02d}4"
        return f"{base_code}{value_suffix}" if is_aec else base_code

    if inductance >= 10.0:
        value = round(inductance)
        base_code = f"{value:02d}3"
        return f"{base_code}{value_suffix}" if is_aec else base_code

    if inductance >= 1.0:
        value = round(inductance * 10)
        base_code = f"{value:02d}2"
        return f"{base_code}{value_suffix}" if is_aec else base_code

    if inductance >= 0.1:
        value = round(inductance * 100)
        base_code = f"{value:02d}1"
        return f"{base_code}{value_suffix}" if is_aec else base_code

    value = round(inductance * 1000)
    base_code = f"{value:02d}0"
    return f"{base_code}{value_suffix}" if is_aec else base_code


def create_description(
    inductance: float,
    specs: ssi.SeriesSpec,
    is_aec: bool
) -> str:
    """
    Create component description.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, add AEC-Q200 qualification

    Returns:
        Formatted description string
    """
    parts = [
        "INDUCTOR SMD",
        format_inductance_value(inductance),
        specs.tolerance
    ]

    if is_aec and specs.has_aec:
        parts.append("AEC-Q200")

    return " ".join(parts)


def create_part_info(
    inductance: float,
    specs: ssi.SeriesSpec,
    is_aec: bool = True
) -> ssi.PartInfo:
    """
    Create complete part information.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, create AEC-Q200 qualified part

    Returns:
        PartInfo instance with all specifications
    """
    value_code = generate_value_code(
        inductance,
        specs.value_suffix,
        is_aec and specs.has_aec,
    )
    mpn = f"{specs.base_series}-{value_code}"
    trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

    try:
        index = specs.inductance_values.index(inductance)
        max_dc_current = float(specs.max_dc_current[index])
        max_dc_resistance = float(specs.max_dc_resistance[index])
    except ValueError:
        print_error(
            f"Error: Inductance value {inductance} µH "
            f"not found in series {specs.base_series}")
        max_dc_current = 0.0
        max_dc_resistance = 0.0
    except IndexError:
        print_error(
            "Error: No DC specifications found for inductance "
            f"{inductance} µH in series {specs.base_series}")
        max_dc_current = 0.0
        max_dc_resistance = 0.0

    return ssi.PartInfo(
        symbol_name=f"L_{mpn}",
        reference="L",
        value=inductance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(inductance, specs, is_aec),
        manufacturer=specs.manufacturer,
        mpn=mpn,
        tolerance=specs.tolerance,
        series=specs.base_series,
        trustedparts_link=trustedparts_link,
        max_dc_current=max_dc_current,
        max_dc_resistance=max_dc_resistance
    )


def generate_part_numbers(
    specs: ssi.SeriesSpec,
    is_aec: bool = True
) -> List[ssi.PartInfo]:
    """
    Generate all part numbers for the series.

    Args:
        specs: Series specifications
        is_aec: If True, generate AEC-Q200 qualified parts

    Returns:
        List of PartInfo instances
    """
    return [
        create_part_info(value, specs, is_aec)
        for value in specs.inductance_values
    ]


def generate_footprints_for_series(parts_list: List[ssi.PartInfo]) -> None:
    """Generate footprint files for all parts in a series."""
    os.makedirs("inductor_footprints.pretty", exist_ok=True)

    for part in parts_list:
        try:
            ki_ifg.generate_footprint_file(part)
            print_success(
                f"Generated footprint file for {part.mpn}"
            )
        except ValueError as e:
            print_error(f"Error generating footprint: {e}")
        except IOError as e:
            print_error(f"I/O error generating footprint: {e}")


# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    'Symbol Name': lambda part: part.symbol_name,
    'Reference': lambda part: part.reference,
    'Value': lambda part: format_inductance_value(part.value),
    'Footprint': lambda part: part.footprint,
    'Datasheet': lambda part: part.datasheet,
    'Description': lambda part: part.description,
    'Manufacturer': lambda part: part.manufacturer,
    'MPN': lambda part: part.mpn,
    'Tolerance': lambda part: part.tolerance,
    'Series': lambda part: part.series,
    'Trustedparts Search': lambda part: part.trustedparts_link,
    'Maximum DC Current (A)': lambda part: f"{part.max_dc_current:.1f}",
    'Maximum DC Resistance (Ω)': lambda part: f"{part.max_dc_resistance:.3f}"
}


def generate_files_for_series(
    series_name: str,
    is_aec: bool,
    unified_parts_list: List[ssi.PartInfo]
) -> None:
    """
    Generate CSV and KiCad symbol files for specified series.

    Args:
        series_name: Name of the series to generate files for
        is_aec: If True, generate AEC-Q200 qualified parts
        unified_parts_list: List to store generated parts for unified database
    """
    if series_name not in ssi.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = ssi.SERIES_SPECS[series_name]
    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"INDUCTORS_{specs.base_series}_DATA_BASE.kicad_sym"

    try:
        parts_list = generate_part_numbers(specs, is_aec)
        utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
        print_success(
            f"Generated {len(parts_list)} part numbers "
            f"in '{csv_filename}'"
        )

        ki_isg.generate_kicad_symbol(
            f'data/{csv_filename}',
            f'series_kicad_sym/{symbol_filename}'
        )
        print_success(
            f"KiCad symbol file '{symbol_filename}' "
            "generated successfully."
        )

        # Generate footprints for the series
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
        all_parts: List[ssi.PartInfo],
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
        ki_isg.generate_kicad_symbol(
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
        unified_parts: List[ssi.PartInfo] = []

        for series in ssi.SERIES_SPECS:
            print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, True, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_INDUCTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_INDUCTORS_DATA_BASE.kicad_sym"
        print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (ValueError, csv.Error, IOError) as error:
        print_error(f"Error generating files: {error}")
