"""TODO"""

import os
import csv
from typing import Dict, List, Final, NamedTuple

from print_message_utilities import print_info


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


def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print_info(f"Created directory: {directory}")


def read_csv_data(
        input_csv_file: str,
        encoding: str
) -> List[Dict[str, str]]:
    """
    Read component data from a CSV file.

    Args:
        input_csv_file (str): Path to the input CSV file.
        encoding (str): Character encoding of the CSV file.

    Returns:
        List[Dict[str, str]]: List of dictionaries containing component data.
    """
    with open(input_csv_file, 'r', encoding=encoding) as csv_file:
        return list(csv.DictReader(csv_file))
