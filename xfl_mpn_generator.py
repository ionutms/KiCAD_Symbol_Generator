"""
Sumida XFL3012 Series Part Number Generator

This script generates part numbers for Sumida XFL3012 series inductors.
It supports E6 standard values and handles component specifications like
inductance, current ratings, and packaging options.

The script generates:
- Part numbers following Sumida's naming conventions
- CSV files containing component specifications and parameters
- KiCad symbol files for electronic design automation

Features:
- Supports E6 inductance value series
- Handles inductance values from 0.47µH to 100µH
- Includes vendor links and detailed component specifications
- Exports in industry-standard formats (CSV, KiCad)
"""

import csv
from typing import List, NamedTuple, Final, Dict
import kicad_inductor_symbol_generator as ki_isg


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
    inductance: str
    tolerance: str
    dcr_max: str
    idc_rated: str
    idc_saturated: str
    series: str
    height: str
    octopart_link: str


class SeriesSpec(NamedTuple):
    """Specifications for an inductor series."""
    base_series: str
    footprint: str
    height: str
    tolerance: str
    dcr_map: Dict[float, str]
    current_ratings: Dict[float, Dict[str, str]]
    datasheet: str


# Constants
MANUFACTURER: Final[str] = "Sumida"
OCTOPART_BASE_URL: Final[str] = "https://octopart.com/search?q="

# E6 series values for inductors (µH)
E6_VALUES: Final[List[float]] = [
    # 0.47, 0.68, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8, 10, 15, 22, 33, 47, 68,
    100
]

# Series specifications
SERIES_SPECS: Final[SeriesSpec] = SeriesSpec(
    base_series="XFL3012",
    footprint="footprints:L_Sumida_XFL3012",
    height="1.2mm",
    tolerance="±20%",
    # DCR values in mΩ for each inductance value
    dcr_map={
        0.47: "21.0",
        0.68: "26.0",
        1.0: "32.0",
        1.5: "42.0",
        2.2: "58.0",
        3.3: "84.0",
        4.7: "115",
        6.8: "165",
        10: "240",
        15: "350",
        22: "500",
        33: "730",
        47: "1050",
        68: "1500",
        100: "2200"
    },
    # Current ratings (Idc rated and saturated) for each inductance value
    current_ratings={
        0.47: {"rated": "5.10", "saturated": "6.80"},
        0.68: {"rated": "4.30", "saturated": "5.70"},
        1.0: {"rated": "3.60", "saturated": "4.80"},
        1.5: {"rated": "3.00", "saturated": "4.00"},
        2.2: {"rated": "2.50", "saturated": "3.30"},
        3.3: {"rated": "2.10", "saturated": "2.80"},
        4.7: {"rated": "1.75", "saturated": "2.30"},
        6.8: {"rated": "1.45", "saturated": "1.90"},
        10: {"rated": "1.20", "saturated": "1.60"},
        15: {"rated": "1.00", "saturated": "1.30"},
        22: {"rated": "0.82", "saturated": "1.10"},
        33: {"rated": "0.67", "saturated": "0.89"},
        47: {"rated": "0.56", "saturated": "0.75"},
        68: {"rated": "0.47", "saturated": "0.62"},
        100: {"rated": "0.39", "saturated": "0.52"}
    },
    datasheet="https://www.sumida.com/products/pdf/XFL3012.pdf"
)


def format_inductance_value(inductance: float) -> str:
    """
    Convert an inductance value to a human-readable string format.

    Args:
        inductance: The inductance value in µH

    Returns:
        A formatted string with appropriate unit suffix
    """
    if inductance < 1:
        return f"{inductance*1000:.0f}nH"
    return f"{inductance:.1f}µH"


def generate_value_code(inductance: float) -> str:
    """
    Generate the value code portion of a Sumida part number.

    Args:
        inductance: The inductance value in µH

    Returns:
        A 3-digit string representing the value code

    Example:
        4.7µH -> "475" (47 × 10^-1)
        10µH -> "100" (10 × 10^0)
    """
    if inductance < 1:
        return f"{int(inductance * 1000):03d}"
    elif inductance < 10:
        return f"{int(inductance * 10):02d}0"
    else:
        return f"{int(inductance):03d}"


def create_part_info(inductance: float, specs: SeriesSpec) -> PartInfo:
    """
    Create a PartInfo instance with complete component specifications.

    Args:
        inductance: Inductance value in µH
        specs: SeriesSpec instance containing series specifications

    Returns:
        PartInfo instance containing all component details
    """
    value_code = generate_value_code(inductance)
    mpn = f"{specs.base_series}-{value_code}MEC"
    symbol_name = f"L_{mpn}"

    description = (
        f"INDUCTOR SMD {format_inductance_value(inductance)} "
        f"{specs.tolerance} {specs.height} "
        f"RATED {specs.current_ratings[inductance]['rated']}A"
    )

    octopart_link = f"{OCTOPART_BASE_URL}{mpn}"

    return PartInfo(
        symbol_name=symbol_name,
        reference="L",
        value=inductance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=description,
        manufacturer=MANUFACTURER,
        mpn=mpn,
        inductance=format_inductance_value(inductance),
        tolerance=specs.tolerance,
        dcr_max=f"{specs.dcr_map[inductance]}mΩ",
        idc_rated=f"{specs.current_ratings[inductance]['rated']}A",
        idc_saturated=f"{specs.current_ratings[inductance]['saturated']}A",
        series=specs.base_series,
        height=specs.height,
        octopart_link=octopart_link
    )


def generate_part_numbers(specs: SeriesSpec) -> List[PartInfo]:
    """
    Generate all possible part numbers for the inductor series.

    Args:
        specs: SeriesSpec instance containing series specifications

    Returns:
        List of PartInfo instances for all valid combinations
    """
    return [create_part_info(value, specs) for value in E6_VALUES]


def write_to_csv(
    parts_list: List[PartInfo],
    output_file: str,
    encoding: str = 'utf-8'
) -> None:
    """
    Write component specifications to a CSV file.

    Args:
        parts_list: List of PartInfo instances to write
        output_file: Name of the output file
        encoding: Character encoding for the CSV file (default: utf-8)
    """
    headers: Final[List[str]] = [
        'Symbol Name', 'Reference', 'Value', 'Footprint', 'Datasheet',
        'Description', 'Manufacturer', 'MPN', 'Inductance', 'Tolerance',
        'DCR Max', 'Idc Rated', 'Idc Saturated', 'Series', 'Height',
        'Octopart Search'
    ]

    with open(f'data/{output_file}', 'w', newline='', encoding=encoding) \
            as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for part_info in parts_list:
            writer.writerow([
                part_info.symbol_name,
                part_info.reference,
                format_inductance_value(part_info.value),
                part_info.footprint,
                part_info.datasheet,
                part_info.description,
                part_info.manufacturer,
                part_info.mpn,
                part_info.inductance,
                part_info.tolerance,
                part_info.dcr_max,
                part_info.idc_rated,
                part_info.idc_saturated,
                part_info.series,
                part_info.height,
                part_info.octopart_link
            ])


def generate_files() -> None:
    """
    Generate CSV and KiCad symbol files for the XFL3012 series.

    Creates:
    1. A CSV file containing all component specifications
    2. A KiCad symbol file for use in electronic design

    Raises:
        FileNotFoundError: If CSV file cannot be found for symbol generation
        csv.Error: If CSV processing fails
        IOError: If file operations fail
    """
    series_code = SERIES_SPECS.base_series
    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"INDUCTORS_{series_code}_DATA_BASE.kicad_sym"

    # Generate part numbers and write to CSV
    parts_list = generate_part_numbers(SERIES_SPECS)
    write_to_csv(parts_list, csv_filename)
    print(f"Generated {len(parts_list)} part numbers in '{csv_filename}'")

    # Generate KiCad symbol file
    try:
        ki_isg.generate_kicad_symbol(f'data/{csv_filename}', symbol_filename)
        print(f"KiCad symbol file '{symbol_filename}' generated successfully.")
    except FileNotFoundError as file_error:
        print(f"CSV file not found: {file_error}")
    except csv.Error as csv_error:
        print(f"CSV processing error: {csv_error}")
    except IOError as io_error:
        print(f"I/O error when generating KiCad symbol file: {io_error}")


if __name__ == "__main__":
    try:
        generate_files()
    except (csv.Error, IOError) as file_error:
        print(f"Error generating files: {file_error}")
