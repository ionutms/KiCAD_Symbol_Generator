"""
Murata GCM Series Capacitor Part Number Generator

Generates part numbers for Murata GCM series capacitors based on
standard capacitance values and specifications. Outputs both CSV
and KiCad symbol files.
"""

import csv
from typing import List, NamedTuple, Final, Iterator, Dict, Set
from enum import Enum
import kicad_capacitor_symbol_generator as ki_csg


class SeriesType(Enum):
    """Enumeration for capacitor series types."""
    X7R = "X7R"


class PartInfo(NamedTuple):
    """Structure to hold component part information."""
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
    """Specifications for a capacitor series."""
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


# Constants
MANUFACTURER: Final[str] = "Murata Electronics"
TRUSTEDPARTS_BASE_URL: Final[str] = "https://www.trustedparts.com/en/search/"
DATASHEET_BASE_URL: Final[str] = \
    "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/"


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
    """
    Convert capacitance value to human-readable format.
    Handles unit conversion to ensure most appropriate unit is used.
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
    """
    Generate the capacitance code portion of the Murata part number.
    Format:
    - For values < 10pF: uses R notation (e.g., 1R5 for 1.5pF)
    - For values ≥ 10pF and < 1000pF: direct value in pF (e.g., 100pF -> "101")
    - For values ≥ 1000pF: first two digits + zeros (e.g., 1000pF -> "102")
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


def get_gcm155_code(capacitance: float) -> str:
    """
    Determine the characteristic code for the GCM155 series based on
    capacitance value.

    Args:
        capacitance (float): Capacitance value in Farads.

    Returns:
        str:
            The characteristic code for the GCM155 series based on
            capacitance thresholds.

    Logic:
        - Returns "E02" if capacitance > 22nF.
        - Returns "A55" if 5.6nF <= capacitance <= 22nF.
        - Returns "A37" if capacitance < 5.6nF.
    """
    if capacitance > 22e-9:
        return "E02"
    if capacitance >= 5.6e-9:
        return "A55"
    return "A37"


def get_gcm188_code(capacitance: float) -> str:
    """
    Determine the characteristic code for the GCM188 series based on
    capacitance value.

    Args:
        capacitance (float): Capacitance value in Farads.

    Returns:
        str:
            The characteristic code for the GCM188 series based on
            capacitance thresholds.

    Logic:
        - Returns "A64" if capacitance > 100nF.
        - Returns "A57" if 47nF < capacitance <= 100nF.
        - Returns "A55" if 27nF <= capacitance <= 47nF.
        - Returns "A37" if capacitance < 27nF.
    """
    if capacitance > 100e-9:
        return "A64"
    if 47e-9 < capacitance <= 100e-9:
        return "A57"
    if capacitance >= 27e-9:
        return "A55"
    return "A37"


# Add characteristic code function for GCM216
def get_gcm216_code(capacitance: float) -> str:
    """
    Determine the characteristic code for the GCM216 series based on
    capacitance value.

    Args:
        capacitance (float): Capacitance value in Farads.

    Returns:
        str: The characteristic code for the GCM216 series.
    """
    if capacitance > 22e-9:
        return "A55"
    return "A37"


def get_gcm31m_code(capacitance: float) -> str:
    """
    Determine the characteristic code for the GCM31M series based on
    capacitance value.

    Args:
        capacitance (float): Capacitance value in Farads.

    Returns:
        str: The characteristic code for the GCM31M series.
    """
    if capacitance >= 560e-9:
        return "A55"
    if capacitance >= 100e-9:
        return "A37"
    return "A55"


def get_gcm31c_code(capacitance: float) -> str:
    """
    Determine the characteristic code for the GCM31C series based on
    capacitance value.

    Args:
        capacitance (float): Capacitance value in Farads.

    Returns:
        str: The characteristic code for the GCM31C series.
    """
    if capacitance >= 4.7e-6:
        return "A55"


def get_characteristic_code(capacitance: float, specs: SeriesSpec) -> str:
    """
    Determine the characteristic code based on capacitance and
    series specification.

    Args:
        capacitance (float): Capacitance value in Farads.
        specs (SeriesSpec):
            An instance of SeriesSpec containing series information,
            such as the `base_series` attribute.

    Returns:
        str: The characteristic code for the specified series and capacitance.

    Raises:
        ValueError:
            If the series in `specs.base_series` is unknown or unsupported.
    """
    if specs.base_series == "GCM155":
        return get_gcm155_code(capacitance)
    if specs.base_series == "GCM188":
        return get_gcm188_code(capacitance)
    if specs.base_series == "GCM216":
        return get_gcm216_code(capacitance)
    if specs.base_series == "GCM31M":
        return get_gcm31m_code(capacitance)
    if specs.base_series == "GCM31C":
        return get_gcm31m_code(capacitance)

    raise ValueError(f"Unknown series: {specs.base_series}")


def generate_standard_values(
    min_value: float,
    max_value: float,
    excluded_values: Set[float]
) -> Iterator[float]:
    """
    Generate standard capacitance values (E12 series) within range.

    Args:
        min_value: Minimum capacitance value in Farads
        max_value: Maximum capacitance value in Farads
        excluded_values: Set of capacitance values to exclude
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


def create_part_info(
    capacitance: float,
    tolerance_code: str,
    tolerance_value: str,
    packaging: str,
    series_type: SeriesType,
    specs: SeriesSpec
) -> PartInfo:
    """Create a PartInfo instance for given parameters."""
    capacitance_code = generate_capacitance_code(capacitance)
    characteristic_code = get_characteristic_code(capacitance, specs)
    formatted_value = format_capacitance(capacitance)

    mpn = (
        f"{specs.base_series}"
        f"{specs.dielectric_code[series_type]}"
        f"{specs.voltage_code}"
        f"{capacitance_code}"
        f"{tolerance_code}"
        f"{characteristic_code}"
        f"{packaging}"
    )

    symbol_name = f"C_{mpn}"
    description = (
        f"CAP SMD {formatted_value} "
        f"{series_type.value} {tolerance_value} "
        f"{specs.case_code_in} {specs.voltage_rating}"
    )
    trustedparts_link = f"{TRUSTEDPARTS_BASE_URL}{mpn}"
    datasheet_url = generate_datasheet_url(mpn)

    return PartInfo(
        symbol_name=symbol_name,
        reference="C",
        value=capacitance,
        formatted_value=formatted_value,
        footprint=specs.footprint,
        datasheet=datasheet_url,
        description=description,
        manufacturer=MANUFACTURER,
        mpn=mpn,
        dielectric=series_type.value,
        tolerance=tolerance_value,
        voltage_rating=specs.voltage_rating,
        case_code_in=specs.case_code_in,
        case_code_mm=specs.case_code_mm,
        series=specs.base_series,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(specs: SeriesSpec) -> List[PartInfo]:
    """Generate all possible part numbers for both X7R series."""
    parts_list: List[PartInfo] = []

    for series_type in SeriesType:
        if series_type in specs.value_range:
            min_val, max_val = specs.value_range[series_type]

            for capacitance in generate_standard_values(
                min_val, max_val, specs.excluded_values
            ):
                for tolerance_code, tolerance_value in \
                        specs.tolerance_map[series_type].items():
                    for packaging in specs.packaging_options:
                        parts_list.append(create_part_info(
                            capacitance,
                            tolerance_code,
                            tolerance_value,
                            packaging,
                            series_type,
                            specs
                        ))

    return sorted(parts_list, key=lambda x: (x.dielectric, x.value))


def write_to_csv(
    parts_list: List[PartInfo],
    output_file: str,
    encoding: str = 'utf-8'
) -> None:
    """Write the generated part numbers to a CSV file."""
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


def generate_files_for_series(series_name: str) -> None:
    """Generate CSV and KiCad symbol files for a specific series."""
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
        ki_csg.generate_kicad_symbol(f'data/{csv_filename}', symbol_filename)
        print(f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError as file_error:
        print(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print(f"CSV processing error: {csv_error}")
    except IOError as io_error:
        print(f"I/O error when generating KiCad symbol file: {io_error}")


if __name__ == "__main__":
    for current_series in SERIES_SPECS:
        try:
            generate_files_for_series(current_series)
        except ValueError as val_error:
            print(
                "Invalid series specification for "
                f"{current_series}: {val_error}")
        except (csv.Error, IOError) as file_error:
            print(f"File operation error for {current_series}: {file_error}")
