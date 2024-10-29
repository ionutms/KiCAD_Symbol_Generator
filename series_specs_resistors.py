"""todo"""
from typing import List, NamedTuple, Final, Dict
from enum import Enum


class SeriesType(Enum):
    """Enumeration for resistor series types."""
    E96 = "E96"
    E24 = "E24"


class SeriesSpec(NamedTuple):
    """Specifications for a resistor series."""
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
    """Structure to hold component part information."""
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
        footprint="footprints:R_0402_1005Metric",
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
        footprint="footprints:R_0603_1608Metric",
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
        footprint="footprints:R_0805_2012Metric",
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
        footprint="footprints:R_1206_3216Metric",
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
        footprint="footprints:R_0805_2012Metric",
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
        footprint="footprints:R_0603_1608Metric",
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
