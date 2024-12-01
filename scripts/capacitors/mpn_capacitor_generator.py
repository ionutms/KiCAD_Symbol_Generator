"""Murata GCM Series Capacitor Part Number Generator.

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

import csv
import os
import sys
from collections.abc import Iterator
from typing import Final

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import footprint_capacitor_generator
import symbol_capacitor_generator
import symbol_capacitors_specs
from utilities import file_handler_utilities, print_message_utilities


def format_capacitance_value(capacitance: float) -> str:
    """Convert capacitance value to human-readable format with units.

    Args:
        capacitance: Capacitance value in Farads

    Returns:
        Formatted string with appropriate unit prefix (pF, nF, or µF)

    """
    pf_value = capacitance * 1e12

    # 1 µF and above
    if capacitance >= 1e-6:  # noqa: PLR2004
        value = capacitance / 1e-6
        unit = "µF"

    # 1000 pF and above -> convert to nF
    elif pf_value >= 1000:  # noqa: PLR2004
        value = pf_value / 1000
        unit = "nF"
    else:  # Below 1000 pF
        value = pf_value
        unit = "pF"

    # Format the number to remove unnecessary decimals
    if value % 1 == 0:
        return f"{int(value)} {unit}"
    formatted = f"{value:.3g}"
    value = pf_value / 1000

    return f"{formatted} {unit}"


def generate_capacitance_code(capacitance: float) -> str:
    """Generate the capacitance portion of Murata part number.

    Args:
        capacitance: Capacitance value in Farads

    Returns:
        str: Three-character code representing the capacitance value

    """
    # Convert to picofarads
    pf_value = capacitance * 1e12

    # Handle values under 10pF
    if pf_value < 10:  # noqa: PLR2004
        whole = int(pf_value)
        decimal = int((pf_value - whole) * 10)
        return f"{whole}R{decimal}"

    # Handle values under 1000pF
    if pf_value < 1000:  # noqa: PLR2004
        significant = round(pf_value)
        if significant % 10 == 0:
            significant += 1
        return f"{significant:03d}"

    # Handle values 1000pF and above
    # Convert to scientific notation with 2 significant digits
    sci_notation = f"{pf_value:.2e}"

    # Split into significand and power
    parts = sci_notation.split("e")
    significand = float(parts[0])
    power = int(parts[1])

    # Calculate first two digits and zero count
    first_two = int(round(significand * 10))
    zero_count = power - 1

    return f"{first_two}{zero_count}"


def get_characteristic_code(
    capacitance: float,
    specs: symbol_capacitors_specs.SeriesSpec,
) -> str:
    """Determine characteristic code based on series and capacitance.

    Args:
        capacitance: Capacitance value in Farads
        specs: Series specifications including base series name

    Returns:
        Appropriate characteristic code for the series/value combination

    Raises:
        ValueError: If series is not found or supports no characteristic codes

    """
    if specs.base_series.startswith("CL"):
        return "X7R"

    # Simplified series-specific characteristic code lookup
    for threshold, code in sorted(
            specs.characteristic_codes.items(), reverse=True):
        if capacitance > threshold:
            return code

    return list(specs.characteristic_codes.values())[-1]


def generate_standard_values(
    min_value: float,
    max_value: float,
    excluded_values: set[float],
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
    e12_multipliers: Final[list[float]] = [
        1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

    # Convert excluded values to normalized form
    normalized_excluded = {float(f"{value:.1e}") for value in excluded_values}

    decade = 1.0e-12
    while decade <= max_value:
        for multiplier in e12_multipliers:
            normalized_value = float(f"{decade * multiplier:.1e}")
            if min_value <= normalized_value <= max_value:  # noqa: SIM102
                if normalized_value not in normalized_excluded:
                    yield normalized_value
        decade *= 10


def generate_datasheet_url(
    mpn: str,
    specs: symbol_capacitors_specs.SeriesSpec,
) -> str:
    """Generate the datasheet URL for a given Murata part number.

    Args:
        mpn: Complete manufacturer part number
        specs: Series specifications containing base datasheet URL

    Returns:
        URL to the appropriate datasheet for the series and specific part

    """
    if specs.manufacturer == "Murata Electronics":
        # Remove the last character (packaging code) from MPN
        base_mpn = mpn[:-1]
        # Get specific series characteristics (voltage code, dielectric code)
        specific_part = base_mpn[len(specs.base_series):]
        # Combine base URL with specific part characteristics
        return f"{specs.datasheet_url}{specific_part}-01.pdf"
    return f"{specs.datasheet_url}{mpn}"


def create_part_info(  # noqa: PLR0913
    capacitance: float,
    tolerance_code: str,
    tolerance_value: str,
    packaging: str,
    dielectric_type: str,
    specs: symbol_capacitors_specs.SeriesSpec,
) -> symbol_capacitors_specs.PartInfo:
    """Create complete part information from component parameters.

    Args:
        capacitance: Capacitance value in Farads
        tolerance_code: Code indicating component tolerance
        tolerance_value: Human-readable tolerance specification
        packaging: Component packaging code
        dielectric_type: Dielectric type specification
        specs: Complete series specifications

    Returns:
        PartInfo containing all component information and identifiers

    """
    capacitance_code = generate_capacitance_code(capacitance)
    characteristic_code = get_characteristic_code(capacitance, specs)
    formatted_value = format_capacitance_value(capacitance)

    if specs.manufacturer == "Murata Electronics":
        mpn = (
            f"{specs.base_series}"
            f"{specs.dielectric_code[dielectric_type]}"
            f"{specs.voltage_code}"
            f"{capacitance_code}"
            f"{tolerance_code}"
            f"{characteristic_code}"
            f"{packaging}"
        )
    else:
        mpn = (
            f"{specs.base_series}"
            f"{specs.dielectric_code[dielectric_type]}"
            f"{capacitance_code}"
            f"{tolerance_code}"
            f"{specs.voltage_code}"
            f"{packaging}"
        )

    description = (
        f"CAP SMD {formatted_value} "
        f"{dielectric_type} {tolerance_value} "
        f"{specs.case_code_in} {specs.voltage_rating}"
    )

    trustedparts_link = f"{specs.trustedparts_url}/{mpn}"
    datasheet_url = generate_datasheet_url(mpn, specs)

    return symbol_capacitors_specs.PartInfo(
        symbol_name=f"{specs.reference}_{mpn}",
        reference="C",
        value=capacitance,
        formatted_value=formatted_value,
        footprint=specs.footprint,
        datasheet=datasheet_url,
        description=description,
        manufacturer=specs.manufacturer,
        mpn=mpn,
        dielectric=dielectric_type,
        tolerance=tolerance_value,
        voltage_rating=specs.voltage_rating,
        case_code_in=specs.case_code_in,
        case_code_mm=specs.case_code_mm,
        series=specs.base_series,
        trustedparts_link=trustedparts_link,
    )


def generate_part_numbers(
    specs: symbol_capacitors_specs.SeriesSpec,
) -> list[symbol_capacitors_specs.PartInfo]:
    """Generate all valid part numbers for a series specification.

    Args:
        specs: Complete series specifications

    Returns:
        List of PartInfo objects for all valid component combinations,
        sorted by dielectric type and capacitance value

    """
    parts_list: list[symbol_capacitors_specs.PartInfo] = []

    dielectric_types = ["X7R"]

    for dielectric_type in dielectric_types:
        if dielectric_type in specs.value_range:
            min_val, max_val = specs.value_range[dielectric_type]

            for capacitance in generate_standard_values(
                    min_val, max_val, specs.excluded_values):
                for tolerance_code, tolerance_value in specs.tolerance_map[
                        dielectric_type].items():
                    for packaging in specs.packaging_options:
                        parts_list.append(create_part_info(  # noqa: PERF401
                            capacitance=capacitance,
                            tolerance_code=tolerance_code,
                            tolerance_value=tolerance_value,
                            packaging=packaging,
                            dielectric_type=dielectric_type,
                            specs=specs,
                        ))

    return sorted(parts_list, key=lambda x: (x.dielectric, x.value))


# Global header to attribute mapping
HEADER_MAPPING: Final[dict] = {
    "Symbol Name": lambda part: part.symbol_name,
    "Reference": lambda part: part.reference,
    "Value": lambda part: format_capacitance_value(part.value),
    "Footprint": lambda part: part.footprint,
    "Datasheet": lambda part: part.datasheet,
    "Description": lambda part: part.description,
    "Manufacturer": lambda part: part.manufacturer,
    "MPN": lambda part: part.mpn,
    "Dielectric": lambda part: part.dielectric,
    "Tolerance": lambda part: part.tolerance,
    "Voltage Rating": lambda part: part.voltage_rating,
    "Case Code - in": lambda part: part.case_code_in,
    "Case Code - mm": lambda part: part.case_code_mm,
    "Series": lambda part: part.series,
    "Trustedparts Search": lambda part: part.trustedparts_link,
}


def generate_files_for_series(
    series_name: str,
    unified_parts_list: list[symbol_capacitors_specs.PartInfo],
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
    if series_name not in symbol_capacitors_specs.SERIES_SPECS:
        msg = f"Unknown series: {series_name}"
        raise ValueError(msg)

    specs = symbol_capacitors_specs.SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")

    # Ensure required directories exist
    file_handler_utilities.ensure_directory_exists("data")
    file_handler_utilities.ensure_directory_exists("series_kicad_sym")
    file_handler_utilities.ensure_directory_exists("symbols")
    file_handler_utilities.ensure_directory_exists("footprints")
    footprint_dir = "footprints/capacitor_footprints.pretty"
    file_handler_utilities.ensure_directory_exists(footprint_dir)

    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"CAPACITORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    file_handler_utilities.write_to_csv(
        parts_list, csv_filename, HEADER_MAPPING)
    print_message_utilities.print_success(
        f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        symbol_capacitor_generator.generate_kicad_symbol(
            f"data/{csv_filename}", f"series_kicad_sym/{symbol_filename}")
        print_message_utilities.print_success(
            f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError as file_error:
        print_message_utilities.print_error(
            f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print_message_utilities.print_error(
            f"CSV processing error: {csv_error}")
    except OSError as io_error:
        print_message_utilities.print_error(
            f"I/O error when generating KiCad symbol file: {io_error}")

    # Generate KiCad footprint file
    try:
        footprint_capacitor_generator.generate_footprint_file(
            series_name, footprint_dir)
        footprint_name = f"{series_name}_{specs.case_code_in}.kicad_mod"
        print_message_utilities.print_success(
            f"KiCad footprint file '{footprint_name}' "
            "generated successfully.")
    except KeyError as key_error:
        print_message_utilities.print_error(
            f"Invalid series specification: {key_error}")
    except OSError as io_error:
        print_message_utilities.print_error(
            f"I/O error when generating footprint file: {io_error}")

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
    all_parts: list[symbol_capacitors_specs.PartInfo],
    unified_csv: str,
    unified_symbol: str,
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
    file_handler_utilities.write_to_csv(
        all_parts, unified_csv, HEADER_MAPPING)
    print_message_utilities.print_success(
        f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        symbol_capacitor_generator.generate_kicad_symbol(
            f"data/{unified_csv}", f"symbols/{unified_symbol}")
        print_message_utilities.print_success(
            "Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as file_error:
        print_message_utilities.print_error(
            f"Unified CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print_message_utilities.print_error(
            f"CSV processing error for unified file: {csv_error}")
    except OSError as io_error:
        print_message_utilities.print_error(
            f"Error when generating unified KiCad symbol file: {io_error}")


if __name__ == "__main__":
    try:
        unified_parts: list[symbol_capacitors_specs.PartInfo] = []

        for series in symbol_capacitors_specs.SERIES_SPECS:
            print_message_utilities.print_info(
                f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_CAPACITORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_CAPACITORS_DATA_BASE.kicad_sym"
        print_message_utilities.print_info("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (OSError, csv.Error) as file_error:
        print_message_utilities.print_error(
            f"Error generating unified files: {file_error}")
