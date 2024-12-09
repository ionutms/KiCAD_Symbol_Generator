"""Library for managing diode specifications.

This module provides data structures and definitions for various diode
series, including their specifications and individual component
information.
"""

from typing import NamedTuple, Optional, Self

from utilities import print_message_utilities


class SeriesSpec(NamedTuple):
    """Diode series specifications.

    This class defines the complete specifications for a series of diodes,
    including physical, electrical, and documentation characteristics.
    """

    manufacturer: str
    base_series: str
    footprint: str
    datasheet: str
    voltage_rating: list[float]
    trustedparts_link: str
    current_rating: list[float]
    package: str
    diode_type: str
    part_number_suffix: Optional[str] = None  # noqa: FA100
    reference: str = "D"


class PartInfo(NamedTuple):
    """Component part information structure for individual diodes."""

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
    current_rating: float
    package: str
    diode_type: str

    @staticmethod
    def format_value(value: float) -> str:
        """Format the diode voltage value with a 'V' suffix.

        Args:
            value (float): The voltage rating of the diode.

        Returns:
            str: Formatted voltage value with 'V' appended.

        """
        return f"{value} V"

    @classmethod
    def create_description(
        cls, value: float, diode_type: str = "DIODE") -> str:
        """Create a descriptive string for the diode component.

        Args:
            value (float): The voltage rating of the diode.
            diode_type (str, optional): Type of diode. Defaults to "DIODE".

        Returns:
            str:
                A descriptive string combining diode type
                and formatted voltage.

        """
        parts = [f"{diode_type} SMD", cls.format_value(value)]
        return " ".join(parts)

    @classmethod
    def create_part_info(
        cls: type[Self],
        value: float,
        specs: SeriesSpec,
    ) -> Optional[Self]:  # noqa: FA100
        """Create a PartInfo object for a specific diode component.

        Args:
            value (float): The voltage rating of the diode.
            specs (SeriesSpec): Specifications for the diode series.

        Returns:
            Optional[PartInfo]:
                A comprehensive part information object for the diode.

        Raises:
            ValueError: If the voltage rating is not found in the series.
            IndexError:
                If no DC specifications are found for the given voltage.

        """
        # Construct MPN with optional suffix
        mpn = f"{specs.base_series}"
        if specs.part_number_suffix:
            # Find index of voltage in ratings list
            try:
                index = specs.voltage_rating.index(value)
                # Adjust index to start from 21
                adjusted_index = index + 21
                mpn = (
                    f"{specs.base_series}{adjusted_index}"
                    f"{specs.part_number_suffix}")
            except ValueError:
                print_message_utilities.print_error(
                    f"Error: value {value} V "
                    f"not found in series {specs.base_series}")
                return None

        trustedparts_link = f"{specs.trustedparts_link}/{mpn}"

        try:
            index = specs.voltage_rating.index(value)
            current_rating = float(specs.current_rating[index])
        except ValueError:
            print_message_utilities.print_error(
                f"Error: value {value} V "
                f"not found in series {specs.base_series}")
            current_rating = 0.0
        except IndexError:
            print_message_utilities.print_error(
                "Error: No DC specifications found for value "
                f"{value} V in series {specs.base_series}")
            current_rating = 0.0

        return cls(
            symbol_name=f"{specs.reference}_{mpn}",
            reference=specs.reference,
            value=value,
            footprint=specs.footprint,
            datasheet=specs.datasheet,
            description=cls.create_description(value, specs.diode_type),
            manufacturer=specs.manufacturer,
            mpn=mpn,
            package=specs.package,
            series=specs.base_series,
            trustedparts_link=trustedparts_link,
            current_rating=current_rating,
            diode_type=specs.diode_type,
        )


SYMBOLS_SPECS: dict[str, SeriesSpec] = {
    "DFLS1200-7": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="DFLS1200-7",
        footprint="diode_footprints:PowerDI_123",
        datasheet="https://www.diodes.com/datasheet/download/DFLS1200.pdf",
        voltage_rating=[100.0],
        current_rating=[1.2],
        package="PowerDI_123",
        diode_type="Schottky",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix=None,
    ),
    "MMSZ52": SeriesSpec(
        manufacturer="Onsemi",
        base_series="MMSZ52",
        footprint="diode_footprints:SOD_123",
        datasheet=(
            "https://www.onsemi.com/download/data-sheet/"
            "pdf/mmsz5221bt1-d.pdf"),
        voltage_rating=[
            2.4, 2.5, 2.7, 2.8, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7,
            5.1, 5.6, 6.0, 6.2, 6.8, 7.5, 8.2, 8.7, 9.1, 10.0,
            11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0,
            22.0, 24.0, 25.0, 27.0, 28.0, 30.0, 33.0, 36.0, 39.0, 43.0,
            47.0, 51.0, 56.0, 60.0, 62.0, 68.0, 75.0, 82.0, 87.0, 91.0],
        current_rating=[0.5] * 51,
        package="SOD_123",
        diode_type="Zener",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix="BT1G",
    ),
    "US1DWF": SeriesSpec(
        manufacturer="Diodes Incorporated",
        base_series="US1DWF",
        footprint="diode_footprints:SOD_123F",
        datasheet="https://www.diodes.com/assets/Datasheets/US1DWF.pdf",
        voltage_rating=[200.0],
        current_rating=[1.0],
        package="SOD_123F",
        diode_type="Rectifier",
        trustedparts_link="https://www.trustedparts.com/en/search",
        part_number_suffix=None,
    ),
}
