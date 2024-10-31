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
"""

import csv
from dataclasses import dataclass
from typing import List, Final, Iterator, Dict, Set
import kicad_capacitor_symbol_generator as ki_csg
import series_specs_capacitors as ssc
import file_handler_utilities as utils


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
    series_type: ssc.SeriesType
    specs: ssc.SeriesSpec


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


def get_characteristic_code(capacitance: float, specs: ssc.SeriesSpec) -> str:
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


def generate_datasheet_url(mpn: str, specs: ssc.SeriesSpec) -> str:
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


def create_part_info(params: PartParameters) -> ssc.PartInfo:
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

    return ssc.PartInfo(
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


def generate_part_numbers(specs: ssc.SeriesSpec) -> List[ssc.PartInfo]:
    """Generate all valid part numbers for a series specification.

    Args:
        specs: Complete series specifications

    Returns:
        List of PartInfo objects for all valid component combinations,
        sorted by dielectric type and capacitance value
    """
    parts_list: List[ssc.PartInfo] = []

    for series_type in ssc.SeriesType:
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
    unified_parts_list: List[ssc.PartInfo]
) -> None:
    """Generate CSV and KiCad files for a specific series.

    Args:
        series_name: Series identifier (must exist in SERIES_SPECS)
        unified_parts_list: List to append generated parts to

    Raises:
        ValueError: If series_name is not found in SERIES_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Generated files are saved in 'data/' and 'series_kicad_sym/'
        directories. The directories must exist before running this function.
    """
    if series_name not in ssc.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = ssc.SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")
    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"CAPACITORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    utils.write_to_csv(parts_list, csv_filename, HEADER_MAPPING)
    print(f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        ki_csg.generate_kicad_symbol(
            f'data/{csv_filename}',
            f'series_kicad_sym/{symbol_filename}')
        print(f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError as file_error:
        print(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print(f"CSV processing error: {csv_error}")
    except IOError as io_error:
        print(f"I/O error when generating KiCad symbol file: {io_error}")

    # Add parts to unified list
    unified_parts_list.extend(parts_list)


def generate_unified_files(
    all_parts: List[ssc.PartInfo],
        unified_csv: str,
        unified_symbol: str
) -> None:
    """Generate unified CSV and KiCad files containing all series.

    Args:
        all_parts: Complete list of parts to include in unified files

    Raises:
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails or data formatting is invalid
        IOError: If file operations fail due to permissions or disk space

    Note:
        Creates two files:
        - data/UNITED_CAPACITORS_DATA_BASE.csv
        - UNITED_CAPACITORS_DATA_BASE.kicad_sym

        The 'data' directory must exist before running this function.
        Existing files will be overwritten.
    """
    # Write unified CSV file
    utils.write_to_csv(all_parts, unified_csv, HEADER_MAPPING)
    print(f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        ki_csg.generate_kicad_symbol(f'data/{unified_csv}', unified_symbol)
        print("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as file_error:
        print(f"Unified CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print(f"CSV processing error for unified file: {csv_error}")
    except IOError as io_error:
        print(
            f"I/O error when generating unified KiCad symbol file: {io_error}")


if __name__ == "__main__":
    try:
        unified_parts: List[ssc.PartInfo] = []

        for series in ssc.SERIES_SPECS:
            print(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, unified_parts)

        # Generate unified files after all series are processed
        UNIFIED_CSV = "UNITED_CAPACITORS_DATA_BASE.csv"
        UNIFIED_SYMBOL = "UNITED_CAPACITORS_DATA_BASE.kicad_sym"
        print("\nGenerating unified files:")
        generate_unified_files(unified_parts, UNIFIED_CSV, UNIFIED_SYMBOL)

    except (csv.Error, IOError) as file_error:
        print(f"Error generating unified files: {file_error}")
