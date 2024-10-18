#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Panasonic ERJ-2RK Part Number Generator

This script generates all possible part numbers for the Panasonic ERJ-2RK
resistor series based on the E96 standard resistance values, tolerance
options, and packaging options. The results are saved to a CSV file.

The script generates part numbers for resistors with:
- Values following E96 standard (10Ω to 1MΩ)
- Tolerances: 1% (F) and 0.5% (D)
- Packaging: tape (T) and bulk (P)
"""

from __future__ import annotations
import csv
from typing import List, NamedTuple, Final


class PartInfo(NamedTuple):
    """
    Structure to hold component part information.

    Attributes:
        symbol_name: Unique identifier for the component
        reference: Component reference designator
        value: Resistance value in ohms
        footprint: PCB footprint specification
        datasheet: URL to component datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer Part Number
        tolerance: Resistance tolerance specification
        voltage_rating: Maximum voltage rating
    """
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


# Constants for the ERJ-2RK series
BASE_SERIES: Final[str] = "ERJ-2RK"
FOOTPRINT: Final[str] = "R_0402_1005Metric"
MANUFACTURER: Final[str] = "Panasonic"
DATASHEET: Final[str] = (
    "https://industrial.panasonic.com/cdbs/www-data/pdf/"
    "RDA0000/AOA0000C304.pdf"
)
VOLTAGE_RATING: Final[str] = "50V"

# E96 series base resistance values (1Ω to 10Ω range)
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

# Multipliers to scale base values (1, 10, 100, ..., 1MΩ)
MULTIPLIERS: Final[List[float]] = [1, 10, 100, 1000, 10000, 100000]

# Tolerance options with their full values
TOLERANCE_MAP: Final[dict[str, str]] = {
    'F': '1%',
    'D': '0.5%'
}

# Packaging options
PACKAGING_OPTIONS: Final[List[str]] = ['T', 'P']  # T = Tape, P = Bulk


def format_resistance_value(value: float) -> str:
    """
    Convert resistance value to a human-readable format with appropriate units.

    Args:
        value: The resistance value in ohms

    Returns:
        A formatted string with resistance value and units (Ω, kΩ, or MΩ)
    """
    def clean_number(num: float) -> str:
        """Remove trailing zeros from floating point number."""
        return f"{num:g}"

    if value >= 1_000_000:
        return f"{clean_number(value / 1_000_000)} MΩ"
    if value >= 1_000:
        return f"{clean_number(value / 1_000)} kΩ"
    return f"{clean_number(value)} Ω"


def generate_part_numbers() -> List[PartInfo]:
    """
    Generate all possible part numbers for the ERJ-2RK series.

    This function creates combinations of:
    - E96 standard resistance values
    - Available tolerances
    - Packaging options

    Returns:
        A list of PartInfo objects containing all component specifications
    """
    part_numbers: List[PartInfo] = []
    symbol_counter = 1

    for base_value in E96_BASE_VALUES:
        for multiplier in MULTIPLIERS:
            scaled_resistance: float = base_value * multiplier
            if 10 <= scaled_resistance <= 1_000_000:
                # Generate resistance code for part number
                if scaled_resistance >= 1_000_000:
                    resistance_code = f"{int(base_value)}M"
                elif scaled_resistance >= 1_000:
                    resistance_code = f"{int(base_value)}K"
                else:
                    resistance_code = f"{int(base_value)}"

                for tolerance_code, tolerance_value in TOLERANCE_MAP.items():
                    for packaging in PACKAGING_OPTIONS:
                        mpn = \
                            f"{BASE_SERIES}{resistance_code}" + \
                            f"{tolerance_code}{packaging}"
                        symbol_name = f"R_{symbol_counter:06d}"

                        description = (
                            "RES SMD "
                            f"{format_resistance_value(scaled_resistance)} "
                            f"{tolerance_value} 0402 {VOLTAGE_RATING}"
                        )

                        part_numbers.append(PartInfo(
                            symbol_name=symbol_name,
                            reference="R",
                            value=scaled_resistance,
                            footprint=FOOTPRINT,
                            datasheet=DATASHEET,
                            description=description,
                            manufacturer=MANUFACTURER,
                            mpn=mpn,
                            tolerance=tolerance_value,
                            voltage_rating=VOLTAGE_RATING
                        ))
                        symbol_counter += 1

    return part_numbers


def write_to_csv(
    part_numbers: List[PartInfo],
    filename: str = 'ERJ2RK_part_numbers.csv',
    encoding: str = 'utf-8'
) -> None:
    """
    Write the generated part numbers and their information to a CSV file.

    Args:
        part_numbers: List of PartInfo objects to write to the file
        filename: Name of the output CSV file
        encoding: Character encoding for the CSV file
    """
    headers: Final[List[str]] = [
        'Symbol Name', 'Reference', 'Value', 'Footprint', 'Datasheet',
        'Description', 'Manufacturer', 'MPN', 'Tolerance', 'Voltage Rating'
    ]

    with open(filename, 'w', newline='', encoding=encoding) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for part_info in part_numbers:
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
                part_info.voltage_rating
            ])


def main() -> None:
    """Generate part numbers and write them to a CSV file."""
    generated_part_numbers: List[PartInfo] = generate_part_numbers()
    write_to_csv(generated_part_numbers)
    print("Part numbers have been written to 'ERJ2RK_part_numbers.csv'")


if __name__ == "__main__":
    main()
