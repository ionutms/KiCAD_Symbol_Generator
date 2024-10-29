"""todo"""
from typing import NamedTuple, Final, Dict, List, Set
from enum import Enum


class SeriesType(Enum):
    """Enumeration of supported capacitor series dielectric types."""
    X7R = "X7R"


class SeriesSpec(NamedTuple):
    """Specifications defining a capacitor series.

    Attributes:
        base_series: Base part number series
        manufacturer: Component manufacturer name
        footprint: PCB footprint identifier
        voltage_rating: Maximum voltage specification
        case_code_in: Package dimensions (inches)
        case_code_mm: Package dimensions (millimeters)
        packaging_options: Available packaging codes
        tolerance_map: Mapping of series types to tolerance codes and values
        value_range: Valid capacitance range per series type
        voltage_code: Voltage rating code for part number
        dielectric_code: Dielectric material codes per series type
        excluded_values: Set of unsupported capacitance values
        datasheet_url: Complete URL to the series datasheet
        trustedparts_url: Base URL for component listing on Trustedparts
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
    """Container for capacitor part information.

    Attributes:
        symbol_name: KiCad symbol identifier
        reference: Component reference designator
        value: Capacitance value in Farads
        formatted_value: Human-readable capacitance value with units
        footprint: PCB footprint reference
        datasheet: URL to component datasheet
        description: Component description text
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        dielectric: Dielectric material type
        tolerance: Component tolerance value
        voltage_rating: Maximum voltage rating
        case_code_in: Package size in inches
        case_code_mm: Package size in millimeters
        series: Component series identifier
        trustedparts_link: URL to component listing
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
        footprint="footprints:C_0402_1005Metric",
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
        footprint="footprints:C_0603_1608Metric",
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
        footprint="footprints:C_0805_2012Metric",
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
        footprint="footprints:C_1206_3216Metric",
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
        footprint="footprints:C_1206_3216Metric",
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
