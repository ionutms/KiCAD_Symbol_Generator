"""Library for managing transistor specifications.

This module provides data structures and definitions for various transistor
series, including their specifications and individual component
information.
"""

from typing import NamedTuple

from utilities import print_message_utilities


class SeriesSpec(NamedTuple):
    """Transistor series specifications.

    This class defines the complete specifications for a series of
    transistors, including physical, electrical,
    and documentation characteristics.
    """

    manufacturer: str
    base_series: str
    footprint: str
    datasheet: str
    drain_source_voltage: list[float]
    trustedparts_link: str
    drain_current: list[float]
    package: str
    transistor_type: str
    reference: str = "Q"


class PartInfo(NamedTuple):
    """Component part information structure for individual transistors."""

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

    @classmethod
    def create_description(cls, value: float) -> str:
        """Create a descriptive string for the transistor component.

        Args:
            value (float): The voltage rating of the transistor.

        Returns:
            str:
                A descriptive string combining
                'Transistor' and formatted voltage.

        """
        parts = ["Transistor", f"{value} V"]
        return " ".join(parts)

    @classmethod
    def create_part_info(
        cls,
        value: float,
        specs: SeriesSpec,
    ) -> "PartInfo":
        """Create a PartInfo object for a specific transistor component.

        Args:
            value (float): The voltage rating of the transistor.
            specs (SeriesSpec): Specifications for the transistor series.

        Returns:
            PartInfo:
                A comprehensive part information object for the transistor.

        Raises:
            ValueError: If the voltage rating is not found in the series.
            IndexError:
                If no DC specifications are found for the given voltage.

        """
        # Construct MPN with optional suffix
        mpn = f"{specs.base_series}"

        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        try:
            index = specs.drain_source_voltage.index(value)
            drain_current = float(specs.drain_current[index])
        except ValueError:
            print_message_utilities.print_error(
                f"Error: value {value} V "
                f"not found in series {specs.base_series}")
            drain_current = 0.0
        except IndexError:
            print_message_utilities.print_error(
                "Error: No DC specifications found for value "
                f"{value} V in series {specs.base_series}")
            drain_current = 0.0

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=value,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(value),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            package=specs.package,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            drain_current=drain_current,
            transistor_type=specs.transistor_type,
        )

    @classmethod
    def generate_part_numbers(
        cls,
        specs: SeriesSpec,
    ) -> list["PartInfo"]:
        """Generate all part numbers for the series.

        Args:
            specs: Series specifications

        Returns:
            List of PartInfo instances

        """
        return [
            cls.create_part_info(value, specs)
            for value in specs.drain_source_voltage
            if cls.create_part_info(value, specs) is not None]


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
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "BUK9M120-100EX": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9M120-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M120-100E.pdf"),
        drain_source_voltage =[100.0], drain_current=[11.5],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "BUK9M156-100EX": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9M156-100EX",
        footprint="transistor_footprints:LFPAK33-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9M156-100E.pdf"),
        drain_source_voltage =[100.0], drain_current=[9.3],
        package="LFPAK33-8", transistor_type="N-Channel",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "BUK9K29-100E": SeriesSpec(
        manufacturer="Nexperia", base_series="BUK9K29-100E",
        footprint="transistor_footprints:LFPAK56D-8",
        datasheet=(
            "https://assets.nexperia.com/documents/data-sheet/"
            "BUK9K29-100E.pdf"),
        drain_source_voltage =[100], drain_current=[30],
        package="LFPAK56D-8", transistor_type="N-Channel Dual",
        trustedparts_link="https://www.trustedparts.com/en/search"),

    "SI7997DP-T1-GE3": SeriesSpec(
        manufacturer="Vishay Semiconductors", base_series="SI7997DP-T1-GE3",
        footprint="transistor_footprints:PowerPAK SO-8",
        datasheet=("https://www.vishay.com/docs/66719/si7997dp.pdf"),
        drain_source_voltage =[-30], drain_current=[-60],
        package="PowerPAK SO-8", transistor_type="P-Channel Dual",
        trustedparts_link="https://www.trustedparts.com/en/search"),
}
