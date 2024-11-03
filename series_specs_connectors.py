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
    """
    manufacturer: str
    base_series: str
    footprint_pattern: str
    datasheet: str
    pin_counts: List[int]
    trustedparts_link: str


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


SERIES_SPECS: Dict[str, SeriesSpec] = {
    "TBP02R2-381": SeriesSpec(
        manufacturer="Same Sky",
        base_series="TBP02R2-381",
        footprint_pattern="footprints:TBP02R2-381-{:02d}BE",
        datasheet="https://www.sameskydevices.com/" +
        "product/resource/tbp02r2-381.pdf",
        pin_counts=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16],
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}


def generate_part_info(
    series_spec: SeriesSpec,
    pin_count: int,
) -> PartInfo:
    """
    Generate a PartInfo instance for a specific connector configuration.

    Args:
        series_spec: SeriesSpec instance containing series information
        pin_count: Number of pins for this connector variant
        color: Color of the connector housing
        contact_material: Material of the contacts
        temp_range: Operating temperature range

    Returns:
        PartInfo: Complete part information for the specified connector
    """
    mpn = f"{series_spec.base_series}-{pin_count:02d}BE"
    symbol_name = f"J_{mpn}"
    description = (
        f"Connector {pin_count}BE {series_spec.pitch}mm pitch, "
        f"{series_spec.current_rating}A per contact"
    )

    return PartInfo(
        symbol_name=symbol_name,
        reference="J",
        value=f"{mpn}",
        footprint=series_spec.footprint_pattern.format(pin_count),
        datasheet=series_spec.datasheet,
        description=description,
        manufacturer=series_spec.manufacturer,
        mpn=mpn,
        series=series_spec.base_series,
        trustedparts_link=f"{series_spec.trustedparts_link}/{mpn}",
        pitch=series_spec.pitch,
        current_rating=series_spec.current_rating,
        voltage_rating=series_spec.voltage_rating,
    )
