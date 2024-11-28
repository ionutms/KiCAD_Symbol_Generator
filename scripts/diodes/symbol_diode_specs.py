"""Library for managing inductor specifications.

This module provides data structures and definitions for various Coilcraft
inductor series, including their specifications and individual component
information. It is used to maintain a standardized database of inductor
specifications and generate consistent part information.
"""

from typing import NamedTuple


class SeriesSpec(NamedTuple):
    """Inductor series specifications for Coilcraft components.

    This class defines the complete specifications for a series of inductors,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Name of the component manufacturer (e.g., "Coilcraft")
        base_series: Base model number for the series (e.g., "XAL1513")
        footprint: PCB footprint identifier used in schematic/layout tools
        tolerance: Component value tolerance (e.g., "±20%")
        datasheet: URL to the manufacturer's datasheet
        voltage_rating: List of available inductance values in µH
        trustedparts_link: URL to the component listing on Trusted Parts
        value_suffix:
            Manufacturer's suffix for the component value (e.g., "ME")
        has_aec: Whether the series is AEC-Q200 qualified (defaults to True)
        current_rating: Maximum DC current rating in Amperes (A)
        max_dc_resistance: Maximum DC resistance in milliohms (mΩ)

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


class PartInfo(NamedTuple):
    """Component part information structure for individual inductors.

    This class contains all necessary information to fully specify a single
    inductor component, including its specifications, documentation, and
    sourcing information.

    Attributes:
        symbol_name: Schematic symbol identifier
        reference: Component reference designator
        value: Inductance value in µH
        footprint: PCB footprint identifier
        datasheet: URL to the manufacturer's datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        tolerance: Component value tolerance
        series: Product series identifier
        trustedparts_link: URL to component listing on Trusted Parts
        current_rating: Maximum DC current rating in Amperes (A)
        max_dc_resistance: Maximum DC resistance in milliohms (mΩ)

    """

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
        trustedparts_link="https://www.trustedparts.com/en/search"),
    "MMSZ52": SeriesSpec(
        manufacturer="Onsemi",
        base_series="MMSZ5265BT1G",
        footprint="diode_footprints:PowerDI_123", # change footprint
        datasheet=(
            "https://ro.mouser.com/datasheet/2/308/1/"
            "MMSZ5221BT1_D-2316205.pdf"),
        voltage_rating=[62.0],
        current_rating=[1.2],
        package="PowerDI_123", # change package
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search"),
}
