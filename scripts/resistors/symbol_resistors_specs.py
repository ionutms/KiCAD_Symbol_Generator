"""Specifications and data structures for Panasonic ERJ series resistors.

This module defines the specifications for various Panasonic ERJ series
resistors, supporting both E96 and E24 value series.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from collections.abc import Iterator
from typing import Final, NamedTuple, Optional, Union


class SeriesSpec(NamedTuple):
    """Detailed specifications for a resistor series.

    Contains all necessary parameters to define a specific resistor series,
    including physical characteristics, electrical ratings,
    and available configurations.

    Attributes:
        mpn_prefix: Part number prefix
        footprint: PCB footprint ID for the component
        voltage_rating: Maximum operating voltage specification
        case_code_in: Package dimensions in inches (e.g., '0402')
        case_code_mm: Package dimensions in millimeters (e.g., '1005')
        power_rating: Maximum power dissipation specification
        resistance_range: Minimum and maximum resistance values in ohms
        mpn_sufix: Part number sufix
        tolerance_map:
            Maps series types to available tolerance codes and values
            Format: {str: {code: value}}
        datasheet: Complete URL to component datasheet
        manufacturer: Name of the component manufacturer
        trustedparts_url:
            Base URL for component listing on Trustedparts platform
        reference: Reference designator for the component
        excluded_values: Optional list of values to exclude from calculations
        specified_values: Optional list of values to specifically include

    """

    mpn_prefix: str
    footprint: str
    voltage_rating: str
    case_code_in: str
    case_code_mm: str
    power_rating: str
    mpn_sufix: str
    tolerance_map: dict[str, dict[str, str]]
    datasheet: str
    manufacturer: str
    trustedparts_url: str
    resistance_range: list[Union[int, float]] = [10, 1_000_000]  # noqa: FA100, RUF012
    reference: str = "R"
    excluded_values: Optional[list[float]] = None  # noqa: FA100
    specified_values: Optional[list[float]] = None  # noqa: FA100


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
        specs: SeriesSpec,
    ) -> str:
        """Generate the resistance code portion of a Panasonic part number.

        Args:
            resistance: The resistance value in ohms
            specs: Series specifications

        Returns:
            A string representing the resistance code

        Raises:
            ValueError: If resistance is outside valid range

        """
        # Unpack resistance range
        min_resistance, max_resistance = specs.resistance_range

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
        if specs.mpn_prefix in ("ERJ-2GEJ", "ERJ-3GEYJ", "ERJ-6GEYJ"):
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
        resistance_code = cls.generate_resistance_code(resistance, specs)

        packaging_code = packaging

        mpn = f"{specs.mpn_prefix}{resistance_code}{packaging_code}"

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
            series=specs.mpn_prefix,
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
                specs.mpn_sufix,
                specs,
            )
            for series_type in specs.tolerance_map
            for resistance in cls._filtered_resistance_values(
                E96_BASE_VALUES if series_type == "E96" else E24_BASE_VALUES,
                specs.resistance_range,
                specs.excluded_values,
                specs.specified_values,
            )
            for tolerance_value in [specs.tolerance_map[series_type]]
        ]

    @classmethod
    def _filtered_resistance_values(
        cls,
        base_values: list[float],
        resistance_range: list[Union[int, float]],  # noqa: FA100
        excluded_values: Optional[list[float]] = None,  # noqa: FA100
        specified_values: Optional[list[float]] = None,  # noqa: FA100
    ) -> Iterator[float]:
        """Generate resistance values with optional exclusions and inclusions.

        Args:
            base_values: List of base resistance values (E96 or E24 series)
            resistance_range:
                Minimum and maximum resistance values to generate
            excluded_values: Optional list of values to exclude
            specified_values: Optional list of values to include if not None

        Yields:
            float: Valid resistance values in ascending order

        """
        min_resistance, max_resistance = resistance_range
        multipliers = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000]

        for base_value in base_values:
            for multiplier in multipliers:
                resistance = round(base_value * multiplier, 2)

                # Check if resistance is within range
                is_within_range = \
                    min_resistance <= resistance <= max_resistance

                # Check exclusion conditions
                is_not_excluded = (
                    excluded_values is None or
                    resistance not in excluded_values
                )

                # Check specified values condition
                is_specified = (
                    specified_values is None or
                    resistance in specified_values
                )

                # Yield only if all conditions are met
                if is_within_range and is_not_excluded and is_specified:
                    yield resistance

PANASONIC_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "ERJ-2RKF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-2RKF",
        mpn_sufix="X",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-3EKF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-3EKF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-6ENF": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6ENF",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[10, 2_200_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P08F": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-P08F",
        mpn_sufix="V",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="500V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.66W",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P06F": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-P06F",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="400V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.5W",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-P03F": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-P03F",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="150V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.25W",
        resistance_range=[10, 1_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-2GEJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-2GEJ",
        mpn_sufix="X",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        resistance_range=[1, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-3GEYJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-3GEYJ",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        resistance_range=[1, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "ERJ-6GEYJ": SeriesSpec(
        manufacturer="Panasonic",
        mpn_prefix="ERJ-6GEYJ",
        mpn_sufix="V",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[1, 1_000_000],
        tolerance_map={"E24": "5%"},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}

YAGEO_SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "RT0805BRA07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRA07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[20, 50_000],
        specified_values=[
            41.2, 205, 806, 1000, 1050, 1800, 2000, 3000, 4020, 6800,
            8060, 10000, 11000, 12000, 15000, 20000, 22000, 27000, 49900],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRB07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRB07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[4.7, 1_000_000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRC07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRC07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[4.7, 1_000_000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRD07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRD07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[1, 1_500_000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805BRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805BRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[1, 3_000_000],
        tolerance_map={"E96": "0.1%", "E24": "0.1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805CRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805CRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[1, 3_000_000],
        tolerance_map={"E96": "0.25%", "E24": "0.25%"},
        specified_values=[
            6.8, 8.2, 18, 24.9, 36, 60.4, 75, 100, 110, 124, 200, 374, 402,
            510, 680, 900, 909, 1000, 1200, 1270, 1500, 1800, 1890, 2320,
            2430, 2490, 2700, 3000, 3010, 3160, 3300, 3570, 4020, 4580, 4700,
            4990, 5050, 5100, 5490, 5620, 6190, 9100, 10000, 11000, 11100,
            11500, 12000, 13000, 15000, 17400, 20000, 20500, 21500, 22100,
            22300, 23200, 24000, 24900, 25500, 26100, 26700, 33000, 33200,
            40200, 45300, 46400, 47000, 49900, 51000, 60400, 62000, 66500,
            68000, 68100, 73200, 91000, 100000, 158000, 160000, 205000,
            249000, 330000, 360000, 390000, 417000, 470000, 604000, 698000,
            910000, 931000, 976000, 1000000],
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),

    "RT0805FRE07": SeriesSpec(
        manufacturer="Yageo",
        mpn_prefix="RT0805FRE07",
        mpn_sufix="L",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        resistance_range=[1, 3_000_000],
        tolerance_map={"E96": "1%", "E24": "1%"},
        datasheet=(
            "https://www.yageo.com/en/ProductSearch/"
            "PartNumberSearch?part_number="),
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}

# Combined specifications dictionary
SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    **PANASONIC_SYMBOLS_SPECS, **YAGEO_SYMBOLS_SPECS}
