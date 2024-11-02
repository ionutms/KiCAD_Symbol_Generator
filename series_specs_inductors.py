"""
Library for managing Coilcraft inductor series specifications and part info.

This module provides data structures and definitions for various Coilcraft
inductor series, including their specifications and individual component
information. It is used to maintain a standardized database of inductor
specifications and generate consistent part information.
"""

from typing import List, NamedTuple, Dict


class SeriesSpec(NamedTuple):
    """Inductor series specifications for Coilcraft components.

    This class defines the complete specifications for a series of inductors,
    including physical, electrical, and documentation characteristics.

    Attributes:
        manufacturer: Name of the component manufacturer (e.g., "Coilcraft")
        base_series: Base model number for the series (e.g., "XAL1513")
        footprint: PCB footprint identifier used in schematic/layout tools
        tolerance: Component value tolerance (e.g., "±20%")
        datasheet: URL to the manufacturer's datasheet
        inductance_values: List of available inductance values in µH
        trustedparts_link: URL to the component listing on Trusted Parts
        value_suffix:
            Manufacturer's suffix for the component value (e.g., "ME")
        has_aec: Whether the series is AEC-Q200 qualified (defaults to True)
        max_dc_current: Maximum DC current rating in Amperes (A)
    """
    manufacturer: str
    base_series: str
    footprint: str
    tolerance: str
    datasheet: str
    inductance_values: List[float]
    trustedparts_link: str
    value_suffix: str
    has_aec: bool = True
    max_dc_current: List[float] = []


class PartInfo(NamedTuple):
    """Component part information structure for individual inductors.

    This class contains all necessary information to fully specify a single
    inductor component, including its specifications, documentation, and
    sourcing information.

    Attributes:
        symbol_name: Schematic symbol identifier
        reference: Component reference designator
        value: Inductance value in µH
        footprint: PCB footprint identifier
        datasheet: URL to the manufacturer's datasheet
        description: Human-readable component description
        manufacturer: Component manufacturer name
        mpn: Manufacturer part number
        tolerance: Component value tolerance
        series: Product series identifier
        trustedparts_link: URL to component listing on Trusted Parts
        max_dc_current: Maximum DC current rating in Amperes (A)
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
    series: str
    trustedparts_link: str
    max_dc_current: float


SERIES_SPECS: Dict[str, SeriesSpec] = {
    "XAL1513": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1513",
        footprint="footprints:XAL1513",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "129ad6f3-0445-47fd-a0b3-edeb49177c17/xal1513.pdf",
        inductance_values=[15.0],
        max_dc_current=[22.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1510": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1510",
        footprint="footprints:XAL1510",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "cd1cef27-13f0-4568-8894-f7311475209b/xal1510.pdf",
        inductance_values=[4.7, 6.8, 8.2, 10.0, 15.0, 22.0, 33.0],
        max_dc_current=[29.0, 26.0, 24.0, 22.0, 18.0, 14.0, 12.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1580": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1580",
        footprint="footprints:XAL1580",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "7fdfd306-5217-4ddc-b6b7-a2659ceeb6e3/xal1580.pdf",
        inductance_values=[
            0.4, 0.74, 1.0, 1.3, 1.8, 2.0, 3.0, 4.5, 5.3, 6.1
        ],
        max_dc_current=[
            60.0, 59.7, 57.5, 46.7, 43.8, 39.9, 34.4, 27.0, 26.5, 22.6
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1350": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1350",
        footprint="footprints:XAL1350",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "dc536f86-3a3b-454f-950e-8e153260e61c/xal1350.pdf",
        inductance_values=[0.63, 0.93, 1.3, 2.2, 3.0],
        max_dc_current=[38.0, 33.0, 32.0, 24.0, 21.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1010",
        footprint="footprints:XAL1010",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "dd74e670-e705-456a-9a69-585fe02eaf3c/xal1010.pdf",
        inductance_values=[
            0.22, 0.45, 0.68, 1.0, 1.5, 2.2, 3.3,
            4.7, 5.6, 6.8, 8.2, 10.0, 15.0
        ],
        max_dc_current=[
            55.5, 53.0, 48.0, 43.5, 40.5, 32.0, 25.0,
            24.0, 21.2, 18.5, 17.1, 15.5, 13.8
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1080": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1080",
        footprint="footprints:XAL1080",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "18b60eaf-2c95-4723-8b7f-5f43f66ed007/xal1080.pdf",
        inductance_values=[10.0, 12.0, 15.0, 18.0, 22.0, 33.0],
        max_dc_current=[14.8, 13.9, 11.7, 10.8, 10.0, 7.5],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1060",
        footprint="footprints:XAL1060",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "8909f858-b441-4d60-acff-8b8ca36f9ede/xal1060.pdf",
        inductance_values=[0.18, 0.4, 0.68, 1.2, 1.5, 2.2, 3.3, 4.7],
        max_dc_current=[46.0, 36.8, 33.9, 26.3, 24.4, 20.0, 16.8, 14.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL1030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL1030",
        footprint="footprints:XAL1030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "7b108457-7731-456d-9256-ca72f2e1a551/xal1030.pdf",
        inductance_values=[0.16, 0.3, 0.56, 1.0],
        max_dc_current=[42.0, 35.0, 32.0, 23.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL8080": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL8080",
        footprint="footprints:XAL8080",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "345e50d6-a804-4ecb-9a92-5185221faf3e/xal8080.pdf",
        inductance_values=[
            0.68, 0.84, 1.0, 2.2, 4.7, 6.8, 10.0,
            12.0, 15.0, 18.0, 22.0, 33.0, 47.0
        ],
        max_dc_current=[
            37.0, 35.0, 34.1, 21.5, 14.6, 11.3, 8.7,
            10.5, 9.4, 8.3, 7.6, 6.0, 4.8
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL8050": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL8050",
        footprint="footprints:XAL8050",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "5885ede8-ea4f-464a-9dcb-18dbf143a845/xal8050.pdf",
        inductance_values=[22.0],
        max_dc_current=[5.2],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL7070": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7070",
        footprint="footprints:XAL7070",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "1ba55433-bcc8-4838-9b21-382f497e12e0/xal7070.pdf",
        inductance_values=[
            0.16, 0.3, 0.55, 0.65, 0.8, 1.0, 1.2, 1.8, 2.2, 3.3,
            4.7, 5.6, 6.8, 10.0, 12.0, 15.0, 18.0, 22.0, 33.0, 47.0
        ],
        max_dc_current=[
            36.1, 33.4, 29.0, 26.5, 25.8, 25.0, 21.6, 21.0, 17.8, 15.1,
            13.6, 11.4, 9.2, 9.3, 8.2, 7.4, 6.8, 6.5, 4.9, 4.1],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL7050": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7050",
        footprint="footprints:XAL7050",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "13a991b3-4273-4be3-81ba-f3cf372b4691/xal7050.pdf",
        inductance_values=[10.0, 15.0, 18.0, 22.0, 33.0, 47.0],
        max_dc_current=[8.5, 7.0, 6.2, 5.0, 4.6, 3.5],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL7030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7030",
        footprint="footprints:XAL7030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "0d05a05e-d55d-4a0c-911d-46bd73686633/xal7030.pdf",
        inductance_values=[
            0.16, 0.3, 0.6, 1.0, 1.5, 2.2, 2.7,
            3.3, 4.7, 5.6, 6.8, 8.2, 10.0
        ],
        max_dc_current=[
            32.5, 27.6, 23.0, 21.8, 15.0, 12.9, 11.4,
            10.0, 9.0, 7.3, 6.8, 5.9, 5.3
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL7020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL7020",
        footprint="footprints:XAL7020",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "0197e98c-67f7-4375-9e38-14d7376a46f3/xal7020.pdf",
        inductance_values=[0.15, 0.27, 0.33, 0.47, 0.68, 1.0, 1.2, 1.5, 2.2],
        max_dc_current=[24.0, 21.0, 20.0, 17.0, 13.0, 11.0, 10.0, 9.0, 7.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL6060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL6060",
        footprint="footprints:XAL6060",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf",
        inductance_values=[4.7, 5.6, 6.8, 8.2, 10.0, 15.0, 22.0, 33.0],
        max_dc_current=[11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0, 3.6],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL6030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL6030",
        footprint="footprints:XAL6030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf",
        inductance_values=[0.18, 0.33, 0.56, 1.0, 1.2, 1.8, 2.2, 3.3],
        max_dc_current=[32.0, 25.0, 22.0, 18.0, 16.0, 14.0, 10.0, 8.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL6020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL6020",
        footprint="footprints:XAL6020",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "467ff589-8942-4e57-92d0-5bef6e04ce09/xal6020.pdf",
        inductance_values=[0.12, 0.16, 0.27, 0.45, 0.6, 0.9, 1.1],
        max_dc_current=[27.0, 26.0, 25.0, 22.0, 18.5, 15.2, 12.0],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL5050": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL5050",
        footprint="footprints:XAL5050",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "49bc46c8-4b2c-45b9-9b6c-2eaa235ea698/xal50xx.pdf",
        inductance_values=[4.7, 5.6, 6.8, 8.2, 10.0, 15.0, 22.0],
        max_dc_current=[8.2, 7.2, 6.4, 6.1, 4.9, 3.9, 3.4],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL5030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL5030",
        footprint="footprints:XAL5030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "49bc46c8-4b2c-45b9-9b6c-2eaa235ea698/xal50xx.pdf",
        inductance_values=[0.16, 0.33, 0.6, 0.8, 1.0, 1.2, 2.2, 3.3, 4.7],
        max_dc_current=[22.2, 19.2, 17.7, 13.0, 11.1, 10.4, 9.7, 8.1, 5.9],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL5020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL5020",
        footprint="footprints:XAL5020",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "1941eff1-c018-493c-8cd6-d88d2edf5029/xal5020.pdf",
        inductance_values=[0.16, 0.33, 0.56, 0.8, 1.2],
        max_dc_current=[18.8, 14.4, 13.9, 13.0, 9.4],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL4040": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL4040",
        footprint="footprints:XAL4040",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf",
        inductance_values=[8.2, 10.0, 15.0],
        max_dc_current=[3.4, 3.1, 2.8],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL4030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL4030",
        footprint="footprints:XAL4030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf",
        inductance_values=[3.3, 4.7, 6.8],
        max_dc_current=[6.6, 5.1, 3.9],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XAL4020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XAL4020",
        footprint="footprints:XAL4020",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf",
        inductance_values=[0.22, 0.4, 0.6, 1.0, 1.2, 1.5, 2.2],
        max_dc_current=[16.8, 14.0, 11.7, 9.6, 9.0, 7.5, 5.5],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL2005": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2005",
        footprint="footprints:XFL2005",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "73b70df2-8cfe-46c3-92db-66951708f060/xfl2005.pdf",
        inductance_values=[
            0.15, 0.22, 0.33, 0.47, 0.68, 1.0, 1.5,
            2.2, 3.3, 4.7, 5.6, 6.8, 8.2, 10.0
        ],
        max_dc_current=[
            1.60, 1.48, 1.30, 1.25, 1.05, 0.84, 0.70,
            0.66, 0.50, 0.41, 0.39, 0.38, 0.33, 0.29
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL2006": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2006",
        footprint="footprints:XFL2006",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "65419ba7-9eac-409b-830a-74bf182a8aca/xfl2006.pdf",
        inductance_values=[
            1.0, 2.2, 3.3, 4.7, 5.6, 6.8, 8.2, 10.0,
            15.0, 22.0, 33.0, 47.0, 56.0, 68.0, 82.0, 100.0
        ],
        max_dc_current=[
            1.22, 0.950, 0.72, 0.66, 0.6, 0.52, 0.49, 0.44,
            0.35, 0.305, 0.205, 0.205, 0.195, 0.155, 0.165, 0.135],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL2010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL2010",
        footprint="footprints:XFL2010",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "50382b97-998f-4b75-b5ee-4a93b0ac4411/xfl2010.pdf",
        inductance_values=[
            0.04, 0.12, 0.22, 0.38, 0.6, 0.82, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8,
            8.2, 10.0, 18.0, 22.0, 33.0, 47.0, 56.0, 68.0, 82.0, 100.0, 220.0
        ],
        max_dc_current=[
            4.8, 3.7, 3.1, 2.85, 2.35, 2.15, 1.8, 1.55, 1.35, 1.2, 0.91, 0.79,
            0.76, 0.67, 0.46, 0.42, 0.35, 0.31, 0.27, 0.26, 0.21, 0.2, 0.14
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL3012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL3012",
        footprint="footprints:XFL3012",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "f76a3c9b-4fff-4397-8028-ef8e043eb200/xfl3012.pdf",
        inductance_values=[
            0.33, 0.56, 0.68, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8,
            10.0, 15.0, 22.0, 33.0, 39.0, 47.0, 56.0, 68.0,
            82.0, 100.0, 220.0
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL3010": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL3010",
        footprint="footprints:XFL3010",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "0118859e-f2e2-4063-93cf-e50ed636ea4e/xfl3010.pdf",
        inductance_values=[
            0.60, 1.0, 1.5, 2.2, 3.3, 4.7, 6.8, 10.0, 15.0,
            22.0, 33.0, 47.0, 68.0, 82.0, 100.0
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4012",
        footprint="footprints:XFL4012",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "2d7c4d90-1677-4c05-9569-33b6dc7153e7/xfl4012.pdf",
        inductance_values=[
            0.12, 0.25, 0.47, 0.6
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4015",
        footprint="footprints:XFL4015",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "84927b8b-f089-421b-a7f4-a0fa23afe908/xfl4015.pdf",
        inductance_values=[
            0.18, 0.33, 0.47, 0.7, 1.2
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4020": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4020",
        footprint="footprints:XFL4020",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "50632d43-da1b-4cdb-8ab4-3029cab51df3/xfl4020.pdf",
        inductance_values=[
            0.12, 0.24, 0.33, 0.47, 0.56, 1.0, 1.5, 2.2, 3.3, 4.7
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL4030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL4030",
        footprint="footprints:XFL4030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "d12f7f67-cfc1-404a-9993-f09a1451b0a9/xfl4030.pdf",
        inductance_values=[
            0.47, 1.0, 2.0, 3.0, 4.7
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL5015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5015",
        footprint="footprints:XFL5015",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "5f7b596c-8f2f-415e-931e-74a5b6804936/xfl5015.pdf",
        inductance_values=[
            0.22, 0.42, 0.68, 1.2, 1.5
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL5018": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5018",
        footprint="footprints:XFL5018",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "5f7b596c-8f2f-415e-931e-74a5b6804936/xfl5015.pdf",
        inductance_values=[
            2.2, 3.3
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL5030": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL5030",
        footprint="footprints:XFL5030",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "f01e4ccd-6be9-43eb-bb01-c23b4deeb2c5/xfl5030.pdf",
        inductance_values=[
            0.27, 0.56, 1.0, 2.2, 3.3, 4.7
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL6012": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL6012",
        footprint="footprints:XFL6012",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "ae4a44fc-deeb-45d7-81a6-abe1d0432add/xfl6012.pdf",
        inductance_values=[
            0.18, 0.39, 0.6, 0.8, 1.0
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL6060": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL6060",
        footprint="footprints:XFL6060",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "9e8cc1df-cee0-4215-90fb-b5193fa22761/xfl6060-473.pdf",
        inductance_values=[
            47.0
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
    "XFL7015": SeriesSpec(
        manufacturer="Coilcraft",
        base_series="XFL7015",
        footprint="footprints:XFL7015",
        tolerance="±20%",
        datasheet="https://www.coilcraft.com/getmedia/" +
        "ccf09628-6e8c-462a-9dc9-fa4346e7cf0a/xfl7015.pdf",
        inductance_values=[
            0.25, 0.47, 0.68, 1.0, 1.5
        ],
        value_suffix="ME",
        trustedparts_link="https://www.trustedparts.com/en/search"
    ),
}
