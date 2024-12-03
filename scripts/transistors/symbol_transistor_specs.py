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
    drain_source_voltage : list[float]
    trustedparts_link: str
    drain_current: list[float]
    package: str
    transistor_type: str
    reference: str = "Q"


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
    drain_current: float
    package: str
    transistor_type: str


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "SI7309DN-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors", base_series="SI7309DN-T1-GE3",
        footprint="transistor_footprints:PowerPAK 1212-8",
        datasheet="https://www.vishay.com/docs/73434/si7309dn.pdf",
        drain_source_voltage =[-60.0], drain_current=[-8.0],
        package="PowerPAK 1212-8", transistor_type="P-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "PSMN040-100MSEX": SeriesSpec(
        manufacturer="Nexperia", base_series="PSMN040-100MSEX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "PSMN040-100MSE.pdf"),
        drain_source_voltage =[100.0], drain_current=[30],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "BUK9M34-100EX": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9M34-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M34-100E.pdf"),
        drain_source_voltage =[100.0], drain_current=[29],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "BUK9M43-100EX": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9M43-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M43-100E.pdf"),
        drain_source_voltage =[100.0], drain_current=[25],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "PSMN075-100MSEX": SeriesSpec(
        manufacturer="Nexperia", base_series="PSMN075-100MSEX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "PSMN075-100MSE.pdf"),
        drain_source_voltage =[100.0], drain_current=[18],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9M120-100EX": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9M120-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M120-100E.pdf"),
        drain_source_voltage =[100.0], drain_current=[11.5],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
    "BUK9M156-100EX": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9M156-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M156-100E.pdf"),
        drain_source_voltage =[100.0], drain_current=[9.3],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search",
    ),
}
