"""
Coilcraft XFL3012 Series Part Number Generator

Generates part numbers and specifications for Coilcraft XFL3012 series
inductors.
Supports both standard and AEC-Q200 qualified parts with E6 series values.
"""

import csv
from typing import List, NamedTuple, Final, Dict
import kicad_inductor_symbol_generator as ki_isg


class PartInfo(NamedTuple):
    """Component part information structure."""
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
    """Inductor series specifications."""
    base_series: str
    footprint: str
    height: str
    tolerance: str
    dcr_map: Dict[float, str]
    current_ratings: Dict[float, Dict[str, str]]
    datasheet: str


# Constants
MANUFACTURER: Final[str] = "Coilcraft"
TRUSTEDPARTS_BASE_URL: Final[str] = (
    "https://www.trustedparts.com/en/search/"
)

# E6 series values for inductors (µH)
E6_VALUES: Final[List[float]] = [
    0.47, 0.68, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8,
    10, 15, 22, 33, 47, 68, 100
]

# DCR values in mΩ for each inductance value
DCR_MAP: Final[Dict[float, str]] = {
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
    100: "3000"  # 3Ω for 100µH
}

# Current ratings for each inductance value
CURRENT_RATINGS: Final[Dict[float, Dict[str, str]]] = {
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
    100: {"rated": "0.39", "saturated": "0.54"}  # 390mA rated
}

# Series specifications
SERIES_SPECS: Final[SeriesSpec] = SeriesSpec(
    base_series="XFL3012",
    footprint="footprints:L_Coilcraft_XFL3012",
    height="1.2mm",
    tolerance="±20%",
    dcr_map=DCR_MAP,
    current_ratings=CURRENT_RATINGS,
    datasheet="https://www.coilcraft.com/en-us/products/xfl3012/"
)


def format_inductance_value(inductance: float) -> str:
    """
    Format inductance value with appropriate unit.

    Args:
        inductance: Value in µH

    Returns:
        Formatted string with unit
    """
    if inductance < 1:
        return f"{inductance*1000:.0f}nH"
    return f"{inductance:.1f}µH"


def generate_value_code(
    inductance: float,
    is_aec: bool = True
) -> str:
    """
    Generate Coilcraft value code.

    Args:
        inductance: Value in µH
        is_aec: If True, add AEC-Q200 suffix

    Returns:
        Formatted value code string following standard inductor codes:
        - R47 for 0.47µH
        - 1R0 for 1.0µH
        - 102 for 1000nH
        - 104 for 100µH
    """
    # Standard inductor codes mapping
    value_codes = {
        0.47: "R47",
        0.68: "R68",
        1.0: "1R0",
        1.5: "1R5",
        2.2: "2R2",
        3.3: "3R3",
        4.7: "4R7",
        6.8: "6R8",
        10: "100",
        15: "150",
        22: "220",
        33: "330",
        47: "470",
        68: "680",
        100: "104"  # Fixed value code for 100µH
    }

    if inductance not in value_codes:
        raise ValueError(f"Invalid inductance value: {inductance}µH")

    base_code = value_codes[inductance]
    return f"{base_code}MEC" if is_aec else base_code


def create_description(
    inductance: float,
    specs: SeriesSpec,
    is_aec: bool
) -> str:
    """
    Create component description.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, add AEC-Q200 qualification

    Returns:
        Formatted description string
    """
    parts = [
        "INDUCTOR SMD",
        format_inductance_value(inductance),
        specs.tolerance,
        specs.height,
        f"RATED {specs.current_ratings[inductance]['rated']}A"
    ]

    if is_aec:
        parts.append("AEC-Q200")

    return " ".join(parts)


def create_part_info(
    inductance: float,
    specs: SeriesSpec,
    is_aec: bool = True
) -> PartInfo:
    """
    Create complete part information.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, create AEC-Q200 qualified part

    Returns:
        PartInfo instance with all specifications
    """
    value_code = generate_value_code(inductance, is_aec)
    mpn = f"{specs.base_series}-{value_code}"

    trustedparts_link = (
        f"{TRUSTEDPARTS_BASE_URL}"
        f"{MANUFACTURER.replace(' ', '%20')}/"
        f"{mpn.replace('-', '%2D')}"
    )

    return PartInfo(
        symbol_name=f"L_{mpn}",
        reference="L",
        value=inductance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(inductance, specs, is_aec),
        manufacturer=MANUFACTURER,
        mpn=mpn,
        inductance=format_inductance_value(inductance),
        tolerance=specs.tolerance,
        dcr_max=f"{specs.dcr_map[inductance]}mΩ",
        idc_rated=f"{specs.current_ratings[inductance]['rated']}A",
        idc_saturated=(
            f"{specs.current_ratings[inductance]['saturated']}A"
        ),
        series=specs.base_series,
        height=specs.height,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(
    specs: SeriesSpec,
    is_aec: bool = True
) -> List[PartInfo]:
    """
    Generate all part numbers for the series.

    Args:
        specs: Series specifications
        is_aec: If True, generate AEC-Q200 qualified parts

    Returns:
        List of PartInfo instances
    """
    return [
        create_part_info(value, specs, is_aec)
        for value in E6_VALUES
    ]


def write_to_csv(
    parts_list: List[PartInfo],
    output_file: str,
    encoding: str = 'utf-8'
) -> None:
    """
    Write specifications to CSV file.

    Args:
        parts_list: List of parts to write
        output_file: Output filename
        encoding: Character encoding
    """
    headers = [
        'Symbol Name', 'Reference', 'Value', 'Footprint',
        'Datasheet', 'Description', 'Manufacturer', 'MPN',
        'Inductance', 'Tolerance', 'DCR Max', 'Idc Rated',
        'Idc Saturated', 'Series', 'Height', 'TrustedParts Search'
    ]

    with open(
        f'data/{output_file}',
        'w',
        newline='',
        encoding=encoding
    ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for part in parts_list:
            writer.writerow([
                part.symbol_name,
                part.reference,
                format_inductance_value(part.value),
                part.footprint,
                part.datasheet,
                part.description,
                part.manufacturer,
                part.mpn,
                part.inductance,
                part.tolerance,
                part.dcr_max,
                part.idc_rated,
                part.idc_saturated,
                part.series,
                part.height,
                part.trustedparts_link
            ])


def generate_files() -> None:
    """Generate CSV and KiCad symbol files."""
    series_code = SERIES_SPECS.base_series
    csv_filename = f"{series_code}_part_numbers.csv"
    symbol_filename = f"INDUCTORS_{series_code}_DATA_BASE.kicad_sym"

    try:
        # Generate part numbers and write to CSV
        parts_list = generate_part_numbers(SERIES_SPECS)
        write_to_csv(parts_list, csv_filename)
        print(
            f"Generated {len(parts_list)} part numbers "
            f"in '{csv_filename}'"
        )

        # Generate KiCad symbol file
        ki_isg.generate_kicad_symbol(
            f'data/{csv_filename}',
            symbol_filename
        )
        print(
            f"KiCad symbol file '{symbol_filename}' "
            "generated successfully."
        )

    except FileNotFoundError as e:
        print(f"CSV file not found: {e}")
    except csv.Error as e:
        print(f"CSV processing error: {e}")
    except IOError as e:
        print(f"I/O error when generating files: {e}")


if __name__ == "__main__":
    try:
        generate_files()
    except (csv.Error, IOError) as file_error:
        print(f"Error generating files: {file_error}")
