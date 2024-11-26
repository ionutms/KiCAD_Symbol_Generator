"""Library for managing diode specifications and part info.

This module provides data structures and definitions for various diode series,
including their specifications and individual component information.
"""

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Specification for a diode series.

    Attributes:
        manufacturer: Name of the component manufacturer.
        base_series: Complete part number for the series.
        footprint: PCB footprint identifier for schematic/layout tools.
        voltage_rating: Maximum reverse voltage rating (e.g., "100V").
        current_rating: Maximum forward current rating (e.g., "1.2A").
        datasheet: URL to the manufacturer's datasheet.
        description: General description of the diode type.
        package: Package type (e.g., "PowerDI-123").
        trustedparts_link: URL to the component listing on Trusted Parts.

    """

    manufacturer: str
    base_series: str
    footprint: str
    voltage_rating: str
    current_rating: str
    datasheet: str
    description: str
    package: str
    trustedparts_link: str


class PartInfo(NamedTuple):
    """Information structure for individual diodes.

    Attributes:
        symbol_name: Schematic symbol identifier.
        reference: Component reference designator (e.g., "D").
        value: Component value/part number.
        footprint: PCB footprint identifier.
        datasheet: URL to the manufacturer's datasheet.
        description: Human-readable component description.
        manufacturer: Component manufacturer name.
        mpn: Manufacturer part number.
        voltage_rating: Maximum reverse voltage rating.
        current_rating: Maximum forward current rating.
        package: Package type.
        trustedparts_link: URL to component listing on Trusted Parts.

    """

    symbol_name: str
    reference: str
    value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    voltage_rating: str
    current_rating: str
    package: str
    trustedparts_link: str


SERIES_SPECS: dict[str, SeriesSpec] = {
    "DFLS1200-7": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="DFLS1200-7",
        footprint="diode_footprints:D_PowerDI-123",
        voltage_rating="100V",
        current_rating="1.2A",
        datasheet="https://www.diodes.com/datasheet/download/DFLS1200.pdf",
        description="Power Schottky Rectifier",
        package="PowerDI-123",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}
