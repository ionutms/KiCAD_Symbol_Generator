"""
Coilcraft XFL3012 Series Part Number Generator

This script generates part numbers for Coilcraft XFL3012 series inductors.
It supports E6 standard values and handles component specifications like
inductance, current ratings, and packaging options.

The script generates:
- Part numbers following Coilcraft's naming conventions
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
    trustedparts_link: str


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
MANUFACTURER: Final[str] = "Coilcraft"
TRUSTEDPARTS_BASE_URL: Final[str] = "https://www.trustedparts.com/en/search/"

# E6 series values for inductors (µH)
E6_VALUES: Final[List[float]] = [
    0.47, 0.68, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8, 10, 15, 22, 33, 47, 68, 100
]

# Series specifications - Modified for Coilcraft typical specifications
SERIES_SPECS: Final[SeriesSpec] = SeriesSpec(
    base_series="XFL3012",
    footprint="footprints:L_Coilcraft_XFL3012",
    height="1.2mm",
    tolerance="±10%",
    dcr_map={
        0.47: "18.0",
        0.68: "23.0",
        1.0: "29.0",
        1.5: "38.0",
        2.2: "52.0",
        3.3: "76.0",
        4.7: "105",
        6.8: "150",
        10: "220",
        15: "320",
        22: "460",
        33: "670",
        47: "950",
        68: "1350",
        100: "2000"
    },
    # Current ratings (Idc rated and saturated) for each inductance value
    current_ratings={
        0.47: {"rated": "5.50", "saturated": "7.00"},
        0.68: {"rated": "4.60", "saturated": "6.00"},
        1.0: {"rated": "3.80", "saturated": "5.00"},
        1.5: {"rated": "3.20", "saturated": "4.20"},
        2.2: {"rated": "2.70", "saturated": "3.50"},
        3.3: {"rated": "2.20", "saturated": "2.90"},
        4.7: {"rated": "1.85", "saturated": "2.40"},
        6.8: {"rated": "1.55", "saturated": "2.00"},
        10: {"rated": "1.30", "saturated": "1.70"},
        15: {"rated": "1.05", "saturated": "1.40"},
        22: {"rated": "0.87", "saturated": "1.15"},
        33: {"rated": "0.71", "saturated": "0.94"},
        47: {"rated": "0.59", "saturated": "0.78"},
        68: {"rated": "0.49", "saturated": "0.65"},
        100: {"rated": "0.41", "saturated": "0.54"}
    },
    # Update with actual datasheet URL
    datasheet="https://www.coilcraft.com/en-us/products/xfl3012/"
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
    Generate the value code portion of a Coilcraft part number.

    Args:
        inductance: The inductance value in µH

    Returns:
        A string representing the value code in Coilcraft format

    Example:
        4.7µH -> "4R7"
        0.47µH -> "R47"
        10µH -> "100"
    """
    if inductance < 1:
        # Format as R47 for 0.47µH
        return f"R{int(inductance * 100):02d}"
    elif inductance < 10:
        # Format as 4R7 for 4.7µH
        whole = int(inductance)
        decimal = int((inductance - whole) * 10)
        return f"{whole}R{decimal}"
    else:
        # Format as 100 for 10µH, 220 for 22µH, etc.
        return f"{int(inductance)}0"


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
    mpn = f"{specs.base_series}-{value_code}"
    symbol_name = f"L_{mpn}"

    description = (
        f"INDUCTOR SMD {format_inductance_value(inductance)} "
        f"{specs.tolerance} {specs.height} "
        f"RATED {specs.current_ratings[inductance]['rated']}A"
    )

    # Format TrustedParts search URL with manufacturer and part number
    trustedparts_link = (
        f"{TRUSTEDPARTS_BASE_URL}{MANUFACTURER.replace(' ', '%20')}/"
        f"{mpn.replace('-', '%2D')}"
    )

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
        trustedparts_link=trustedparts_link  # Changed from octopart_link
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
        'TrustedParts Search'
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
                part_info.trustedparts_link
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
