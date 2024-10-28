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
from typing import List, NamedTuple, Final, Iterator, Dict
from enum import Enum
import kicad_resistor_symbol_generator as ki_rsg


class SeriesType(Enum):
    """Enumeration for resistor series types."""
    E96 = "E96"
    E24 = "E24"


class PartInfo(NamedTuple):
    """Structure to hold component part information."""
    symbol_name: str
    reference: str
    value: float
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    tolerance: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    series: str
    trustedparts_link: str


class SeriesSpec(NamedTuple):
    """Specifications for a resistor series."""
    base_series: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    power_rating: str
    max_resistance: int
    packaging_options: List[str]
    tolerance_map: Dict[SeriesType, Dict[str, str]]
    datasheet: str
    manufacturer: str
    trustedparts_url: str
    high_resistance_tolerance: Dict[str, str] | None = None


# Series specifications
SERIES_SPECS: Final[Dict[str, SeriesSpec]] = {
    "ERJ-2RK": SeriesSpec(
        base_series="ERJ-2RK",
        footprint="footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=['X'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'J': '5%'}
        },
        datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/" +
        "RDA0000/AOA0000C304.pdf",
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-3EK": SeriesSpec(
        base_series="ERJ-3EK",
        footprint="footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'J': '5%'}
        },
        datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/" +
        "RDA0000/AOA0000C304.pdf",
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-6EN": SeriesSpec(
        base_series="ERJ-6EN",
        footprint="footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        max_resistance=2_200_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'J': '5%'}
        },
        datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/" +
        "RDA0000/AOA0000C304.pdf",
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/",
        high_resistance_tolerance={'F': '1%'}
    ),
    "ERJ-P08": SeriesSpec(
        base_series="ERJ-P08",
        footprint="footprints:R_1206_3216Metric",
        voltage_rating="500V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.66W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'F': '1%'}
        },
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"
        ),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-P06": SeriesSpec(
        base_series="ERJ-P06",
        footprint="footprints:R_0805_2012Metric",
        voltage_rating="400V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.5W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'F': '1%'}
        },
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"
        ),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-P03": SeriesSpec(
        base_series="ERJ-P03",
        footprint="footprints:R_0603_1608Metric",
        voltage_rating="150V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.25W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'F': '1%'}
        },
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"
        ),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
}

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
    specs: SeriesSpec
) -> PartInfo:
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

    return PartInfo(
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


def generate_part_numbers(specs: SeriesSpec) -> List[PartInfo]:
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
    parts_list: List[PartInfo] = []

    for series_type in SeriesType:
        base_values = (
            E96_BASE_VALUES if series_type == SeriesType.E96
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


def write_to_csv(
    parts_list: List[PartInfo],
    output_file: str,
    encoding: str = 'utf-8'
) -> None:
    """
    Write component specifications to a CSV file.

    Creates a CSV file in the 'data' directory containing all component
    specifications including:
    - Symbol and reference designators
    - Component values and tolerances
    - Physical specifications (case size, voltage rating)
    - Manufacturer information and part numbers
    - Vendor links

    Args:
        parts_list: List of PartInfo instances to write
        output_file: Name of the output file
        encoding: Character encoding for the CSV file (default: utf-8)

    Raises:
        IOError: If unable to create or write to the output file
    """
    headers: Final[List[str]] = [
        'Symbol Name', 'Reference', 'Value', 'Footprint', 'Datasheet',
        'Description', 'Manufacturer', 'MPN', 'Tolerance', 'Voltage Rating',
        'Case Code - in', 'Case Code - mm', 'Series',
        'Trustedparts Search'
    ]

    with open(f'data/{output_file}', 'w', newline='', encoding=encoding) \
            as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for part_info in parts_list:
            writer.writerow([
                part_info.symbol_name,
                part_info.reference,
                format_resistance_value(part_info.value),
                part_info.footprint,
                part_info.datasheet,
                part_info.description,
                part_info.manufacturer,
                part_info.mpn,
                part_info.tolerance,
                part_info.voltage_rating,
                part_info.case_code_in,
                part_info.case_code_mm,
                part_info.series,
                part_info.trustedparts_link
            ])


def generate_files_for_series(
    series_name: str,
    unified_parts_list: List[PartInfo]
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
    if series_name not in SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")
    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"RESISTORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    write_to_csv(parts_list, csv_filename)
    print(f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        ki_rsg.generate_kicad_symbol(
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


def generate_unified_files(all_parts: List[PartInfo]) -> None:
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
    unified_csv = "UNITED_RESISTORS_DATA_BASE.csv"
    unified_symbol = "UNITED_RESISTORS_DATA_BASE.kicad_sym"

    # Write unified CSV file
    write_to_csv(all_parts, unified_csv)
    print(f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        ki_rsg.generate_kicad_symbol(f'data/{unified_csv}', unified_symbol)
        print("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as file_error:
        print(f"Unified CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print(f"CSV processing error for unified file: {csv_error}")
    except IOError as io_error:
        print(
            f"I/O error when generating unified KiCad symbol file: {io_error}")


if __name__ == "__main__":
    unified_parts: List[PartInfo] = []

    # Generate individual series files and collect all parts
    for current_series in SERIES_SPECS:
        try:
            generate_files_for_series(current_series, unified_parts)
        except ValueError as val_error:
            print(
                "Invalid series specification for "
                f"{current_series}: {val_error}")
        except (csv.Error, IOError) as file_error:
            print(f"File operation error for {current_series}: {file_error}")

    # Generate unified files after all series are processed
    try:
        generate_unified_files(unified_parts)
    except (csv.Error, IOError) as file_error:
        print(f"Error generating unified files: {file_error}")
