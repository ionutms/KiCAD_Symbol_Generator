"""
Connector Series Specifications Module

This module defines data structures and specifications for connector series,
providing a framework for managing connector component information.
"""

from typing import List, NamedTuple, Dict


class SeriesSpec(NamedTuple):
    """Connector series specifications.

    This class defines the complete specifications for a series of connectors,
    including physical characteristics and documentation.

    Attributes:
        manufacturer: Name of the component manufacturer
        base_series: Base model number for the series
        footprint_pattern: Pattern string for generating footprint names
        datasheet: URL to the manufacturer's datasheet
        pin_counts: List of available pin configurations
        trustedparts_link: URL to the component listing on Trusted Parts
        color: Color of the connector housing
        pitch: Pin-to-pin spacing in millimeters
    """
    manufacturer: str
    base_series: str
    footprint_pattern: str
    datasheet: str
    pin_counts: List[int]
    trustedparts_link: str
    color: str
    pitch: float


class PartInfo(NamedTuple):
    """Component part information structure for individual connectors.

    Attributes:
        symbol_name: Schematic symbol identifier
        reference: Component reference designator (typically "J")
        value: Component value field in schematic
        footprint: PCB footprint identifier
        datasheet: URL to the manufacturer's datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        series: Product series identifier
        trustedparts_link: URL to component listing on Trusted Parts
        color: Color of the connector housing
        pitch: Pin-to-pin spacing in millimeters
        pin_count: Number of pins in the connector
    """
    symbol_name: str
    reference: str
    value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    series: str
    trustedparts_link: str
    color: str
    pitch: float
    pin_count: int


SERIES_SPECS: Dict[str, SeriesSpec] = {
    "TBP02R2-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02R2-381",
        footprint_pattern="footprints:TBP02R2-381-{:02d}BE",
        datasheet="https://www.sameskydevices.com/" +
        "product/resource/tbp02r2-381.pdf",
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16],
        trustedparts_link="https://www.trustedparts.com/en/search",
        color="Blue",
        pitch=3.81
    ),
}


def create_part_info(
    pin_count: int,
    specs: SeriesSpec,
) -> PartInfo:
    """
    Create complete part information.

    Args:
        pin_count: Number of pins
        specs: Series specifications

    Returns:
        PartInfo instance with all specifications
    """
    mpn = generate_part_code(pin_count, specs.base_series)
    footprint = specs.footprint_pattern.format(pin_count)
    trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

    return PartInfo(
        symbol_name=f"J_{mpn}",
        reference="J",
        value=mpn,
        footprint=footprint,
        datasheet=specs.datasheet,
        description=create_description(pin_count, specs),
        manufacturer=specs.manufacturer,
        mpn=mpn,
        series=specs.base_series,
        trustedparts_link=trustedparts_link,
        color=specs.color,
        pitch=specs.pitch,
        pin_count=pin_count
    )


def generate_part_code(
    pin_count: int,
    series_code: str,
) -> str:
    """
    Generate connector part code based on pin count.

    Args:
        pin_count: Number of pins
        series_code: Base series code

    Returns:
        str: Part code string
    """
    return f"{series_code}-{pin_count:02d}BE"


def create_description(
    pin_count: int,
    specs: SeriesSpec,
) -> str:
    """
    Create component description with comprehensive specifications.

    Args:
        pin_count: Number of pins
        specs: Series specifications

    Returns:
        Formatted description string including manufacturer, series, pins,
        and pitch
    """
    parts = [
        f"{specs.manufacturer}",
        f"{specs.base_series} series",
        f"{pin_count} positions connector",
        f"{specs.pitch} mm pitch",
        f"{specs.color}"
    ]

    return " ".join(parts)
