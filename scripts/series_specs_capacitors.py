"""
Specifications and data structures for Murata GCM series ceramic capacitors.

This module defines the data structures and specifications for various Murata
GCM series ceramic capacitors, primarily focusing on X7R dielectric types.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from typing import NamedTuple, Final, Dict, List, Set
from enum import Enum


class SeriesType(Enum):
    """Defines supported dielectric types for capacitor series."""
    X7R = "X7R"


class SeriesSpec(NamedTuple):
    """Detailed specifications for a capacitor series.

    Contains all necessary parameters to define a specific capacitor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        base_series: Part number series identifier (e.g., 'GCM155')
        manufacturer: Name of the component manufacturer
        footprint: PCB footprint ID for the component
        voltage_rating: Maximum operating voltage specification
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        packaging_options: List of available packaging codes (e.g., ['D', 'J'])
        tolerance_map:
            Maps series types to available tolerance codes and values
            Format: {SeriesType: {code: value}}
        value_range: Valid capacitance range for each series type
            Format: {SeriesType: (min_value, max_value)}
        voltage_code: Voltage rating code used in part numbering
        dielectric_code: Maps series types to their dielectric material codes
            Format: {SeriesType: code}
        excluded_values: Set of unsupported capacitance values within range
        datasheet_url: Complete URL to component datasheet
        trustedparts_url:
            Base URL for component listing on Trustedparts platform
    """
    base_series: str
    manufacturer: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    packaging_options: List[str]
    tolerance_map: Dict[SeriesType, Dict[str, str]]
    value_range: Dict[SeriesType, tuple[float, float]]
    voltage_code: str
    dielectric_code: Dict[SeriesType, str]
    excluded_values: Set[float]
    datasheet_url: str
    trustedparts_url: str


class PartInfo(NamedTuple):
    """Container for detailed capacitor component information.

    Stores comprehensive information about a specific capacitor part,
    including its electrical characteristics, physical properties,
    and documentation links.

    Attributes:
        symbol_name: KiCad schematic symbol identifier
        reference: Component reference designator (e.g., 'C1')
        value: Capacitance value in Farads (float)
        formatted_value: Human-readable capacitance with units (e.g., '0.1 µF')
        footprint: PCB footprint library reference
        datasheet: URL to component documentation
        description: Descriptive text about the component
        manufacturer: Component manufacturer name
        mpn: Manufacturer's part number
        dielectric: Dielectric material type specification
        tolerance: Component tolerance specification
        voltage_rating: Maximum voltage specification
        case_code_in: Package dimensions in inches
        case_code_mm: Package dimensions in millimeters
        series: Component series identifier
        trustedparts_link: URL to component listing on Trustedparts
    """
    symbol_name: str
    reference: str
    value: float
    formatted_value: str
    footprint: str
    datasheet: str
    description: str
    manufacturer: str
    mpn: str
    dielectric: str
    tolerance: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    series: str
    trustedparts_link: str


SERIES_SPECS: Final[Dict[str, SeriesSpec]] = {
    "GCM155": SeriesSpec(
        base_series="GCM155",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        packaging_options=['D', 'J'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (220e-12, 0.1e-6)  # 220pF to 0.1µF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={
            27e-9,  # 27 nF
            39e-9,  # 39 nF
            56e-9,  # 56 nF
            82e-9   # 82 nF
        },
        datasheet_url="https://search.murata.co.jp/Ceramy/"
        "image/img/A01X/G101/ENG/GCM155",
        trustedparts_url="https://www.trustedparts.com/en/search"
    ),
    "GCM188": SeriesSpec(
        base_series="GCM188",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="50V",
        case_code_in="0603",
        case_code_mm="1608",
        packaging_options=['D', 'J'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (1e-9, 220e-9)  # Updated: 1nF to 220nF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={
            120e-9,  # 120 nF
            180e-9,  # 180 nF,
        },
        datasheet_url="https://search.murata.co.jp/Ceramy/"
        "image/img/A01X/G101/ENG/GCM188",
        trustedparts_url="https://www.trustedparts.com/en/search"
    ),
    "GCM216": SeriesSpec(
        base_series="GCM216",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="50V",
        case_code_in="0805",
        case_code_mm="2012",
        packaging_options=['D', 'J'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (1e-9, 22e-9)  # 1nF to 22nF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={},
        datasheet_url="https://search.murata.co.jp/Ceramy/"
        "image/img/A01X/G101/ENG/GCM216",
        trustedparts_url="https://www.trustedparts.com/en/search"
    ),
    "GCM31M": SeriesSpec(
        base_series="GCM31M",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=['K', 'L'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (100e-9, 1e-6)  # 100nF to 1µF
        },
        voltage_code="1H",
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values={
            180e-9,  # 180 nF
            560e-9,  # 560 nF,
        },
        datasheet_url="https://search.murata.co.jp/Ceramy/"
        "image/img/A01X/G101/ENG/GCM31M",
        trustedparts_url="https://www.trustedparts.com/en/search"
    ),
    "GCM31C": SeriesSpec(
        base_series="GCM31C",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=['K', 'L'],
        tolerance_map={
            SeriesType.X7R: {'K': '10%'}
        },
        value_range={
            SeriesType.X7R: (4.7e-6, 4.7e-6)  # Only 4.7µF
        },
        voltage_code="1E",  # 25V code
        dielectric_code={
            SeriesType.X7R: "R7"
        },
        excluded_values=set(),
        datasheet_url="https://search.murata.co.jp/Ceramy/" +
        "image/img/A01X/G101/ENG/GCM31C",
        trustedparts_url="https://www.trustedparts.com/en/search"
    ),
}
