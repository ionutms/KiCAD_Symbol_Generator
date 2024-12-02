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


SERIES_SPECS: dict[str, SeriesSpec] = {
    "SI7309DN-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors",
        base_series="SI7309DN-T1-GE3",
        footprint="transistor_footprints:PowerPAK 1212-8",
        datasheet="https://www.vishay.com/docs/73434/si7309dn.pdf",
        voltage_rating=[100.0],
        current_rating=[1.2],
        package="PowerPAK 1212-8",
        diode_type="P-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix=None,
    ),
}
