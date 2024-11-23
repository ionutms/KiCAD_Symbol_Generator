"""
Library for managing diode specifications and part info.

This module provides data structures and definitions for various diode series,
including their specifications and individual component information.
"""

from typing import NamedTuple, Dict


class SeriesSpec(NamedTuple):
    """Diode series specifications.

    This class defines the complete specifications for diodes,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Name of the component manufacturer
        base_series: Base model number for the series
        footprint: PCB footprint identifier used in schematic/layout tools
        voltage_rating: Maximum reverse voltage rating (e.g., "100V")
        current_rating: Maximum forward current rating (e.g., "1.2A")
        datasheet: URL to the manufacturer's datasheet
        description: General description of the diode type
        package: Package type (e.g., "PowerDI-123")
        trustedparts_link: URL to the component listing on Trusted Parts
        has_thermal_pad: Whether the package includes a thermal pad
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
    has_thermal_pad: bool = False


class PartInfo(NamedTuple):
    """Component part information structure for individual diodes.

    This class contains all necessary information to fully specify a single
    diode component, including its specifications and documentation.

    Attributes:
        symbol_name: Schematic symbol identifier
        reference: Component reference designator (e.g., "D")
        value: Diode part number
        footprint: PCB footprint identifier
        datasheet: URL to the manufacturer's datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        voltage_rating: Maximum reverse voltage rating
        current_rating: Maximum forward current rating
        package: Package type
        trustedparts_link: URL to component listing on Trusted Parts
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


# Example diode series specifications
SERIES_SPECS: Dict[str, SeriesSpec] = {
    "DFLS1200": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="DFLS1200",
        footprint="diode_footprints:D_PowerDI-123",
        voltage_rating="100V",
        current_rating="1.2A",
        datasheet="https://www.diodes.com/assets/Datasheets/DFLS1200.pdf",
        description="Power Schottky Rectifier",
        package="PowerDI-123",
        trustedparts_link="https://www.trustedparts.com/en/search/DFLS1200",
        has_thermal_pad=False
    ),
}
