"""TODO"""

from typing import TextIO


def write_symbol_header(
        symbol_file: TextIO,
        symbol_name: str
) -> None:
    """
    Write the header for a single symbol.

    Args:
        symbol_file (TextIO): File object for writing the symbol file.
        symbol_name (str): Name of the symbol.
    """
    symbol_file.write(f"""
        (symbol "{symbol_name}"
            (pin_names(offset 0.254))
            (exclude_from_sim no)
            (in_bom yes)
            (on_board yes)
        """)
