"""
Library for managing Coilcraft coupled coupled inductor series specifications
and part info.

This module provides data structures and definitions for various Coilcraft
coupled coupled inductor series, including their specifications and individual
component information.
It is used to maintain a standardized database of coupled coupled inductor
specifications and generate consistent part information.
"""

from typing import List, NamedTuple, Dict, Optional


class PinConfig(NamedTuple):
    """Configuration specification for a single transformer pin.

    Attributes:
        number: Pin identifier/number as string (e.g., "1", "2")
        y_pos: Vertical position of the pin in millimeters relative to center
        pin_type: Pin type specification (e.g., "unspecified", "no_connect")
        hide: Boolean flag indicating if pin should be hidden in schematic
    """
    number: str
    y_pos: float
    pin_type: str
    lenght: float
    hide: bool = False


class SidePinConfig(NamedTuple):
    """Pin configuration specification for both sides of a transformer.

    Defines the complete pin layout for a transformer by specifying pins
    on both the left and right sides of the component.

    Attributes:
        left: List of PinConfig objects for the left side pins
        right: List of PinConfig objects for the right side pins
    """
    left: List[PinConfig]
    right: List[PinConfig]


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
    pin_config: Optional[SidePinConfig] = None


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
            4.430, 5.000, 6.800, 7.800
        ],
        value_suffix="ML",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("4", -5.08, "unspecified", 5.08)
            ],
            right=[
                PinConfig("3", 5.08, "unspecified", 5.08),
                PinConfig("2", -5.08, "unspecified", 5.08)
            ]
        )
    ),
    "MSD1048": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="MSD1048",
        footprint="coupled_inductor_footprints:MSD1048",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "2945f640-8140-48a6-993e-28832f57720a/msd1048.pdf",
        inductance_values=[10.0, 22.0, 47.0, 68.0, 100.0],
        max_dc_current=[2.1, 1.9, 1.6, 1.4, 1.2],
        max_dc_resistance=[0.053, 0.098, 0.208, 0.297, 0.387],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("4", -5.08, "unspecified", 5.08)
            ],
            right=[
                PinConfig("3", 5.08, "unspecified", 5.08),
                PinConfig("2", -5.08, "unspecified", 5.08)
            ]
        )
    ),
    "MSD1260": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="MSD1260",
        footprint="coupled_inductor_footprints:MSD1260",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "79bacbf1-ec2a-4e20-9b30-12448424231b/msd1260.pdf",
        inductance_values=[
            4.7, 5.6, 6.8, 8.2, 10.0, 12.0, 15.0, 18.0, 22.0,
            27.0, 33.0, 39.0, 47.0, 56.0, 68.0, 82.0, 100.0
        ],
        max_dc_current=[
            4.47, 4.24, 3.88, 3.72, 3.46, 3.12, 2.92, 2.73, 2.49,
            2.41, 2.32, 2.25, 2.03, 1.91, 1.83, 1.62, 1.50
        ],
        max_dc_resistance=[
            0.036, 0.040, 0.048, 0.052, 0.060, 0.074, 0.085, 0.097, 0.116,
            0.124, 0.134, 0.142, 0.174, 0.198, 0.216, 0.274, 0.322
        ],
        value_suffix="ML",
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified", 5.08),
                PinConfig("4", -5.08, "unspecified", 5.08)
            ],
            right=[
                PinConfig("3", 5.08, "unspecified", 5.08),
                PinConfig("2", -5.08, "unspecified", 5.08)
            ]
        )
    ),
}
