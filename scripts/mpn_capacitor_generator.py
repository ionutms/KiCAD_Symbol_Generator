"""
Murata GCM Series Capacitor Part Number Generator

A module for generating standardized part numbers for Murata GCM series
capacitors. Supports multiple series types and specifications, producing both
individual series files and unified output in CSV and KiCad symbol formats.

Features:
    - Generates part numbers for GCM155, GCM188, GCM216, GCM31M,
        and GCM31C series
    - Supports X7R dielectric type
    - Creates individual series and unified output files
    - Produces both CSV and KiCad symbol format outputs
    - Handles standard E12 series values with exclusions
    - Generates KiCad footprint files for each series
"""

import os
import csv
from dataclasses import dataclass
from typing import List, Final, Iterator, Dict, Set
from colorama import init, Fore, Style
import symbol_capacitor_generator as sym_cap_gen
import footprint_capacitor_generator as ftp_cap_gen
import symbol_capacitors_specs as sym_cap_spec
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


@dataclass
class PartParameters:
    """Input parameters for creating a part number.

    Attributes:
        capacitance: Capacitance value in Farads
        tolerance_code: Code indicating component tolerance
        tolerance_value: Human-readable tolerance specification
        packaging: Component packaging code
        series_type: Dielectric type specification
        specs: Complete series specifications
    """
    capacitance: float
    tolerance_code: str
    tolerance_value: str
    packaging: str
    series_type: sym_cap_spec.SeriesType
    specs: sym_cap_spec.SeriesSpec


def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print_info(f"Created directory: {directory}")


@dataclass(frozen=True)
class CharacteristicThreshold:
    """Threshold configuration for characteristic codes.

    Attributes:
        threshold: Capacitance threshold in Farads
        code: Characteristic code to use when value exceeds threshold
    """
    threshold: float
    code: str


CHARACTERISTIC_CONFIGS: Final[Dict[str, List[CharacteristicThreshold]]] = {
    "GCM155": [
        CharacteristicThreshold(22e-9, "E02"),
        CharacteristicThreshold(4.7e-9, "A55"),
        CharacteristicThreshold(0, "A37")
    ],
    "GCM188": [
        CharacteristicThreshold(100e-9, "A64"),
        CharacteristicThreshold(47e-9, "A57"),
        CharacteristicThreshold(22e-9, "A55"),
        CharacteristicThreshold(0, "A37")
    ],
    "GCM216": [
        CharacteristicThreshold(22e-9, "A55"),
        CharacteristicThreshold(0, "A37")
    ],
    "GCM31M": [
        CharacteristicThreshold(560e-9, "A55"),
        CharacteristicThreshold(100e-9, "A37"),
        CharacteristicThreshold(0, "A37")
    ],
    "GCM31C": [
        CharacteristicThreshold(4.7e-6, "A55"),
        CharacteristicThreshold(0, "A55")
    ]
}


def format_capacitance_value(capacitance: float) -> str:
    """Convert capacitance value to human-readable format with units.

    Args:
        capacitance: Capacitance value in Farads

    Returns:
        Formatted string with appropriate unit prefix (pF, nF, or µF)
    """
    pf_value = capacitance * 1e12

    if capacitance >= 1e-6:  # 1 µF and above
        value = capacitance/1e-6
        unit = "µF"
    elif pf_value >= 1000:  # 1000 pF and above -> convert to nF
        value = pf_value/1000
        unit = "nF"
    else:  # Below 1000 pF
        value = pf_value
        unit = "pF"

    # Format the number to remove unnecessary decimals
    if value % 1 == 0:
        return f"{int(value)} {unit}"
    formatted = f"{value:.3g}"
    value = pf_value/1000

    return f"{formatted} {unit}"


def generate_capacitance_code(
        capacitance: float
) -> str:
    """Generate the capacitance portion of Murata part number.

    Args:
        capacitance: Capacitance value in Farads

    Returns:
        str: Three-character code representing the capacitance value
    """
    # Convert to picofarads
    pf_value = capacitance * 1e12

    # Handle values under 10pF
    if pf_value < 10:
        whole = int(pf_value)
        decimal = int((pf_value - whole) * 10)
        return f"{whole}R{decimal}"

    # Handle values under 1000pF
    if pf_value < 1000:
        significant = round(pf_value)
        if significant % 10 == 0:
            significant += 1
        return f"{significant:03d}"

    # Handle values 1000pF and above
    # Convert to scientific notation with 2 significant digits
    sci_notation = f"{pf_value:.2e}"

    # Split into significand and power
    parts = sci_notation.split('e')
    significand = float(parts[0])
    power = int(parts[1])

    # Calculate first two digits and zero count
    first_two = int(round(significand * 10))
    zero_count = power - 1

    return f"{first_two}{zero_count}"


def get_characteristic_code(
        capacitance: float,
        specs: sym_cap_spec.SeriesSpec
) -> str:
    """Determine characteristic code based on series and capacitance.

    Args:
        capacitance: Capacitance value in Farads
        specs: Series specifications including base series name

    Returns:
        Appropriate characteristic code for the series/value combination

    Raises:
        ValueError: If specs.base_series is not a supported series
    """
    if specs.base_series not in CHARACTERISTIC_CONFIGS:
        raise ValueError(f"Unknown series: {specs.base_series}")

    thresholds = CHARACTERISTIC_CONFIGS[specs.base_series]

    for threshold in thresholds:
        if capacitance > threshold.threshold:
            return threshold.code

    return thresholds[-1].code


def generate_standard_values(
    min_value: float,
    max_value: float,
    excluded_values: Set[float]
) -> Iterator[float]:
    """Generate standard E12 series capacitance values within range.

    Args:
        min_value: Minimum capacitance in Farads
        max_value: Maximum capacitance in Farads
        excluded_values: Set of values to exclude from output

    Yields:
        float:
            Standard E12 series values between min and max,
            excluding specified values

    Note:
        Values are normalized to avoid floating point precision issues.
        The function uses the E12 series multipliers:
            1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2
    """
    e12_multipliers: Final[List[float]] = [
        1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2
    ]

    # Convert excluded values to normalized form
    normalized_excluded = {float(f"{value:.1e}") for value in excluded_values}

    decade = 1.0e-12
    while decade <= max_value:
        for multiplier in e12_multipliers:
            normalized_value = float(f"{decade * multiplier:.1e}")
            if min_value <= normalized_value <= max_value:
                if normalized_value not in normalized_excluded:
                    yield normalized_value
        decade *= 10


def generate_datasheet_url(
        mpn: str,
        specs: sym_cap_spec.SeriesSpec
) -> str:
    """Generate the datasheet URL for a given Murata part number.

    Args:
        mpn: Complete manufacturer part number
        specs: Series specifications containing base datasheet URL

    Returns:
        URL to the appropriate datasheet for the series and specific part
    """
    # Remove the last character (packaging code) from MPN
    base_mpn = mpn[:-1]
    # Get specific series characteristics (voltage code, dielectric code)
    specific_part = base_mpn[len(specs.base_series):]
    # Combine base URL with specific part characteristics
    return f"{specs.datasheet_url}{specific_part}-01.pdf"


def create_part_info(
        params: PartParameters
) -> sym_cap_spec.PartInfo:
    """Create complete part information from component parameters.

    Args:
        params: Complete set of parameters needed to create part info

    Returns:
        PartInfo containing all component information and identifiers
    """
    capacitance_code = generate_capacitance_code(params.capacitance)
    characteristic_code = get_characteristic_code(
        params.capacitance,
        params.specs
    )
    formatted_value = format_capacitance_value(params.capacitance)

    mpn = (
        f"{params.specs.base_series}"
        f"{params.specs.dielectric_code[params.series_type]}"
        f"{params.specs.voltage_code}"
        f"{capacitance_code}"
        f"{params.tolerance_code}"
        f"{characteristic_code}"
        f"{params.packaging}"
    )

    symbol_name = f"C_{mpn}"
    description = (
        f"CAP SMD {formatted_value} "
        f"{params.series_type.value} {params.tolerance_value} "
        f"{params.specs.case_code_in} {params.specs.voltage_rating}"
    )
    trustedparts_link = f"{params.specs.trustedparts_url}/{mpn}"
    datasheet_url = generate_datasheet_url(mpn, params.specs)

    return sym_cap_spec.PartInfo(
        symbol_name=symbol_name,
        reference="C",
        value=params.capacitance,
        formatted_value=formatted_value,
        footprint=params.specs.footprint,
        datasheet=datasheet_url,
        description=description,
        manufacturer=params.specs.manufacturer,
        mpn=mpn,
        dielectric=params.series_type.value,
        tolerance=params.tolerance_value,
        voltage_rating=params.specs.voltage_rating,
        case_code_in=params.specs.case_code_in,
        case_code_mm=params.specs.case_code_mm,
        series=params.specs.base_series,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(
        specs: sym_cap_spec.SeriesSpec
) -> List[sym_cap_spec.PartInfo]:
    """Generate all valid part numbers for a series specification.

    Args:
        specs: Complete series specifications

    Returns:
        List of PartInfo objects for all valid component combinations,
        sorted by dielectric type and capacitance value
    """
    parts_list: List[sym_cap_spec.PartInfo] = []

    for series_type in sym_cap_spec.SeriesType:
        if series_type in specs.value_range:
            min_val, max_val = specs.value_range[series_type]

            for capacitance in generate_standard_values(
                min_val,
                max_val,
                specs.excluded_values
            ):
                for tolerance_code, tolerance_value in \
                        specs.tolerance_map[series_type].items():
                    for packaging in specs.packaging_options:
                        params = PartParameters(
                            capacitance=capacitance,
                            tolerance_code=tolerance_code,
                            tolerance_value=tolerance_value,
                            packaging=packaging,
                            series_type=series_type,
                            specs=specs
                        )
                        parts_list.append(create_part_info(params))

    return sorted(parts_list, key=lambda x: (x.dielectric, x.value))


# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    'Symbol Name': lambda part: part.symbol_name,
    'Reference': lambda part: part.reference,
    'Value': lambda part: format_capacitance_value(part.value),
    'Footprint': lambda part: part.footprint,
    'Datasheet': lambda part: part.datasheet,
    'Description': lambda part: part.description,
    'Manufacturer': lambda part: part.manufacturer,
    'MPN': lambda part: part.mpn,
    'Dielectric': lambda part: part.dielectric,
    'Tolerance': lambda part: part.tolerance,
    'Voltage Rating': lambda part: part.voltage_rating,
    'Case Code - in': lambda part: part.case_code_in,
    'Case Code - mm': lambda part: part.case_code_mm,
    'Series': lambda part: part.series,
    'Trustedparts Search': lambda part: part.trustedparts_link
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: List[sym_cap_spec.PartInfo]
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
        'capacitor_footprints.pretty/' directories.
    """
    if series_name not in sym_cap_spec.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = sym_cap_spec.SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")

    # Ensure required directories exist
    ensure_directory_exists('data')
    ensure_directory_exists('series_kicad_sym')
    ensure_directory_exists('symbols')
    ensure_directory_exists('capacitor_footprints.pretty')
    footprint_dir = "capacitor_footprints.pretty"

    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"CAPACITORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
    print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        sym_cap_gen.generate_kicad_symbol(
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

    # Generate KiCad footprint file
    try:
        ftp_cap_gen.generate_footprint_file(series_name, footprint_dir)
        footprint_name = f"{series_name}_{specs.case_code_in}.kicad_mod"
        print_success(
            f"KiCad footprint file '{footprint_name}' generated successfully.")
    except KeyError as key_error:
        print_error(f"Invalid series specification: {key_error}")
    except IOError as io_error:
        print_error(f"I/O error when generating footprint file: {io_error}")

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
    all_parts: List[sym_cap_spec.PartInfo],
    unified_csv: str,
    unified_symbol: str
) -> None:
    """Generate unified component database files containing all series.

    Args:
        all_parts: Complete list of parts to include in unified files
        unified_csv: Name of the unified CSV file
        unified_symbol: Name of the unified symbol file

    Raises:
        FileNotFoundError: If unified CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Creates:
        1. A unified CSV file containing all component specifications
        2. A unified KiCad symbol file containing all components
        3. A complete footprint library for all series
    """
    # Write unified CSV file
    utils.write_to_csv(all_parts, unified_csv, HEADER_MAPPING)
    print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        sym_cap_gen.generate_kicad_symbol(
            f'data/{unified_csv}', f'symbols/{unified_symbol}')
        print_success("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as file_error:
        print_error(f"Unified CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print_error(f"CSV processing error for unified file: {csv_error}")
    except IOError as io_error:
        print_error(
            f"I/O error when generating unified KiCad symbol file: {io_error}")

    # Generate footprints for all series
    print_info("\nGenerating footprints for all series:")
    footprint_dir = "capacitor_footprints.pretty"
    ensure_directory_exists(footprint_dir)

    for part_series in sym_cap_spec.SERIES_SPECS:
        try:
            ftp_cap_gen.generate_footprint_file(part_series, footprint_dir)
            print_success(f"Generated footprint for {part_series}")
        except (KeyError, IOError) as error:
            print_error(
                f"Error generating footprint for {part_series}: {error}")


if __name__ == "__main__":
    try:
        unified_parts: List[sym_cap_spec.PartInfo] = []

        for series in sym_cap_spec.SERIES_SPECS:
            print_info(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_CAPACITORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_CAPACITORS_DATA_BASE.kicad_sym"
        print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (csv.Error, IOError) as file_error:
        print_error(f"Error generating unified files: {file_error}")
