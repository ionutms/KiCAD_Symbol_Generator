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
    "MSD7342": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="MSD7342",
        footprint="coupled_inductor_footprints:MSD7342",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "bd00e7ca-3707-4fbb-84fc-c9b381ce0e78/msd7342.pdf",
        inductance_values=[
            2.5, 3.3, 4.7, 5.6, 6.8, 8.2, 10.0, 12.0, 15.0,
            18.0, 22.0, 27.0, 33.0, 39.0, 47.0, 56.0, 68.0, 82.0,
            100.0, 120.0, 150.0, 180.0, 220.0, 270.0, 330.0, 390.0, 470.0,
            560.0, 680.0, 820.0, 1000.0
            ],
        max_dc_current=[
            3.06, 2.89, 2.46, 2.22, 2.10, 2.03, 1.76, 1.61, 1.54,
            1.35, 1.19, 1.11, 1.07, 0.90, 0.86, 0.82, 0.72, 0.67,
            0.63, 0.55, 0.48, 0.45, 0.42, 0.36, 0.34, 0.32, 0.28,
            0.26, 0.25, 0.21, 0.20
            ],
        max_dc_resistance=[
            0.033, 0.037, 0.051, 0.063, 0.070, 0.075, 0.100, 0.120, 0.130,
            0.170, 0.220, 0.250, 0.270, 0.380, 0.420, 0.460, 0.600, 0.680,
            0.770, 1.030, 1.350, 1.520, 1.720, 2.410, 2.700, 3.050, 4.000,
            4.430, 5.000, 6.800, 7.800],
        value_suffix="ML",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
}
