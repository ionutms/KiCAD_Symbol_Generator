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
from typing import List, NamedTuple, Final, Iterator, Dict, Set
from enum import Enum
import kicad_capacitor_symbol_generator as ki_csg


class SeriesType(Enum):
    """Enumeration of supported capacitor series dielectric types."""
    X7R = "X7R"


class PartInfo(NamedTuple):
    """Container for capacitor part information.

    Attributes:
        symbol_name: KiCad symbol identifier
        reference: Component reference designator
        value: Capacitance value in Farads
        formatted_value: Human-readable capacitance value with units
        footprint: PCB footprint reference
        datasheet: URL to component datasheet
        description: Component description text
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        dielectric: Dielectric material type
        tolerance: Component tolerance value
        voltage_rating: Maximum voltage rating
        case_code_in: Package size in inches
        case_code_mm: Package size in millimeters
        series: Component series identifier
        trustedparts_link: URL to component listing
    """
    symbol_name: str
    reference: str
    value: float
    formatted_value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    dielectric: str
    tolerance: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    series: str
    trustedparts_link: str


class SeriesSpec(NamedTuple):
    """Specifications defining a capacitor series.

    Attributes:
        base_series: Base part number series
        footprint: PCB footprint identifier
        voltage_rating: Maximum voltage specification
        case_code_in: Package dimensions (inches)
        case_code_mm: Package dimensions (millimeters)
        packaging_options: Available packaging codes
        tolerance_map: Mapping of series types to tolerance codes and values
        value_range: Valid capacitance range per series type
        voltage_code: Voltage rating code for part number
        dielectric_code: Dielectric material codes per series type
        excluded_values: Set of unsupported capacitance values
    """
    base_series: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    packaging_options: List[str]
    tolerance_map: Dict[SeriesType, Dict[str, str]]
    value_range: Dict[SeriesType, tuple[float, float]]
    voltage_code: str
    dielectric_code: Dict[SeriesType, str]
    excluded_values: Set[float]


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
    series_type: SeriesType
    specs: SeriesSpec


# Constants
MANUFACTURER: Final[str] = "Murata Electronics"
TRUSTEDPARTS_BASE_URL: Final[str] = "https://www.trustedparts.com/en/search/"
DATASHEET_BASE_URL: Final[str] = \
    "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/"


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

# Series specifications
SERIES_SPECS: Final[Dict[str, SeriesSpec]] = {
    "GCM155": SeriesSpec(
        base_series="GCM155",
        footprint="footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        packaging_options=['D', 'J'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (220e-12, 0.1e-6)  # 220pF to 0.1µF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={
            27e-9,  # 27 nF
            39e-9,  # 39 nF
            56e-9,  # 56 nF
            82e-9   # 82 nF
        }
    ),
    "GCM188": SeriesSpec(
        base_series="GCM188",
        footprint="footprints:C_0603_1608Metric",
        voltage_rating="50V",
        case_code_in="0603",
        case_code_mm="1608",
        packaging_options=['D', 'J'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (1e-9, 220e-9)  # Updated: 1nF to 220nF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={
            120e-9,  # 120 nF
            180e-9,  # 180 nF,
        }
    ),
    "GCM216": SeriesSpec(
        base_series="GCM216",
        footprint="footprints:C_0805_2012Metric",
        voltage_rating="50V",
        case_code_in="0805",
        case_code_mm="2012",
        packaging_options=['D', 'J'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (1e-9, 22e-9)  # 1nF to 22nF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={}
    ),
    "GCM31M": SeriesSpec(
        base_series="GCM31M",
        footprint="footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=['K', 'L'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (100e-9, 1e-6)  # 100nF to 1µF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={
            180e-9,  # 180 nF
            560e-9,  # 560 nF,
        }
    ),
    "GCM31C": SeriesSpec(  # Added new GCM31C series
        base_series="GCM31C",
        footprint="footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=['K', 'L'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (4.7e-6, 4.7e-6)  # Only 4.7µF
        },
        voltage_code="1E",  # 25V code
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values=set()
    ),
}


def format_capacitance(capacitance: float) -> str:
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
        Three-character code representing the capacitance value

    Format:
        - Values < 10pF: Use R notation (e.g., 1R5 for 1.5pF)
        - Values ≥ 10pF and < 1000pF: Direct pF value (e.g., 101)
        - Values ≥ 1000pF: First two digits + zeros (e.g., 102)
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


def get_characteristic_code(capacitance: float, specs: SeriesSpec) -> str:
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
        Standard E12 series values between min and max,
        excluding specified values
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


def generate_datasheet_url(mpn: str) -> str:
    """Generate the datasheet URL for a given Murata part number."""
    base_mpn = mpn[:-1]
    return f"{DATASHEET_BASE_URL}{base_mpn}-01.pdf"


def create_part_info(params: PartParameters) -> PartInfo:
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
    formatted_value = format_capacitance(params.capacitance)

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
    trustedparts_link = f"{TRUSTEDPARTS_BASE_URL}{mpn}"
    datasheet_url = generate_datasheet_url(mpn)

    return PartInfo(
        symbol_name=symbol_name,
        reference="C",
        value=params.capacitance,
        formatted_value=formatted_value,
        footprint=params.specs.footprint,
        datasheet=datasheet_url,
        description=description,
        manufacturer=MANUFACTURER,
        mpn=mpn,
        dielectric=params.series_type.value,
        tolerance=params.tolerance_value,
        voltage_rating=params.specs.voltage_rating,
        case_code_in=params.specs.case_code_in,
        case_code_mm=params.specs.case_code_mm,
        series=params.specs.base_series,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(specs: SeriesSpec) -> List[PartInfo]:
    """Generate all valid part numbers for a series specification.

    Args:
        specs: Complete series specifications

    Returns:
        List of PartInfo objects for all valid component combinations,
        sorted by dielectric type and capacitance value
    """
    parts_list: List[PartInfo] = []

    for series_type in SeriesType:
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


def write_to_csv(
    parts_list: List[PartInfo],
    output_file: str,
    encoding: str = 'utf-8'
) -> None:
    """Write part information to CSV file.

    Args:
        parts_list: List of parts to write
        output_file: Output filename
        encoding: Character encoding for file (default: utf-8)

    The file is created in the 'data' subdirectory.
    """
    headers: Final[List[str]] = [
        'Symbol Name', 'Reference', 'Value', 'Footprint', 'Datasheet',
        'Description', 'Manufacturer', 'MPN', 'Dielectric', 'Tolerance',
        'Voltage Rating', 'Case Code - in', 'Case Code - mm', 'Series',
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
                part_info.formatted_value,
                part_info.footprint,
                part_info.datasheet,
                part_info.description,
                part_info.manufacturer,
                part_info.mpn,
                part_info.dielectric,
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
    """Generate CSV and KiCad files for a specific series.

    Args:
        series_name: Series identifier (must exist in SERIES_SPECS)
        unified_parts_list: List to append generated parts to

    Raises:
        ValueError: If series_name is not found in SERIES_SPECS
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails
        IOError: If file operations fail
    """
    if series_name not in SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = SERIES_SPECS[series_name]
    series_code = series_name.replace("-", "")
    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"CAPACITORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(specs)
    write_to_csv(parts_list, csv_filename)
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


def generate_unified_files(all_parts: List[PartInfo]) -> None:
    """Generate unified CSV and KiCad files containing all series.

    Args:
        all_parts: Complete list of parts to include

    Creates:
        - UNITED_CAPACITORS_DATA_BASE.csv
        - UNITED_CAPACITORS_DATA_BASE.kicad_sym

    Raises:
        FileNotFoundError: If CSV file creation fails
        csv.Error: If CSV processing fails
        IOError: If file operations fail
    """
    unified_csv = "UNITED_CAPACITORS_DATA_BASE.csv"
    unified_symbol = "UNITED_CAPACITORS_DATA_BASE.kicad_sym"

    # Write unified CSV file
    write_to_csv(all_parts, unified_csv)
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
