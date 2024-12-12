"""Specifications and data structures for ceramic capacitors.

This module defines the data structures and specifications for various ceramic
capacitors, including Murata GCM series and Samsung CL series, focusing on X7R
dielectric types. It provides comprehensive component information including
physical dimensions, electrical characteristics, and packaging options.
"""

from typing import Final, Iterator, NamedTuple  # noqa: UP035


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
    excluded_values: set[float]
    datasheet_url: str
    trustedparts_url: str
    voltage_code: str = ""
    dielectric_code: dict[str, str] = {}  # noqa: RUF012
    characteristic_codes: dict[float, str] = {}  # noqa: RUF012
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

    @staticmethod
    def format_capacitance_value(capacitance: float) -> str:
        """Convert capacitance value to human-readable format with units."""
        pf_value = capacitance * 1e12

        # 1 µF and above
        if capacitance >= 1e-6:  # noqa: PLR2004
            value = capacitance / 1e-6
            unit = "µF"

        # 1000 pF and above -> convert to nF
        elif pf_value >= 1000:  # noqa: PLR2004
            value = pf_value / 1000
            unit = "nF"
        else:  # Below 1000 pF
            value = pf_value
            unit = "pF"

        # Format the number to remove unnecessary decimals
        if value % 1 == 0:
            return f"{int(value)} {unit}"
        formatted = f"{value:.3g}"

        return f"{formatted} {unit}"

    @staticmethod
    def generate_capacitance_code(capacitance: float) -> str:
        """Generate the capacitance portion of Murata part number."""
        pf_value = capacitance * 1e12

        # Handle values under 10pF
        if pf_value < 10:  # noqa: PLR2004
            whole = int(pf_value)
            decimal = int((pf_value - whole) * 10)
            return f"{whole}R{decimal}"

        # Handle values under 1000pF
        if pf_value < 1000:  # noqa: PLR2004
            significant = round(pf_value)
            if significant % 10 == 0:
                significant += 1
            return f"{significant:03d}"

        # Handle values 1000pF and above
        sci_notation = f"{pf_value:.2e}"
        parts = sci_notation.split("e")
        significand = float(parts[0])
        power = int(parts[1])

        first_two = int(round(significand * 10))
        zero_count = power - 1

        return f"{first_two}{zero_count}"

    @classmethod
    def get_characteristic_code(
        cls,
        capacitance: float,
        specs: SeriesSpec,
    ) -> str:
        """Determine characteristic code based on series and capacitance."""
        if specs.base_series.startswith("CL"):
            return "X7R"

        if not specs.characteristic_codes:
            return ""

        for threshold, code in sorted(
                specs.characteristic_codes.items(), reverse=True):
            if capacitance > threshold:
                return code

        return list(specs.characteristic_codes.values())[-1]

    @classmethod
    def generate_standard_values(
        cls,
        min_value: float,
        max_value: float,
        excluded_values: set[float],
    ) -> Iterator[float]:
        """Generate standard E12 series capacitance values within range."""
        e12_multipliers = [
            1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

        normalized_excluded = {
            float(f"{value:.1e}") for value in excluded_values}

        decade = 1.0e-12
        while decade <= max_value:
            for multiplier in e12_multipliers:
                normalized_value = float(f"{decade * multiplier:.1e}")
                if min_value <= normalized_value <= max_value:  # noqa: SIM102
                    if normalized_value not in normalized_excluded:
                        yield normalized_value
            decade *= 10

    @staticmethod
    def generate_datasheet_url(
        mpn: str,
        specs: SeriesSpec,
    ) -> str:
        """Generate the datasheet URL for a given Murata part number."""
        if specs.manufacturer == "Murata Electronics":
            base_mpn = mpn[:-1]
            specific_part = base_mpn[len(specs.base_series):]
            return f"{specs.datasheet_url}{specific_part}-01.pdf"
        return f"{specs.datasheet_url}{mpn}"

    @classmethod
    def create_part_info(  # noqa: PLR0913
        cls,
        capacitance: float,
        tolerance_code: str,
        tolerance_value: str,
        packaging: str,
        dielectric_type: str,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create complete part information from component parameters."""
        capacitance_code = cls.generate_capacitance_code(capacitance)
        characteristic_code = cls.get_characteristic_code(capacitance, specs)
        formatted_value = cls.format_capacitance_value(capacitance)

        dielectric_part = (
            specs.dielectric_code.get(dielectric_type, dielectric_type)
            if specs.dielectric_code
            else dielectric_type
        )

        if specs.manufacturer == "Murata Electronics":
            mpn = (
                f"{specs.base_series}"
                f"{dielectric_part}"
                f"{specs.voltage_code}"
                f"{capacitance_code}"
                f"{tolerance_code}"
                f"{characteristic_code}"
                f"{packaging}"
            )
        elif specs.manufacturer == "TDK":
            mpn = (
                f"{specs.base_series}"
                f"{specs.voltage_code}"
                f"{capacitance_code}"
                f"{tolerance_code}"
                f"{packaging}"
            )
        else:
            mpn = (
                f"{specs.base_series}"
                f"{capacitance_code}"
                f"{tolerance_code}"
                f"{specs.voltage_code}"
                f"{packaging}"
            )

        description = (
            f"CAP SMD {formatted_value} "
            f"{dielectric_type} {tolerance_value} "
            f"{specs.case_code_in} {specs.voltage_rating}"
        )

        trustedparts_link = f"{specs.trustedparts_url}/{mpn}"
        datasheet_url = cls.generate_datasheet_url(mpn, specs)

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference="C",
            value=capacitance,
            formatted_value=formatted_value,
            footprint=specs.footprint,
            datasheet=datasheet_url,
            description=description,
            manufacturer=specs.manufacturer,
            mpn=mpn,
            dielectric=dielectric_type,
            tolerance=tolerance_value,
            voltage_rating=specs.voltage_rating,
            case_code_in=specs.case_code_in,
            case_code_mm=specs.case_code_mm,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list["PartInfo"]:
        """Generate all valid part numbers for a series specification."""
        parts_list: list[PartInfo] = []
        dielectric_types = ["X7R", "X7S"]

        for dielectric_type in dielectric_types:
            if dielectric_type in specs.value_range:
                min_val, max_val = specs.value_range[dielectric_type]

                for capacitance in cls.generate_standard_values(
                        min_val, max_val, specs.excluded_values):
                    for tolerance_code, tolerance_value in \
                            specs.tolerance_map[dielectric_type].items():
                        for packaging in specs.packaging_options:
                            parts_list.append(cls.create_part_info(  # noqa: PERF401
                                capacitance=capacitance,
                                tolerance_code=tolerance_code,
                                tolerance_value=tolerance_value,
                                packaging=packaging,
                                dielectric_type=dielectric_type,
                                specs=specs,
                            ))

        return sorted(parts_list, key=lambda x: (x.dielectric, x.value))


# Base URLs for documentation
MURATA_DOC_BASE = "https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG"

MURATA_SYMBOLS_SPECS = {
    "GCM155": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GCM155",
        dielectric_code={"X7R": "R7"},
        voltage_code="1H",
        value_range={"X7R": (220e-12, 0.1e-6)},  # 220pF to 0.1µF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={22e-9: "E02", 4.7e-9: "A55", 0: "A37"},
        packaging_options=["D", "J"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={27e-9, 39e-9, 56e-9, 82e-9},
        datasheet_url=f"{MURATA_DOC_BASE}/GCM155",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),

    "GCM188": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GCM188",
        dielectric_code={"X7R": "R7"},
        voltage_code="1H",
        value_range={"X7R": (1e-9, 220e-9)},  # 1nF to 220nF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={
            100e-9: "A64", 47e-9: "A57", 22e-9: "A55", 0: "A37"},
        packaging_options=["D", "J"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="50V",
        case_code_in="0603",
        case_code_mm="1608",
        excluded_values={120e-9, 180e-9},
        datasheet_url=f"{MURATA_DOC_BASE}/GCM188",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM216": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GCM216",
        dielectric_code={"X7R": "R7"},
        voltage_code="1H",
        value_range={"X7R": (1e-9, 22e-9)},  # 1nF to 22nF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={22e-9: "A55", 0: "A37"},
        packaging_options=["D", "J"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="50V",
        case_code_in="0805",
        case_code_mm="2012",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}/GCM216",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM31M": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GCM31M",
        dielectric_code={"X7R": "R7"},
        voltage_code="1H",
        value_range={"X7R": (100e-9, 1e-6)},  # 100nF to 1µF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={560e-9: "A55", 100e-9: "A37", 0: "A37"},
        packaging_options=["K", "L"],
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        excluded_values={180e-9, 560e-9},
        datasheet_url=f"{MURATA_DOC_BASE}/GCM31M",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM31C": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GCM31C",
        dielectric_code={"X7R": "R7"},
        voltage_code="1E",
        value_range={"X7R": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        tolerance_map={"X7R": {"K": "10%"}},
        characteristic_codes={4.7e-6: "A55", 0: "A55"},
        packaging_options=["K", "L"],
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="25V",
        case_code_in="1206",
        case_code_mm="3216",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}/GCM31C",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GRM188": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GRM188",
        dielectric_code={"X7S": "C7"},
        voltage_code="1A",
        value_range={"X7S": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={0: "E11"},
        packaging_options=["D"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="10V",
        case_code_in="0603",
        case_code_mm="1608",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}/GRM188",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "GCM32D": SeriesSpec(
        manufacturer="Murata Electronics",
        base_series="GCM32D",
        dielectric_code={"X7S": "C7"},
        voltage_code="2A",
        value_range={"X7S": (4.7e-6, 4.7e-6)},  # Only 4.7µF
        tolerance_map={"X7S": {"K": "10%"}},
        characteristic_codes={0: "E02"},
        packaging_options=["K"],
        footprint="capacitor_footprints:C_1210_3225Metric",
        voltage_rating="100V",
        case_code_in="1210",
        case_code_mm="3225",
        excluded_values=set(),
        datasheet_url=f"{MURATA_DOC_BASE}/GCM32D",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Base URLs for documentation
SAMSUNG_DOC_BASE = (
    "https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=")

SAMSUNG_SYMBOLS_SPECS = {
    "CL31B": SeriesSpec(
        base_series="CL31B",
        manufacturer="Samsung Electro-Mechanics",
        footprint="capacitor_footprints:C_1206_3216Metric",
        voltage_rating="50V",
        case_code_in="1206",
        case_code_mm="3216",
        packaging_options=["BHNNN#"],
        tolerance_map={"X7R": {"K": "10%"}},
        value_range={"X7R": (0.47e-6, 10e-6)},
        dielectric_code={"X7R": "B"},
        excluded_values={
            0.56e-6, 0.68e-6, 0.82e-6, 1.2e-6, 1.5e-6, 1.8e-6, 2.7e-6, 3.3e-6,
            3.9e-6, 5.6e-6, 6.8e-6, 8.2e-6},
        datasheet_url=f"{SAMSUNG_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search/CL31",
    ),
}

# Base URLs for documentation
TDK_DOC_BASE = (
    "https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=")

TDK_SYMBOLS_SPECS = {
    "C1005X7S1A": SeriesSpec(
        manufacturer="TDK",
        base_series="C1005X7S1A",
        value_range={"X7S": (0.33e-6, 2.2e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        packaging_options=["050BC"],
        footprint="capacitor_footprints:C_0402_1005Metric",
        voltage_rating="10V",
        case_code_in="0402",
        case_code_mm="1005",
        excluded_values={0.39e-6, 0.56e-6, 0.82e-6, 1.2e-6, 1.8e-6},
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C1608X7S1A": SeriesSpec(
        manufacturer="TDK",
        base_series="C1608X7S1A",
        value_range={"X7S": (2.2e-6, 4.7e-6)},
        tolerance_map={"X7S": {"K": "10%"}},
        packaging_options=["080AC"],
        footprint="capacitor_footprints:C_0603_1608Metric",
        voltage_rating="10V",
        case_code_in="0603",
        case_code_mm="1608",
        excluded_values={2.7e-6, 3.3e-6, 3.9e-6},
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
    "C2012X7S1A": SeriesSpec(
        manufacturer="TDK",
        base_series="C2012X7S1A",
        value_range={"X7S": (15e-6, 22e-6)},
        tolerance_map={"X7S": {"M": "20%"}},
        packaging_options=["125AC"],
        footprint="capacitor_footprints:C_0805_2012Metric",
        voltage_rating="10V",
        case_code_in="0805",
        case_code_mm="2012",
        excluded_values={18e-6},
        datasheet_url=f"{TDK_DOC_BASE}",
        trustedparts_url="https://www.trustedparts.com/en/search",
    ),
}

# Combined specifications dictionary
SERIES_SPECS: Final[dict[str, SeriesSpec]] = {
    **MURATA_SYMBOLS_SPECS, **SAMSUNG_SYMBOLS_SPECS, **TDK_SYMBOLS_SPECS}
