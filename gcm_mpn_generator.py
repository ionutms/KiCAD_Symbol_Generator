"""
Murata GCM Series Capacitor Part Number Generator

Generates part numbers for Murata GCM series capacitors based on
standard capacitance values and specifications. Outputs both CSV
and KiCad symbol files.
"""

import csv
from enum import Enum
from typing import Dict, Final, Iterator, List, NamedTuple
import kicad_capacitor_symbol_generator as ki_csg


class SeriesType(Enum):
    """Enumeration for capacitor series types."""
    X7R = "X7R"
    X5R = "X5R"
    C0G = "C0G"


class PartInfo(NamedTuple):
    """Structure to hold component part information."""
    symbol_name: str
    reference: str
    value: float  # in Farads
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
    qualification: str
    trustedparts_link: str


class SeriesSpec(NamedTuple):
    """Specifications for a capacitor series."""
    base_series: str
    footprint: str
    voltage_ratings: List[str]
    case_code_in: str
    case_code_mm: str
    min_temp: str
    max_temp: str
    packaging_options: List[str]
    tolerance_options: List[str]
    qualification: str
    datasheet: str
    value_range: Dict[SeriesType, tuple[float, float]]


# Constants
MANUFACTURER: Final[str] = "Murata Electronics"
BASE_FOOTPRINT: Final[str] = "footprints:C_"
TRUSTEDPARTS_BASE: Final[str] = "https://www.trustedparts.com/en/search/"

# Dielectric code mapping
DIELECTRIC_MAP: Final[Dict[str, str]] = {
    "X7R": "R7",
    "X5R": "R6",
    "C0G": "C0"
}

# Series specifications
SERIES_SPECS: Final[Dict[str, SeriesSpec]] = {
    "GCM155": SeriesSpec(
        base_series="GCM155",
        footprint=f"{BASE_FOOTPRINT}0402_1005Metric",
        voltage_ratings=["1H"],  # 50V code
        case_code_in="0402",
        case_code_mm="1005",
        min_temp="- 55 C",
        max_temp="+ 125 C",
        packaging_options=['D', 'J'],
        tolerance_options=['K'],  # 10%
        qualification="AEC-Q200",
        datasheet=(
            "https://www.murata.com/-/media/webrenewal/support/"
            "library/catalog/products/capacitor/mlcc/c02e.ashx"
        ),
        value_range={
            SeriesType.X7R: (220e-12, 0.1e-6),  # 220pF to 0.1µF
        }
    ),
    "GCM188": SeriesSpec(
        base_series="GCM188",
        footprint=f"{BASE_FOOTPRINT}0603_1608Metric",
        voltage_ratings=["1H", "2A"],  # 50V, 100V codes
        case_code_in="0603",
        case_code_mm="1608",
        min_temp="- 55 C",
        max_temp="+ 125 C",
        packaging_options=['D', 'J'],
        tolerance_options=['K', 'M'],
        qualification="AEC-Q200",
        datasheet=(
            "https://www.murata.com/-/media/webrenewal/support/"
            "library/catalog/products/capacitor/mlcc/c02e.ashx"
        ),
        value_range={
            SeriesType.X7R: (100e-12, 4.7e-6),  # 100pF to 4.7µF
            SeriesType.X5R: (1e-6, 10e-6),      # 1µF to 10µF
            SeriesType.C0G: (1e-12, 470e-12),   # 1pF to 470pF
        }
    ),
}


def get_characteristic_code(capacitance: float) -> str:
    """Determine the characteristic code based on capacitance value."""
    # Convert to microfarads for easier comparison
    value_uf = capacitance * 1e6

    if value_uf >= 0.01:  # 10nF and above
        return "A55"
    else:  # Below 10nF
        return "A37"


def format_capacitance(capacitance: float) -> str:
    """Convert capacitance value to human-readable format."""
    if capacitance >= 1e-6:
        return f"{capacitance/1e-6:.3g} µF"
    elif capacitance >= 1e-9:
        return f"{capacitance/1e-9:.3g} nF"
    else:
        return f"{capacitance/1e-12:.3g} pF"


def parse_capacitance(value_str: str) -> float:
    """Convert a capacitance string to Farads."""
    value_str = value_str.strip().lower()
    multiplier = 1e-12  # default to picofarads

    if 'uf' in value_str or 'µf' in value_str:
        multiplier = 1e-6
    elif 'nf' in value_str:
        multiplier = 1e-9

    num = float(value_str.split()[0])
    return num * multiplier


def generate_capacitance_code(capacitance: float) -> str:
    """Generate the capacitance code for Murata part number."""
    if capacitance < 1e-12 or capacitance > 1e-2:
        raise ValueError("Capacitance value out of range")

    pf_value = capacitance * 1e12

    if pf_value < 10:
        whole = int(pf_value)
        decimal = int((pf_value - whole) * 10)
        return f"{whole}R{decimal}"

    # For all other values, we ensure 3 significant digits
    # Adjust to ensure correct code format, e.g., 220pF -> 221
    significant = round(pf_value)

    # If the result is 100 or more, round to nearest three-digit number
    if significant % 10 == 0:
        significant += 1  # Fix for 220pF -> 221 instead of 2201

    return f"{significant:03d}"


def create_part_info(
    capacitance: float,
    voltage: str,
    dielectric: SeriesType,
    tolerance: str,
    packaging: str,
    specs: SeriesSpec
) -> PartInfo:
    """Create a PartInfo instance for given parameters."""
    capacitance_code = generate_capacitance_code(capacitance)
    dielectric_code = DIELECTRIC_MAP.get(dielectric.value, "R7")
    characteristic_code = get_characteristic_code(capacitance)

    mpn = (
        f"{specs.base_series}"
        f"{dielectric_code}"
        f"{voltage}"
        f"{capacitance_code}"
        f"{tolerance}"
        f"{characteristic_code}"
        f"{packaging}"
    )

    symbol_name = f"C_{mpn}"
    description = (
        f"CAP SMD {format_capacitance(capacitance)} "
        f"{dielectric.value} {tolerance}% {specs.case_code_in} {voltage}V"
    )

    return PartInfo(
        symbol_name=symbol_name,
        reference="C",
        value=capacitance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=description,
        manufacturer=MANUFACTURER,
        mpn=mpn,
        dielectric=dielectric.value,
        tolerance=tolerance,
        voltage_rating=voltage,
        case_code_in=specs.case_code_in,
        case_code_mm=specs.case_code_mm,
        series=specs.base_series,
        qualification=specs.qualification,
        trustedparts_link=f"{TRUSTEDPARTS_BASE}{mpn}"
    )


def generate_standard_values(
    min_value: float,
    max_value: float,
    multipliers: List[float] = None
) -> Iterator[float]:
    """Generate standard capacitance values within range."""
    if multipliers is None:
        multipliers = [1.0, 1.2, 1.5, 1.8, 2.2,
                       2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

    current = min_value
    while current <= max_value:
        for multiplier in multipliers:
            value = current * multiplier
            if min_value <= value <= max_value:
                yield value
        current *= 10


def generate_part_numbers(specs: SeriesSpec) -> List[PartInfo]:
    """Generate all possible part numbers for the series."""
    parts_list: List[PartInfo] = []

    for dielectric_type, (min_val, max_val) in specs.value_range.items():
        for voltage in specs.voltage_ratings:
            for capacitance in generate_standard_values(min_val, max_val):
                for tolerance in specs.tolerance_options:
                    for packaging in specs.packaging_options:
                        parts_list.append(
                            create_part_info(
                                capacitance,
                                voltage,
                                dielectric_type,
                                tolerance,
                                packaging,
                                specs
                            )
                        )

    return sorted(parts_list, key=lambda x: (x.dielectric, x.value))


def write_to_csv(
    parts_list: List[PartInfo],
    output_file: str,
    encoding: str = 'utf-8'
) -> None:
    """Write generated part numbers to CSV file."""
    headers = [
        'Symbol Name',
        'Reference',
        'Value',
        'Footprint',
        'Datasheet',
        'Description',
        'Manufacturer',
        'MPN',
        'Dielectric',
        'Tolerance',
        'Voltage Rating',
        'Case Code - in',
        'Case Code - mm',
        'Series',
        'Qualification',
        'Trustedparts Search'
    ]

    with open(output_file, 'w', newline='', encoding=encoding) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for part in parts_list:
            writer.writerow([
                part.symbol_name,
                part.reference,
                format_capacitance(part.value),
                part.footprint,
                part.datasheet,
                part.description,
                part.manufacturer,
                part.mpn,
                part.dielectric,
                part.tolerance,
                part.voltage_rating,
                part.case_code_in,
                part.case_code_mm,
                part.series,
                part.qualification,
                part.trustedparts_link
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
        ki_csg.generate_kicad_symbol(csv_filename, symbol_filename)
        print(f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filename}' not found.")
    except csv.Error as e:
        print(f"Error reading CSV file '{csv_filename}': {e}")
    except IOError as e:
        print(f"Error writing to output file '{symbol_filename}': {e}")


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
