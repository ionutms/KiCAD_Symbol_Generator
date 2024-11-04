"""TODO"""
import csv
from typing import List, Final, NamedTuple


def write_to_csv(
    parts_list: List[NamedTuple],
    output_file: str,
    header_mapping: List[str],
    encoding: str = 'utf-8'
) -> None:
    """
    Write specifications to CSV file using global header mapping.

    Args:
        parts_list: List of parts to write
        output_file: Output filename
        encoding: Character encoding
    """

    # Prepare all rows before opening file
    headers: Final[List[str]] = list(header_mapping.keys())
    rows = [headers]
    rows.extend([
        [header_mapping[header](part) for header in headers]
        for part in parts_list
    ])

    # Write all rows at once
    with open(f'data/{output_file}', 'w', newline='', encoding=encoding) as \
            csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
