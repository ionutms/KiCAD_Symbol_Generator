"""
Specifications and data structures for Panasonic ERJ series resistors.

This module defines the data structures and specifications for various
Panasonic ERJ series resistors, supporting both E96 and E24 value series.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from typing import List, NamedTuple, Final, Dict
from enum import Enum


class SeriesType(Enum):
    """Defines supported resistance value series types.

    Values:
        E96: 96 values per decade, typically 1% tolerance
        E24: 24 values per decade, typically 5% tolerance
    """
    E96 = "E96"
    E24 = "E24"


class SeriesSpec(NamedTuple):
    """Detailed specifications for a resistor series.

    Contains all necessary parameters to define a specific resistor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        base_series: Part number series identifier (e.g., 'ERJ-2RK')
        footprint: PCB footprint ID for the component
        voltage_rating: Maximum operating voltage specification
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        power_rating: Maximum power dissipation specification
        max_resistance: Maximum resistance value in ohms
        packaging_options: List of available packaging codes (e.g., ['V', 'X'])
        tolerance_map:
            Maps series types to available tolerance codes and values
            Format: {SeriesType: {code: value}}
        datasheet: Complete URL to component datasheet
        manufacturer: Name of the component manufacturer
        trustedparts_url:
            Base URL for component listing on Trustedparts platform
        high_resistance_tolerance: Optional special tolerances for high values
            Format: {code: value} or None if not applicable
    """
    base_series: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    power_rating: str
    max_resistance: int
    packaging_options: List[str]
    tolerance_map: Dict[SeriesType, Dict[str, str]]
    datasheet: str
    manufacturer: str
    trustedparts_url: str
    high_resistance_tolerance: Dict[str, str] | None = None


class PartInfo(NamedTuple):
    """Container for detailed resistor component information.

    Stores comprehensive information about a specific resistor part,
    including its electrical characteristics, physical properties,
    and documentation links.

    Attributes:
        symbol_name: KiCad schematic symbol identifier
        reference: Component reference designator (e.g., 'R1')
        value: Resistance value in ohms (float)
        footprint: PCB footprint library reference
        datasheet: URL to component documentation
        description: Descriptive text about the component
        manufacturer: Component manufacturer name
        mpn: Manufacturer's part number
        tolerance: Component tolerance specification (e.g., '1%', '5%')
        voltage_rating: Maximum voltage specification
        case_code_in: Package dimensions in inches
        case_code_mm: Package dimensions in millimeters
        series: Component series identifier
        trustedparts_link: URL to component listing on Trustedparts
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
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    series: str
    trustedparts_link: str


SERIES_SPECS: Final[Dict[str, SeriesSpec]] = {
    "ERJ-2RK": SeriesSpec(
        base_series="ERJ-2RK",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=['X'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'J': '5%'}
        },
        datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/" +
        "RDA0000/AOA0000C304.pdf",
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-3EK": SeriesSpec(
        base_series="ERJ-3EK",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'J': '5%'}
        },
        datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/" +
        "RDA0000/AOA0000C304.pdf",
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-6EN": SeriesSpec(
        base_series="ERJ-6EN",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        max_resistance=2_200_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'J': '5%'}
        },
        datasheet="https://industrial.panasonic.com/cdbs/www-data/pdf/" +
        "RDA0000/AOA0000C304.pdf",
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/",
        high_resistance_tolerance={'F': '1%'}
    ),
    "ERJ-P08": SeriesSpec(
        base_series="ERJ-P08",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="500V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.66W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'F': '1%'}
        },
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"
        ),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-P06": SeriesSpec(
        base_series="ERJ-P06",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="400V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.5W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'F': '1%'}
        },
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"
        ),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
    "ERJ-P03": SeriesSpec(
        base_series="ERJ-P03",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="150V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.25W",
        max_resistance=1_000_000,
        packaging_options=['V'],
        tolerance_map={
            SeriesType.E96: {'F': '1%'},
            SeriesType.E24: {'F': '1%'}
        },
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"
        ),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"
    ),
}
