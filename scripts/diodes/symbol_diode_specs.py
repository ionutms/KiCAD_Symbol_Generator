"""Library for managing diode specifications.

This module provides data structures and definitions for various diode
series, including their specifications and individual component
information.
"""

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Diode series specifications.

    This class defines the complete specifications for a series of diodes,
    including physical, electrical, and documentation characteristics.
    """

    manufacturer: str
    base_series: str
    footprint: str
    datasheet: str
    voltage_rating: list[float]
    trustedparts_link: str
    current_rating: list[float]
    package: str
    diode_type: str
    part_number_suffix: str | None  # noqa: FA102


class PartInfo(NamedTuple):
    """Component part information structure for individual diodes."""

    symbol_name: str
    reference: str
    value: float
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    series: str
    trustedparts_link: str
    current_rating: float
    package: str
    diode_type: str


SERIES_SPECS: dict[str, SeriesSpec] = {
    "DFLS1200-7": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="DFLS1200-7",
        footprint="diode_footprints:PowerDI_123",
        datasheet="https://www.diodes.com/datasheet/download/DFLS1200.pdf",
        voltage_rating=[100.0],
        current_rating=[1.2],
        package="PowerDI_123",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix=None,
    ),
    "MMSZ52": SeriesSpec(
        manufacturer="Onsemi",
        base_series="MMSZ52",
        footprint="diode_footprints:PowerDI_123",
        datasheet=(
            "https://www.onsemi.com/download/data-sheet/"
            "pdf/mmsz5221bt1-d.pdf"),
        voltage_rating=[
            3.0, 3.3, 5.1, 10.0, 12.0, 15.0, 18.0, 22.0, 24.0, 27.0,
            30.0, 33.0, 36.0, 39.0, 43.0, 47.0, 51.0, 56.0, 62.0],
        current_rating=[0.5] * 19,
        package="PowerDI_123",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix="BT1G",
    ),
}
