"""
Murata GCM Series Capacitor Part Number Generator

Generates part numbers for Murata GCM series capacitors based on
standard capacitance values and specifications. Outputs both CSV
and KiCad symbol files.
"""

import csv
from typing import List, NamedTuple, Final, Iterator, Dict
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
    datasheet: str
    value_range: Dict[SeriesType, tuple[float, float]]
    voltage_code: str
    dielectric_code: Dict[SeriesType, str]


# Constants
MANUFACTURER: Final[str] = "Murata Electronics"
TRUSTEDPARTS_BASE_URL: Final[str] = "https://www.trustedparts.com/en/search/"


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
        datasheet=(
            "https://www.murata.com/-/media/webrenewal/support/"
            "library/catalog/products/capacitor/mlcc/c02e.ashx"
        ),
        value_range={
            SeriesType.X7R: (220e-12, 0.1e-6)  # 220pF to 0.1µF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        }
    ),
}


def format_capacitance(capacitance: float) -> str:
    """Convert capacitance value to human-readable format."""
    if capacitance >= 1e-6:
        return f"{capacitance/1e-6:.3g} µF"
    if capacitance >= 1e-9:
        return f"{capacitance/1e-9:.3g} nF"
    return f"{capacitance/1e-12:.3g} pF"


def generate_capacitance_code(capacitance: float) -> str:
    """
    Generate the capacitance code portion of the Murata part number.
    Format: 3 characters for values >= 10pF, 3 characters with 'R' for < 10pF
    """
    pf_value = capacitance * 1e12

    if pf_value < 10:
        whole = int(pf_value)
        decimal = int((pf_value - whole) * 10)
        return f"{whole}R{decimal}"

    significant = round(pf_value)
    if significant % 10 == 0:
        significant += 1

    return f"{significant:03d}"


def get_characteristic_code(capacitance: float) -> str:
    """Determine the characteristic code based on capacitance value."""
    value_uf = capacitance * 1e6
    return "A55" if value_uf >= 0.01 else "A37"


def generate_standard_values(
    min_value: float,
    max_value: float
) -> Iterator[float]:
    """Generate standard capacitance values (E12 series) within range."""
    e12_multipliers: Final[List[float]] = [
        1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2
    ]

    decade = 1.0e-12
    while decade <= max_value:
        for multiplier in e12_multipliers:
            value = decade * multiplier
            if min_value <= value <= max_value:
                yield value
        decade *= 10


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
    characteristic_code = get_characteristic_code(capacitance)

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
        f"CAP SMD {format_capacitance(capacitance)} "
        f"{series_type.value} {tolerance_value} "
        f"{specs.case_code_in} {specs.voltage_rating}"
    )
    trustedparts_link = f"{TRUSTEDPARTS_BASE_URL}{mpn}"

    return PartInfo(
        symbol_name=symbol_name,
        reference="C",
        value=capacitance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
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

            for capacitance in generate_standard_values(min_val, max_val):
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

    with open(output_file, 'w', newline='', encoding=encoding) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for part_info in parts_list:
            writer.writerow([
                part_info.symbol_name,
                part_info.reference,
                format_capacitance(part_info.value),
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
        ki_csg.generate_kicad_symbol(csv_filename, symbol_filename)
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
