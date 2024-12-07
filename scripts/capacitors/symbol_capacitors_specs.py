"""Specifications and data structures for ceramic capacitors.

This module defines the data structures and specifications for various ceramic
capacitors, including Murata GCM series and Samsung CL series, focusing on X7R
dielectric types. It provides comprehensive component information including
physical dimensions, electrical characteristics, and packaging options.
"""

from typing import Final, NamedTuple


class SeriesSpec(NamedTuple):
    """Detailed specifications for a capacitor series.

    Contains all necessary parameters to define a specific capacitor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        base_series: Part number series identifier (e.g., 'GCM155', 'CL31')
        manufacturer: Name of the component manufacturer (enum)
        footprint: PCB footprint ID for the component
        voltage_rating: Maximum operating voltage specification
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        packaging_options: List of available packaging codes
        tolerance_map: Maps dielectric types to tolerance codes and values
        value_range: Valid capacitance range for each dielectric type
        voltage_code: Voltage rating code used in part numbering
        dielectric_code: Maps dielectric types to their material codes
        excluded_values: Set of unsupported capacitance values within range
        datasheet_url: Complete URL to component datasheet
        trustedparts_url: Base URL for component listing on Trustedparts

    """

    base_series: str
    manufacturer: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    packaging_options: list[str]
    tolerance_map: dict[str, dict[str, str]]
    value_range: dict[str, tuple[float, float]]
    voltage_code: str
    dielectric_code: dict[str, str]
    excluded_values: set[float]
    datasheet_url: str
    trustedparts_url: str
    characteristic_codes: dict[float, str]
    reference: str = "C"


class PartInfo(NamedTuple):
    """Container for detailed capacitor component information."""

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


# Base URLs for documentation
MURATA_DOC_BASE = "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG"

# Murata specifications
SYMBOLS_SPECS = {
    "GCM155": SeriesSpec(
        base_series="GCM155",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        packaging_options=["D", "J"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (220e-12, 0.1e-6)},  # 220pF to 0.1µF
        voltage_code="1H",
        dielectric_code={"X7R": "R7"},
        excluded_values={27e-9, 39e-9, 56e-9, 82e-9},
        datasheet_url=f"{MURATA_DOC_BASE}/GCM155",
        trustedparts_url="https://www.trustedparts.com/en/search",
        characteristic_codes={22e-9: "E02", 4.7e-9: "A55", 0: "A37"},
    ),
    "GCM188": SeriesSpec(
        base_series="GCM188",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="50V",
        case_code_in="0603",
        case_code_mm="1608",
        packaging_options=["D", "J"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (1e-9, 220e-9)},  # 1nF to 220nF
        voltage_code="1H",
        dielectric_code={"X7R": "R7"},
        excluded_values={120e-9, 180e-9},
        datasheet_url=f"{MURATA_DOC_BASE}/GCM188",
        trustedparts_url="https://www.trustedparts.com/en/search",
        characteristic_codes={
            100e-9: "A64", 47e-9: "A57", 22e-9: "A55", 0: "A37"},
    ),
    "GCM216": SeriesSpec(
        base_series="GCM216",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="50V",
        case_code_in="0805",
        case_code_mm="2012",
        packaging_options=["D", "J"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (1e-9, 22e-9)},  # 1nF to 22nF
        voltage_code="1H",
        dielectric_code={"X7R": "R7"},
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}/GCM216",
        trustedparts_url="https://www.trustedparts.com/en/search",
        characteristic_codes={22e-9: "A55", 0: "A37"},
    ),
    "GCM31M": SeriesSpec(
        base_series="GCM31M",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=["K", "L"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (100e-9, 1e-6)},  # 100nF to 1µF
        voltage_code="1H",
        dielectric_code={"X7R": "R7"},
        excluded_values={180e-9, 560e-9},
        datasheet_url=f"{MURATA_DOC_BASE}/GCM31M",
        trustedparts_url="https://www.trustedparts.com/en/search",
        characteristic_codes={560e-9: "A55", 100e-9: "A37", 0: "A37"},
    ),
    "GCM31C": SeriesSpec(
        base_series="GCM31C",
        manufacturer="Murata Electronics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=["K", "L"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        voltage_code="1E",
        dielectric_code={"X7R": "R7"},
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}/GCM31C",
        trustedparts_url="https://www.trustedparts.com/en/search",
        characteristic_codes={4.7e-6: "A55", 0: "A55"},
    ),
}

# Base URLs for documentation
SAMSUNG_DOC_BASE = (
    "https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=")

# Samsung specifications (X7R only)
SAMSUNG_SPECS = {
    "CL31": SeriesSpec(
        base_series="CL31",
        manufacturer="Samsung Electro-Mechanics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=["HNNN#"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (0.47e-6, 10e-6)},
        voltage_code="B",
        dielectric_code={"X7R": "B"},
        excluded_values={
            0.56e-6, 0.68e-6, 0.82e-6, 1.2e-6, 1.5e-6, 1.8e-6, 2.7e-6, 3.3e-6,
            3.9e-6, 5.6e-6, 6.8e-6, 8.2e-6},
        datasheet_url=f"{SAMSUNG_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search/CL31",
        characteristic_codes={0: "X7R"},
    ),
}

# Combined specifications dictionary
SERIES_SPECS: Final[dict[str, SeriesSpec]] = {
    **SYMBOLS_SPECS, **SAMSUNG_SPECS}
