"""Specifications and data structures for Panasonic ERJ series resistors.

This module defines the specifications for various Panasonic ERJ series
resistors, supporting both E96 and E24 value series.
It provides comprehensive component information including physical dimensions,
electrical characteristics, and packaging options.
"""

from typing import Final, Iterator, NamedTuple  # noqa: UP035


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
        packaging_options:
            List of available packaging codes (e.g., ['V', 'X'])
        tolerance_map:
            Maps series types to available tolerance codes and values
            Format: {str: {code: value}}
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
    packaging_options: list[str]
    tolerance_map: dict[str, dict[str, str]]
    datasheet: str
    manufacturer: str
    trustedparts_url: str
    high_resistance_tolerance: dict[str, str] | None = None  # noqa: FA102
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
    def generate_resistance_code(  # noqa: C901, PLR0912
        cls,
        resistance: float,
        max_resistance: int,
        series: str,
    ) -> str:
        """Generate the resistance code portion of a Panasonic part number.

        Args:
            resistance: The resistance value in ohms
            max_resistance: Maximum allowed resistance value for the series
            series: Optional series identifier for series-specific encoding

        Returns:
            A string representing the resistance code

        Raises:
            ValueError: If resistance is outside valid range

        """
        if resistance < 10 or resistance > max_resistance:  # noqa: PLR2004
            msg = f"Resistance value out of range (10Ω to {max_resistance}Ω)"
            raise ValueError(msg)

        # Special handling for ERJ-2GE series
        if series in ("ERJ-2GE", "ERJ-3GE", "ERJ-6GE"):
            if resistance < 100:  # noqa: PLR2004
                whole = int(resistance)
                decimal = int(round((resistance - whole) * 10))
                return f"{whole:01d}{decimal}"

            # For values ≥ 100Ω, determine multiplier and significant digits
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
        max_resistance: int,
    ) -> Iterator[float]:
        """Generate all valid resistance values from a list of base values.

        Args:
            base_values: List of base resistance values (E96 or E24 series)
            max_resistance: Maximum resistance value to generate

        Yields:
            float: Valid resistance values in ascending order

        """
        for base_value in base_values:
            current = base_value
            while current <= max_resistance:
                if current >= 10:  # noqa: PLR2004
                    yield current
                current *= 10

    @classmethod
    def create_part_info(
        cls,
        resistance: float,
        tolerance_code: str,
        tolerance_value: str,
        packaging: str,
        specs: "SeriesSpec",
    ) -> "PartInfo":
        """Create a PartInfo instance with complete component specifications.

        Args:
            resistance: Resistance value in ohms
            tolerance_code: Manufacturer's tolerance code (e.g., 'F' for 1%)
            tolerance_value: Human-readable tolerance (e.g., '1%')
            packaging: Packaging code (e.g., 'X' or 'V')
            specs: SeriesSpec instance containing series specifications

        Returns:
            PartInfo instance containing all component details
            and vendor information

        """
        resistance_code = cls.generate_resistance_code(
            resistance, specs.max_resistance, specs.base_series)
        mpn = \
            f"{specs.base_series}{tolerance_code}{resistance_code}{packaging}"
        description = (
            f"RES SMD {cls.format_resistance_value(resistance)} "
            f"{tolerance_value} {specs.case_code_in} {specs.voltage_rating}")
        trustedparts_link = f"{specs.trustedparts_url}{mpn}"

        return PartInfo(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=resistance,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
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
        parts_list: list[PartInfo] = []

        # Determine which series types are available for this specific series
        available_series_types = list(specs.tolerance_map.keys())

        for series_type in available_series_types:
            base_values = (
                E96_BASE_VALUES
                if series_type == "E96"
                else E24_BASE_VALUES)

            for resistance in cls.generate_resistance_values(
                    base_values, specs.max_resistance):
                # Handle special case for high resistance values
                if resistance > 1_000_000 and \
                        specs.high_resistance_tolerance:  # noqa: PLR2004
                    tolerance_codes = specs.high_resistance_tolerance
                else:
                    tolerance_codes = specs.tolerance_map[series_type]

                for tolerance_code, tolerance_value in \
                        tolerance_codes.items():
                    for packaging in specs.packaging_options:
                        parts_list.append(cls.create_part_info(  # noqa: PERF401
                            resistance,
                            tolerance_code,
                            tolerance_value,
                            packaging,
                            specs,
                        ))

        return parts_list


SYMBOLS_SPECS: Final[dict[str, SeriesSpec]] = {
    "ERJ-2RK": SeriesSpec(
        base_series="ERJ-2RK",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=["X"],
        tolerance_map={"E96": {"F": "1%"}, "E24": {"J": "5%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-3EK": SeriesSpec(
        base_series="ERJ-3EK",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": {"F": "1%"}, "E24": {"J": "5%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-6EN": SeriesSpec(
        base_series="ERJ-6EN",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        max_resistance=2_200_000,
        packaging_options=["V"],
        tolerance_map={"E96": {"F": "1%"}, "E24": {"J": "5%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C304.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/",
        high_resistance_tolerance={"F": "1%"}),
    "ERJ-P08": SeriesSpec(
        base_series="ERJ-P08",
        footprint="resistor_footprints:R_1206_3216Metric",
        voltage_rating="500V",
        case_code_in="1206",
        case_code_mm="3216",
        power_rating="0.66W",
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": {"F": "1%"}, "E24": {"F": "1%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-P06": SeriesSpec(
        base_series="ERJ-P06",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="400V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.5W",
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": {"F": "1%"}, "E24": {"F": "1%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-P03": SeriesSpec(
        base_series="ERJ-P03",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="150V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.25W",
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E96": {"F": "1%"}, "E24": {"F": "1%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDO0000/AOA0000C331.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-2GE": SeriesSpec(
        base_series="ERJ-2GE",
        footprint="resistor_footprints:R_0402_1005Metric",
        voltage_rating="50V",
        case_code_in="0402",
        case_code_mm="1005",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=["X"],
        tolerance_map={"E24": {"J": "5%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-3GE": SeriesSpec(
        base_series="ERJ-3GE",
        footprint="resistor_footprints:R_0603_1608Metric",
        voltage_rating="75V",
        case_code_in="0603",
        case_code_mm="1608",
        power_rating="0.1W",
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E24": {"YJ": "5%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
    "ERJ-6GE": SeriesSpec(
        base_series="ERJ-6GE",
        footprint="resistor_footprints:R_0805_2012Metric",
        voltage_rating="150V",
        case_code_in="0805",
        case_code_mm="2012",
        power_rating="0.125W",
        max_resistance=1_000_000,
        packaging_options=["V"],
        tolerance_map={"E24": {"YJ": "5%"}},
        datasheet=(
            "https://industrial.panasonic.com/cdbs/www-data/pdf/"
            "RDA0000/AOA0000C301.pdf"),
        manufacturer="Panasonic",
        trustedparts_url="https://www.trustedparts.com/en/search/"),
}
