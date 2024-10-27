"""
Coilcraft XFL3012 Series Part Number Generator

Generates part numbers and specifications for Coilcraft XFL3012 series
inductors with custom inductance values.
Supports both standard and AEC-Q200 qualified parts.
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

# Custom inductance values (in µH)
INDUCTANCE_VALUES: Final[List[float]] = [
    0.22,  # 220 nH
    0.36,  # 360 nH
    0.60,  # 600 nH
    0.68,  # 680 nH
    33.0,  # 33 µH
    39.0,  # 39 µH
    56.0,  # 56 µH
    82.0,  # 82 µH
    100.0  # 100 µH
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
    Shows integer values where possible (no decimal places needed).

    Args:
        inductance: Value in µH

    Returns:
        Formatted string with unit
    """
    if inductance < 1:
        # Convert to nH and always show as integer
        return f"{int(inductance*1000)} nH"
    elif inductance.is_integer():
        # For whole µH values, show as integer
        return f"{int(inductance)} µH"
    else:
        # For fractional µH values, show one decimal place
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
        Formatted value code string following Coilcraft standard
    """
    if inductance < 1:
        # Convert to nH for sub-1µH values
        nh_value = inductance * 1000
        if nh_value == 220:
            base_code = "R22"
        elif nh_value == 360:
            base_code = "R36"
        elif nh_value == 600:
            base_code = "R60"
        elif nh_value == 680:
            base_code = "R68"
        else:
            raise ValueError(f"Invalid inductance value: {inductance}µH")
    else:
        # Handle values >= 1µH
        value_codes = {
            33.0: "330",    # 33 × 10⁰
            39.0: "390",    # 39 × 10⁰
            56.0: "560",    # 56 × 10⁰
            82.0: "820",    # 82 × 10⁰
            100.0: "104"    # 10 × 10⁴
        }
        base_code = value_codes.get(inductance)
        if base_code is None:
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
        for value in INDUCTANCE_VALUES
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
