"""
Coilcraft Inductor Series Part Number Generator

Generates part numbers and specifications for Coilcraft inductor series
with custom inductance values.
Supports both standard and AEC-Q200 qualified parts.
Generates both individual series files and unified component database.
"""

import csv
from typing import List
import kicad_inductor_symbol_generator as ki_isg
import series_specs_inductors as ssi


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
        return f"{int(inductance*1000)} nH"
    if inductance.is_integer():
        return f"{int(inductance)} µH"
    return f"{inductance:.1f} µH"


def generate_value_code(
    inductance: float,
    is_aec: bool = True,
    value_suffix: str = "ME"
) -> str:
    """
    Generate Coilcraft value code according to datasheet format.

    Args:
        inductance: Value in µH
        is_aec: If True, add AEC suffix
        value_suffix: Suffix to use for AEC qualified parts

    Returns:
        Formatted value code string
    """
    if inductance < 1:
        nh_value = inductance * 1000
        value_codes = {
            40: "400",
            120: "121",
            180: "181",
            220: "221",
            240: "241",
            250: "251",
            270: "271",
            330: "331",
            380: "381",
            390: "391",
            420: "421",
            470: "471",
            560: "561",
            600: "601",
            680: "681",
            700: "701",
            800: "801",
            820: "821"
        }
        base_code = value_codes.get(int(nh_value))
        if base_code is None:
            raise ValueError(f"Invalid inductance value: {inductance}µH")
    elif inductance < 10:
        value_codes = {
            1.0: "102",
            1.2: "122",
            1.5: "152",
            2.0: "202",
            2.2: "222",
            3.0: "302",
            3.3: "332",
            4.7: "472",
            6.8: "682",
            8.2: "822",
        }
        base_code = value_codes.get(inductance)
        if base_code is None:
            raise ValueError(f"Invalid inductance value: {inductance}µH")
    else:
        value_codes = {
            10.0: "103",
            15.0: "153",
            18.0: "183",
            22.0: "223",
            33.0: "333",
            39.0: "393",
            47.0: "473",
            56.0: "563",
            68.0: "683",
            82.0: "823",
            100.0: "104",
            220.0: "224",
        }
        base_code = value_codes.get(inductance)
        if base_code is None:
            raise ValueError(f"Invalid inductance value: {inductance}µH")

    return f"{base_code}{value_suffix}" if is_aec else base_code


def create_description(
    inductance: float,
    specs: ssi.SeriesSpec,
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

    if is_aec and specs.has_aec:
        parts.append("AEC-Q200")

    return " ".join(parts)


def create_part_info(
    inductance: float,
    specs: ssi.SeriesSpec,
    is_aec: bool = True
) -> ssi.PartInfo:
    """
    Create complete part information.

    Args:
        inductance: Value in µH
        specs: Series specifications
        is_aec: If True, create AEC-Q200 qualified part

    Returns:
        PartInfo instance with all specifications
    """
    value_code = generate_value_code(
        inductance,
        is_aec and specs.has_aec,
        specs.value_suffix
    )
    mpn = f"{specs.base_series}-{value_code}"
    trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

    return ssi.PartInfo(
        symbol_name=f"L_{mpn}",
        reference="L",
        value=inductance,
        footprint=specs.footprint,
        datasheet=specs.datasheet,
        description=create_description(inductance, specs, is_aec),
        manufacturer=specs.manufacturer,
        mpn=mpn,
        tolerance=specs.tolerance,
        series=specs.base_series,
        trustedparts_link=trustedparts_link
    )


def generate_part_numbers(
    specs: ssi.SeriesSpec,
    is_aec: bool = True
) -> List[ssi.PartInfo]:
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
        for value in specs.inductance_values
    ]


def write_to_csv(
    parts_list: List[ssi.PartInfo],
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


def generate_files_for_series(
    series_name: str,
    is_aec: bool,
    unified_parts_list: List[ssi.PartInfo]
) -> None:
    """
    Generate CSV and KiCad symbol files for specified series.

    Args:
        series_name: Name of the series to generate files for
        is_aec: If True, generate AEC-Q200 qualified parts
        unified_parts_list: List to store generated parts for unified database
    """
    if series_name not in ssi.SERIES_SPECS:
        raise ValueError(f"Unknown series: {series_name}")

    specs = ssi.SERIES_SPECS[series_name]
    csv_filename = f"{specs.base_series}_part_numbers.csv"
    symbol_filename = f"INDUCTORS_{specs.base_series}_DATA_BASE.kicad_sym"

    try:
        parts_list = generate_part_numbers(specs, is_aec)
        write_to_csv(parts_list, csv_filename)
        print(
            f"Generated {len(parts_list)} part numbers "
            f"in '{csv_filename}'"
        )

        ki_isg.generate_kicad_symbol(
            f'data/{csv_filename}',
            f'series_kicad_sym/{symbol_filename}'
        )
        print(
            f"KiCad symbol file '{symbol_filename}' "
            "generated successfully."
        )

        # Add parts to unified list
        unified_parts_list.extend(parts_list)

    except FileNotFoundError as e:
        print(f"CSV file not found: {e}")
    except csv.Error as e:
        print(f"CSV processing error: {e}")
    except IOError as e:
        print(f"I/O error when generating files: {e}")


def generate_unified_files(all_parts: List[ssi.PartInfo]) -> None:
    """
    Generate unified component database files containing all series.

    Creates:
    1. A unified CSV file containing all component specifications
    2. A unified KiCad symbol file containing all components

    Args:
        all_parts: List of all PartInfo instances across all series
    """
    unified_csv = "UNITED_INDUCTORS_DATA_BASE.csv"
    unified_symbol = "UNITED_INDUCTORS_DATA_BASE.kicad_sym"

    # Write unified CSV file
    write_to_csv(all_parts, unified_csv)
    print(f"Generated unified CSV file with {len(all_parts)} part numbers")

    # Generate unified KiCad symbol file
    try:
        ki_isg.generate_kicad_symbol(f'data/{unified_csv}', unified_symbol)
        print("Unified KiCad symbol file generated successfully.")
    except FileNotFoundError as e:
        print(f"Unified CSV file not found: {e}")
    except csv.Error as e:
        print(f"CSV processing error for unified file: {e}")
    except IOError as e:
        print(f"I/O error when generating unified KiCad symbol file: {e}")


if __name__ == "__main__":
    try:
        unified_parts: List[ssi.PartInfo] = []

        # Generate files for both series
        for series in ssi.SERIES_SPECS:
            print(f"\nGenerating files for {series} series:")
            generate_files_for_series(series, True, unified_parts)

        # Generate unified files after all series are processed
        print("\nGenerating unified files:")
        generate_unified_files(unified_parts)

    except (ValueError, csv.Error, IOError) as error:
        print(f"Error generating files: {error}")
