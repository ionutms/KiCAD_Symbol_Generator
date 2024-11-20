"""
Library for managing Coilcraft coupled coupled inductor series specifications
and part info.

This module provides data structures and definitions for various Coilcraft
coupled coupled inductor series, including their specifications and individual
component information.
It is used to maintain a standardized database of coupled coupled inductor
specifications and generate consistent part information.
"""

from typing import List, NamedTuple, Dict


class SeriesSpec(NamedTuple):
    """coupled coupled inductor series specifications for Coilcraft components.

    This class defines the complete specifications for a series of inductors,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Name of the component manufacturer (e.g., "Coilcraft")
        base_series: Base model number for the series (e.g., "XAL1513")
        footprint: PCB footprint identifier used in schematic/layout tools
        tolerance: Component value tolerance (e.g., "±20%")
        datasheet: URL to the manufacturer's datasheet
        inductance_values: List of available inductance values in µH
        trustedparts_link: URL to the component listing on Trusted Parts
        value_suffix:
            Manufacturer's suffix for the component value (e.g., "ME")
        has_aec: Whether the series is AEC-Q200 qualified (defaults to True)
        max_dc_current: Maximum DC current rating in Amperes (A)
        max_dc_resistance: Maximum DC resistance in milliohms (mΩ)
    """
    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    inductance_values: List[float]
    trustedparts_link: str
    value_suffix: str
    has_aec: bool = True
    max_dc_current: List[float] = []
    max_dc_resistance: List[float] = []


class PartInfo(NamedTuple):
    """Component part information structure for individual inductors.

    This class contains all necessary information to fully specify a single
    coupled inductor component, including its specifications, documentation,
    and sourcing information.

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
        max_dc_current: Maximum DC current rating in Amperes (A)
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
    tolerance: str
    series: str
    trustedparts_link: str
    max_dc_current: float
    max_dc_resistance: float


SERIES_SPECS: Dict[str, SeriesSpec] = {
    "ZA9384": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="ZA9384",
        footprint="transformer_footprints:ZA9384",
        tolerance="±10%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "cc4df0c9-0883-48fa-b8fb-d5dedac2b455/za9384.pdf",
        inductance_values=[470.0],
        max_dc_current=[0.80],
        max_dc_resistance=[1.1],
        value_suffix="ALD",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "ZA9644": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="ZA9644",
        footprint="transformer_footprints:ZA9644",
        tolerance="±10%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "cc4df0c9-0883-48fa-b8fb-d5dedac2b455/za9384.pdf",
        inductance_values=[470.0],
        max_dc_current=[0.49],
        max_dc_resistance=[1.8],
        value_suffix="AED",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
}
