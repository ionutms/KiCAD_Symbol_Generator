"""Specifications and data structures for Panasonic ERJ series resistors.

This module defines the specifications for various Panasonic ERJ series
resistors, supporting both E96 and E24 value series.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from collections.abc import Iterator
from typing import Final, NamedTuple


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
        min_resistance: Minimum resistance value in ohms
        max_resistance: Maximum resistance value in ohms
        packaging_options:
            List of available packaging codes (e.g., ['V', 'X'])
        tolerance_map:
            Maps series types to available tolerance codes and values
            Format: {str: {code: value}}
        datasheet: Complete URL to component datasheet
        manufacturer: Name of the component manufacturer
        trustedparts_url:
            Base URL for component listing on Trustedparts platform

    """

    base_series: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    power_rating: str
    packaging_options: list[str]
    tolerance_map: dict[str, dict[str, str]]
    datasheet: str
    manufacturer: str
    trustedparts_url: str
    min_resistance: int = 10
    max_resistance: int = 1_000_000
    reference: str = "R"


E96_BASE_VALUES: Final[list[float]] = [
    10.0, 10.2, 10.5, 10.7, 11.0, 11.3, 11.5, 11.8, 12.1, 12.4, 12.7,
    13.0, 13.3, 13.7, 14.0, 14.3, 14.7, 15.0, 15.4, 15.8, 16.2, 16.5,
    16.9, 17.4, 17.8, 18.2, 18.7, 19.1, 19.6, 20.0, 20.5, 21.0, 21.5,
    22.1, 22.6, 23.2, 23.7, 24.3, 24.9, 25.5, 26.1, 26.7, 27.4, 28.0,
    28.7, 29.4, 30.1, 30.9, 31.6, 32.4, 33.2, 34.0, 34.8, 35.7, 36.5,
    37.4, 38.3, 39.2, 40.2, 41.2, 42.2, 43.2, 44.2, 45.3, 46.4, 47.5,
    48.7, 49.9, 51.1, 52.3, 53.6, 54.9, 56.2, 57.6, 59.0, 60.4, 61.9,
    63.4, 64.9, 66.5, 68.1, 69.8, 71.5, 73.2, 75.0, 76.8, 78.7, 80.6,
    82.5, 84.5, 86.6, 88.7, 90.9, 93.1, 95.3, 97.6,
]

E24_BASE_VALUES: Final[list[float]] = [
    10.0, 11.0, 12.0, 13.0, 15.0, 16.0, 18.0, 20.0, 22.0, 24.0, 27.0,
    30.0, 33.0, 36.0, 39.0, 43.0, 47.0, 51.0, 56.0, 62.0, 68.0, 75.0,
    82.0, 91.0,
]


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

    @classmethod
    def format_resistance_value(cls, resistance: float) -> str:
        """Convert a resistance value to a human-readable string format.

        Args:
            resistance: The resistance value in ohms

        Returns:
            A formatted string with appropriate unit suffix (Ω, kΩ, or MΩ)

        """
        def clean_number(num: float) -> str:
            return f"{num:g}"

        if resistance >= 1_000_000:  # noqa: PLR2004
            return f"{clean_number(resistance / 1_000_000)} MΩ"
        if resistance >= 1_000:  # noqa: PLR2004
            return f"{clean_number(resistance / 1_000)} kΩ"
        return f"{clean_number(resistance)} Ω"

    @classmethod
    def generate_resistance_code(
        cls,
        resistance: float,
        min_resistance: int,
        max_resistance: int,
        specs: SeriesSpec,
    ) -> str:
        """Generate the resistance code portion of a Panasonic part number.

        Args:
            resistance: The resistance value in ohms
            min_resistance: Minimum allowed resistance value for the series
            max_resistance: Maximum allowed resistance value for the series
            specs: Series specifications

        Returns:
            A string representing the resistance code

        Raises:
            ValueError: If resistance is outside valid range

        """
        # Check resistance range first
        if resistance < min_resistance or resistance > max_resistance:
            msg = (
                f"Resistance value out of range "
                f"({min_resistance}Ω to {max_resistance}Ω)")
            raise ValueError(msg)

        # Special handling for Yageo manufacturer
        if specs.manufacturer == "Yageo":
            return cls._generate_yageo_resistance_code(resistance)

        # Special handling for specific ERJ series
        if specs.base_series in ("ERJ-2GEJ", "ERJ-3GEYJ", "ERJ-6GEYJ"):
            return cls._generate_erj_special_series_code(resistance)

        # Standard Panasonic/generic resistance code generation
        return cls._generate_standard_resistance_code(resistance)

    @classmethod
    def _generate_yageo_resistance_code(cls, resistance: float) -> str:
        """Generate resistance code for Yageo manufacturer."""
        if resistance < 1000:  # < 1kΩ  # noqa: PLR2004
            whole = int(resistance)
            decimal = str(int(round((resistance - whole) * 100))).rstrip("0")
            return f"{whole:01d}R{decimal}"

        if resistance < 10_000:  # 1-10kΩ  # noqa: PLR2004
            whole = int(resistance / 1000)
            decimal = str(int(round((resistance % 1000) / 10))).rstrip("0")
            return f"{whole}K{decimal}"

        # ≥ 10kΩ
        whole = int(resistance / 1000000)
        decimal = str(int(round((resistance % 1000000) / 10))).rstrip("0")
        return f"{whole}M{decimal}"

    @classmethod
    def _generate_erj_special_series_code(cls, resistance: float) -> str:
        """Generate resistance code for special ERJ series."""
        if resistance < 10:  # < 10Ω  # noqa: PLR2004
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:01d}R{decimal}"

        if resistance < 100:  # 10-99Ω  # noqa: PLR2004
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:01d}{decimal}"

        # Determine multiplier and significant digits for values ≥ 100Ω
        if resistance < 1000:  # 100-999Ω  # noqa: PLR2004
            significant = int(round(resistance / 10))
            multiplier = "1"
        elif resistance < 10000:  # 1k-9.99kΩ  # noqa: PLR2004
            significant = int(round(resistance / 100))
            multiplier = "2"
        elif resistance < 100000:  # 10k-99.9kΩ  # noqa: PLR2004
            significant = int(round(resistance / 1000))
            multiplier = "3"
        elif resistance < 1000000:  # 100k-999kΩ  # noqa: PLR2004
            significant = int(round(resistance / 10000))
            multiplier = "4"
        else:  # 1MΩ+
            significant = int(round(resistance / 100000))
            multiplier = "5"

        return f"{significant:02d}{multiplier}"

    @classmethod
    def _generate_standard_resistance_code(cls, resistance: float) -> str:
        """Generate standard resistance code for Panasonic style."""
        # Handle values less than 100Ω using R notation
        if resistance < 100:  # noqa: PLR2004
            whole = int(resistance)
            decimal = int(round((resistance - whole) * 10))
            return f"{whole:02d}R{decimal}"

        # For values ≥ 100Ω, determine multiplier and significant digits
        if resistance < 1000:  # 100-999Ω  # noqa: PLR2004
            significant = int(round(resistance))
            multiplier = "0"
        elif resistance < 10000:  # 1k-9.99kΩ  # noqa: PLR2004
            significant = int(round(resistance / 10))
            multiplier = "1"
        elif resistance < 100000:  # 10k-99.9kΩ  # noqa: PLR2004
            significant = int(round(resistance / 100))
            multiplier = "2"
        elif resistance < 1000000:  # 100k-999kΩ  # noqa: PLR2004
            significant = int(round(resistance / 1000))
            multiplier = "3"
        else:  # 1MΩ+
            significant = int(round(resistance / 10000))
            multiplier = "4"

        return f"{significant:03d}{multiplier}"

    @classmethod
    def generate_resistance_values(
        cls,
        base_values: list[float],
        min_resistance: int,
        max_resistance: int,
    ) -> Iterator[float]:
        """Generate all valid resistance values from a list of base values.

        Args:
            base_values: List of base resistance values (E96 or E24 series)
            min_resistance: Minimum resistance value to generate
            max_resistance: Maximum resistance value to generate

        Yields:
            float: Valid resistance values in ascending order

        """
        multipliers = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000]

        for base_value in base_values:
            for multiplier in multipliers:
                resistance = base_value * multiplier
                if min_resistance <= resistance <= max_resistance:
                    yield resistance

    @classmethod
    def create_part_info(
        cls,
        resistance: float,
        tolerance_value: str,
        packaging: str,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create a PartInfo instance with complete component specifications.

        Args:
            resistance: Resistance value in ohms
            tolerance_value: Human-readable tolerance (e.g., '1%')
            packaging: Packaging code (e.g., 'X' or 'V')
            specs: SeriesSpec instance containing series specifications

        Returns:
            PartInfo instance containing all component details
            and vendor information

        """
        resistance_code = cls.generate_resistance_code(
            resistance, specs.min_resistance, specs.max_resistance,
            specs)

        packaging_code = packaging

        mpn = f"{specs.base_series}{resistance_code}{packaging_code}"

        description = (
            f"RES SMD {cls.format_resistance_value(resistance)} "
            f"{tolerance_value} {specs.case_code_in} {specs.voltage_rating}")
        trustedparts_link = f"{specs.trustedparts_url}{mpn}"

        datasheet = specs.datasheet
        if specs.manufacturer == "Yageo":
            datasheet = f"{specs.datasheet}{mpn}"

        return PartInfo(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=resistance,
            footprint=specs.footprint,
            datasheet=datasheet,
            description=description,
            manufacturer=specs.manufacturer,
            mpn=mpn,
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
        """Generate all possible part numbers for a resistor series.

        Args:
            specs: SeriesSpec instance containing series specifications

        Returns:
            List of PartInfo instances for all valid combinations

        """
        return [
            cls.create_part_info(
                resistance,
                tolerance_value,
                packaging,
                specs,
            )
            for series_type in specs.tolerance_map
            for resistance in cls.generate_resistance_values(
                E96_BASE_VALUES if series_type == "E96" else E24_BASE_VALUES,
                specs.min_resistance,
                specs.max_resistance,
            )
            for tolerance_value in [specs.tolerance_map[series_type]]
            for packaging in specs.packaging_options
        ]


PANASONIC_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "ERJ-2RKF": SeriesSpec(
        manufacturer="Panasonic",
        base_series="ERJ-2RKF",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        min_resistance=10,
        max_resistance=1_000_000,
        packaging_options=["X"],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-3EKF": SeriesSpec(
        base_series="ERJ-3EKF",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        min_resistance=10,
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-6ENF": SeriesSpec(
        base_series="ERJ-6ENF",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        min_resistance=10,
        max_resistance=2_200_000,
        packaging_options=["V"],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P08F": SeriesSpec(
        base_series="ERJ-P08F",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="500V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.66W",
        min_resistance=10,
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P06F": SeriesSpec(
        base_series="ERJ-P06F",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="400V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.5W",
        min_resistance=10,
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P03F": SeriesSpec(
        base_series="ERJ-P03F",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="150V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.25W",
        min_resistance=10,
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-2GEJ": SeriesSpec(
        base_series="ERJ-2GEJ",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        min_resistance=1,
        max_resistance=1_000_000,
        packaging_options=["X"],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-3GEYJ": SeriesSpec(
        base_series="ERJ-3GEYJ",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        min_resistance=1,
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-6GEYJ": SeriesSpec(
        base_series="ERJ-6GEYJ",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        min_resistance=1,
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}

YAGEO_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "RT0805BRB07": SeriesSpec(
        manufacturer="Yageo",
        base_series="RT0805BRB07",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        min_resistance=4.7,
        max_resistance=1_000_000,
        packaging_options=["L"],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRC07": SeriesSpec(
        manufacturer="Yageo",
        base_series="RT0805BRC07",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        min_resistance=4.7,
        max_resistance=1_000_000,
        packaging_options=["L"],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRD07": SeriesSpec(
        manufacturer="Yageo",
        base_series="RT0805BRD07",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        min_resistance=1,
        max_resistance=1_500_000,
        packaging_options=["L"],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRE07": SeriesSpec(
        manufacturer="Yageo",
        base_series="RT0805BRE07",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        min_resistance=1,
        max_resistance=3_000_000,
        packaging_options=["L"],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}

# Combined specifications dictionary
SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    **PANASONIC_SYMBOLS_SPECS, **YAGEO_SYMBOLS_SPECS}
