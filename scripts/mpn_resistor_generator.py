"""
Panasonic ERJ Series Part Number Generator

This script generates part numbers for Panasonic ERJ resistor series including
ERJ-2RK, ERJ-3EK, ERJ-6EN, ERJ-P08, ERJ-P06, and ERJ-P03. It supports both E96
and E24 standard values and handles component specifications like size, power
rating, resistance range, and packaging options.

The script generates:
- Part numbers following Panasonic's naming conventions
- CSV files containing component specifications and parameters
- KiCad symbol files for electronic design automation

Features:
- Supports E96 and E24 resistance value series
- Handles resistance values from 10Ω to 2.2MΩ depending on series
- Generates both individual series files and unified component database
- Includes vendor links and detailed component specifications
- Exports in industry-standard formats (CSV, KiCad)
"""

import csv
from typing import List, Final, Iterator
from colorama import init, Fore, Style
import kicad_resistor_symbol_generator as ki_rsg
import series_specs_resistors as ssr
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


E96_BASE_VALUES: Final[List[float]] = [
    10.0, 10.2, 10.5, 10.7, 11.0, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7, 13.0,
    13.3, 13.7, 14.0, 14.3, 14.7, 15.0, 15.4, 15.8, 16.2, 16.5, 16.9, 17.4,
    17.8, 18.2, 18.7, 19.1, 19.6, 20.0, 20.5, 21.0, 21.5, 22.1, 22.6, 23.2,
    23.7, 24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28.0, 28.7, 29.4, 30.1, 30.9,
    31.6, 32.4, 33.2, 34.0, 34.8, 35.7, 36.5, 37.4, 38.3, 39.2, 40.2, 41.2,
    42.2, 43.2, 44.2, 45.3, 46.4, 47.5, 48.7, 49.9, 51.1, 52.3, 53.6, 54.9,
    56.2, 57.6, 59.0, 60.4, 61.9, 63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2,
    75.0, 76.8, 78.7, 80.6, 82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6
]

E24_BASE_VALUES: Final[List[float]] = [
    10.0, 11.0, 12.0, 13.0, 15.0, 16.0, 18.0, 20.0, 22.0, 24.0, 27.0, 30.0,
    33.0, 36.0, 39.0, 43.0, 47.0, 51.0, 56.0, 62.0, 68.0, 75.0, 82.0, 91.0
]


def format_resistance_value(resistance: float) -> str:
    """
    Convert a resistance value to a human-readable string format.

    Args:
        resistance: The resistance value in ohms

    Returns:
        A formatted string with appropriate unit suffix (Ω, kΩ, or MΩ)
    """
    def clean_number(num: float) -> str:
        return f"{num:g}"

    if resistance >= 1_000_000:
        return f"{clean_number(resistance / 1_000_000)} MΩ"
    if resistance >= 1_000:
        return f"{clean_number(resistance / 1_000)} kΩ"
    return f"{clean_number(resistance)} Ω"


def generate_resistance_code(resistance: float, max_resistance: int) -> str:
    """
    Generate the resistance code portion of a Panasonic part number.

    The code follows Panasonic's format:
    - For values < 100Ω: Uses R notation (e.g., 10R0 for 10Ω)
    - For values ≥ 100Ω: Uses 3 significant digits + multiplier digit where:
        0 = ×1 (100-999Ω)
        1 = ×10 (1k-9.99kΩ)
        2 = ×100 (10k-99.9kΩ)
        3 = ×1000 (100k-999kΩ)
        4 = ×10000 (1MΩ+)

    Args:
        resistance: The resistance value in ohms
        max_resistance: Maximum allowed resistance value for the series

    Returns:
        A 4-character string representing the resistance code

    Raises:
        ValueError:
            If resistance is outside valid range (10Ω to max_resistance)
    """
    if resistance < 10 or resistance > max_resistance:
        raise ValueError(
            f"Resistance value out of range (10Ω to {max_resistance}Ω)")

    # Handle values less than 100Ω using R notation
    if resistance < 100:
        whole = int(resistance)
        decimal = int(round((resistance - whole) * 10))
        return f"{whole:02d}R{decimal}"

    # For values ≥ 100Ω, determine multiplier and significant digits
    if resistance < 1000:  # 100-999Ω
        significant = int(round(resistance))
        multiplier = "0"
    elif resistance < 10000:  # 1k-9.99kΩ
        significant = int(round(resistance / 10))
        multiplier = "1"
    elif resistance < 100000:  # 10k-99.9kΩ
        significant = int(round(resistance / 100))
        multiplier = "2"
    elif resistance < 1000000:  # 100k-999kΩ
        significant = int(round(resistance / 1000))
        multiplier = "3"
    else:  # 1MΩ+
        significant = int(round(resistance / 10000))
        multiplier = "4"

    return f"{significant:03d}{multiplier}"


def generate_resistance_values(
    base_values: List[float],
    max_resistance: int
) -> Iterator[float]:
    """
    Generate all valid resistance values from a list of base values.

    For each base value, generates a geometric sequence by multiplying by 10
    until reaching max_resistance. Only yields values ≥ 10Ω.

    Args:
        base_values: List of base resistance values (E96 or E24 series)
        max_resistance: Maximum resistance value to generate

    Yields:
        float: Valid resistance values in ascending order
    """
    for base_value in base_values:
        current = base_value
        while current <= max_resistance:
            if current >= 10:
                yield current
            current *= 10


def create_part_info(
    resistance: float,
    tolerance_code: str,
    tolerance_value: str,
    packaging: str,
    specs: ssr.SeriesSpec
) -> ssr.PartInfo:
    """
    Create a PartInfo instance with complete component specifications.

    Args:
        resistance: Resistance value in ohms
        tolerance_code: Manufacturer's tolerance code (e.g., 'F' for 1%)
        tolerance_value: Human-readable tolerance (e.g., '1%')
        packaging: Packaging code (e.g., 'X' or 'V')
        specs: SeriesSpec instance containing series specifications

    Returns:
        PartInfo instance containing all component details
        and vendor information
    """
    resistance_code = generate_resistance_code(
        resistance, specs.max_resistance)
    mpn = f"{specs.base_series}{tolerance_code}{resistance_code}{packaging}"
    symbol_name = f"R_{mpn}"
    description = (
        f"RES SMD {format_resistance_value(resistance)} "
        f"{tolerance_value} {specs.case_code_in} {specs.voltage_rating}"
    )
    trustedparts_link = f"{specs.trustedparts_url}{mpn}"

    return ssr.PartInfo(
        symbol_name=symbol_name,
        reference="R",
        value=resistance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=description,
        manufacturer=specs.manufacturer,
        mpn=mpn,
        tolerance=tolerance_value,
        voltage_rating=specs.voltage_rating,
        case_code_in=specs.case_code_in,
        case_code_mm=specs.case_code_mm,
        series=specs.base_series,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(specs: ssr.SeriesSpec) -> List[ssr.PartInfo]:
    """
    Generate all possible part numbers for a resistor series.

    Generates part numbers for both E96 and E24 value series, considering:
    - All valid resistance values up to max_resistance
    - All tolerance options for each series type
    - All packaging options
    - Special handling for high resistance values (>1MΩ) if applicable

    Args:
        specs: SeriesSpec instance containing series specifications

    Returns:
        List of PartInfo instances for all valid combinations
    """
    parts_list: List[ssr.PartInfo] = []

    for series_type in ssr.SeriesType:
        base_values = (
            E96_BASE_VALUES if series_type == ssr.SeriesType.E96
            else E24_BASE_VALUES
        )

        for resistance in generate_resistance_values(
                base_values, specs.max_resistance):
            # Handle special case for high resistance values
            if resistance > 1_000_000 and specs.high_resistance_tolerance:
                tolerance_codes = specs.high_resistance_tolerance
            else:
                tolerance_codes = specs.tolerance_map[series_type]

            for tolerance_code, tolerance_value in tolerance_codes.items():
                for packaging in specs.packaging_options:
                    parts_list.append(create_part_info(
                        resistance,
                        tolerance_code,
                        tolerance_value,
                        packaging,
                        specs
                    ))

    return parts_list


# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    'Symbol Name': lambda part: part.symbol_name,
    'Reference': lambda part: part.reference,
    'Value': lambda part: format_resistance_value(part.value),
    'Footprint': lambda part: part.footprint,
    'Datasheet': lambda part: part.datasheet,
    'Description': lambda part: part.description,
    'Manufacturer': lambda part: part.manufacturer,
    'MPN': lambda part: part.mpn,
    'Tolerance': lambda part: part.tolerance,
    'Voltage Rating': lambda part: part.voltage_rating,
    'Case Code - in': lambda part: part.case_code_in,
    'Case Code - mm': lambda part: part.case_code_mm,
    'Series': lambda part: part.series,
    'Trustedparts Search': lambda part: part.trustedparts_link
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: List[ssr.PartInfo]
) -> None:
    """
    Generate CSV and KiCad symbol files for a specific resistor series.

    Creates:
    1. A CSV file containing all component specifications
    2. A KiCad symbol file for use in electronic design
    3. Adds generated parts to the unified parts list

    Args:
        series_name: Name of the resistor series (e.g., 'ERJ-2RK')
        unified_parts_list: List to store generated parts for unified database

    Raises:
        ValueError: If series_name is not recognized
        FileNotFoundError: If CSV file cannot be found for symbol generation
        csv.Error: If CSV processing fails
        IOError: If file operations fail
    """
    if series_name not in ssr.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = ssr.SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")
    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"RESISTORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
    print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        ki_rsg.generate_kicad_symbol(
            f'data/{csv_filename}',
            f'series_kicad_sym/{symbol_filename}')
        print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError as file_error:
        print_error(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print_error(f"CSV processing error: {csv_error}")
    except IOError as io_error:
        print_error(f"I/O error when generating KiCad symbol file: {io_error}")

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
        all_parts: List[ssr.PartInfo],
        unified_csv: str,
        unified_symbol: str
) -> None:
    """
    Generate unified component database files containing all series.

    Creates:
    1. A unified CSV file containing all component specifications
    2. A unified KiCad symbol file containing all components

    These files combine data from all series into single reference files
    for easier component selection and management.

    Args:
        all_parts: List of all PartInfo instances across all series

    Raises:
        FileNotFoundError: If unified CSV file cannot be found
        csv.Error: If CSV processing fails
        IOError: If file operations fail
    """

    # Write unified CSV file
    utils.write_to_csv(all_parts, unified_csv, HEADER_MAPPING)
    print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        ki_rsg.generate_kicad_symbol(
            f'data/{unified_csv}', f'symbols/{unified_symbol}')
        print_success("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as file_error:
        print_error(f"Unified CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print_error(f"CSV processing error for unified file: {csv_error}")
    except IOError as io_error:
        print_error(
            f"I/O error when generating unified KiCad symbol file: {io_error}")


if __name__ == "__main__":
    try:
        unified_parts: List[ssr.PartInfo] = []

        for series in ssr.SERIES_SPECS:
            print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_RESISTORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_RESISTORS_DATA_BASE.kicad_sym"
        print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (csv.Error, IOError) as file_error:
        print_error(f"Error generating files: {file_error}")
