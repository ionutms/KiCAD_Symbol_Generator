"""
Coilcraft XFL3012 Series Part Number Generator

Generates part numbers and specifications for Coilcraft XFL3012 series
inductors.
Supports both standard and AEC-Q200 qualified parts with E6 series values.
"""

import csv
from typing import List, NamedTuple, Final
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
    tolerance: str
    series: str
    trustedparts_link: str


class SeriesSpec(NamedTuple):
    """Inductor series specifications."""
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str


# Constants
MANUFACTURER: Final[str] = "Coilcraft"
TRUSTEDPARTS_BASE_URL: Final[str] = "https://www.trustedparts.com/en/search/"

# E6 series values for inductors (µH)
E6_VALUES: Final[List[float]] = [
    0.47, 0.68, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8,
    10, 15, 22, 33, 47, 68, 100
]

# Series specifications
SERIES_SPECS: Final[SeriesSpec] = SeriesSpec(
    base_series="XFL3012",
    footprint="footprints:L_Coilcraft_XFL3012",
    tolerance="±20%",
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
        return f"{inductance*1000:.0f} nH"
    return f"{inductance:.1f} µH"


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
        Formatted value code string following Coilcraft standard:
        For values < 10µH:
        - R47 for 0.47µH
        - 1R0 for 1.0µH

        For values >= 10µH:
        - 100 for 10µH (10 × 10⁰)
        - 150 for 15µH
        - 220 for 22µH
        - 330 for 33µH
        - 470 for 47µH
        - 680 for 68µH
        - 104 for 100µH (10 × 10⁴)
    """
    if inductance < 10:
        # For values less than 10µH, use decimal point format
        value_codes = {
            0.47: "R47",
            0.68: "R68",
            1.0: "1R0",
            1.5: "1R5",
            2.2: "2R2",
            3.3: "3R3",
            4.7: "4R7",
            6.8: "6R8"
        }
        base_code = value_codes.get(inductance)
    else:
        # For values 10µH and above, use 3-digit format
        # where third digit is number of zeros
        value_codes = {
            10: "100",    # 10 × 10⁰
            15: "150",    # 15 × 10⁰
            22: "220",    # 22 × 10⁰
            33: "330",    # 33 × 10⁰
            47: "470",    # 47 × 10⁰
            68: "680",    # 68 × 10⁰
            100: "104"    # 10 × 10⁴
        }
        base_code = value_codes.get(inductance)

    if not base_code:
        raise ValueError(f"Invalid inductance value: {inductance}µH")

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
        specs.tolerance
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
    trustedparts_link = f"{TRUSTEDPARTS_BASE_URL}{mpn}"

    return PartInfo(
        symbol_name=f"L_{mpn}",
        reference="L",
        value=inductance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(inductance, specs, is_aec),
        manufacturer=MANUFACTURER,
        mpn=mpn,
        tolerance=specs.tolerance,
        series=specs.base_series,
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
        'Tolerance', 'Series', 'Trustedparts Search'
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
                part.tolerance,
                part.series,
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
