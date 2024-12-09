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
    reference: str = "D"


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


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
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
        footprint="diode_footprints:SOD_123",
        datasheet=(
            "https://www.onsemi.com/download/data-sheet/"
            "pdf/mmsz5221bt1-d.pdf"),
        voltage_rating=[
            2.4, 2.5, 2.7, 2.8, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7,
            5.1, 5.6, 6.0, 6.2, 6.8, 7.5, 8.2, 8.7, 9.1, 10.0,
            11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0,
            22.0, 24.0, 25.0, 27.0, 28.0, 30.0, 33.0, 36.0, 39.0, 43.0,
            47.0, 51.0, 56.0, 60.0, 62.0, 68.0, 75.0, 82.0, 87.0, 91.0],
        current_rating=[0.5] * 51,
        package="SOD_123",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix="BT1G",
    ),
    "US1DWF": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="US1DWF",
        footprint="diode_footprints:SOD_123F",
        datasheet="https://www.diodes.com/assets/Datasheets/US1DWF.pdf",
        voltage_rating=[200.0],
        current_rating=[1.0],
        package="SOD_123F",
        diode_type="Rectifier",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix=None,
    ),
}
