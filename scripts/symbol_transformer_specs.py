"""Module for defining and managing transformer component specifications.

This module provides data structures and configurations
for managing transformer and coupled inductor specifications,
particularly for Coilcraftcomponents.
It includes definitions for pin layouts, series specifications,
and individual component details used in electronic design.

The module supports:
- Pin configuration management for transformer components
- Series specifications for different transformer families
- Detailed part information tracking for individual components
- Standard configurations for common transformer layouts
"""

from typing import List, NamedTuple, Dict, Optional


class PinConfig(NamedTuple):
    """Configuration specification for a single transformer pin.

    Attributes:
        number: Pin identifier/number as string (e.g., "1", "2")
        y_pos: Vertical position of the pin in millimeters relative to center
        type: Pin type specification (e.g., "unspecified", "no_connect")
        hide: Boolean flag indicating if pin should be hidden in schematic
    """
    number: str
    y_pos: float
    type: str
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
    """Specifications for a series of coupled inductors.

    Comprehensive specification for a transformer series, including electrical
    characteristics, documentation references, and mechanical specifications.

    Attributes:
        manufacturer: Name of the component manufacturer
        base_series: Base series identifier for the component family
        footprint: PCB footprint identifier for the component series
        tolerance: Component value tolerance specification
        datasheet: URL to the manufacturer's datasheet
        inductance_values: List of available inductance values in µH
        trustedparts_link: URL to component listing on Trusted Parts
        value_suffix: Suffix used in part numbering for the series
        has_aec: Boolean indicating AEC-Q200 qualification status
        max_dc_current: List of maximum DC current ratings in Amperes (A)
        max_dc_resistance:
            List of maximum DC resistance values in milliohms (mΩ)
        pin_config: Optional pin configuration specification
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
    """Detailed specification for an individual transformer component.

    Provides a complete description of a single transformer or coupled inductor
    component, including electrical specifications, documentation references,
    and sourcing information.

    Attributes:
        symbol_name: Schematic symbol identifier for the component
        reference: Component reference designator used in schematics
        value: Inductance value in microhenries (µH)
        footprint: PCB footprint identifier
        datasheet: URL to component datasheet
        description: Human-readable component description
        manufacturer: Name of component manufacturer
        mpn: Manufacturer part number
        tolerance: Component value tolerance specification
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


# Series specifications for supported transformer families
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
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "no_connect", True),
                PinConfig("2", 2.54, "unspecified"),
                PinConfig("3", -2.54, "no_connect", True),
                PinConfig("4", -5.08, "unspecified")
            ],
            right=[
                PinConfig("5", 5.08, "unspecified"),
                PinConfig("6", 2.54, "no_connect", True),
                PinConfig("7", -2.54, "no_connect", True),
                PinConfig("8", -5.08, "unspecified")
            ]
        )
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
        trustedparts_link="https://www.trustedparts.com/en/search",
        pin_config=SidePinConfig(
            left=[
                PinConfig("1", 5.08, "unspecified"),
                PinConfig("2", 2.54, "no_connect", True),
                PinConfig("3", -2.54, "no_connect", True),
                PinConfig("4", -5.08, "unspecified")
            ],
            right=[
                PinConfig("5", 5.08, "unspecified"),
                PinConfig("6", 2.54, "no_connect", True),
                PinConfig("7", -2.54, "no_connect", True),
                PinConfig("8", -5.08, "unspecified")
            ]
        )
    ),
}
